#!/usr/bin/env python3
"""
Voice Rotation System for Minute Myths
======================================

Intelligent voice selection based on mythology type and story characteristics.
Uses Google Chirp3-HD voices for optimal storytelling variety.
"""

import logging
import random
from typing import Dict, List, Optional
from dataclasses import dataclass
from core.audio.types import VoiceConfig, TTSProvider, AudioFormat

logger = logging.getLogger(__name__)


@dataclass
class VoiceProfile:
    """Represents a voice with its characteristics"""
    voice_id: str
    name: str
    characteristics: List[str]
    best_for_mythologies: List[str]
    best_for_moods: List[str]
    personality: str
    speed_modifier: float = 1.15  # Default for myths


class MythologyVoiceRotation:
    """
    Intelligent voice rotation system for mythology stories.
    
    Features:
    - Mythology-specific voice matching
    - Mood-based voice selection
    - Character type optimization
    - Variety and freshness
    """
    
    def __init__(self):
        self.voice_profiles = self._init_voice_profiles()
        self.usage_history = {}  # Track voice usage for variety
        self.default_voice = "en-US-Chirp3-HD-Schedar"
        
        logger.info(f"🎭 Voice Rotation System initialized with {len(self.voice_profiles)} voices")
    
    def _init_voice_profiles(self) -> Dict[str, VoiceProfile]:
        """Initialize Chirp3-HD voice profiles with characteristics"""
        
        profiles = {
            "schedar": VoiceProfile(
                voice_id="en-US-Chirp3-HD-Schedar",
                name="Schedar",
                characteristics=["Authoritative", "Wise", "Mysterious"],
                best_for_mythologies=["Greek", "Roman", "Celtic"],
                best_for_moods=["Epic", "Wisdom", "Mystery"],
                personality="The Ancient Sage - Perfect for classical mythology and wise teachings"
            ),
            
            "achernar": VoiceProfile(
                voice_id="en-US-Chirp3-HD-Achernar", 
                name="Achernar",
                characteristics=["Dramatic", "Intense", "Powerful"],
                best_for_mythologies=["Norse", "Germanic", "Slavic"],
                best_for_moods=["Battle", "Conflict", "Transformation"],
                personality="The Epic Narrator - Ideal for dramatic tales and heroic sagas"
            ),
            
            "altair": VoiceProfile(
                voice_id="en-US-Chirp3-HD-Altair",
                name="Altair", 
                characteristics=["Swift", "Energetic", "Dynamic"],
                best_for_mythologies=["Egyptian", "Mesopotamian", "Aztec"],
                best_for_moods=["Adventure", "Discovery", "Transformation"],
                personality="The Swift Storyteller - Great for action-packed adventures"
            ),
            
            "vega": VoiceProfile(
                voice_id="en-US-Chirp3-HD-Vega",
                name="Vega",
                characteristics=["Elegant", "Graceful", "Mystical"],
                best_for_mythologies=["Japanese", "Chinese", "Hindu"],
                best_for_moods=["Spiritual", "Romantic", "Mystical"],
                personality="The Mystical Voice - Perfect for spiritual and romantic tales"
            ),
            
            "sirius": VoiceProfile(
                voice_id="en-US-Chirp3-HD-Sirius",
                name="Sirius",
                characteristics=["Bold", "Commanding", "Heroic"],
                best_for_mythologies=["Roman", "Greek", "Persian"],
                best_for_moods=["Heroic", "Victory", "Leadership"],
                personality="The Hero's Voice - Ideal for tales of triumph and leadership"
            )
        }
        
        return profiles
    
    def select_voice_for_myth(self, mythology: str, character: str, 
                             story_mood: str = "neutral", 
                             force_variety: bool = True) -> VoiceConfig:
        """
        Select optimal voice based on mythology and story characteristics.
        
        Args:
            mythology: Greek, Norse, Egyptian, etc.
            character: Main character name
            story_mood: epic, mysterious, romantic, heroic, etc.
            force_variety: Avoid recently used voices
        """
        
        # Score voices based on mythology and mood matching
        scored_voices = []
        
        for voice_key, profile in self.voice_profiles.items():
            score = 0
            
            # Mythology match (highest weight)
            if mythology in profile.best_for_mythologies:
                score += 5
            
            # Mood match
            if story_mood.lower() in [mood.lower() for mood in profile.best_for_moods]:
                score += 3
            
            # Character-based adjustments
            character_lower = character.lower()
            if any(trait in character_lower for trait in ["god", "king", "emperor"]):
                if "Authoritative" in profile.characteristics:
                    score += 2
            
            if any(trait in character_lower for trait in ["warrior", "hero", "fighter"]):
                if "Heroic" in profile.characteristics or "Bold" in profile.characteristics:
                    score += 2
            
            if any(trait in character_lower for trait in ["goddess", "priestess", "oracle"]):
                if "Mystical" in profile.characteristics or "Elegant" in profile.characteristics:
                    score += 2
            
            # Variety bonus (avoid recently used voices)
            if force_variety and voice_key in self.usage_history:
                recent_usage = self.usage_history[voice_key]
                if recent_usage < 3:  # Haven't used recently
                    score += 1
                else:
                    score -= 2  # Heavily used recently
            
            scored_voices.append((voice_key, profile, score))
        
        # Sort by score and add randomness for top matches
        scored_voices.sort(key=lambda x: x[2], reverse=True)
        
        # Select from top 2-3 voices for variety
        top_voices = scored_voices[:min(3, len(scored_voices))]
        selected_key, selected_profile, score = random.choice(top_voices)
        
        # Update usage history
        self.usage_history[selected_key] = self.usage_history.get(selected_key, 0) + 1
        
        # Reset usage counts if all voices have been used multiple times
        if all(count >= 5 for count in self.usage_history.values()):
            self.usage_history = {key: 0 for key in self.usage_history}
        
        logger.info(f"🎭 Selected voice: {selected_profile.name} for {mythology} - {character}")
        logger.info(f"   Reasoning: {selected_profile.personality}")
        logger.info(f"   Score: {score} | Usage: {self.usage_history[selected_key]}")
        
        # Create voice configuration
        voice_config = VoiceConfig(
            provider=TTSProvider.GOOGLE,
            voice_id=selected_profile.voice_id,
            language_code="en-US",
            speed=selected_profile.speed_modifier,
            pitch=0.0,  # Chirp3 voices don't support pitch
            volume_gain_db=0.0,
            audio_format=AudioFormat.MP3,
            sample_rate_hertz=22050
        )
        
        return voice_config
    
    def get_voice_recommendations(self, mythology: str) -> List[VoiceProfile]:
        """Get voice recommendations for a specific mythology"""
        
        recommendations = []
        for profile in self.voice_profiles.values():
            if mythology in profile.best_for_mythologies:
                recommendations.append(profile)
        
        # Sort by best match and add variety
        recommendations.sort(key=lambda p: len([m for m in p.best_for_mythologies if m == mythology]), reverse=True)
        
        return recommendations
    
    def get_voice_analytics(self) -> Dict:
        """Get analytics on voice usage patterns"""
        
        total_uses = sum(self.usage_history.values())
        
        analytics = {
            "total_voice_selections": total_uses,
            "voice_distribution": {},
            "most_used_voice": None,
            "least_used_voice": None,
            "variety_score": 0.0
        }
        
        if total_uses > 0:
            # Calculate distribution
            for voice_key, profile in self.voice_profiles.items():
                usage = self.usage_history.get(voice_key, 0)
                percentage = (usage / total_uses) * 100
                
                analytics["voice_distribution"][profile.name] = {
                    "usage_count": usage,
                    "percentage": round(percentage, 1),
                    "characteristics": profile.characteristics
                }
            
            # Find most/least used
            if self.usage_history:
                most_used_key = max(self.usage_history, key=self.usage_history.get)
                least_used_key = min(self.usage_history, key=self.usage_history.get)
                
                analytics["most_used_voice"] = self.voice_profiles[most_used_key].name
                analytics["least_used_voice"] = self.voice_profiles[least_used_key].name
            
            # Calculate variety score (0-1, where 1 is perfect variety)
            if len(self.usage_history) > 1:
                usage_values = list(self.usage_history.values())
                mean_usage = sum(usage_values) / len(usage_values)
                variance = sum((x - mean_usage) ** 2 for x in usage_values) / len(usage_values)
                variety_score = max(0, 1 - (variance / (mean_usage ** 2)) if mean_usage > 0 else 0)
                analytics["variety_score"] = round(variety_score, 2)
        
        return analytics
    
    def reset_usage_history(self):
        """Reset voice usage history for fresh rotation"""
        self.usage_history = {}
        logger.info("🔄 Voice usage history reset")


