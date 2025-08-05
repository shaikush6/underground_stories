#!/usr/bin/env python3
"""
Underground Stories Voice Manager
===============================

Centralized voice selection and management system.
Foundation for UI control and easy voice switching.
"""

import json
from typing import Dict, List, Optional
from pathlib import Path
from dataclasses import dataclass, asdict
from enum import Enum

from .audio.types import VoiceConfig, TTSProvider, AudioFormat


class VoiceCategory(Enum):
    STORYTELLING = "storytelling"
    NARRATION = "narration"
    CHARACTER = "character"
    ENERGETIC = "energetic"
    SOPHISTICATED = "sophisticated"
    DRAMATIC = "dramatic"


@dataclass
class VoiceProfile:
    """Complete voice profile with metadata"""
    id: str
    name: str
    provider: TTSProvider
    voice_id: str
    category: VoiceCategory
    description: str
    gender: str
    sample_file: Optional[str] = None
    instructions: Optional[str] = None
    recommended_for: List[str] = None
    
    def to_voice_config(self, speed: float = 1.0, pitch: float = 0.0) -> VoiceConfig:
        """Convert to VoiceConfig for audio generation"""
        return VoiceConfig(
            provider=self.provider,
            voice_id=self.voice_id,
            language_code="en-US",
            speed=speed,
            pitch=pitch,
            volume_gain_db=0.0,
            audio_format=AudioFormat.MP3,
            sample_rate_hertz=22050
        )


