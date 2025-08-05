#!/usr/bin/env python3
"""
Timeless Retold - OpenAI Backup Adapter
=====================================

"Break glass in case of emergency" OpenAI TTS pipeline for Timeless Retold.
Ready to plug-and-play if Google Chirp3 has issues.

This mirrors the Fairer Tales OpenAI implementation but optimized for classic literature.
"""

import asyncio
import logging
import sys
from typing import Dict, Optional
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

# Add packages to path
sys.path.append(str(Path(__file__).parent.parent))

from core.audio.audio_pipeline import AudioPipeline
from core.audio.types import VoiceConfig, TTSProvider, AudioFormat
from core.audio.providers.openai_tts import OpenAITTSProvider

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)


class TimelessRetoldOpenAIBackup:
    """
    Emergency OpenAI backup for Timeless Retold pipeline.
    
    Features:
    - Advanced OpenAI TTS with storytelling instructions
    - Same chunking system as Fairer Tales
    - Optimized for classic literature narration
    - Drop-in replacement for Google Chirp3 system
    """
    
    def __init__(self):
        self.audio_pipeline = AudioPipeline()
        
        # Register OpenAI TTS provider
        openai_provider = OpenAITTSProvider()
        self.audio_pipeline.register_provider(TTSProvider.OPENAI, openai_provider)
        
        # OpenAI voice config optimized for classic literature
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
        
        self.modernized_dir = Path("output/text")
        self.output_dir = Path("content/timeless-retold/audio/openai_backup")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info("🔧 OpenAI backup adapter initialized for Timeless Retold")
    
    async def process_classic_text_openai(self, text: str, title: str, author: str, 
                                        chapter: str, job_id: Optional[str] = None) -> Dict:
        """
        Process classic text using OpenAI TTS with storytelling optimization.
        Drop-in replacement for the Google Chirp3 method.
        """
        
        logger.info(f"🎭 Processing with OpenAI backup: {title} - {chapter}")
        
        # Create Underground Stories format for classic literature
        formatted_text = f"""Underground Classics presents: {title} by {author}
        
{chapter}

{text}

This timeless story brought to you by Underground Stories - where classic literature meets modern storytelling."""
        
        # Create output path
        safe_title = title.replace(" ", "_").replace(":", "").replace("'", "")
        safe_chapter = chapter.replace(" ", "_").replace(":", "")
        output_path = self.output_dir / f"{safe_title}_{safe_chapter}_openai.mp3"
        
        try:
            # Use advanced OpenAI TTS with custom instructions
            from openai import AsyncOpenAI
            client = AsyncOpenAI()
            
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
            
            file_size = output_path.stat().st_size
            
            # Estimate duration (roughly)
            word_count = len(formatted_text.split())
            estimated_duration = (word_count / 150) * 60  # 150 WPM average
            
            # Estimate cost (OpenAI pricing: $15 per million characters)
            character_count = len(formatted_text)
            cost_cents = max(1, int((character_count / 1_000_000) * 1500))
            
            logger.info(f"✅ OpenAI backup generation complete:")
            logger.info(f"   Audio: {output_path}")
            logger.info(f"   Duration: ~{estimated_duration:.1f} minutes")
            logger.info(f"   File size: {file_size} bytes")
            logger.info(f"   Cost: {cost_cents}¢")
            
            # Create Underground Stories metadata
            underground_metadata = self._create_backup_metadata(title, author, chapter, 
                                                              estimated_duration, cost_cents)
            
            return {
                "success": True,
                "audio_path": str(output_path),
                "duration_seconds": estimated_duration * 60,
                "cost_cents": cost_cents,
                "file_size": file_size,
                "underground_metadata": underground_metadata,
                "provider": "openai_backup"
            }
            
        except Exception as e:
            logger.error(f"❌ OpenAI backup failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "provider": "openai_backup"
            }
    
    def _create_backup_metadata(self, title: str, author: str, chapter: str, 
                              duration_minutes: float, cost_cents: int) -> Dict:
        """Create metadata for OpenAI backup generation"""
        
        underground_title = f"Underground Classics: {title} - {chapter} | Timeless Retold [OpenAI Backup]"
        
        description = f"""⚡ Underground Stories - Timeless Retold [OpenAI Emergency Backup]

Classic literature for modern audiences. This is {title} by {author}, {chapter} - masterfully narrated using our premium OpenAI backup system.

📚 {title}: Timeless themes, modern delivery
🎭 Author: {author}
📖 Chapter: {chapter}

Every classic holds eternal truths. Every story transcends time. Experience the greatest works of literature with contemporary storytelling that honors the original while making it accessible to today's audience.

This is {author}'s {title} - raw, powerful, and unforgettable.

⚡ TIMELESS RETOLD: Classic literature at premium quality
📚 Every story bridges centuries in minutes  
🎭 Premium narration that honors literary tradition
🔧 OpenAI Backup System: Emergency high-quality delivery

Subscribe to Underground Stories for daily classics that matter.

#UndergroundStories #TimelessRetold #ClassicLiterature #{author.replace(' ', '')} #{title.replace(' ', '')} #Literature #Audiobook #ClassicBooks #LiteraryClassics #BookLovers

Story: {title} by {author}, {chapter}
Voice: OpenAI Advanced TTS (Sage) with storytelling optimization
Duration: ~{duration_minutes:.0f} minutes
Backup System: Emergency OpenAI pipeline for premium delivery
Part of Underground Stories - Timeless Retold collection

Classic stories, modern energy, timeless truths.
"""
        
        tags = [
            "underground stories", "timeless retold", "classic literature",
            author.lower().replace(" ", ""), title.lower().replace(" ", ""), 
            "literature", "audiobook", "classic books", "literary classics",
            "book lovers", "openai backup", "premium narration"
        ]
        
        return {
            "title": underground_title,
            "description": description,
            "tags": tags,
            "category_id": "27",  # Education  
            "privacy_status": "public",
            "series": "Timeless Retold",
            "channel_series": "Underground Stories",
            "author": author,
            "book_title": title,
            "chapter": chapter,
            "duration_minutes": duration_minutes,
            "cost_cents": cost_cents,
            "provider": "openai_backup"
        }


async def test_openai_backup():
    """Test the OpenAI backup system"""
    
    logging.basicConfig(level=logging.INFO)
    logger.info("🔧 Testing Timeless Retold OpenAI Backup System")
    
    backup_adapter = TimelessRetoldOpenAIBackup()
    
    # Test with a sample text
    test_text = """In the heart of Victorian London, where gas lamps flickered through perpetual fog, extraordinary adventures awaited those brave enough to seek them. Professor Challenger stood before the Royal Geographic Society, his wild hair catching the lamplight as he declared the impossible: a lost world where dinosaurs still roamed."""
    
    result = await backup_adapter.process_classic_text_openai(
        text=test_text,
        title="The Lost World",
        author="Arthur Conan Doyle",
        chapter="Test Chapter",
        job_id="backup_test"
    )
    
    if result["success"]:
        logger.info("🎉 SUCCESS! OpenAI backup system working perfectly!")
        logger.info(f"Generated: {result['audio_path']}")
        logger.info(f"Cost: {result['cost_cents']}¢")
        logger.info("🔧 Ready for emergency deployment!")
    else:
        logger.error(f"❌ FAILED: {result['error']}")


if __name__ == "__main__":
    asyncio.run(test_openai_backup())