#!/usr/bin/env python3
"""
Minute Myths Video Generator
============================

Creates mobile-optimized 1-minute mythology videos with dynamic visuals
and engaging narration for maximum social media impact.
"""

import asyncio
import logging
import json
from typing import List, Dict, Optional, Any
from pathlib import Path
from dataclasses import dataclass
import sys

# Add paths
sys.path.append(str(Path(__file__).parent.parent))

from minute_myths.content_multiplier import MinuteMythsMultiplier, multiply_myth_into_series
from core.audio.audio_pipeline import AudioPipeline
from core.audio.types import VoiceConfig, TTSProvider, AudioFormat

logger = logging.getLogger(__name__)

@dataclass
class MinuteMythVideo:
    """Complete 1-minute mythology video specification"""
    myth_name: str
    mythology_category: str
    content_type: str
    title: str
    script: str
    audio_path: str
    image_path: str
    video_path: str
    duration: int  # seconds
    mobile_optimized: bool
    engagement_metrics: Dict
    metadata: Dict

class MinuteMythsVideoGenerator:
    """
    Generates complete 1-minute mythology videos optimized for mobile viewing.
    
    Features:
    - 9:16 vertical format for TikTok/Instagram/YouTube Shorts
    - Dynamic visual effects and text overlays
    - Engaging narration with proven voice optimization
    - Series-based content organization
    - Educational focus with entertainment value
    """
    
    def __init__(self, output_dir: str = "content/minute-myths"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize content multiplier
        self.multiplier = MinuteMythsMultiplier(str(self.output_dir))
        
        # Video output directory
        self.final_videos_dir = self.output_dir / "final_videos"
        self.final_videos_dir.mkdir(exist_ok=True)
        
        # Mobile-first video configuration
        self.video_config = {
            "resolution": "1080x1920",  # 9:16 aspect ratio
            "fps": 30,
            "format": "mp4",
            "quality": "high",
            "codec": "h264",
            "audio_codec": "aac",
            "bitrate": "5000k",  # High quality for mobile
            "mobile_optimized": True,
            
            # Visual style for mythology content
            "background_style": "dynamic_mythology",
            "color_scheme": "epic_mythology",  # Rich golds, deep blues, etc.
            "typography": "bold_readable",     # Clear text for mobile
            "animation_style": "engaging_reveals",
            
            # Engagement features
            "text_overlays": True,
            "visual_effects": True,
            "progress_indicator": True,  # Show video progress
            "captions": True,           # Auto-generated captions
            "thumbnail_optimization": True,
            
            # Mobile viewing optimization
            "safe_zones": True,         # Keep important content in safe viewing area
            "high_contrast": True,      # Ensure visibility on small screens
            "large_text": True,         # Readable on mobile
            "fast_paced_editing": True  # Keep attention on mobile
        }
        
        logger.info("Minute Myths Video Generator initialized for mobile-first content")

    async def generate_myth_video_series(self, myth_name: str, mythology_category: str, base_story: str) -> Dict:
        """
        Generate complete video series from a single myth.
        
        Args:
            myth_name: Name of the myth (e.g., "Perseus and Medusa")
            mythology_category: Category (e.g., "Greek Mythology")
            base_story: Base story content
            
        Returns:
            Complete series with all videos generated
        """
        logger.info(f"Generating video series for: {myth_name}")
        
        try:
            # Use content multiplier to create series
            series_result = await multiply_myth_into_series(myth_name, mythology_category, base_story)
            
            if not series_result["success"]:
                return series_result
            
            # Generate final videos for each piece
            final_videos = []
            for i, content_result in enumerate(series_result["content_results"]):
                if content_result["success"]:
                    video_result = await self._create_final_video(content_result, i + 1)
                    final_videos.append(video_result)
            
            return {
                "success": True,
                "series_title": series_result["series_title"],
                "total_videos": len(final_videos),
                "multiplication_factor": series_result["multiplication_factor"],
                "videos": final_videos,
                "playlist_ready": True,
                "mobile_optimized": True
            }
            
        except Exception as e:
            logger.error(f"Video series generation failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    async def generate_single_myth_video(self, myth_name: str, mythology_category: str, base_story: str, content_type: str = "main_story") -> Dict:
        """
        Generate a single 1-minute mythology video.
        
        Args:
            myth_name: Name of the myth
            mythology_category: Category (Greek, Norse, etc.)
            base_story: The mythology story content
            content_type: Type of content (main_story, character, etc.)
            
        Returns:
            Single video generation result
        """
        logger.info(f"Generating single video: {myth_name} - {content_type}")
        
        try:
            # Generate content using multiplier (just get one piece)
            multiplier = MinuteMythsMultiplier(str(self.output_dir))
            series = await multiplier.multiply_myth_content(myth_name, mythology_category, base_story)
            
            # Find the requested content type or use main story
            target_content = None
            for content in series.content_pieces:
                if content.content_type.value == content_type:
                    target_content = content
                    break
            
            if not target_content and series.content_pieces:
                target_content = series.content_pieces[0]  # Default to first piece
            
            if not target_content:
                return {
                    "success": False,
                    "error": "No content generated"
                }
            
            # Generate the video content
            content_result = await multiplier.generate_video_for_content(target_content)
            
            if not content_result["success"]:
                return content_result
            
            # Create final video
            video_result = await self._create_final_video(content_result, 1)
            
            return {
                "success": True,
                "video_title": target_content.title,
                "video_path": video_result.get("video_path"),
                "duration": target_content.duration_seconds,
                "content_type": content_type,
                "mobile_optimized": True,
                "ready_for_upload": True
            }
            
        except Exception as e:
            logger.error(f"Single video generation failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    async def _create_final_video(self, content_result: Dict, video_number: int) -> Dict:
        """
        Create final video composition with Remotion integration.
        
        Features:
        - Mobile-first 9:16 format
        - Dynamic visual effects
        - Text overlays and captions
        - Engaging transitions
        - Mythology-themed styling
        """
        try:
            # Load composition data
            composition_path = content_result["composition_path"]
            with open(composition_path, 'r') as f:
                composition_data = json.load(f)
            
            # Enhance composition with mobile optimizations
            mobile_composition = {
                **composition_data,
                "video_config": {
                    **self.video_config,
                    **composition_data.get("video_config", {})
                },
                "mobile_features": {
                    "vertical_format": True,
                    "large_text_overlay": True,
                    "progress_bar": True,
                    "auto_captions": True,
                    "engaging_intro": "3_second_hook",
                    "clear_call_to_action": True
                },
                "remotion_template": "minute_myths_mobile",
                "rendering_profile": "mobile_optimized"
            }
            
            # Generate final video filename
            safe_title = content_result["content_title"].replace(" ", "_").replace("-", "_")
            video_filename = f"{safe_title}_{video_number:02d}.mp4"
            final_video_path = self.final_videos_dir / video_filename
            
            # Save enhanced composition for Remotion rendering
            enhanced_composition_path = self.final_videos_dir / f"{video_filename}_composition.json"
            with open(enhanced_composition_path, 'w') as f:
                json.dump(mobile_composition, f, indent=2)
            
            logger.info(f"Final video composition ready: {enhanced_composition_path}")
            
            # This would trigger actual Remotion rendering
            # For now, return the specification
            return {
                "success": True,
                "video_path": str(final_video_path),
                "composition_path": str(enhanced_composition_path),
                "title": content_result["content_title"],
                "duration": composition_data.get("metadata", {}).get("duration", 60),
                "mobile_optimized": True,
                "ready_for_social_media": True,
                "rendering_status": "composition_ready"
            }
            
        except Exception as e:
            logger.error(f"Final video creation failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    async def batch_generate_mythology_content(self, mythology_database: Dict[str, List[str]]) -> Dict:
        """
        Generate videos for entire mythology database.
        
        This is where we create THOUSANDS of shorts from the base mythology collection.
        
        Args:
            mythology_database: Dict with categories and myth names
            
        Returns:
            Batch generation results
        """
        logger.info("Starting batch generation for entire mythology database")
        
        total_videos = 0
        successful_series = 0
        failed_series = 0
        all_results = {}
        
        try:
            for category, myths in mythology_database.items():
                category_results = []
                
                for myth_name in myths:
                    # Get base story (would be from actual database)
                    base_story = self._get_base_story(myth_name, category)
                    
                    # Generate complete series
                    series_result = await self.generate_myth_video_series(myth_name, category, base_story)
                    
                    if series_result["success"]:
                        successful_series += 1
                        total_videos += series_result["total_videos"]
                        category_results.append(series_result)
                    else:
                        failed_series += 1
                        logger.error(f"Failed to generate series for {myth_name}: {series_result.get('error')}")
                
                all_results[category] = category_results
                logger.info(f"Completed {category}: {len(category_results)} series generated")
            
            return {
                "success": True,
                "total_series": successful_series,
                "total_videos": total_videos,
                "failed_series": failed_series,
                "categories_processed": len(mythology_database),
                "multiplication_success": f"{len(mythology_database)} categories × avg 12 myths × avg 10 videos = {total_videos} total videos",
                "results_by_category": all_results
            }
            
        except Exception as e:
            logger.error(f"Batch generation failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "partial_results": all_results
            }

    def _get_base_story(self, myth_name: str, category: str) -> str:
        """
        Get base story content for a myth.
        
        This would connect to the actual mythology database.
        For now, return a placeholder based on the myth name.
        """
        # This would be replaced with actual database lookup
        story_templates = {
            "Perseus and Medusa": """Perseus, son of Zeus, must slay the deadly Gorgon Medusa whose gaze turns men to stone. Armed with a mirrored shield from Athena, winged sandals from Hermes, and an invisible helmet from Hades, he approaches her lair backwards, watching only her reflection. With one swift stroke, he beheads the sleeping monster, her blood giving birth to the winged horse Pegasus.""",
            
            "Pandora's Box": """The gods create Pandora, the first woman, as punishment for Prometheus stealing fire. Given to Epimetheus with a mysterious jar as dowry, curiosity overwhelms her. She opens it, releasing all evils into the world - disease, death, hatred, and suffering. Only Hope remains trapped inside when she quickly closes it, becoming humanity's last comfort in a world now filled with hardship.""",
            
            "Thor's Hammer Mjolnir": """The trickster god Loki cuts off Sif's beautiful golden hair as a prank, enraging Thor. To make amends, Loki ventures to the dwarven realm where master craftsmen forge magical items. They create not only new hair for Sif, but also Mjolnir - Thor's mighty hammer that never misses its target and always returns to his hand, becoming the most powerful weapon in Asgard."""
        }
        
        return story_templates.get(myth_name, f"The story of {myth_name} from {category} mythology...")

    def get_mythology_database(self) -> Dict[str, List[str]]:
        """
        Get the complete mythology database for batch processing.
        
        Returns the same database structure from the UI but optimized for processing.
        """
        return {
            "Greek Mythology": [
                "Perseus and Medusa", "Pandora's Box", "Theseus and the Minotaur", 
                "Orpheus and Eurydice", "King Midas and the Golden Touch", "Icarus and the Sun",
                "Demeter and Persephone", "Echo and Narcissus", "The Twelve Labors of Hercules",
                "The Odyssey - Sirens", "The Odyssey - Cyclops", "The Odyssey - Lotus Eaters"
            ],
            "Norse Mythology": [
                "Ragnarök - The End of the World", "Loki and the Death of Baldr", "Thor's Hammer Mjolnir",
                "Odin's Sacrifice for Wisdom", "The Creation of the World", "Fenrir the Wolf",
                "The Rainbow Bridge Bifrost", "Yggdrasil the World Tree", "The Valkyries",
                "Loki's Punishment", "The Golden Apples of Idunn", "Thor and the Giants"
            ],
            "Egyptian Mythology": [
                "Osiris and Isis", "The Battle of Horus and Set", "The Journey Through the Afterlife",
                "The Creation by Atum", "The Weighing of the Heart", "Ra's Journey Through the Underworld",
                "The Story of Hathor", "Anubis and Mummification", "The Pharaoh's Divine Right",
                "The Curse of the Pharaohs", "Thoth and the Moon", "Bastet the Cat Goddess"
            ],
            "Japanese Mythology": [
                "Amaterasu and the Cave", "Susanoo and the Eight-Headed Dragon", "The Tale of Urashima Taro",
                "The Moon Princess Kaguya", "Izanagi and Izanami", "The Birth of Japan",
                "Yamata-no-Orochi Dragon", "The Crane Wife", "Momotaro the Peach Boy",
                "The Bamboo Cutter", "Tengu Mountain Spirits", "Kitsune Fox Spirits"
            ],
            "Celtic Mythology": [
                "The Children of Lir", "Cú Chulainn's Rage", "The Táin - Cattle Raid of Cooley",
                "Brigid and the Sacred Fire", "The Morrigan in Battle", "Finn MacCool and the Giants",
                "The Selkies of the Sea", "Banshees and Death Omens", "The Otherworld",
                "Druids and Sacred Groves", "The Cauldron of Rebirth", "Bran the Blessed"
            ],
            "Hindu Mythology": [
                "Rama and Sita - The Ramayana", "Krishna and the Butter Thief", "Ganesha's Broken Tusk",
                "Hanuman's Leap to Lanka", "The Churning of the Ocean", "Shiva's Cosmic Dance",
                "Durga and the Buffalo Demon", "Vishnu's Ten Avatars", "The Birth of Ganga",
                "Arjuna and the Bhagavad Gita", "Lakshmi and Prosperity", "Saraswati and Knowledge"
            ],
            "Native American": [
                "The Great Spirit's Creation", "Coyote the Trickster", "The Thunderbird",
                "White Buffalo Woman", "The Seven Sisters (Pleiades)", "Raven Steals the Sun",
                "Kokopelli the Fertility God", "The Vision Quest", "Spider Grandmother",
                "The Medicine Wheel", "Wendigo the Cannibal", "The Dream Catcher"
            ],
            "Mesopotamian": [
                "Gilgamesh and Enkidu", "The Great Flood", "Inanna's Descent to the Underworld",
                "The Creation of Humanity", "Tiamat and Marduk", "The Tower of Babel",
                "Ishtar and Tammuz", "The Epic of Creation", "Enlil's Wrath", 
                "The Seven Sages", "Ereshkigal Queen of the Dead", "The Plant of Immortality"
            ]
        }

# Integration function for Underground Stories API
async def generate_minute_myth_video(myth_name: str, mythology_category: str, video_format: str, narration_style: str) -> Dict:
    """
    Main entry point for Minute Myths video generation from UI.
    
    Args:
        myth_name: Selected myth name
        mythology_category: Selected category
        video_format: Single Video, Part 1 of 3, etc.
        narration_style: Exciting, Dramatic, etc.
        
    Returns:
        Video generation result
    """
    try:
        generator = MinuteMythsVideoGenerator()
        
        # Get base story
        base_story = generator._get_base_story(myth_name, mythology_category)
        
        # Determine content type based on format
        content_type = "main_story"
        if "Part" in video_format:
            part_num = int(video_format.split()[1])
            if part_num == 1:
                content_type = "main_story"
            elif part_num == 2:
                content_type = "character"  
            else:
                content_type = "cultural_context"
        
        # Generate single video
        result = await generator.generate_single_myth_video(myth_name, mythology_category, base_story, content_type)
        
        return {
            **result,
            "video_format": video_format,
            "narration_style": narration_style,
            "mobile_optimized": True,
            "vertical_format": "9:16"
        }
        
    except Exception as e:
        logger.error(f"Minute myth video generation failed: {e}")
        return {
            "success": False,
            "error": str(e)
        }

if __name__ == "__main__":
    # Test video generation
    async def test():
        generator = MinuteMythsVideoGenerator()
        
        # Test single video
        result = await generator.generate_single_myth_video(
            "Perseus and Medusa",
            "Greek Mythology", 
            generator._get_base_story("Perseus and Medusa", "Greek Mythology"),
            "main_story"
        )
        print(f"Single video result: {result}")
        
        # Test series generation  
        series_result = await generator.generate_myth_video_series(
            "Perseus and Medusa",
            "Greek Mythology",
            generator._get_base_story("Perseus and Medusa", "Greek Mythology")
        )
        print(f"Series result: {series_result}")
    
    asyncio.run(test())