class VoiceManager:
    """
    Centralized voice management system for Underground Stories.
    
    Features:
    - Voice catalog with samples
    - Easy switching between providers
    - Pipeline-specific recommendations
    - UI-ready voice selection
    """
    
    def __init__(self):
        self.voices_catalog = self._initialize_voice_catalog()
        self.pipeline_defaults = self._initialize_pipeline_defaults()
    
    def _initialize_voice_catalog(self) -> Dict[str, VoiceProfile]:
        """Initialize the complete voice catalog"""
        
        voices = {}
        
        # OpenAI Advanced Voices with Storytelling Instructions
        openai_storytelling_instruction = """Voice: Warm, engaging storyteller with natural character variation and emotional depth.
Tone: Rich and captivating, balancing empathy with intrigue for complex narratives.
Delivery: Conversational yet compelling, with authentic emotional resonance.
Pacing: Natural rhythm that keeps listeners engaged while allowing story beats to land."""
        
        openai_narration_instruction = """Voice: Authoritative yet accessible narrator with classical literary sensibility.
Tone: Scholarly but approachable, maintaining gravitas while being digestible.
Delivery: Measured and articulate, with sophisticated storytelling rhythm.
Pacing: Contemplative and deliberate, honoring literary elegance."""
        
        openai_energetic_instruction = """Voice: Dynamic and compelling with infectious energy that captures attention.
Tone: Urgent and captivating, building momentum like a master storyteller.
Delivery: Crisp and purposeful, maximizing impact within timeframes.
Pacing: Rhythmic and driving, with strategic emphasis on key moments."""
        
        # OpenAI Voices
        voices.update({
            "openai_ballad": VoiceProfile(
                id="openai_ballad",
                name="Ballad (Emotional Storyteller)",
                provider=TTSProvider.OPENAI,
                voice_id="ballad",
                category=VoiceCategory.STORYTELLING,
                description="Warm, expressive, emotionally rich - perfect for character-driven stories",
                gender="neutral",
                sample_file="voice_samples_storytelling/fairer_tales_ballad.mp3",
                instructions=openai_storytelling_instruction,
                recommended_for=["fairer_tales", "character_voices", "emotional_content"]
            ),
            
            "openai_sage": VoiceProfile(
                id="openai_sage",
                name="Sage (Wise Narrator)",
                provider=TTSProvider.OPENAI,
                voice_id="sage",
                category=VoiceCategory.NARRATION,
                description="Wise, thoughtful, contemplative - perfect for classic literature",
                gender="neutral",
                sample_file="voice_samples_storytelling/timeless_retold_sage.mp3",
                instructions=openai_narration_instruction,
                recommended_for=["timeless_retold", "classic_literature", "educational_content"]
            ),
            
            "openai_ash": VoiceProfile(
                id="openai_ash",
                name="Ash (Sophisticated Jazz Host)",
                provider=TTSProvider.OPENAI,
                voice_id="ash",
                category=VoiceCategory.SOPHISTICATED,
                description="Deep, velvety, effortlessly cool like a late-night jazz radio host",
                gender="neutral",
                sample_file="voice_samples_storytelling/fairer_tales_ash.mp3",
                instructions=openai_storytelling_instruction,
                recommended_for=["fairer_tales", "sophisticated_content", "atmospheric_stories"]
            ),
            
            "openai_coral": VoiceProfile(
                id="openai_coral",
                name="Coral (High Energy)",
                provider=TTSProvider.OPENAI,
                voice_id="coral",
                category=VoiceCategory.ENERGETIC,
                description="High-energy, upbeat, encouraging - perfect for viral content",
                gender="neutral",
                sample_file="voice_samples_storytelling/minute_myths_coral.mp3",
                instructions=openai_energetic_instruction,
                recommended_for=["minute_myths", "viral_content", "motivational_content"]
            ),
            
            "openai_echo": VoiceProfile(
                id="openai_echo",
                name="Echo (Dramatic Narrator)",
                provider=TTSProvider.OPENAI,
                voice_id="echo",
                category=VoiceCategory.DRAMATIC,
                description="Commanding and dramatic with theatrical flair",
                gender="neutral",
                sample_file="voice_samples_storytelling/minute_myths_echo.mp3",
                instructions=openai_energetic_instruction,
                recommended_for=["minute_myths", "dramatic_content", "mythology"]
            ),
            
            "openai_fable": VoiceProfile(
                id="openai_fable",
                name="Fable (Gentle Storyteller)",
                provider=TTSProvider.OPENAI,
                voice_id="fable",
                category=VoiceCategory.STORYTELLING,
                description="Gentle, warm, reassuring like a master storyteller",
                gender="neutral",
                sample_file="voice_samples_storytelling/fairer_tales_fable.mp3",
                instructions=openai_storytelling_instruction,
                recommended_for=["fairer_tales", "gentle_stories", "children_content"]
            ),
            
            "openai_alloy": VoiceProfile(
                id="openai_alloy",
                name="Alloy (Professional)",
                provider=TTSProvider.OPENAI,
                voice_id="alloy",
                category=VoiceCategory.NARRATION,
                description="Clear, authoritative, professional narrator",
                gender="neutral",
                sample_file="voice_samples_storytelling/timeless_retold_alloy.mp3",
                instructions=openai_narration_instruction,
                recommended_for=["timeless_retold", "professional_content", "educational"]
            ),
            
            "openai_onyx": VoiceProfile(
                id="openai_onyx",
                name="Onyx (Deep Authority)",
                provider=TTSProvider.OPENAI,
                voice_id="onyx",
                category=VoiceCategory.NARRATION,
                description="Deep, resonant, powerfully authoritative",
                gender="male",
                sample_file="voice_samples_storytelling/timeless_retold_onyx.mp3",
                instructions=openai_narration_instruction,
                recommended_for=["timeless_retold", "authoritative_content", "serious_topics"]
            )
        })
        
        # Google Chirp3-HD Voices
        voices.update({
            "google_zephyr": VoiceProfile(
                id="google_zephyr",
                name="Zephyr (Chirp3-HD)",
                provider=TTSProvider.GOOGLE,
                voice_id="en-US-Chirp3-HD-Zephyr",
                category=VoiceCategory.STORYTELLING,
                description="Google's newest voice technology - energetic storytelling",
                gender="neutral",
                sample_file="voice_samples_chirp3/chirp3_zephyr.mp3",
                recommended_for=["minute_myths", "energetic_content"]
            ),
            
            "google_achernar": VoiceProfile(
                id="google_achernar",
                name="Achernar (Chirp3-HD)",
                provider=TTSProvider.GOOGLE,
                voice_id="en-US-Chirp3-HD-Achernar",
                category=VoiceCategory.NARRATION,
                description="Google's newest voice technology - sophisticated narrator",
                gender="neutral",
                sample_file="voice_samples_chirp3/chirp3_achernar.mp3",
                recommended_for=["timeless_retold", "sophisticated_content"]
            ),
            
            "google_fenrir": VoiceProfile(
                id="google_fenrir",
                name="Fenrir (Chirp3-HD)",
                provider=TTSProvider.GOOGLE,
                voice_id="en-US-Chirp3-HD-Fenrir",
                category=VoiceCategory.DRAMATIC,
                description="Google's newest voice technology - dramatic power",
                gender="neutral",
                sample_file="voice_samples_chirp3/chirp3_fenrir.mp3",
                recommended_for=["minute_myths", "dramatic_content", "mythology"]
            )
        })
        
        return voices
    
    def _initialize_pipeline_defaults(self) -> Dict[str, str]:
        """Set default voices for each pipeline"""
        return {
            "fairer_tales": "openai_ballad",      # Emotional storyteller
            "timeless_retold": "google_achernar",  # Chirp3-HD sophisticated
            "minute_myths": "google_zephyr",       # Chirp3-HD energetic
            "backup_timeless": "openai_sage"       # OpenAI backup
        }
    
    def get_voice_profile(self, voice_id: str) -> Optional[VoiceProfile]:
        """Get voice profile by ID"""
        return self.voices_catalog.get(voice_id)
    
    def get_voices_by_category(self, category: VoiceCategory) -> List[VoiceProfile]:
        """Get all voices in a category"""
        return [voice for voice in self.voices_catalog.values() 
                if voice.category == category]
    
    def get_voices_by_provider(self, provider: TTSProvider) -> List[VoiceProfile]:
        """Get all voices from a provider"""
        return [voice for voice in self.voices_catalog.values() 
                if voice.provider == provider]
    
    def get_recommended_voices(self, pipeline: str) -> List[VoiceProfile]:
        """Get recommended voices for a pipeline"""
        return [voice for voice in self.voices_catalog.values()
                if pipeline in voice.recommended_for or []]
    
    def get_pipeline_default(self, pipeline: str) -> Optional[VoiceProfile]:
        """Get default voice for a pipeline"""
        default_id = self.pipeline_defaults.get(pipeline)
        if default_id:
            return self.get_voice_profile(default_id)
        return None
    
    def set_pipeline_default(self, pipeline: str, voice_id: str) -> bool:
        """Set default voice for a pipeline"""
        if voice_id in self.voices_catalog:
            self.pipeline_defaults[pipeline] = voice_id
            return True
        return False
    
    def save_configuration(self, config_path: Path):
        """Save voice configuration to file"""
        config = {
            "pipeline_defaults": self.pipeline_defaults,
            "voices_catalog": {vid: asdict(voice) for vid, voice in self.voices_catalog.items()}
        }
        
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2, default=str)
    
    def load_configuration(self, config_path: Path):
        """Load voice configuration from file"""
        if config_path.exists():
            with open(config_path, 'r') as f:
                config = json.load(f)
            
            self.pipeline_defaults = config.get("pipeline_defaults", {})
            # Note: Would need to reconstruct VoiceProfile objects from dict
    
    def list_all_voices(self) -> Dict[str, Dict]:
        """Get all voices formatted for UI display"""
        result = {}
        
        for category in VoiceCategory:
            category_voices = self.get_voices_by_category(category)
            result[category.value] = [
                {
                    "id": voice.id,
                    "name": voice.name,
                    "provider": voice.provider.value,
                    "description": voice.description,
                    "gender": voice.gender,
                    "sample_file": voice.sample_file,
                    "recommended_for": voice.recommended_for or []
                }
                for voice in category_voices
            ]
        
        return result


# Global voice manager instance
voice_manager = VoiceManager()


def get_voice_manager() -> VoiceManager:
    """Get the global voice manager instance"""
    return voice_manager