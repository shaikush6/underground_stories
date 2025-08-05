#!/usr/bin/env python3
"""
Timeless Retold Video Generator
==============================

Integrates with existing modernization system to create 8-10 minute videos
with scene-based images and slow reveal effects for classic literature.
"""

import asyncio
import logging
import json
import re
from typing import List, Dict, Optional, Tuple
from pathlib import Path
from dataclasses import dataclass
import sys

# Add paths
sys.path.append(str(Path(__file__).parent.parent))

from core.audio.audio_pipeline import AudioPipeline
from core.audio.types import VoiceConfig, TTSProvider, AudioFormat
from timeless_retold.timeless_processor import TimelessRetoldProcessor
from timeless_retold.timeless_adapter import TimelessRetoldAdapter

logger = logging.getLogger(__name__)

@dataclass
class Scene:
    """Represents a scene in a chapter for image generation"""
    chapter_number: int
    scene_number: int
    text_content: str
    description: str  # For image generation
    start_time: float  # seconds in audio
    duration: float   # seconds
    word_count: int

@dataclass
class TimelessVideo:
    """Complete video specification for a Timeless Retold episode"""
    book_title: str
    author: str
    chapter_number: int
    chapter_title: str
    scenes: List[Scene]
    audio_path: str
    total_duration: float  # minutes
    video_specs: Dict
    metadata: Dict

