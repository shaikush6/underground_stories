#!/usr/bin/env python3
"""
Timeless Retold Adapter - Google TTS Integration
==============================================

Integrates your existing perfect modernization system with Google Cloud TTS.
Preserves all the sophisticated text processing and character registry.
"""

import asyncio
import logging
import sys
from pathlib import Path
from typing import List, Dict, Optional
import json

# Add packages to path
sys.path.append(str(Path(__file__).parent.parent))

from core.audio.audio_pipeline import AudioPipeline
from core.audio.types import VoiceConfig, TTSProvider, AudioFormat

# Optional Google TTS import
try:
    from core.audio.providers.google_tts import GoogleTTSProvider
    GOOGLE_TTS_AVAILABLE = True
except ImportError:
    GoogleTTSProvider = None
    GOOGLE_TTS_AVAILABLE = False

logger = logging.getLogger(__name__)


class TimelessRetoldAdapter:
    """
    Adapter for your existing modernization system with Google TTS.
    
    Uses your existing beautifully modernized chapters from output/text/
    Just changes the TTS provider from OpenAI to Google Cloud.
    """
    
    def __init__(self):
        self.audio_pipeline = AudioPipeline()
        
        # Register OpenAI TTS provider for premium storytelling
        from core.audio.providers.openai_tts import OpenAITTSProvider
        from dotenv import load_dotenv
        load_dotenv()
        
        openai_provider = OpenAITTSProvider()
        self.audio_pipeline.register_provider(TTSProvider.OPENAI, openai_provider)
        
        # PREMIUM OpenAI voice config for classic literature with storytelling instructions
        self.voice_config = VoiceConfig(
            provider=TTSProvider.OPENAI,
            voice_id="sage",  # Wise and thoughtful - perfect for literature
            language_code="en-US", 
            speed=0.95,  # Slightly slower for literature comprehension
            pitch=0.0,
            volume_gain_db=0.0,
            audio_format=AudioFormat.MP3,
            sample_rate_hertz=22050
        )
        
        # Storytelling instructions for classic literature
        self.storytelling_instructions = """Voice: Authoritative yet accessible narrator with classical literary sensibility and sophisticated delivery.

Tone: Scholarly but never stuffy, maintaining the gravitas of great literature while making complex themes digestible for modern audiences.

Delivery: Measured and articulate, with the rhythm of a master storyteller who understands both the beauty of language and the power of ideas.

Pacing: Unhurried and contemplative, allowing the weight of literary themes to resonate while building narrative tension naturally.

Emphasis: Honor the elegance of classical prose while highlighting timeless human truths that transcend historical periods.

Articulation: Clear and precise pronunciation that respects the author's original voice while making it accessible to contemporary listeners."""
        
        # Background music integration (optional)
        try:
            from core.audio.background_music import BackgroundMusicManager
            self.music_manager = BackgroundMusicManager()
            self.enable_background_music = True  # User can toggle this
        except ImportError:
            self.music_manager = None
            self.enable_background_music = False
            logger.info("⚠️ Background music not available")
        
        # Paths to your existing modernized content
        self.modernized_dir = Path("output/text")
        self.output_dir = Path("content/timeless-retold/audio")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    async def generate_lost_world_episodes(self) -> List[Dict]:
        """
        Generate audio for your existing modernized Lost World chapters.
        Uses the perfect text you already created.
        """
        logger.info("🎭 Generating Timeless Retold episodes using existing modernized chapters")
        
        # Load your existing metadata
        metadata_path = self.modernized_dir / "the_lost_world_modernization_metadata.json"
        if not metadata_path.exists():
            raise FileNotFoundError(f"Modernization metadata not found: {metadata_path}")
        
        with open(metadata_path, 'r') as f:
            metadata = json.load(f)
        
        logger.info(f"Found metadata for: {metadata['book_config']['title']} by {metadata['book_config']['author']}")
        logger.info(f"Character registry: {len(metadata['character_registry'])} characters")
        
        # Find all modernized chapters
        
    async def generate_chapter_audio(self, content: str, output_path: str, book_title: str, chapter_number: int):
        """
        Generate audio for a single chapter.
        
        Args:
            content: Modernized chapter text
            output_path: Where to save the audio file
            book_title: Name of the book
            chapter_number: Chapter number
        """
        logger.info(f"Generating audio for {book_title} Chapter {chapter_number}")
        
        # Add storytelling context to the content
        enhanced_content = f"{self.storytelling_instructions}\n\n{content}"
        
        # Generate audio using the pipeline
        audio_result = await self.audio_pipeline.generate_audio(
            text=enhanced_content,
            voice_config=self.voice_config,
            output_path=Path(output_path)
        )
        
        if self.enable_background_music and self.music_manager:
            # Add subtle background music for classic literature
            await self.music_manager.add_background_music(
                audio_path=output_path,
                music_type="classical_subtle",
                volume=0.1  # Very subtle
            )
        
        logger.info(f"Audio generated: {output_path}")
        return audio_result
    
    async def _generate_openai_audio_with_instructions(self, text: str, output_path: Path, chapter_num: str):
        """Generate audio using OpenAI Advanced TTS with storytelling instructions"""
        
        try:
            from openai import AsyncOpenAI
            client = AsyncOpenAI()
            
            # Create Underground Stories format
            formatted_text = f"""Underground Classics presents: Classic Literature Modernized
            
Chapter {chapter_num}

{text}

This timeless story brought to you by Underground Stories - where classic literature meets modern storytelling."""
            
            # Use advanced OpenAI TTS with custom instructions
            response = await client.audio.speech.create(
                model="gpt-4o-mini-tts",
                voice=self.voice_config.voice_id,
                input=formatted_text,
                instructions=self.storytelling_instructions,
                response_format="mp3"
            )
            
            # Save the audio file
            with open(output_path, "wb") as f:
                f.write(response.content)
            
            file_size = Path(output_path).stat().st_size
            
            # Estimate duration (roughly)
            word_count = len(formatted_text.split())
            estimated_duration = (word_count / 150) * 60  # 150 WPM average
            
            # Estimate cost (OpenAI pricing: $15 per million characters)
            character_count = len(formatted_text)
            cost_cents = max(1, int((character_count / 1_000_000) * 1500))
            
            # Create a mock result object similar to audio pipeline
            class MockResult:
                def __init__(self):
                    self.success = True
                    self.cost_cents = cost_cents
                    self.audio_file = type('obj', (object,), {
                        'duration_seconds': estimated_duration,
                        'size_bytes': file_size
                    })
            
            return MockResult()
            
        except Exception as e:
            logger.error(f"OpenAI TTS failed: {e}")
            class MockFailedResult:
                def __init__(self):
                    self.success = False
                    self.error_message = str(e)
            
            return MockFailedResult()
    
    async def _generate_chapter_audio(self, chapter_file: Path, metadata: Dict) -> Dict:
        """Generate audio for a single modernized chapter"""
        
        # Extract chapter number from filename
        chapter_num = chapter_file.stem.split('_')[1]
        
        logger.info(f"🎙️ Generating audio for Chapter {chapter_num}")
        
        # Read your beautifully modernized text
        with open(chapter_file, 'r', encoding='utf-8') as f:
            modernized_text = f.read()
        
        # Create output filename
        output_path = self.output_dir / f"The_Lost_World_Chapter_{chapter_num}.mp3"
        
        # Generate audio using OpenAI Advanced TTS with storytelling instructions
        result = await self._generate_openai_audio_with_instructions(
            text=modernized_text,
            output_path=output_path,
            chapter_num=chapter_num
        )
        
        if result.success:
            # Add background music if enabled
            final_audio_path = output_path
            final_result = result
            background_track = None
            
            if self.enable_background_music and self.music_manager:
                # Select appropriate classical music
                background_track = self.music_manager.select_music_for_story(
                    story_type="timeless_retold",
                    story_mood="peaceful",
                    duration_seconds=result.audio_file.duration_seconds
                )
                
                if background_track:
                    output_path_obj = Path(output_path)
                    mixed_path = output_path_obj.parent / f"{output_path_obj.stem}_with_music{output_path_obj.suffix}"
                    
                    mix_result = await self.music_manager.mix_audio_with_background(
                        voice_audio_path=output_path,
                        background_track=background_track,
                        output_path=mixed_path,
                        story_type="timeless_retold"
                    )
                    
                    if mix_result["success"]:
                        final_audio_path = Path(mix_result["mixed_audio_path"])
                        logger.info(f"🎵 Added background music: {background_track.composer} - {background_track.title}")
                    else:
                        logger.warning(f"⚠️ Background music mixing failed: {mix_result.get('error')}")
            
            # Calculate episode info
            word_count = len(modernized_text.split())
            duration_minutes = final_result.audio_file.duration_seconds / 60
            
            logger.info(f"✅ Chapter {chapter_num} complete:")
            logger.info(f"   Audio: {final_audio_path}")
            logger.info(f"   Duration: {duration_minutes:.1f} minutes")
            logger.info(f"   Words: {word_count}")
            logger.info(f"   Cost: {result.cost_cents}¢")
            
            # Create Underground Stories metadata
            underground_metadata = self._create_underground_metadata(
                chapter_num, modernized_text, metadata, result
            )
            
            return {
                "success": True,
                "chapter": chapter_num,
                "audio_path": str(final_audio_path),
                "duration_minutes": duration_minutes,
                "word_count": word_count,
                "cost_cents": result.cost_cents,
                "underground_metadata": underground_metadata,
                "has_background_music": self.enable_background_music and self.music_manager and background_track is not None
            }
        else:
            logger.error(f"❌ Chapter {chapter_num} failed: {result.error_message}")
            return {
                "success": False,
                "chapter": chapter_num,
                "error": result.error_message
            }
    
    def _create_underground_metadata(self, chapter_num: str, text: str, metadata: Dict, result) -> Dict:
        """Create Underground Stories metadata for YouTube upload"""
        
        book_title = metadata['book_config']['title']
        author = metadata['book_config']['author']
        
        # Extract chapter title from text
        lines = text.split('\n')
        chapter_title = f"Chapter {chapter_num}"
        for line in lines[:5]:
            if line.strip() and not line.startswith('CHAPTER'):
                if len(line.strip()) < 100:  # Likely a title
                    chapter_title = line.strip().strip('"')
                    break
        
        underground_title = f"Underground Classics: {book_title} - {chapter_title} | Timeless Retold"
        
        description = f"""🎭 Welcome to Underground Stories - Timeless Retold

Experience classic literature like never before. This is {book_title} by {author}, brought to life with professional narration and modern accessibility.

📖 {chapter_title}

Step into a world where classic literature meets contemporary storytelling. Every chapter is a journey through timeless tales that have captivated readers for generations, now modernized for today's audience while preserving the original's literary brilliance.

This is {book_title} - the adventure that defined a genre.

🎬 TIMELESS RETOLD: Classic literature with underground storytelling
📚 Every chapter brings new discoveries  
🎭 Professional Google Cloud TTS narration
✨ Intelligently modernized while preserving literary quality

Subscribe to Underground Stories for more classic literature brought to life.

#UndergroundStories #ClassicLiterature #TimelessRetold #Audiobook #TheLostWorld #ArthurConanDoyle #LiteraryAdventure #BookLovers #ClassicTales #ModernizedClassics

Story: {book_title} by {author}
Voice: Professional Google Cloud TTS (Neural2)
Duration: ~{result.audio_file.duration_seconds/60:.0f} minutes
Part of Underground Stories - Timeless Retold pipeline

Original text modernized using sophisticated AI processing while preserving character voices and literary quality.
"""
        
        tags = [
            "underground stories", "timeless retold", "classic literature", "audiobook",
            "the lost world", "arthur conan doyle", "literary adventure", "book lovers",
            "classic tales", "modernized classics", "storytelling", "adventure fiction",
            "prehistoric adventure", "professor challenger", "victorian literature",
            "google cloud tts", "professional narration"
        ]
        
        return {
            "title": underground_title,
            "description": description,
            "tags": tags,
            "category_id": "22",  # Entertainment
            "privacy_status": "public",
            "series": "Timeless Retold",
            "channel_series": "Underground Stories",
            "episode_number": int(chapter_num),
            "book_title": book_title,
            "author": author,
            "chapter_title": chapter_title
        }


