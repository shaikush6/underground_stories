#!/usr/bin/env python3
"""
Core audio types and protocols for TTS provider abstraction.
Following CLAUDE.md standards for branded types and protocols.
"""

from typing import Protocol, Dict, Any, Optional, Literal
from dataclasses import dataclass
from pathlib import Path
from enum import Enum


# Branded types following C-5 standard
class AudioFileId(str):
    """Branded type for audio file identifiers"""
    pass


class VoiceConfigId(str):
    """Branded type for voice configuration identifiers"""
    pass


class TTSJobId(str):
    """Branded type for TTS job identifiers"""
    pass


# Audio quality and format enums
class AudioFormat(str, Enum):
    MP3 = "mp3"
    WAV = "wav"
    FLAC = "flac"
    OGG = "ogg"


class TTSProvider(str, Enum):
    GOOGLE = "google"
    OPENAI = "openai"
    ELEVENLABS = "elevenlabs"


class AudioQuality(str, Enum):
    STANDARD = "standard"
    HIGH = "high"
    PREMIUM = "premium"


@dataclass
class VoiceConfig:
    """Voice configuration for TTS generation"""
    provider: TTSProvider
    voice_id: str
    language_code: str
    speed: float = 1.0
    pitch: float = 0.0
    volume_gain_db: float = 0.0
    sample_rate_hertz: int = 24000
    audio_format: AudioFormat = AudioFormat.MP3
    extra_params: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.extra_params is None:
            self.extra_params = {}


@dataclass
class AudioFile:
    """Represents a generated audio file"""
    file_id: AudioFileId
    file_path: Path
    duration_seconds: float
    size_bytes: int
    format: AudioFormat
    sample_rate: int
    bitrate: int
    voice_config: VoiceConfig
    generated_at: str  # ISO timestamp
    text_input: str  # Original text used
    
    @property
    def exists(self) -> bool:
        """Check if audio file exists on disk"""
        return self.file_path.exists()
    
    def get_duration_minutes(self) -> float:
        """Get duration in minutes"""
        return self.duration_seconds / 60.0


@dataclass
class TTSRequest:
    """Request for TTS generation"""
    job_id: TTSJobId
    text: str
    voice_config: VoiceConfig
    output_path: Path
    max_retries: int = 3
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


@dataclass
class TTSResult:
    """Result of TTS generation"""
    success: bool
    audio_file: Optional[AudioFile] = None
    error_message: Optional[str] = None
    cost_cents: Optional[int] = None  # Cost in cents
    provider_response: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.provider_response is None:
            self.provider_response = {}


@dataclass
class ProviderLimits:
    """Provider-specific limits and capabilities"""
    max_characters: int
    max_requests_per_minute: int
    cost_per_million_characters: int  # Cost in cents
    supported_formats: list[AudioFormat]
    supported_languages: list[str]
    max_speech_rate: float
    min_speech_rate: float


class TTSProviderProtocol(Protocol):
    """Protocol for TTS provider implementations"""
    
    async def synthesize(self, request: TTSRequest) -> TTSResult:
        """
        Generate speech from text using the provider's API.
        
        Args:
            request: TTS generation request with text and configuration
            
        Returns:
            TTSResult with audio file or error information
        """
        ...
    
    def get_limits(self) -> ProviderLimits:
        """Get provider-specific limits and capabilities"""
        ...
    
    def validate_config(self, config: VoiceConfig) -> bool:
        """Validate voice configuration for this provider"""
        ...
    
    def estimate_cost(self, text: str) -> int:
        """Estimate cost in cents for generating audio from text"""
        ...
    
    def get_available_voices(self) -> list[str]:
        """Get list of available voice IDs for this provider"""
        ...