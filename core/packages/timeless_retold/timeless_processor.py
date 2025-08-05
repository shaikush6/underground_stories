#!/usr/bin/env python3
"""
Timeless Retold Pipeline - Classic Literature Processor
======================================================

Processes classic literature for Underground Stories - Timeless Retold pipeline.
Handles chapter splitting, episode formatting, and audio generation.
"""

import asyncio
import logging
import re
from typing import List, Dict, Optional, Tuple
from pathlib import Path
from dataclasses import dataclass
import sys

# Add packages to path
sys.path.append(str(Path(__file__).parent.parent))

from core.audio.audio_pipeline import AudioPipeline
from core.audio.types import VoiceConfig, TTSProvider, AudioFormat

logger = logging.getLogger(__name__)


@dataclass
class Chapter:
    """Represents a chapter in a classic work"""
    number: int
    title: str
    content: str
    word_count: int
    estimated_duration: float  # minutes


@dataclass
class TimelessEpisode:
    """Represents an episode for Timeless Retold pipeline"""
    book_title: str
    author: str
    chapter: Chapter
    underground_title: str  # Underground Stories formatted title
    description: str
    tags: List[str]
    estimated_cost: float  # cents


class TimelessRetoldProcessor:
    """
    Processes classic literature for Underground Stories format.
    
    Features:
    - Intelligent chapter detection and splitting
    - 10-15 minute episode optimization 
    - Classic literature voice configuration
    - Underground Stories branding
    """
    
    def __init__(self, output_dir: str = "content/timeless-retold"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Audio pipeline for generation
        self.audio_pipeline = AudioPipeline()
        
        # Voice configuration for classic literature
        self.voice_config = VoiceConfig(
            provider=TTSProvider.OPENAI,  # Will switch to Google when API key ready
            voice_id="ash",  # Proven narrator voice
            language_code="en-US",
            speed=0.95,  # Slightly slower for literature
            pitch=0.0,
            volume_gain_db=0.0,
            audio_format=AudioFormat.MP3,
            sample_rate_hertz=22050
        )
        
        # Episode targeting (similar to Fairer Tales success)
        self.target_duration_minutes = 12  # 10-15 minute sweet spot
        self.target_words = 1800  # ~150 words/minute * 12 minutes
        
    async def process_book(self, book_path: Path) -> List[TimelessEpisode]:
        """
        Process a complete classic book into Underground Stories episodes.
        
        Args:
            book_path: Path to text file containing the book
            
        Returns:
            List of TimelessEpisode objects ready for audio generation
        """
        logger.info(f"Processing classic literature: {book_path}")
        
        # Read the book
        with open(book_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract book metadata
        book_info = self._extract_book_info(content)
        logger.info(f"Book: '{book_info['title']}' by {book_info['author']}")
        
        # Split into chapters
        chapters = self._split_into_chapters(content)
        logger.info(f"Found {len(chapters)} chapters")
        
        # Create episodes
        episodes = []
        for chapter in chapters:
            episode = self._create_episode(book_info, chapter)
            episodes.append(episode)
            
        logger.info(f"Created {len(episodes)} episodes for '{book_info['title']}'")
        return episodes
    
    async def generate_episode_audio(self, episode: TimelessEpisode, job_id: Optional[str] = None) -> Path:
        """
        Generate audio for a Timeless Retold episode.
        
        Args:
            episode: TimelessEpisode to generate audio for
            job_id: Optional job identifier
            
        Returns:
            Path to generated audio file
        """
        logger.info(f"Generating audio for: {episode.underground_title}")
        
        # Create output path
        safe_title = re.sub(r'[^\\w\\-_\\.]', '_', episode.underground_title)
        output_path = self.output_dir / "audio" / f"{safe_title}.mp3"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Generate audio using core pipeline (with chunking if needed)
        result = await self.audio_pipeline.generate_audio(
            text=episode.chapter.content,
            voice_config=self.voice_config,
            output_path=output_path,
            job_id=job_id or f"timeless_{episode.chapter.number}"
        )
        
        if result.success:
            logger.info(f"✅ Audio generated: {output_path}")
            logger.info(f"💰 Cost: {result.cost_cents}¢")
            return output_path
        else:
            raise Exception(f"Audio generation failed: {result.error_message}")
    
    def _extract_book_info(self, content: str) -> Dict[str, str]:
        """Extract book title and author from content"""
        lines = content.split('\n')
        
        # Look for title in first few lines
        title = "Unknown Classic"
        author = "Classic Author"
        
        for i, line in enumerate(lines[:20]):
            line = line.strip()
            if line and not line.startswith('CHAPTER') and len(line) > 3:
                # First substantial line is likely the title
                if title == "Unknown Classic":
                    title = line
                    continue
                # Look for "by [Author]" pattern
                if line.lower().startswith('by '):
                    author = line[3:].strip()
                    break
        
        # For The Lost World specifically
        if "lost world" in content.lower()[:1000]:
            title = "The Lost World"
            author = "Sir Arthur Conan Doyle"
        
        return {
            "title": title,
            "author": author
        }
    
    def _split_into_chapters(self, content: str) -> List[Chapter]:
        """Split book content into chapters"""
        chapters = []
        
        # Find chapter markers
        chapter_pattern = r'\\b(CHAPTER|Chapter)\\s+([IVXLCDM]+|\\d+)(?:\\s*[\\-:]?\\s*(.+?))?\\s*\\n'
        matches = list(re.finditer(chapter_pattern, content))
        
        if not matches:
            # No chapters found, treat as single chapter
            logger.warning("No chapter markers found, creating single episode")
            chapter = Chapter(
                number=1,
                title="Complete Story",
                content=content.strip(),
                word_count=len(content.split()),
                estimated_duration=self._estimate_duration(content)
            )
            return [chapter]
        
        # Extract chapters
        for i, match in enumerate(matches):
            chapter_start = match.start()
            chapter_end = matches[i + 1].start() if i + 1 < len(matches) else len(content)
            
            # Extract chapter info
            chapter_num_str = match.group(2)
            chapter_title = match.group(3) or f"Chapter {chapter_num_str}"
            chapter_content = content[chapter_start:chapter_end].strip()
            
            # Convert roman numerals if needed
            try:
                chapter_num = int(chapter_num_str) if chapter_num_str.isdigit() else self._roman_to_int(chapter_num_str)
            except:
                chapter_num = i + 1
            
            # Clean up content (remove chapter header)
            lines = chapter_content.split('\\n')
            if len(lines) > 1:
                chapter_content = '\\n'.join(lines[1:]).strip()
            
            chapter = Chapter(
                number=chapter_num,
                title=chapter_title.strip('"'),
                content=chapter_content,
                word_count=len(chapter_content.split()),
                estimated_duration=self._estimate_duration(chapter_content)
            )
            
            chapters.append(chapter)
        
        return chapters
    
    def _create_episode(self, book_info: Dict[str, str], chapter: Chapter) -> TimelessEpisode:
        """Create a TimelessEpisode from book info and chapter"""
        
        # Format Underground Stories title
        underground_title = f"Underground Classics: {book_info['title']} - {chapter.title} | Timeless Retold"
        
        # Create description
        description = self._create_episode_description(book_info, chapter)
        
        # Generate tags
        tags = self._generate_tags(book_info, chapter)
        
        # Estimate cost (using proven Fairer Tales model)
        estimated_cost = len(chapter.content) * 0.0015  # ~22¢ per 14,781 chars
        
        return TimelessEpisode(
            book_title=book_info['title'],
            author=book_info['author'],
            chapter=chapter,
            underground_title=underground_title,
            description=description,
            tags=tags,
            estimated_cost=estimated_cost
        )
    
    def _create_episode_description(self, book_info: Dict[str, str], chapter: Chapter) -> str:
        """Create YouTube description for episode"""
        return f"""🎭 Welcome to Underground Stories - Timeless Retold

Experience classic literature like never before. This is {book_info['title']} by {book_info['author']}, brought to life with professional narration and immersive storytelling.

📖 {chapter.title}

Step into a world where classic literature meets modern storytelling. Every chapter is a journey through timeless tales that have captivated readers for generations.

This is {book_info['title']} - the story that defined adventure literature.

🎬 TIMELESS RETOLD: Classic literature with underground storytelling
📚 Every chapter brings new discoveries
🎭 Professional narration that brings characters to life

Subscribe to Underground Stories for more classic literature brought to life.

#UndergroundStories #ClassicLiterature #TimelessRetold #Audiobook #{book_info['title'].replace(' ', '')} #{book_info['author'].replace(' ', '').replace('.', '')} #LiteraryAdventure #BookLovers #ClassicTales

Story: {book_info['title']} by {book_info['author']}
Voice: Professional narration with Ash (OpenAI TTS)
Duration: ~{chapter.estimated_duration:.0f} minutes
Part of Underground Stories - Timeless Retold pipeline
"""
    
    def _generate_tags(self, book_info: Dict[str, str], chapter: Chapter) -> List[str]:
        """Generate YouTube tags for episode"""
        base_tags = [
            "underground stories",
            "timeless retold", 
            "classic literature",
            "audiobook",
            "literary adventure",
            "classic tales",
            "book lovers",
            "storytelling"
        ]
        
        # Add book-specific tags
        book_tags = [
            book_info['title'].lower().replace(' ', ''),
            book_info['author'].lower().replace(' ', '').replace('.', ''),
        ]
        
        # The Lost World specific tags
        if "lost world" in book_info['title'].lower():
            book_tags.extend([
                "arthur conan doyle",
                "adventure fiction",
                "prehistoric adventure",
                "dinosaurs",
                "exploration",
                "professor challenger",
                "victorian literature"
            ])
        
        return base_tags + book_tags
    
    def _estimate_duration(self, text: str) -> float:
        """Estimate duration in minutes for text"""
        words = len(text.split())
        # Average: 150 words per minute for narration
        return words / 150
    
    def _roman_to_int(self, roman: str) -> int:
        """Convert Roman numerals to integers"""
        roman_map = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
        result = 0
        prev = 0
        
        for char in reversed(roman.upper()):
            value = roman_map.get(char, 0)
            if value < prev:
                result -= value
            else:
                result += value
            prev = value
        
        return result


# Convenience function for easy testing
async def process_the_lost_world() -> List[TimelessEpisode]:
    """Process The Lost World as first Timeless Retold test"""
    processor = TimelessRetoldProcessor()
    book_path = Path("content/timeless-retold/the_lost_world.txt")
    
    if not book_path.exists():
        raise FileNotFoundError(f"The Lost World not found at {book_path}")
    
    episodes = await processor.process_book(book_path)
    return episodes


if __name__ == "__main__":
    # Test the processor
    async def main():
        logging.basicConfig(level=logging.INFO)
        logger.info("Testing Timeless Retold processor...")
        
        episodes = await process_the_lost_world()
        
        logger.info(f"\\n📚 THE LOST WORLD PROCESSING RESULTS:")
        logger.info(f"Total episodes: {len(episodes)}")
        
        total_cost = sum(ep.estimated_cost for ep in episodes)
        total_duration = sum(ep.chapter.estimated_duration for ep in episodes)
        
        logger.info(f"Estimated total cost: ${total_cost/100:.2f}")
        logger.info(f"Total content duration: {total_duration:.1f} minutes")
        
        # Show first few episodes
        for i, episode in enumerate(episodes[:3]):
            logger.info(f"\\nEpisode {i+1}: {episode.underground_title}")
            logger.info(f"  Duration: {episode.chapter.estimated_duration:.1f}m")
            logger.info(f"  Cost: {episode.estimated_cost:.1f}¢")
            logger.info(f"  Words: {episode.chapter.word_count}")
    
    asyncio.run(main())