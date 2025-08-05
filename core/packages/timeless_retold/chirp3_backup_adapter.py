#!/usr/bin/env python3
"""
Timeless Retold - Chirp3 Backup Adapter
======================================

Chirp3-HD backup system for Timeless Retold.
Ready to plug-and-play if OpenAI has issues.
"""

import asyncio
import logging
import sys
from typing import Dict, Optional
from pathlib import Path
from datetime import datetime

# Add packages to path
sys.path.append(str(Path(__file__).parent.parent))

from core.audio.audio_pipeline import AudioPipeline
from core.audio.types import VoiceConfig, TTSProvider, AudioFormat
from core.audio.providers.google_tts import GoogleTTSProvider

logger = logging.getLogger(__name__)


class TimelessRetoldChirp3Backup:
    """
    Chirp3-HD backup for Timeless Retold pipeline.
    
    Features:
    - Google's newest Chirp3-HD voices
    - Drop-in replacement for OpenAI system
    - Optimized for classic literature narration
    """
    
    def __init__(self):
        self.audio_pipeline = AudioPipeline()
        
        # Register Google TTS provider
        credentials_path = "config/google-cloud-credentials.json"
        project_id = "gen-lang-client-0693450484"
        google_provider = GoogleTTSProvider(credentials_path=credentials_path, project_id=project_id)
        self.audio_pipeline.register_provider(TTSProvider.GOOGLE, google_provider)
        
        # Chirp3-HD voice config optimized for classic literature
        self.voice_config = VoiceConfig(
            provider=TTSProvider.GOOGLE,
            voice_id="en-US-Chirp3-HD-Achernar",  # Sophisticated narrator
            language_code="en-US",
            speed=0.95,  # Slightly slower for literature comprehension
            pitch=0.0,   # Chirp3 voices don't support pitch
            volume_gain_db=0.0,
            audio_format=AudioFormat.MP3,
            sample_rate_hertz=22050
        )
        
        self.modernized_dir = Path("output/text")
        self.output_dir = Path("content/timeless-retold/audio/chirp3_backup")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info("🔧 Chirp3-HD backup adapter initialized for Timeless Retold")
    
    async def process_classic_text_chirp3(self, text: str, title: str, author: str, 
                                        chapter: str, job_id: Optional[str] = None) -> Dict:
        """
        Process classic text using Chirp3-HD TTS.
        Drop-in replacement for the OpenAI method.
        """
        
        logger.info(f"🌟 Processing with Chirp3-HD backup: {title} - {chapter}")
        
        # Create Underground Stories format for classic literature
        formatted_text = f"""Underground Classics presents: {title} by {author}
        
{chapter}

{text}

This timeless story brought to you by Underground Stories - where classic literature meets cutting-edge narration."""
        
        # Create output path
        safe_title = title.replace(" ", "_").replace(":", "").replace("'", "")
        safe_chapter = chapter.replace(" ", "_").replace(":", "")
        output_path = self.output_dir / f"{safe_title}_{safe_chapter}_chirp3.mp3"
        
        try:
            # Use Chirp3-HD TTS
            result = await self.audio_pipeline.generate_audio(
                text=formatted_text,
                voice_config=self.voice_config,
                output_path=output_path,
                job_id=job_id or f"chirp3_backup_{safe_chapter}"
            )
            
            if result.success:
                logger.info(f"✅ Chirp3-HD backup generation complete:")
                logger.info(f"   Audio: {output_path}")
                logger.info(f"   Duration: {result.audio_file.duration_seconds:.1f} seconds")
                logger.info(f"   File size: {result.audio_file.size_bytes} bytes")
                logger.info(f"   Cost: {result.cost_cents}¢")
                
                # Create Underground Stories metadata
                underground_metadata = self._create_backup_metadata(title, author, chapter, 
                                                                  result.audio_file.duration_seconds / 60, 
                                                                  result.cost_cents)
                
                return {
                    "success": True,
                    "audio_path": str(output_path),
                    "duration_seconds": result.audio_file.duration_seconds,
                    "cost_cents": result.cost_cents,
                    "file_size": result.audio_file.size_bytes,
                    "underground_metadata": underground_metadata,
                    "provider": "chirp3_backup"
                }
            else:
                return {
                    "success": False,
                    "error": result.error_message,
                    "provider": "chirp3_backup"
                }
                
        except Exception as e:
            logger.error(f"❌ Chirp3-HD backup failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "provider": "chirp3_backup"
            }
    
    def _create_backup_metadata(self, title: str, author: str, chapter: str, 
                              duration_minutes: float, cost_cents: int) -> Dict:
        """Create metadata for Chirp3-HD backup generation"""
        
        underground_title = f"Underground Classics: {title} - {chapter} | Timeless Retold [Chirp3-HD Backup]"
        
        description = f"""⚡ Underground Stories - Timeless Retold [Chirp3-HD Backup System]

Classic literature for modern audiences. This is {title} by {author}, {chapter} - narrated using Google's newest Chirp3-HD voice technology.

📚 {title}: Timeless themes, cutting-edge narration
🎭 Author: {author}
📖 Chapter: {chapter}

Every classic holds eternal truths. Every story transcends time. Experience the greatest works of literature with Google's most advanced text-to-speech technology.

This is {author}'s {title} - sophisticated, powerful, and unforgettable.

⚡ TIMELESS RETOLD: Classic literature with premium technology
📚 Every story bridges centuries with modern innovation
🌟 Chirp3-HD voices: Google's newest breakthrough in natural speech
🔧 Backup System: Reliable high-quality delivery

Subscribe to Underground Stories for daily classics that matter.

#UndergroundStories #TimelessRetold #ClassicLiterature #{author.replace(' ', '')} #{title.replace(' ', '')} #Literature #Audiobook #ClassicBooks #GoogleChirp3HD #AdvancedTTS

Story: {title} by {author}, {chapter}
Voice: Google Chirp3-HD (Achernar) - Advanced narration technology
Duration: ~{duration_minutes:.0f} minutes
Backup System: Chirp3-HD emergency pipeline
Part of Underground Stories - Timeless Retold collection

Classic stories, modern technology, timeless truths.
"""
        
        tags = [
            "underground stories", "timeless retold", "classic literature",
            author.lower().replace(" ", ""), title.lower().replace(" ", ""), 
            "literature", "audiobook", "classic books", "literary classics",
            "book lovers", "chirp3 hd", "google tts", "advanced narration"
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
            "provider": "chirp3_backup"
        }


async def test_chirp3_backup():
    """Test the Chirp3-HD backup system"""
    
    logging.basicConfig(level=logging.INFO)
    logger.info("🔧 Testing Timeless Retold Chirp3-HD Backup System")
    
    backup_adapter = TimelessRetoldChirp3Backup()
    
    # Test with a sample text
    test_text = """In the heart of Victorian London, where gas lamps flickered through perpetual fog, extraordinary adventures awaited those brave enough to seek them. Professor Challenger stood before the Royal Geographic Society, his wild hair catching the lamplight as he declared the impossible: a lost world where dinosaurs still roamed."""
    
    result = await backup_adapter.process_classic_text_chirp3(
        text=test_text,
        title="The Lost World",
        author="Arthur Conan Doyle",
        chapter="Test Chapter",
        job_id="chirp3_backup_test"
    )
    
    if result["success"]:
        logger.info("🎉 SUCCESS! Chirp3-HD backup system working perfectly!")
        logger.info(f"Generated: {result['audio_path']}")
        logger.info(f"Cost: {result['cost_cents']}¢")
        logger.info("🌟 Ready for emergency deployment!")
    else:
        logger.error(f"❌ FAILED: {result['error']}")


if __name__ == "__main__":
    asyncio.run(test_chirp3_backup())