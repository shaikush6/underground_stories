#!/usr/bin/env python3
"""
Google Cloud Text-to-Speech provider implementation.
Optimized for Timeless, Retold (classics) and Minute Myths (shorts).
"""

import asyncio
import logging
import json
from typing import List, Optional
from pathlib import Path
from datetime import datetime
import aiohttp
import os
from google.cloud import texttospeech
from google.oauth2 import service_account

from ..types import (
    TTSProviderProtocol, TTSRequest, TTSResult, VoiceConfig, 
    AudioFile, AudioFileId, ProviderLimits, AudioFormat, TTSProvider
)


logger = logging.getLogger(__name__)


class GoogleTTSProvider:
    """
    Google Cloud Text-to-Speech provider implementation.
    
    Supports Neural2 voices for cost-effective classics and 
    Chirp3 HD voices for premium shorts content.
    """
    
    def __init__(self, credentials_path: Optional[str] = None, project_id: Optional[str] = None):
        self.project_id = project_id or os.getenv('GOOGLE_PROJECT_ID')
        self.credentials_path = credentials_path or os.getenv('GOOGLE_CLOUD_CREDENTIALS_PATH')
        
        # Initialize client with explicit credentials
        if self.credentials_path and Path(self.credentials_path).exists():
            logger.info(f"Using Google credentials from: {self.credentials_path}")
            credentials = service_account.Credentials.from_service_account_file(
                self.credentials_path
            )
            # Set the project explicitly to avoid quota issues
            credentials = credentials.with_quota_project(self.project_id)
            self.client = texttospeech.TextToSpeechClient(credentials=credentials)
        else:
            logger.warning(f"Credentials not found at {self.credentials_path}, using default")
            # Use default credentials (e.g., from environment)
            self.client = texttospeech.TextToSpeechClient()
        
        # Voice mapping for different content types
        self.voice_mapping = {
            # Timeless, Retold - Professional narrator voices
            "timeless_narrator_male": "en-US-Neural2-J",
            "timeless_narrator_female": "en-US-Neural2-F", 
            "timeless_british_male": "en-GB-Neural2-B",
            
            # Minute Myths - Engaging HD voices
            "myths_energetic_male": "en-US-Chirp3-HD-A",
            "myths_energetic_female": "en-US-Chirp3-HD-B",
            "myths_dramatic": "en-US-Chirp3-HD-C"
        }
        
        logger.info("Google TTS provider initialized")
    
    async def synthesize(self, request: TTSRequest) -> TTSResult:
        """Generate speech using Google Cloud Text-to-Speech"""
        try:
            # Prepare synthesis input
            synthesis_input = texttospeech.SynthesisInput(text=request.text)
            
            # Configure voice with appropriate gender
            voice_gender = self._get_voice_gender(request.voice_config.voice_id)
            voice = texttospeech.VoiceSelectionParams(
                language_code=request.voice_config.language_code,
                name=request.voice_config.voice_id,
                ssml_gender=voice_gender
            )
            
            # Configure audio output
            audio_config = texttospeech.AudioConfig(
                audio_encoding=self._get_audio_encoding(request.voice_config.audio_format),
                sample_rate_hertz=request.voice_config.sample_rate_hertz,
                speaking_rate=request.voice_config.speed,
                pitch=request.voice_config.pitch,
                volume_gain_db=request.voice_config.volume_gain_db
            )
            
            # Generate speech
            response = await asyncio.get_event_loop().run_in_executor(
                None,
                self.client.synthesize_speech,
                {"input": synthesis_input, "voice": voice, "audio_config": audio_config}
            )
            
            # Save audio file
            request.output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(request.output_path, "wb") as f:
                f.write(response.audio_content)
            
            # Calculate audio properties
            duration = self._estimate_duration(request.text, request.voice_config.speed)
            file_size = len(response.audio_content)
            
            # Create audio file object
            audio_file = AudioFile(
                file_id=AudioFileId(f"google_{request.job_id}"),
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
            cost_cents = self.estimate_cost(request.text, request.voice_config.voice_id)
            
            logger.info(f"Generated audio: {request.output_path} ({duration:.1f}s, {file_size} bytes)")
            
            return TTSResult(
                success=True,
                audio_file=audio_file,
                cost_cents=cost_cents,
                provider_response={"duration": duration, "size": file_size}
            )
            
        except Exception as e:
            logger.error(f"Google TTS synthesis failed: {e}")
            return TTSResult(
                success=False,
                error_message=f"Google TTS error: {str(e)}"
            )
    
    def get_limits(self) -> ProviderLimits:
        """Get Google Cloud TTS limits and capabilities"""
        return ProviderLimits(
            max_characters=4000,  # 5000 bytes ≈ 4000 characters (safe margin)
            max_requests_per_minute=100,
            cost_per_million_characters=1600,  # $16 per million chars (Neural2)
            supported_formats=[AudioFormat.MP3, AudioFormat.WAV, AudioFormat.OGG],
            supported_languages=["en-US", "en-GB", "es-ES", "fr-FR", "de-DE"],
            max_speech_rate=4.0,
            min_speech_rate=0.25
        )
    
    def validate_config(self, config: VoiceConfig) -> bool:
        """Validate voice configuration for Google TTS"""
        if config.provider != TTSProvider.GOOGLE:
            return False
        
        # Check voice availability
        available_voices = self.get_available_voices()
        if config.voice_id not in available_voices:
            logger.warning(f"Voice {config.voice_id} not available in Google TTS")
            return False
        
        # Check parameter ranges
        if not (0.25 <= config.speed <= 4.0):
            return False
        if not (-20.0 <= config.pitch <= 20.0):
            return False
        if not (-96.0 <= config.volume_gain_db <= 16.0):
            return False
        
        return True
    
    def estimate_cost(self, text: str, voice_id: str = None) -> int:
        """Estimate cost in cents for text generation"""
        character_count = len(text)
        
        # Google pricing tiers (in cents per million characters)
        if voice_id and ("Journey" in voice_id or "Studio" in voice_id):
            cost_per_million = 16000  # Premium voices: $160/million chars
        elif voice_id and "Wavenet" in voice_id:
            cost_per_million = 1600   # Wavenet: $16/million chars  
        else:
            cost_per_million = 400    # Neural2: $4/million chars
        
        # Estimate based on character count
        cost_cents = (character_count / 1_000_000) * cost_per_million
        
        # Minimum cost of 1 cent
        return max(1, int(cost_cents))
    
    def get_available_voices(self) -> List[str]:
        """Get list of available Google TTS voices"""
        try:
            # Get voices from Google API
            voices = self.client.list_voices()
            
            # Filter for English voices only for now
            english_voices = [
                voice.name for voice in voices.voices 
                if voice.language_codes[0].startswith('en-')
            ]
            
            return english_voices
            
        except Exception as e:
            logger.warning(f"Could not fetch Google voices: {e}")
            # Return fallback list
            return [
                "en-US-Neural2-A", "en-US-Neural2-C", "en-US-Neural2-D",
                "en-US-Neural2-F", "en-US-Neural2-G", "en-US-Neural2-H", 
                "en-US-Neural2-I", "en-US-Neural2-J",
                "en-GB-Neural2-A", "en-GB-Neural2-B", "en-GB-Neural2-C"
            ]
    
    def _get_audio_encoding(self, format: AudioFormat) -> texttospeech.AudioEncoding:
        """Convert AudioFormat to Google TTS encoding"""
        format_mapping = {
            AudioFormat.MP3: texttospeech.AudioEncoding.MP3,
            AudioFormat.WAV: texttospeech.AudioEncoding.LINEAR16,
            AudioFormat.OGG: texttospeech.AudioEncoding.OGG_OPUS
        }
        return format_mapping.get(format, texttospeech.AudioEncoding.MP3)
    
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
    
    def _get_voice_gender(self, voice_id: str) -> texttospeech.SsmlVoiceGender:
        """Get appropriate gender for voice ID"""
        # Map voice IDs to genders (including premium Journey voices)
        female_voices = [
            # Neural2 voices
            "en-US-Neural2-C", "en-US-Neural2-E", "en-US-Neural2-F", "en-US-Neural2-G", "en-US-Neural2-H",
            # Premium Journey voices
            "en-US-Journey-F",
            # Studio voices - O is female
            "en-US-Studio-O"
        ]
        male_voices = [
            # Neural2 voices  
            "en-US-Neural2-A", "en-US-Neural2-B", "en-US-Neural2-D", "en-US-Neural2-I", "en-US-Neural2-J",
            # Premium Journey voices
            "en-US-Journey-D", "en-US-Journey-O",
            # Studio voices - Q is male
            "en-US-Studio-Q",
            # Wavenet voices - A, B, D, I, J are male
            "en-US-Wavenet-A", "en-US-Wavenet-B", "en-US-Wavenet-D", "en-US-Wavenet-I", "en-US-Wavenet-J"
        ]
        
        if voice_id in female_voices:
            return texttospeech.SsmlVoiceGender.FEMALE
        elif voice_id in male_voices:
            return texttospeech.SsmlVoiceGender.MALE
        else:
            return texttospeech.SsmlVoiceGender.NEUTRAL