async def test_voice_rotation():
    """Test the voice rotation system"""
    
    logging.basicConfig(level=logging.INFO)
    logger.info("🎭 Testing Voice Rotation System")
    
    rotation = MythologyVoiceRotation()
    
    # Test scenarios
    test_cases = [
        {"mythology": "Greek", "character": "Pandora", "mood": "mysterious"},
        {"mythology": "Norse", "character": "Loki", "mood": "epic"},
        {"mythology": "Egyptian", "character": "Isis", "mood": "mystical"},
        {"mythology": "Celtic", "character": "Brigid", "mood": "spiritual"},
        {"mythology": "Japanese", "character": "Susanoo", "mood": "dramatic"},
        {"mythology": "Greek", "character": "Zeus", "mood": "heroic"},  # Test variety
        {"mythology": "Norse", "character": "Thor", "mood": "battle"},   # Test variety
    ]
    
    logger.info("\n🎯 Testing Voice Selection:")
    for i, test_case in enumerate(test_cases, 1):
        logger.info(f"\n--- Test {i}: {test_case['mythology']} - {test_case['character']} ---")
        
        voice_config = rotation.select_voice_for_myth(
            mythology=test_case["mythology"],
            character=test_case["character"], 
            story_mood=test_case["mood"]
        )
        
        logger.info(f"Selected: {voice_config.voice_id}")
    
    # Show analytics
    analytics = rotation.get_voice_analytics()
    logger.info(f"\n📊 Voice Usage Analytics:")
    logger.info(f"Total selections: {analytics['total_voice_selections']}")
    logger.info(f"Variety score: {analytics['variety_score']}")
    
    if analytics["voice_distribution"]:
        logger.info("Voice distribution:")
        for voice_name, stats in analytics["voice_distribution"].items():
            logger.info(f"  {voice_name}: {stats['usage_count']} uses ({stats['percentage']}%)")
    
    # Test recommendations
    logger.info(f"\n💡 Voice Recommendations for Greek Mythology:")
    recommendations = rotation.get_voice_recommendations("Greek")
    for profile in recommendations:
        logger.info(f"  {profile.name}: {profile.personality}")


if __name__ == "__main__":
    import asyncio
    asyncio.run(test_voice_rotation())