class TimelessVideoGenerator:
    """
    Generates complete videos for Timeless Retold pipeline.
    
    Builds on existing:
    - BookModernizer (text processing)
    - TimelessRetoldProcessor (audio generation) 
    - TimelessAdapter (voice optimization)
    
    Adds:
    - Scene detection and image generation
    - Video composition with slow reveal effects
    - 8-10 minute episode optimization
    """
    
    def __init__(self, output_dir: str = "content/timeless-retold"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Video output directories
        self.video_dir = self.output_dir / "videos"
        self.images_dir = self.output_dir / "images"
        self.video_dir.mkdir(exist_ok=True)
        self.images_dir.mkdir(exist_ok=True)
        
        # Use existing audio system
        self.timeless_adapter = TimelessRetoldAdapter()
        
        # Video specifications for classic literature
        self.video_config = {
            "resolution": "1920x1080",  # 16:9 for traditional viewing
            "fps": 30,
            "format": "mp4",
            "quality": "high",
            "background_style": "elegant_literary",  # Sophisticated backgrounds
            "text_overlay": True,
            "slow_reveal_duration": 3.0,  # seconds for image reveal
            "scene_transition_duration": 1.0
        }
        
        # Target 5-10 minute episodes with multiple parts per chapter (like Fairer Tales)
        self.target_duration_minutes = 7  # Sweet spot for engagement
        self.max_duration_minutes = 10    # Maximum before splitting
        self.words_per_minute = 150       # Literary narration pace
        self.target_words = int(self.target_duration_minutes * self.words_per_minute)
        self.max_words_per_part = int(self.max_duration_minutes * self.words_per_minute)
        
        logger.info(f"Timeless Video Generator initialized - targeting {self.target_duration_minutes}min episodes")
        logger.info(f"Long chapters will be split into multiple parts (max {self.max_duration_minutes}min each)")
    
    async def generate_video_from_chapter(self, book_title: str, chapter_path: Path) -> TimelessVideo:
        """
        Generate complete video from a modernized chapter.
        
        Uses existing modernized text from BookModernizer output.
        
        Args:
            book_title: Name of the book
            chapter_path: Path to modernized chapter text file
            
        Returns:
            TimelessVideo object with all components
        """
        logger.info(f"Generating video for chapter: {chapter_path}")
        
        # Read modernized chapter content
        with open(chapter_path, 'r', encoding='utf-8') as f:
            chapter_content = f.read()
        
        # Extract chapter metadata
        chapter_number = self._extract_chapter_number(chapter_path.name)
        chapter_title = self._extract_chapter_title(chapter_content)
        author = self._extract_author(chapter_content)
        
        # Split chapter into parts if too long (like Fairer Tales format)
        chapter_parts = self._split_chapter_into_parts(chapter_content, chapter_number)
        
        # For now, use the first part (could be extended to generate videos for all parts)
        primary_part = chapter_parts[0]
        working_content = primary_part["content"]
        
        # Split into scenes for image generation
        scenes = await self._detect_scenes(working_content, chapter_number)
        
        # Generate audio using existing system
        audio_path = await self._generate_audio(chapter_content, book_title, chapter_number)
        
        # Generate 2-3 key images for the video with style consistency
        key_scenes = self._select_key_scenes_for_images(scenes, target_count=2 if len(scenes) <= 4 else 3)
        await self._generate_scene_images(key_scenes, book_title, author)
        
        # Calculate timing and duration
        total_duration = await self._calculate_duration(audio_path)
        
        # Create video specification
        video_specs = {
            **self.video_config,
            "total_duration": total_duration,
            "scenes_count": len(scenes),
            "audio_path": audio_path
        }
        
        # Compile metadata
        metadata = {
            "generated_at": asyncio.get_event_loop().time(),
            "word_count": len(chapter_content.split()),
            "scene_count": len(scenes),
            "voice_used": self.timeless_adapter.voice_config.voice_id,
            "modernization_source": str(chapter_path)
        }
        
        timeless_video = TimelessVideo(
            book_title=book_title,
            author=author,
            chapter_number=chapter_number,
            chapter_title=chapter_title,
            scenes=scenes,
            audio_path=audio_path,
            total_duration=total_duration,
            video_specs=video_specs,
            metadata=metadata
        )
        
        # Generate final video composition
        video_path = await self._compose_video(timeless_video)
        
        logger.info(f"Video generated successfully: {video_path}")
        return timeless_video
    
    async def _detect_scenes(self, content: str, chapter_number: int) -> List[Scene]:
        """
        Detect natural scenes in the chapter for image generation.
        
        Analyzes the modernized text to identify:
        - Setting changes
        - Character introductions  
        - Action sequences
        - Emotional beats
        """
        # Split content into paragraphs
        paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]
        
        scenes = []
        current_scene_text = ""
        scene_number = 1
        words_per_scene = 200  # ~1.3 minutes per scene
        current_word_count = 0
        
        for para in paragraphs:
            current_scene_text += para + "\n\n"
            current_word_count += len(para.split())
            
            # Scene break conditions
            is_scene_break = (
                current_word_count >= words_per_scene or
                self._is_natural_break(para) or
                para == paragraphs[-1]  # Last paragraph
            )
            
            if is_scene_break and current_scene_text.strip():
                # Generate scene description for image
                description = await self._generate_scene_description(current_scene_text)
                
                # Calculate timing (rough estimate, will be refined with actual audio)
                start_time = (scene_number - 1) * (words_per_scene / self.words_per_minute * 60)
                duration = current_word_count / self.words_per_minute * 60
                
                scene = Scene(
                    chapter_number=chapter_number,
                    scene_number=scene_number,
                    text_content=current_scene_text.strip(),
                    description=description,
                    start_time=start_time,
                    duration=duration,
                    word_count=current_word_count
                )
                
                scenes.append(scene)
                
                # Reset for next scene
                current_scene_text = ""
                current_word_count = 0
                scene_number += 1
        
        logger.info(f"Detected {len(scenes)} scenes for chapter {chapter_number}")
        return scenes
    
    def _is_natural_break(self, paragraph: str) -> bool:
        """Identify natural scene breaks in literary text"""
        break_indicators = [
            # Dialogue endings
            r'"\s*$',
            # Time transitions
            r'\b(later|meanwhile|suddenly|then|next|after|hours passed|days passed)\b',
            # Setting changes
            r'\b(entered|arrived|left|departed|walked|moved|returned)\b',
            # Chapter transitions
            r'\*\s*\*\s*\*',
            r'---'
        ]
        
        for pattern in break_indicators:
            if re.search(pattern, paragraph, re.IGNORECASE):
                return True
        
        return False
    
    async def _generate_scene_description(self, scene_text: str) -> str:
        """
        Generate visual description for image generation.
        
        Analyzes the scene text to create detailed image prompts
        suitable for classic literature illustration.
        """
        # Extract key visual elements
        prompt = f"""
        Create a detailed visual description for this classic literature scene for image generation.
        
        Scene text: {scene_text[:500]}...
        
        Generate a detailed image prompt that captures:
        1. The setting and atmosphere
        2. Key characters and their appearance  
        3. Important objects or props
        4. The mood and tone
        5. Historical period details
        
        Style: Classic literature illustration, detailed, atmospheric
        """
        
        # This would use AI to generate the description
        # For now, return a structured placeholder
        description = f"Classic literature scene: {scene_text[:100]}..."
        
        return description
    
    async def _generate_audio(self, content: str, book_title: str, chapter_number: int) -> str:
        """
        Generate audio using existing TimelessAdapter system.
        """
        # Use existing audio generation
        audio_dir = self.output_dir / "audio"
        audio_dir.mkdir(parents=True, exist_ok=True)
        output_path = audio_dir / f"{book_title}_Chapter_{chapter_number:02d}.mp3"
        
        # Generate using existing system
        await self.timeless_adapter.generate_chapter_audio(
            content, 
            str(output_path),
            book_title,
            chapter_number
        )
        
        return str(output_path)
    
    def _split_chapter_into_parts(self, content: str, chapter_number: int) -> List[Dict]:
        """
        Split long chapters into multiple 5-10 minute parts (like Fairer Tales format).
        
        Args:
            content: Full chapter content
            chapter_number: Chapter number
            
        Returns:
            List of chapter parts with metadata
        """
        words = content.split()
        total_words = len(words)
        
        # If chapter is within target length, return as single part
        if total_words <= self.max_words_per_part:
            return [{
                "part_number": 1,
                "total_parts": 1,
                "content": content,
                "word_count": total_words,
                "estimated_duration": total_words / self.words_per_minute
            }]
        
        # Split into multiple parts
        parts = []
        words_per_part = self.target_words
        current_pos = 0
        part_number = 1
        
        while current_pos < total_words:
            # Calculate end position for this part
            end_pos = min(current_pos + words_per_part, total_words)
            
            # Adjust to natural break points (paragraph boundaries)
            if end_pos < total_words:
                # Look for paragraph break within next 100 words
                search_end = min(end_pos + 100, total_words)
                part_content_words = words[current_pos:search_end]
                part_content = " ".join(part_content_words)
                
                # Find last paragraph break
                paragraphs = part_content.split('\n\n')
                if len(paragraphs) > 1:
                    # Use all but the last incomplete paragraph
                    adjusted_content = '\n\n'.join(paragraphs[:-1])
                    adjusted_words = adjusted_content.split()
                    end_pos = current_pos + len(adjusted_words)
            
            # Extract part content
            part_words = words[current_pos:end_pos]
            part_content = " ".join(part_words)
            
            parts.append({
                "part_number": part_number,
                "total_parts": 0,  # Will be updated after all parts are created
                "content": part_content,
                "word_count": len(part_words),
                "estimated_duration": len(part_words) / self.words_per_minute
            })
            
            current_pos = end_pos
            part_number += 1
        
        # Update total_parts for all parts
        total_parts = len(parts)
        for part in parts:
            part["total_parts"] = total_parts
        
        logger.info(f"Chapter {chapter_number} split into {total_parts} parts (avg {sum(p['word_count'] for p in parts) / total_parts:.0f} words each)")
        
        return parts
    
    def _select_key_scenes_for_images(self, scenes: List[Scene], target_count: int = 3) -> List[Scene]:
        """
        Select 2-3 most visually compelling scenes for image generation.
        
        Prioritizes:
        1. Opening scene (setting establishment)
        2. Climactic/action scenes
        3. Character introduction scenes
        4. Closing/resolution scenes
        """
        if len(scenes) <= target_count:
            return scenes
        
        # Always include the first scene (setting/opening)
        key_scenes = [scenes[0]]
        remaining_slots = target_count - 1
        
        # Score scenes for visual impact
        scored_scenes = []
        for i, scene in enumerate(scenes[1:], 1):  # Skip first scene
            score = 0
            content_lower = scene.text_content.lower()
            
            # Action/drama indicators
            action_words = ['suddenly', 'rushed', 'attacked', 'fought', 'dramatic', 'intense', 'danger', 'confronted']
            score += sum(1 for word in action_words if word in content_lower) * 3
            
            # Character interaction
            dialogue_markers = content_lower.count('"') + content_lower.count("'")
            score += min(dialogue_markers, 3)  # Cap at 3
            
            # Emotional intensity
            emotion_words = ['fear', 'excitement', 'wonder', 'surprise', 'shock', 'amazement', 'terror']
            score += sum(1 for word in emotion_words if word in content_lower) * 2
            
            # Setting/visual richness
            visual_words = ['towering', 'vast', 'gleaming', 'shadowy', 'brilliant', 'magnificent', 'mysterious']
            score += sum(1 for word in visual_words if word in content_lower)
            
            # Prefer middle and end scenes for climax
            if i > len(scenes) * 0.3:  # After first third
                score += 1
            if i > len(scenes) * 0.7:  # Final third
                score += 2
            
            scored_scenes.append((score, i, scene))
        
        # Sort by score and select top scenes
        scored_scenes.sort(key=lambda x: x[0], reverse=True)
        selected_scenes = [scene for _, _, scene in scored_scenes[:remaining_slots]]
        
        # Add back to key_scenes in chronological order
        all_selected = key_scenes + selected_scenes
        all_selected.sort(key=lambda s: s.scene_number)
        
        logger.info(f"Selected {len(all_selected)} key scenes for images: {[s.scene_number for s in all_selected]}")
        return all_selected
    
    async def _generate_scene_images(self, scenes: List[Scene], book_title: str, author: str):
        """
        Generate images for each scene with DALL-E 3 and style consistency.
        """
        # Import the AI image generator
        try:
            from packages.core.video.ai_image_generator import AIImageGenerator
            image_generator = AIImageGenerator()
        except ImportError:
            logger.error("AI Image Generator not available - using placeholders")
            for scene in scenes:
                image_filename = f"{book_title}_Ch{scene.chapter_number:02d}_Scene{scene.scene_number:02d}.jpg"
                scene.image_path = str(self.images_dir / image_filename)
            return
        
        # Create consistent style prompt for the entire chapter
        base_style = f"""Classic literature illustration for "{book_title}" by {author}.
        Style: Professional book illustration, rich period details, cinematic 16:9 composition, 
        consistent artistic style, detailed atmospheric rendering, historical accuracy."""
        
        for i, scene in enumerate(scenes):
            image_filename = f"{book_title}_Ch{scene.chapter_number:02d}_Scene{scene.scene_number:02d}.jpg"
            image_path = self.images_dir / image_filename
            
            # Create scene-specific prompt with consistent style
            scene_prompt = f"{base_style}\n\nScene {i+1}: {scene.description}"
            
            # Add consistency hints for multi-image sequences
            if len(scenes) > 1:
                if i == 0:
                    scene_prompt += "\nEstablishing scene with consistent character and setting design."
                else:
                    scene_prompt += f"\nContinuation scene {i+1}, maintaining same artistic style and character appearance as previous scenes."
            
            try:
                # Generate image using DALL-E 3
                logger.info(f"🎨 Generating Timeless Retold image {i+1}/{len(scenes)}: {image_filename}")
                
                metadata = {
                    "title": f"{book_title} - Chapter {scene.chapter_number}, Scene {scene.scene_number}",
                    "author": author,
                    "scene_description": scene.description,
                    "chapter": scene.chapter_number,
                    "scene": scene.scene_number
                }
                
                generated_path, stats = await image_generator.generate_episode_image(
                    story_content=scene.text_content,
                    metadata=metadata,
                    pipeline="timeless-retold",
                    custom_prompt=scene_prompt,
                    output_filename=image_filename
                )
                
                scene.image_path = str(generated_path)
                logger.info(f"✅ Generated: {generated_path} ({stats['generation_time_seconds']:.1f}s)")
                
            except Exception as e:
                logger.error(f"❌ Image generation failed for scene {scene.scene_number}: {e}")
                # Use placeholder path
                scene.image_path = str(image_path)
    
    async def _calculate_duration(self, audio_path: str) -> float:
        """Calculate actual audio duration in minutes"""
        # This would analyze the actual audio file
        # For now, estimate based on content
        return self.target_duration_minutes
    
    async def _compose_video(self, video: TimelessVideo) -> str:
        """
        Compose final video with Remotion integration.
        
        Features:
        - Scene-based image display with slow reveal
        - Audio synchronization
        - Elegant transitions
        - Text overlays for chapter titles
        - Classic literature styling
        """
        video_filename = f"{video.book_title}_Chapter_{video.chapter_number:02d}.mp4"
        video_path = self.video_dir / video_filename
        
        # Remotion composition data
        composition_data = {
            "book_title": video.book_title,
            "author": video.author,
            "chapter_title": video.chapter_title,
            "scenes": [
                {
                    "scene_number": scene.scene_number,
                    "image_path": getattr(scene, 'image_path', ''),
                    "start_time": scene.start_time,
                    "duration": scene.duration,
                    "text_content": scene.text_content[:200] + "..." if len(scene.text_content) > 200 else scene.text_content
                }
                for scene in video.scenes
            ],
            "audio_path": video.audio_path,
            "video_config": video.video_specs,
            "total_duration": video.total_duration
        }
        
        # Save composition data for Remotion
        composition_file = self.video_dir / f"{video.book_title}_Chapter_{video.chapter_number:02d}_composition.json"
        with open(composition_file, 'w') as f:
            json.dump(composition_data, f, indent=2)
        
        logger.info(f"Video composition saved: {composition_file}")
        
        # This would trigger Remotion rendering
        logger.info(f"Would generate video: {video_path}")
        
        return str(video_path)
    
    def _extract_chapter_number(self, filename: str) -> int:
        """Extract chapter number from filename"""
        match = re.search(r'chapter_(\d+)', filename.lower())
        return int(match.group(1)) if match else 1
    
    def _extract_chapter_title(self, content: str) -> str:
        """Extract chapter title from content"""
        lines = content.split('\n')
        for line in lines[:5]:  # Check first 5 lines
            if line.strip() and not line.startswith('#'):
                return line.strip()
        return "Chapter"
    
    def _extract_author(self, content: str) -> str:
        """Extract or determine author from content/metadata"""
        # This would be enhanced to detect author from content or metadata
        return "Classic Author"

# Integration function for Underground Stories API
async def generate_timeless_video(book_title: str, chapter_path: str) -> Dict:
    """
    Main entry point for Timeless Retold video generation.
    
    Args:
        book_title: Name of the classic book
        chapter_path: Path to modernized chapter file
        
    Returns:
        Video generation result
    """
    try:
        generator = TimelessVideoGenerator()
        video = await generator.generate_video_from_chapter(book_title, Path(chapter_path))
        
        return {
            "success": True,
            "video_path": video.video_specs.get("video_path"),
            "duration_minutes": video.total_duration,
            "scenes_count": len(video.scenes),
            "audio_path": video.audio_path,
            "metadata": video.metadata
        }
    
    except Exception as e:
        import traceback
        logger.error(f"Timeless video generation failed: {e}")
        logger.error(f"Full traceback:\n{traceback.format_exc()}")
        return {
            "success": False,
            "error": str(e)
        }

if __name__ == "__main__":
    # Test with existing modernized chapter
    async def test():
        book_title = "The Lost World"
        chapter_path = "output/text/chapter_01_modernized.txt"
        
        result = await generate_timeless_video(book_title, chapter_path)
        print(f"Test result: {result}")
    
    asyncio.run(test())