async def test_timeless_retold_adapter():
    """Test the adapter with your existing modernized content"""
    
    logging.basicConfig(level=logging.INFO)
    logger.info("🧪 Testing Timeless Retold Adapter with Google TTS")
    
    adapter = TimelessRetoldAdapter()
    
    # Test with just the first chapter initially
    chapter_1_path = Path("output/text/chapter_01_modernized.txt")
    
    if not chapter_1_path.exists():
        logger.error(f"Chapter 1 not found: {chapter_1_path}")
        logger.info("Make sure you've run your modernization system first!")
        return
    
    # Load metadata
    metadata_path = Path("output/text/the_lost_world_modernization_metadata.json")
    with open(metadata_path, 'r') as f:
        metadata = json.load(f)
    
    # Test single chapter
    logger.info("🎙️ Testing with Chapter 1...")
    result = await adapter._generate_chapter_audio(chapter_1_path, metadata)
    
    if result["success"]:
        logger.info("🎉 SUCCESS! Timeless Retold adapter working perfectly!")
        logger.info(f"Generated: {result['audio_path']}")
        logger.info(f"Duration: {result['duration_minutes']:.1f} minutes")
        logger.info(f"Cost: {result['cost_cents']}¢")
        logger.info(f"Underground title: {result['underground_metadata']['title']}")
    else:
        logger.error(f"❌ FAILED: {result['error']}")


if __name__ == "__main__":
    asyncio.run(test_timeless_retold_adapter())