#!/usr/bin/env python3
"""
Minute Myths Generator - 60-Second Mythology Stories
===================================================

Generates viral 60-second mythology stories for Underground Stories.
High-energy, fast-paced content optimized for engagement.
"""

import asyncio
import logging
import sys
import random
from typing import List, Dict, Optional
from pathlib import Path
from dataclasses import dataclass

# Add packages to path
sys.path.append(str(Path(__file__).parent.parent))

from core.audio.audio_pipeline import AudioPipeline
from core.audio.types import VoiceConfig, TTSProvider, AudioFormat
from core.audio.providers.google_tts import GoogleTTSProvider

logger = logging.getLogger(__name__)


@dataclass
class MythStory:
    """Represents a 60-second myth story"""
    title: str
    mythology: str  # Greek, Norse, Egyptian, etc.
    character: str
    story_text: str
    moral: str
    word_count: int
    estimated_duration: float


class MinuteMyths:
    """
    Generates viral 60-second mythology stories.
    
    Features:
    - Rapid-fire storytelling optimized for 60 seconds
    - High-energy Google TTS voice
    - Mythology from multiple cultures
    - Engaging hooks and cliffhangers
    """
    
    def __init__(self):
        self.audio_pipeline = AudioPipeline()
        
        # Register Google TTS with energetic voice for myths
        credentials_path = "config/google-cloud-credentials.json"
        project_id = "gen-lang-client-0693450484"
        google_provider = GoogleTTSProvider(credentials_path=credentials_path, project_id=project_id)
        self.audio_pipeline.register_provider(TTSProvider.GOOGLE, google_provider)
        
        # High-energy PREMIUM voice config for mythology - Google Chirp3-HD
        self.voice_config = VoiceConfig(
            provider=TTSProvider.GOOGLE,
            voice_id="en-US-Chirp3-HD-Schedar",  # NEWEST Chirp3-HD voice - default for myths
            language_code="en-US",
            speed=1.15,  # Faster for viral content
            pitch=0.0,   # Chirp3 voices don't support pitch
            volume_gain_db=0.0,
            audio_format=AudioFormat.MP3,
            sample_rate_hertz=22050
        )
        
        self.output_dir = Path("content/minute-myths/audio")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Target 150-160 words for 60-second content
        self.target_words = 155
        
        # Background music integration
        from core.audio.background_music import BackgroundMusicManager
        self.music_manager = BackgroundMusicManager()
        self.enable_background_music = True  # User can toggle this
        
        # Voice rotation system for variety
        from .voice_rotation import MythologyVoiceRotation
        self.voice_rotation = MythologyVoiceRotation()
        self.enable_voice_rotation = True  # User can toggle this
        
    def generate_myth_stories(self, count: int = 5) -> List[MythStory]:
        """Generate multiple myth stories"""
        stories = []
        
        # Quick mythology database
        myths_data = [
            {
                "mythology": "Greek",
                "character": "Pandora",
                "hook": "A woman's curiosity unleashed chaos upon the world",
                "story": "Zeus created Pandora as the perfect woman, but with a fatal flaw: insatiable curiosity. He gave her a mysterious box with one rule - never open it. Pandora tried to resist, but the whispers from within drove her mad. She lifted the lid just a crack. Out poured every evil known to humanity: disease, war, hatred, despair. Horrified, she slammed it shut, but it was too late. The world was forever changed. Yet one thing remained in the box - hope. Even in humanity's darkest hour, hope endures.",
                "moral": "Curiosity has consequences, but hope survives everything"
            },
            {
                "mythology": "Norse",
                "character": "Loki", 
                "hook": "A god's prank triggered the end of the world",
                "story": "Loki, the trickster god, was jealous of Baldr's perfection. Everyone loved Baldr - he was beautiful, kind, and seemingly invincible. Every weapon bounced off him harmlessly. But Loki discovered a secret: mistletoe could harm him. He crafted an arrow from mistletoe and tricked Baldr's blind brother Höðr into throwing it. The arrow pierced Baldr's heart, killing him instantly. The gods' anguish shook the nine realms. This wasn't just murder - it was the first domino falling toward Ragnarök, the end of everything.",
                "moral": "Jealousy destroys more than just its target"
            },
            {
                "mythology": "Egyptian",
                "character": "Isis",
                "hook": "A goddess defied death itself to save her beloved",
                "story": "Set murdered his brother Osiris out of jealousy, dismembering the body and scattering the pieces across Egypt. But Isis, Osiris's wife, refused to accept his death. She searched relentlessly, gathering every fragment of her husband's body. Using powerful magic, she reassembled him and breathed life back into his lifeless form. For one night, Osiris lived again. That single night of love gave them a son - Horus, who would one day avenge his father and become pharaoh of Egypt.",
                "moral": "Love transcends even death"
            },
            {
                "mythology": "Celtic",
                "character": "Brigid",
                "hook": "A goddess forged inspiration from the flames of creation",
                "story": "Brigid was born at sunrise with flames shooting from her head, connecting earth to heaven. She became the patron of smiths, poets, and healers - all who create and transform. When darkness threatened Ireland, she lit the first sacred fire that would burn for centuries. Warriors came seeking blessed weapons, poets sought divine inspiration, and the sick came for healing flames. Her fire didn't just burn - it created. Every spark carried the power to forge new realities, birth new ideas, heal old wounds.",
                "moral": "Creativity is humanity's most divine gift"
            },
            {
                "mythology": "Japanese",
                "character": "Susanoo",
                "hook": "A storm god's rage nearly broke the world",
                "story": "Susanoo, god of storms, threw such violent tantrums that mountains cracked and seas boiled. When his sister Amaterasu, the sun goddess, criticized his behavior, he destroyed her rice fields and defiled her sacred spaces. Horrified, Amaterasu hid in a cave, plunging the world into eternal darkness. Without sunlight, crops died and chaos reigned. The other gods desperately performed a wild dance to lure her out. Finally, curiosity made her peek from the cave. The moment light returned, they sealed the entrance. Balance was restored.",
                "moral": "Unchecked anger brings darkness to everyone"
            }
        ]
        
        # Generate stories from database
        selected_myths = random.sample(myths_data, min(count, len(myths_data)))
        
        for i, myth_data in enumerate(selected_myths, 1):
            story_text = self._create_60_second_story(myth_data)
            
            story = MythStory(
                title=f"Minute Myth #{i}: {myth_data['character']}",
                mythology=myth_data['mythology'],
                character=myth_data['character'],
                story_text=story_text,
                moral=myth_data['moral'],
                word_count=len(story_text.split()),
                estimated_duration=60  # Target duration
            )
            
            stories.append(story)
        
        return stories
    
    def _create_60_second_story(self, myth_data: Dict) -> str:
        """Create optimized 60-second story format"""
        
        # Underground Stories format for viral content
        story = f"""🔥 MINUTE MYTH: {myth_data['character']} 🔥

{myth_data['hook']}!

{myth_data['story']}

💡 THE TRUTH: {myth_data['moral']}.

This is {myth_data['character']} from {myth_data['mythology']} mythology - proving that ancient stories hold timeless truths.

Subscribe to Underground Stories for more myths that changed the world! 

#MinuteMyths #UndergroundStories #{myth_data['mythology']}Mythology #{myth_data['character']} #AncientWisdom"""

        return story
    
    async def generate_myth_audio(self, story: MythStory, job_id: Optional[str] = None) -> Dict:
        """Generate audio for a myth story"""
        
        logger.info(f"🏛️ Generating Minute Myth: {story.title}")
        
        # Select voice using rotation system if enabled
        if self.enable_voice_rotation:
            voice_config = self.voice_rotation.select_voice_for_myth(
                mythology=story.mythology,
                character=story.character,
                story_mood="dramatic",  # Most myths are dramatic
                force_variety=True
            )
            logger.info(f"🎭 Using rotated voice: {voice_config.voice_id}")
        else:
            voice_config = self.voice_config
            logger.info(f"🎭 Using default voice: {voice_config.voice_id}")
        
        # Create output path
        safe_title = story.title.replace(" ", "_").replace("#", "").replace(":", "")
        output_path = self.output_dir / f"{safe_title}.mp3"
        
        # Generate audio (should be single chunk due to 60-second target)
        result = await self.audio_pipeline.generate_audio(
            text=story.story_text,
            voice_config=voice_config,
            output_path=output_path,
            job_id=job_id or f"myth_{story.character.lower()}"
        )
        
        if result.success:
            # Add background music if enabled
            final_audio_path = output_path
            duration_seconds = result.audio_file.duration_seconds
            
            if self.enable_background_music:
                # Select dramatic music for mythology
                background_track = self.music_manager.select_music_for_story(
                    story_type="minute_myths",
                    story_mood="dramatic",
                    duration_seconds=duration_seconds
                )
                
                if background_track:
                    mixed_path = output_path.parent / f"{output_path.stem}_with_music{output_path.suffix}"
                    
                    mix_result = await self.music_manager.mix_audio_with_background(
                        voice_audio_path=output_path,
                        background_track=background_track,
                        output_path=mixed_path,
                        story_type="minute_myths"
                    )
                    
                    if mix_result["success"]:
                        final_audio_path = Path(mix_result["mixed_audio_path"])
                        logger.info(f"🎵 Added background music: {background_track.composer} - {background_track.title}")
                    else:
                        logger.warning(f"⚠️ Background music mixing failed: {mix_result.get('error')}")
            
            logger.info(f"✅ {story.title} complete:")
            logger.info(f"   Audio: {final_audio_path}")
            logger.info(f"   Duration: {duration_seconds:.1f} seconds")
            logger.info(f"   Words: {story.word_count}")
            logger.info(f"   Cost: {result.cost_cents}¢")
            
            # Create Underground Stories metadata
            underground_metadata = self._create_underground_metadata(story, result)
            
            return {
                "success": True,
                "story": story,
                "audio_path": str(final_audio_path),
                "duration_seconds": duration_seconds,
                "cost_cents": result.cost_cents,
                "underground_metadata": underground_metadata,
                "has_background_music": self.enable_background_music and 'background_track' in locals()
            }
        else:
            logger.error(f"❌ {story.title} failed: {result.error_message}")
            return {
                "success": False,
                "story": story,
                "error": result.error_message
            }
    
    def _create_underground_metadata(self, story: MythStory, result) -> Dict:
        """Create Underground Stories metadata for YouTube Shorts"""
        
        underground_title = f"Underground Myths: {story.character} - {story.mythology} Mythology | Minute Myths"
        
        description = f"""⚡ Welcome to Underground Stories - Minute Myths

Ancient wisdom in 60 seconds. This is the story of {story.character} from {story.mythology} mythology - proving that the most powerful truths come from the oldest stories.

🏛️ {story.character}: {story.moral}

Every myth holds a secret. Every legend teaches a lesson. In just one minute, discover the underground truths that shaped civilizations.

This is {story.mythology} mythology - raw, powerful, and unforgettable.

⚡ MINUTE MYTHS: Ancient wisdom at lightning speed
🏛️ Every story changes everything in 60 seconds
🔥 High-energy storytelling that hits different

Subscribe to Underground Stories for daily mythology that matters.

#UndergroundStories #MinuteMyths #{story.mythology}Mythology #{story.character} #AncientWisdom #Mythology #Shorts #ViralMythology #AncientStories #MythologyShorts #LegendsAndMyths #AncientTruths

Story: {story.character} from {story.mythology} mythology
Voice: High-energy Google Cloud TTS (Neural2-C)
Duration: ~{result.audio_file.duration_seconds:.0f} seconds
Part of Underground Stories - Minute Myths pipeline

Ancient stories, modern energy, timeless truths.
"""
        
        tags = [
            "underground stories", "minute myths", story.mythology.lower() + " mythology",
            story.character.lower(), "ancient wisdom", "mythology", "shorts",
            "viral mythology", "ancient stories", "mythology shorts", "legends and myths",
            "ancient truths", "60 second stories", "mythological stories", "viral shorts"
        ]
        
        return {
            "title": underground_title,
            "description": description,
            "tags": tags,
            "category_id": "22",  # Entertainment
            "privacy_status": "public",
            "series": "Minute Myths",
            "channel_series": "Underground Stories",
            "mythology": story.mythology,
            "character": story.character,
            "duration_seconds": result.audio_file.duration_seconds,
            "moral": story.moral
        }


async def test_minute_myths():
    """Test the Minute Myths generator"""
    
    logging.basicConfig(level=logging.INFO)
    logger.info("⚡ Testing Minute Myths Generator")
    
    generator = MinuteMyths()
    
    # Generate test stories
    stories = generator.generate_myth_stories(count=2)
    
    logger.info(f"Generated {len(stories)} myth stories:")
    for story in stories:
        logger.info(f"  {story.title} ({story.word_count} words)")
    
    # Test audio generation with first story
    logger.info(f"\n🎙️ Testing audio generation with: {stories[0].title}")
    result = await generator.generate_myth_audio(stories[0])
    
    if result["success"]:
        logger.info("🎉 SUCCESS! Minute Myths generator working perfectly!")
        logger.info(f"Generated: {result['audio_path']}")
        logger.info(f"Duration: {result['duration_seconds']:.1f} seconds")
        logger.info(f"Cost: {result['cost_cents']}¢") 
        logger.info(f"Underground title: {result['underground_metadata']['title']}")
    else:
        logger.error(f"❌ FAILED: {result['error']}")


if __name__ == "__main__":
    asyncio.run(test_minute_myths())