#!/usr/bin/env python3
"""
Fairer Tales Adapter - Integrates existing 8-agent system with unified audio pipeline.
Preserves the proven story generation system while adding episode splitting and audio generation.
"""

import asyncio
import logging
from typing import List, Dict, Optional
from pathlib import Path
from dataclasses import dataclass
from datetime import datetime
import yaml

from .story_blueprint_processor import FlipsideProcessor
from .modernization_config import POV_STYLES
from ..core.audio.audio_pipeline import AudioPipeline, EpisodeSegment
from ..core.audio.types import VoiceConfig, TTSProvider, AudioFormat, TTSJobId


logger = logging.getLogger(__name__)


@dataclass
class FairerTalesEpisode:
    """Represents a single episode of a Fairer Tales story"""
    story_title: str
    episode_number: int
    episode_title: str
    text_content: str
    estimated_duration_minutes: float
    audio_file_path: Optional[Path] = None
    generated_at: Optional[str] = None


@dataclass 
class FairerTalesStory:
    """Complete Fairer Tales story with episodes"""
    story_id: str
    title: str
    genre: str
    logline: str
    total_episodes: int
    episodes: List[FairerTalesEpisode]
    metadata: Dict
    
    @property
    def total_duration_minutes(self) -> float:
        return sum(ep.estimated_duration_minutes for ep in self.episodes)


