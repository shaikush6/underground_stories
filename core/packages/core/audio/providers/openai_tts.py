#!/usr/bin/env python3
"""
OpenAI Text-to-Speech provider implementation.
Optimized for Fairer Tales villain POV stories.
"""

import asyncio
import logging
import os
from typing import List, Optional
from pathlib import Path
from datetime import datetime
import aiohttp
from openai import AsyncOpenAI

from ..types import (
    TTSProviderProtocol, TTSRequest, TTSResult, VoiceConfig, 
    AudioFile, AudioFileId, ProviderLimits, AudioFormat, TTSProvider, TTSJobId
)
from ..text_chunker import IntelligentTextChunker, TextChunk
from ..audio_concatenator import AudioConcatenator


logger = logging.getLogger(__name__)


class OpenAITTSProvider:
    """
    OpenAI Text-to-Speech provider implementation.
    
    Specialized for Fairer Tales content with proven voice configurations.
    Maintains compatibility with existing audiobook generator setup.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OpenAI API key is required")
        
        self.client = AsyncOpenAI(api_key=self.api_key)
        
        # Voice configurations proven for storytelling
        self.voice_mapping = {
            # Fairer Tales - Proven voices from existing system
            "fairer_tales_narrator": "ash",     # Your current proven voice
            "fairer_tales_dramatic": "nova",    # Alternative for variety
            "fairer_tales_warm": "shimmer",     # Warmer storytelling
            "fairer_tales_serious": "onyx",     # Serious/dark stories
            "fairer_tales_expressive": "echo",  # Expressive delivery
            "fairer_tales_gentle": "fable"      # Gentle narratives
        }
        
        # Model configurations
        self.models = {
            "standard": "tts-1",      # Cost-effective
            "hd": "tts-1-hd"         # Higher quality
        }
        
        logger.info("OpenAI TTS provider initialized")
    
    async def synthesize(self, request: TTSRequest) -> TTSResult:
        """Generate speech using OpenAI TTS API"""
        try:
            # Determine model (default to standard for cost efficiency)
            model = self.models.get("standard", "tts-1")
            if hasattr(request.voice_config, 'extra_params'):
                model = request.voice_config.extra_params.get('model', model)
            
            # Generate speech
            response = await self.client.audio.speech.create(
                model=model,
                voice=request.voice_config.voice_id,
                input=request.text,
                response_format=request.voice_config.audio_format.value,
                speed=request.voice_config.speed
            )
            
            # Save audio file
            request.output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Get audio content from response
            audio_content = response.content
            
            with open(request.output_path, "wb") as f:
                f.write(audio_content)
            
            # Calculate audio properties
            duration = self._estimate_duration(request.text, request.voice_config.speed)
            file_size = len(audio_content)
            
            # Create audio file object
            audio_file = AudioFile(
                file_id=AudioFileId(f"openai_{request.job_id}"),
                file_path=request.output_path,
                duration_seconds=duration,
                size_bytes=file_size,
                format=request.voice_config.audio_format,
                sample_rate=request.voice_config.sample_rate_hertz,
                bitrate=self._estimate_bitrate(file_size, duration),
                voice_config=request.voice_config,
                generated_at=datetime.now().isoformat(),
                text_input=request.text
            )
            
            # Calculate cost
            cost_cents = self.estimate_cost(request.text)
            
            logger.info(f"Generated OpenAI audio: {request.output_path} ({duration:.1f}s)")
            
            return TTSResult(
                success=True,
                audio_file=audio_file,
                cost_cents=cost_cents,
                provider_response={
                    "model": model,
                    "voice": request.voice_config.voice_id,
                    "duration": duration,
                    "size": file_size
                }
            )
            
        except Exception as e:
            logger.error(f"OpenAI TTS synthesis failed: {e}")
            return TTSResult(
                success=False,
                error_message=f"OpenAI TTS error: {str(e)}"
            )
    
    def get_limits(self) -> ProviderLimits:
        """Get OpenAI TTS limits and capabilities"""
        return ProviderLimits(
            max_characters=4096,  # OpenAI's character limit
            max_requests_per_minute=50,
            cost_per_million_characters=1500,  # $15 per million chars
            supported_formats=[AudioFormat.MP3, AudioFormat.OGG, AudioFormat.FLAC],
            supported_languages=["en"],  # Primarily English for our use case
            max_speech_rate=4.0,
            min_speech_rate=0.25
        )
    
    def validate_config(self, config: VoiceConfig) -> bool:
        """Validate voice configuration for OpenAI TTS"""
        if config.provider != TTSProvider.OPENAI:
            return False
        
        # Check voice availability
        available_voices = self.get_available_voices()
        if config.voice_id not in available_voices:
            logger.warning(f"Voice {config.voice_id} not available in OpenAI TTS")
            return False
        
        # Check parameter ranges
        if not (0.25 <= config.speed <= 4.0):
            return False
        
        # OpenAI doesn't support pitch adjustment
        if config.pitch != 0.0:
            logger.warning("OpenAI TTS doesn't support pitch adjustment")
        
        return True
    
    def estimate_cost(self, text: str) -> int:
        """Estimate cost in cents for text generation"""
        character_count = len(text)
        
        # OpenAI pricing: $15 per million characters for TTS-1
        # $30 per million characters for TTS-1-HD
        cost_per_million = 1500  # TTS-1 pricing in cents
        
        # Estimate based on character count
        cost_cents = (character_count / 1_000_000) * cost_per_million
        
        # Minimum cost of 1 cent
        return max(1, int(cost_cents))
    
    def get_available_voices(self) -> List[str]:
        """Get list of available OpenAI TTS voices"""
        # OpenAI TTS available voices as of 2025
        return [
            "alloy",    # Neutral, balanced
            "echo",     # Expressive, dynamic
            "fable",    # Gentle, warm
            "onyx",     # Deep, serious
            "nova",     # Bright, enthusiastic  
            "shimmer",  # Soft, warm
            "ash"       # Your proven choice for Fairer Tales
        ]
    
    def get_voice_characteristics(self) -> dict:
        """Get voice characteristics for content matching"""
        return {
            "ash": "Warm, engaging storyteller - perfect for villain POV",
            "nova": "Bright, dynamic - good for lighter content",
            "onyx": "Deep, serious - ideal for dark stories", 
            "echo": "Expressive, dramatic - great for emotional scenes",
            "fable": "Gentle, comforting - good for redemption arcs",
            "shimmer": "Soft, mysterious - perfect for magical elements",
            "alloy": "Neutral, reliable - good backup option"
        }
    
    async def synthesize_long_text(
        self, 
        text: str, 
        voice_config: VoiceConfig, 
        output_path: Path,
        job_id: Optional[str] = None
    ) -> TTSResult:
        """
        Generate audio for long text by chunking and concatenating.
        
        Handles text longer than the 4,096 character OpenAI limit by:
        1. Intelligently chunking the text at natural break points
        2. Generating audio for each chunk
        3. Concatenating chunks into a seamless episode
        
        Args:
            text: Long text to convert to speech
            voice_config: Voice configuration
            output_path: Final output path for complete audio
            job_id: Optional job identifier
            
        Returns:
            TTSResult with complete episode audio
        """
        
        if len(text) <= 4000:  # Within single request limit
            # Use standard synthesis for short text
            request = TTSRequest(
                job_id=TTSJobId(job_id or f"single_{datetime.now().strftime('%Y%m%d_%H%M%S')}"),
                text=text,
                voice_config=voice_config,
                output_path=output_path
            )
            return await self.synthesize(request)
        
        # Text is too long - need chunking
        logger.info(f"Text too long ({len(text)} chars) - using intelligent chunking")
        
        try:
            # Step 1: Chunk the text intelligently
            chunker = IntelligentTextChunker(max_chars=4000, overlap_chars=50)
            chunks = chunker.chunk_text(text, content_type="story")
            
            logger.info(f"Split into {len(chunks)} chunks")
            
            # Step 2: Generate audio for each chunk
            chunk_files = []
            temp_dir = Path("temp/chunked_audio")
            temp_dir.mkdir(parents=True, exist_ok=True)
            
            total_cost = 0
            total_duration = 0
            
            for i, chunk in enumerate(chunks):
                chunk_path = temp_dir / f"chunk_{i+1:02d}_{job_id or 'episode'}.mp3"
                
                # Create request for this chunk
                chunk_request = TTSRequest(
                    job_id=TTSJobId(f"{job_id}_chunk_{i+1}" if job_id else f"chunk_{i+1}"),
                    text=chunk.text,
                    voice_config=voice_config,
                    output_path=chunk_path
                )
                
                # Generate audio for chunk
                chunk_result = await self.synthesize(chunk_request)
                
                if not chunk_result.success:
                    # Cleanup and return error
                    self._cleanup_chunk_files(chunk_files)
                    return TTSResult(
                        success=False,
                        error_message=f"Chunk {i+1} failed: {chunk_result.error_message}"
                    )
                
                chunk_files.append(chunk_path)
                total_cost += chunk_result.cost_cents or 0
                total_duration += chunk_result.audio_file.duration_seconds if chunk_result.audio_file else 0
                
                logger.info(f"Generated chunk {i+1}/{len(chunks)}")
            
            # Step 3: Concatenate chunks into final episode
            concatenator = AudioConcatenator()
            concat_result = await concatenator.concatenate_chunks(
                audio_files=chunk_files,
                output_path=output_path,
                add_pauses=True,
                crossfade=False  # Keep it simple for speech
            )
            
            if not concat_result.get("success"):
                self._cleanup_chunk_files(chunk_files)
                return TTSResult(
                    success=False,
                    error_message=f"Concatenation failed: {concat_result.get('error', 'Unknown error')}"
                )
            
            # Step 4: Create final audio file object
            final_audio_file = AudioFile(
                file_id=AudioFileId(f"chunked_{job_id or 'episode'}"),
                file_path=output_path,
                duration_seconds=total_duration,
                size_bytes=output_path.stat().st_size,
                format=voice_config.audio_format,
                sample_rate=voice_config.sample_rate_hertz,
                bitrate=128000,  # Estimated for MP3
                voice_config=voice_config,
                generated_at=datetime.now().isoformat(),
                text_input=text[:200] + "..." if len(text) > 200 else text  # Truncated for storage
            )
            
            # Cleanup temp files
            self._cleanup_chunk_files(chunk_files)
            concatenator.cleanup_temp_files()
            
            logger.info(f"Successfully generated long audio: {output_path} ({len(chunks)} chunks, {total_duration:.1f}s)")
            
            return TTSResult(
                success=True,
                audio_file=final_audio_file,
                cost_cents=total_cost,
                provider_response={
                    "method": "chunked_synthesis",
                    "chunks_generated": len(chunks),
                    "total_duration": total_duration,
                    "concatenation_method": concat_result.get("method", "unknown")
                }
            )
            
        except Exception as e:
            logger.error(f"Long text synthesis failed: {e}")
            # Cleanup any partial files
            if 'chunk_files' in locals():
                self._cleanup_chunk_files(chunk_files)
            
            return TTSResult(
                success=False,
                error_message=f"Long text synthesis error: {str(e)}"
            )
    
    def _cleanup_chunk_files(self, chunk_files: List[Path]):
        """Clean up temporary chunk files"""
        for chunk_file in chunk_files:
            try:
                if chunk_file.exists():
                    chunk_file.unlink()
            except Exception as e:
                logger.warning(f"Could not delete chunk file {chunk_file}: {e}")
    
    def _estimate_duration(self, text: str, speed: float) -> float:
        """Estimate audio duration based on text length and speaking rate"""
        # Average: 150 words per minute at normal speed
        words = len(text.split())
        base_wpm = 150
        adjusted_wpm = base_wpm * speed
        duration_minutes = words / adjusted_wpm
        return duration_minutes * 60  # Convert to seconds
    
    def _estimate_bitrate(self, file_size_bytes: int, duration_seconds: float) -> int:
        """Estimate audio bitrate from file size and duration"""
        if duration_seconds <= 0:
            return 128  # Default bitrate
        
        bits_per_second = (file_size_bytes * 8) / duration_seconds
        kbps = int(bits_per_second / 1000)
        return max(32, min(320, kbps))  # Clamp to reasonable range
    
    def optimize_for_storytelling(self, text: str) -> str:
        """
        Optimize text for storytelling narration.
        
        This maintains compatibility with your existing Fairer Tales system.
        """
        # Add natural pauses for storytelling
        optimized_text = text
        
        # Add pauses after dialogue
        optimized_text = optimized_text.replace('"', '"<break time="0.5s">')
        
        # Add emphasis to dramatic moments
        dramatic_words = ['suddenly', 'whispered', 'screamed', 'gasped']
        for word in dramatic_words:
            optimized_text = optimized_text.replace(
                f' {word} ', 
                f' <emphasis level="moderate">{word}</emphasis> '
            )
        
        # Add pauses before scene transitions
        optimized_text = optimized_text.replace('\n\n', '\n\n<break time="1s">')
        
        return optimized_text