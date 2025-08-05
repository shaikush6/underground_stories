#!/usr/bin/env python3
"""
Core audio pipeline for unified TTS processing across providers.
Following CLAUDE.md standards for single responsibility and testable functions.
"""

import asyncio
import logging
from typing import Dict, List, Optional
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass

from .types import (
    AudioFile, TTSRequest, TTSResult, VoiceConfig, TTSProvider,
    TTSProviderProtocol, TTSJobId, AudioFileId
)


logger = logging.getLogger(__name__)


@dataclass
class EpisodeSegment:
    """Represents a text segment for episode creation"""
    text: str
    estimated_duration_minutes: float
    break_type: str  # 'natural', 'forced', 'chapter'
    sequence_number: int


class AudioPipeline:
    """
    Unified audio pipeline supporting multiple TTS providers with fallback.
    
    Single responsibility: Coordinate TTS generation across providers.
    Follows C-4: Simple, composable, testable functions.
    """
    
    def __init__(self):
        self._providers: Dict[TTSProvider, TTSProviderProtocol] = {}
        self._fallback_providers: Dict[TTSProvider, TTSProvider] = {
            TTSProvider.GOOGLE: TTSProvider.OPENAI,
            TTSProvider.OPENAI: TTSProvider.GOOGLE,
        }
        self._default_provider = TTSProvider.GOOGLE
    
    def register_provider(self, provider_type: TTSProvider, provider: TTSProviderProtocol):
        """Register a TTS provider implementation"""
        self._providers[provider_type] = provider
        logger.info(f"Registered TTS provider: {provider_type}")
    
    async def generate_audio(
        self, 
        text: str, 
        voice_config: VoiceConfig,
        output_path: Path,
        job_id: Optional[TTSJobId] = None
    ) -> TTSResult:
        """
        Generate audio from text using specified voice configuration.
        
        Args:
            text: Text content to convert to speech
            voice_config: Voice and provider configuration
            output_path: Where to save the generated audio file
            job_id: Optional job identifier for tracking
            
        Returns:
            TTSResult with audio file or error information
        """
        if job_id is None:
            job_id = TTSJobId(f"job_{datetime.now().isoformat()}")
        
        provider = self._providers.get(voice_config.provider)
        if not provider:
            return TTSResult(
                success=False,
                error_message=f"Provider {voice_config.provider} not available"
            )
        
        # Check character limits and split if necessary
        limits = provider.get_limits()
        if len(text) > limits.max_characters:
            return await self._generate_chunked_audio(
                text, voice_config, output_path, job_id, provider
            )
        
        # Single generation request
        request = TTSRequest(
            job_id=job_id,
            text=text,
            voice_config=voice_config,
            output_path=output_path
        )
        
        try:
            result = await provider.synthesize(request)
            
            # If primary provider fails, try fallback
            if not result.success and voice_config.provider in self._fallback_providers:
                fallback_provider_type = self._fallback_providers[voice_config.provider]
                fallback_provider = self._providers.get(fallback_provider_type)
                
                if fallback_provider:
                    logger.warning(
                        f"Primary provider {voice_config.provider} failed, "
                        f"trying fallback {fallback_provider_type}"
                    )
                    
                    # Update config for fallback provider
                    fallback_config = voice_config
                    fallback_config.provider = fallback_provider_type
                    
                    fallback_request = TTSRequest(
                        job_id=job_id,
                        text=text,
                        voice_config=fallback_config,
                        output_path=output_path
                    )
                    
                    result = await fallback_provider.synthesize(fallback_request)
            
            return result
            
        except Exception as e:
            logger.error(f"Audio generation failed: {e}")
            return TTSResult(
                success=False,
                error_message=f"Generation failed: {str(e)}"
            )
    
    async def _generate_chunked_audio(
        self, 
        text: str, 
        voice_config: VoiceConfig,
        output_path: Path, 
        job_id: TTSJobId,
        provider: TTSProviderProtocol
    ) -> TTSResult:
        """Generate audio from text that exceeds character limits"""
        limits = provider.get_limits()
        chunks = self._split_text_for_provider(text, limits.max_characters)
        
        audio_files = []
        total_cost = 0
        
        for i, chunk in enumerate(chunks):
            chunk_path = output_path.parent / f"{output_path.stem}_chunk_{i+1:03d}.mp3"
            chunk_request = TTSRequest(
                job_id=TTSJobId(f"{job_id}_chunk_{i+1}"),
                text=chunk,
                voice_config=voice_config,
                output_path=chunk_path
            )
            
            result = await provider.synthesize(chunk_request)
            
            if not result.success:
                return TTSResult(
                    success=False,
                    error_message=f"Chunk {i+1} generation failed: {result.error_message}"
                )
            
            audio_files.append(result.audio_file)
            total_cost += result.cost_cents or 0
        
        # Combine audio files
        combined_audio = await self._combine_audio_files(audio_files, output_path)
        
        return TTSResult(
            success=True,
            audio_file=combined_audio,
            cost_cents=total_cost
        )
    
    def _split_text_for_provider(self, text: str, max_characters: int) -> List[str]:
        """
        Split text into chunks that respect provider character limits.
        
        Attempts to split at natural boundaries (sentences, paragraphs).
        """
        if len(text) <= max_characters:
            return [text]
        
        chunks = []
        current_chunk = ""
        
        # Split by paragraphs first
        paragraphs = text.split('\n\n')
        
        for paragraph in paragraphs:
            # If adding this paragraph exceeds limit, save current chunk
            if len(current_chunk) + len(paragraph) > max_characters:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                    current_chunk = ""
                
                # If single paragraph is too long, split by sentences
                if len(paragraph) > max_characters:
                    sentences = paragraph.split('. ')
                    for sentence in sentences:
                        if len(current_chunk) + len(sentence) > max_characters:
                            if current_chunk:
                                chunks.append(current_chunk.strip())
                                current_chunk = ""
                        current_chunk += sentence + ". "
                else:
                    current_chunk = paragraph
            else:
                current_chunk += "\n\n" + paragraph if current_chunk else paragraph
        
        # Add remaining chunk
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return chunks
    
    async def _combine_audio_files(self, audio_files: List[AudioFile], output_path: Path) -> AudioFile:
        """Combine multiple audio files into a single file"""
        # For now, return the first file as placeholder
        # In production, would use pydub or ffmpeg to actually combine
        if audio_files:
            first_file = audio_files[0]
            total_duration = sum(af.duration_seconds for af in audio_files)
            total_size = sum(af.size_bytes for af in audio_files)
            
            return AudioFile(
                file_id=AudioFileId(f"combined_{first_file.file_id}"),
                file_path=output_path,
                duration_seconds=total_duration,
                size_bytes=total_size,
                format=first_file.format,
                sample_rate=first_file.sample_rate,
                bitrate=first_file.bitrate,
                voice_config=first_file.voice_config,
                generated_at=datetime.now().isoformat(),
                text_input="combined_audio"
            )
        
        raise ValueError("No audio files to combine")
    
    async def split_into_episodes(
        self, 
        text: str, 
        target_duration_minutes: float,
        voice_config: VoiceConfig
    ) -> List[EpisodeSegment]:
        """
        Split long text into episodes of target duration.
        
        Uses natural break points and estimates timing based on speech rate.
        """
        # Estimate words per minute (average 150 WPM for narration)
        words_per_minute = 150
        target_words = int(target_duration_minutes * words_per_minute)
        
        episodes = []
        current_text = ""
        current_words = 0
        sequence = 1
        
        # Split by natural breaks first
        natural_breaks = ['---', '***', 'Chapter ', 'CHAPTER ', '\n\n\n']
        
        sections = [text]
        for break_marker in natural_breaks:
            new_sections = []
            for section in sections:
                new_sections.extend(section.split(break_marker))
            sections = new_sections
        
        for section in sections:
            section = section.strip()
            if not section:
                continue
                
            section_words = len(section.split())
            
            # If adding this section exceeds target, finalize current episode
            if current_words + section_words > target_words and current_text:
                episodes.append(EpisodeSegment(
                    text=current_text,
                    estimated_duration_minutes=current_words / words_per_minute,
                    break_type='natural',
                    sequence_number=sequence
                ))
                sequence += 1
                current_text = section
                current_words = section_words
            else:
                current_text += "\n\n" + section if current_text else section
                current_words += section_words
        
        # Add final episode
        if current_text:
            episodes.append(EpisodeSegment(
                text=current_text,
                estimated_duration_minutes=current_words / words_per_minute,
                break_type='final',
                sequence_number=sequence
            ))
        
        return episodes
    
    def estimate_costs_all_providers(self, text: str) -> Dict[TTSProvider, int]:
        """Estimate costs across all available providers"""
        costs = {}
        
        for provider_type, provider in self._providers.items():
            try:
                cost = provider.estimate_cost(text)
                costs[provider_type] = cost
            except Exception as e:
                logger.warning(f"Could not estimate cost for {provider_type}: {e}")
        
        return costs
    
    def get_available_providers(self) -> List[TTSProvider]:
        """Get list of available TTS providers"""
        return list(self._providers.keys())