class FairerTalesAdapter:
    """
    Adapter integrating existing Fairer Tales system with new audio pipeline.
    
    Preserves your proven 8-agent story generation while adding:
    - Episode splitting for 5-minute YouTube videos
    - Unified audio generation with OpenAI TTS
    - Metadata generation for YouTube automation
    """
    
    def __init__(self, voice_config_path: str = "config/voice_profiles.yml"):
        # Initialize your existing processor
        self.story_processor = FlipsideProcessor()
        
        # Initialize our new audio pipeline
        self.audio_pipeline = AudioPipeline()
        
        # Load voice configuration
        self.voice_config = self._load_voice_config(voice_config_path)
        
        # Episode settings for Fairer Tales
        self.target_episode_duration = 5.0  # 5 minutes per episode
        self.target_episodes_per_story = 5   # ~5 episodes per complete story
        
        logger.info("Fairer Tales adapter initialized with audio pipeline integration")
    
    def _load_voice_config(self, config_path: str) -> VoiceConfig:
        """Load voice configuration for Fairer Tales from YAML"""
        try:
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
            
            fairer_config = config.get('fairer_tales', {})
            
            return VoiceConfig(
                provider=TTSProvider(fairer_config.get('provider', 'openai')),
                voice_id=fairer_config.get('voice', 'ash'),
                language_code="en-US",
                speed=fairer_config.get('speed', 1.0),
                audio_format=AudioFormat(fairer_config.get('response_format', 'mp3')),
                sample_rate_hertz=22050,  # Standard for OpenAI
                extra_params={
                    'model': fairer_config.get('model', 'tts-1')
                }
            )
        except Exception as e:
            logger.warning(f"Could not load voice config: {e}, using defaults")
            return VoiceConfig(
                provider=TTSProvider.OPENAI,
                voice_id="ash",  # Your proven voice
                language_code="en-US",
                audio_format=AudioFormat.MP3
            )
    
    async def generate_complete_story(
        self, 
        blueprint_text: str, 
        style: str = "sympathetic_antihero",
        generate_audio: bool = True
    ) -> FairerTalesStory:
        """
        Generate complete Fairer Tales story with episodes and optional audio.
        
        Uses your existing 8-agent pipeline for story generation,
        then splits into 5-minute episodes with audio generation.
        """
        logger.info(f"Generating Fairer Tales story with style: {style}")
        
        # Step 1: Use your existing proven system to generate the complete story
        story_result = self.story_processor.process_blueprint_text(blueprint_text, style)
        
        if not story_result['success']:
            raise ValueError(f"Story generation failed: {story_result.get('error')}")
        
        # Step 2: Read the generated story
        story_path = Path(story_result['filepath'])
        with open(story_path, 'r', encoding='utf-8') as f:
            full_story_text = f.read()
        
        # Step 3: Extract story metadata
        story_metadata = self._extract_story_metadata(full_story_text, story_result)
        
        # Step 4: Split into episodes
        episodes = await self._split_into_episodes(
            full_story_text, 
            story_metadata['title'],
            generate_audio
        )
        
        # Step 5: Create complete story object
        story = FairerTalesStory(
            story_id=story_result['story_id'],
            title=story_metadata['title'],
            genre=story_metadata['genre'],
            logline=story_metadata['logline'],
            total_episodes=len(episodes),
            episodes=episodes,
            metadata={
                **story_result,
                'generation_time': datetime.now().isoformat(),
                'total_duration_minutes': sum(ep.estimated_duration_minutes for ep in episodes),
                'voice_config': self.voice_config.__dict__
            }
        )
        
        logger.info(f"Generated story '{story.title}' with {len(episodes)} episodes")
        return story
    
    def _extract_story_metadata(self, story_text: str, story_result: Dict) -> Dict:
        """Extract metadata from generated story text"""
        lines = story_text.split('\n')
        
        # Find title (first # header)
        title = story_result.get('story_title', 'Untitled Story')
        for line in lines[:5]:  # Check first few lines
            if line.startswith('# '):
                title = line[2:].strip()
                break
        
        # Find genre (usually in italics after title)
        genre = "Dark Fantasy"  # Default for Fairer Tales
        for line in lines[:10]:
            if line.startswith('*') and line.endswith('*'):
                genre = line.strip('*').strip()
                break
        
        # Find logline (usually after **Logline:** marker)
        logline = "A reimagined fairy tale from the villain's perspective"
        for line in lines:
            if 'Logline:' in line:
                logline = line.split('Logline:')[-1].strip().strip('*')
                break
        
        return {
            'title': title,
            'genre': genre,
            'logline': logline
        }
    
    async def _split_into_episodes(
        self, 
        story_text: str, 
        story_title: str, 
        generate_audio: bool
    ) -> List[FairerTalesEpisode]:
        """Split story into 5-minute episodes with optional audio generation"""
        
        # Clean story text (remove headers, metadata)
        clean_text = self._clean_story_text(story_text)
        
        # Use audio pipeline to split into episodes
        episode_segments = await self.audio_pipeline.split_into_episodes(
            text=clean_text,
            target_duration_minutes=self.target_episode_duration,
            voice_config=self.voice_config
        )
        
        episodes = []
        
        for i, segment in enumerate(episode_segments):
            episode_num = i + 1
            episode_title = self._generate_episode_title(story_title, episode_num, segment.text)
            
            episode = FairerTalesEpisode(
                story_title=story_title,
                episode_number=episode_num,
                episode_title=episode_title,
                text_content=segment.text,
                estimated_duration_minutes=segment.estimated_duration_minutes,
                generated_at=datetime.now().isoformat()
            )
            
            # Generate audio if requested
            if generate_audio:
                audio_path = await self._generate_episode_audio(episode)
                episode.audio_file_path = audio_path
            
            episodes.append(episode)
        
        return episodes
    
    def _clean_story_text(self, story_text: str) -> str:
        """Clean story text for episode splitting"""
        lines = story_text.split('\n')
        
        # Remove metadata lines (headers, loglines, etc.)
        clean_lines = []
        skip_until_content = True
        
        for line in lines:
            line = line.strip()
            
            # Skip metadata sections
            if any(marker in line for marker in ['#', '**Logline:**', '====', '----']):
                continue
            
            # Start including content after we hit actual story text
            if skip_until_content and len(line) > 50 and not line.startswith('*'):
                skip_until_content = False
            
            if not skip_until_content and line:
                clean_lines.append(line)
        
        return '\n\n'.join(clean_lines)
    
    def _generate_episode_title(self, story_title: str, episode_num: int, text: str) -> str:
        """Generate appealing episode titles"""
        # Extract first sentence or key phrase for episode title
        first_sentence = text.split('.')[0][:50]
        
        # Create engaging episode titles
        episode_titles = [
            f"The Beginning",
            f"Dark Revelations", 
            f"Twisted Truth",
            f"Hidden Motives",
            f"Final Confrontation"
        ]
        
        if episode_num <= len(episode_titles):
            return f"{story_title} - Episode {episode_num}: {episode_titles[episode_num-1]}"
        else:
            return f"{story_title} - Episode {episode_num}: {first_sentence}..."
    
    async def _generate_episode_audio(self, episode: FairerTalesEpisode) -> Path:
        """Generate audio for a single episode"""
        # Create output path
        audio_dir = Path("content/fairer-tales/audio")
        audio_dir.mkdir(parents=True, exist_ok=True)
        
        safe_title = "".join(c if c.isalnum() or c in (' ', '-', '_') else '' for c in episode.story_title)
        audio_filename = f"{safe_title.replace(' ', '_')}_episode_{episode.episode_number:02d}.mp3"
        audio_path = audio_dir / audio_filename
        
        # Generate audio using unified pipeline
        result = await self.audio_pipeline.generate_audio(
            text=episode.text_content,
            voice_config=self.voice_config,
            output_path=audio_path,
            job_id=TTSJobId(f"fairer_{episode.story_title}_{episode.episode_number}")
        )
        
        if not result.success:
            logger.error(f"Audio generation failed for episode {episode.episode_number}: {result.error_message}")
            return None
        
        logger.info(f"Generated audio for episode {episode.episode_number}: {audio_path}")
        return audio_path
    
    async def generate_from_existing_story(self, story_file_path: Path) -> FairerTalesStory:
        """Generate episodes and audio from an existing story file"""
        with open(story_file_path, 'r', encoding='utf-8') as f:
            story_text = f.read()
        
        # Extract metadata from filename and content
        story_title = story_file_path.stem.replace('_', ' ').title()
        metadata = self._extract_story_metadata(story_text, {'story_title': story_title})
        
        # Split into episodes
        episodes = await self._split_into_episodes(story_text, story_title, generate_audio=True)
        
        return FairerTalesStory(
            story_id=story_file_path.stem,
            title=story_title,
            genre=metadata['genre'],
            logline=metadata['logline'],
            total_episodes=len(episodes),
            episodes=episodes,
            metadata={
                'source_file': str(story_file_path),
                'generation_time': datetime.now().isoformat()
            }
        )
    
    def get_available_styles(self) -> Dict[str, Dict]:
        """Get available POV styles from your existing system"""
        return POV_STYLES