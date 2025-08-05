#!/usr/bin/env python3
"""
Minute Myths Content Multiplier
===============================

Generates THOUSANDS of 1-minute shorts from mythology database.
Each myth becomes 10-20+ content pieces through intelligent segmentation.
"""

import asyncio
import logging
import json
from typing import List, Dict, Optional, Any
from pathlib import Path
from dataclasses import dataclass
from enum import Enum
import sys

# Add paths
sys.path.append(str(Path(__file__).parent.parent))

from core.audio.audio_pipeline import AudioPipeline
from core.audio.types import VoiceConfig, TTSProvider, AudioFormat

logger = logging.getLogger(__name__)

class ContentType(Enum):
    """Types of content that can be generated from each myth"""
    MAIN_STORY = "main_story"           # The core myth (1 min)
    CHARACTER_BACKSTORY = "character"    # Individual character stories
    ORIGIN_STORY = "origin"             # How the myth began
    CULTURAL_CONTEXT = "culture"        # Historical/cultural significance  
    MODERN_PARALLEL = "modern"          # Modern day parallels
    SYMBOLS_MEANING = "symbols"         # Symbolism and deeper meaning
    MORAL_LESSON = "moral"              # Life lessons from the myth
    HISTORICAL_FACTS = "facts"          # Real historical connections
    VARIANT_VERSIONS = "variants"       # Different cultural versions
    AFTERMATH = "aftermath"             # What happened after the main story

@dataclass
class MythContent:
    """Single piece of mythological content optimized for 1-minute videos"""
    myth_name: str
    mythology_category: str  # Greek, Norse, etc.
    content_type: ContentType
    title: str               # Video title
    script: str             # 1-minute narration script (~150 words)
    description: str        # Video description for YouTube
    tags: List[str]         # YouTube tags
    image_prompt: str       # Detailed prompt for image generation
    educational_facts: List[str]  # Key learning points
    engagement_hook: str    # Opening line to grab attention
    call_to_action: str     # Ending to encourage engagement
    series_number: int      # Part of larger series for this myth
    duration_seconds: int   # Target duration (usually 60)
    complexity_level: str   # beginner, intermediate, advanced

@dataclass
class MythSeries:
    """Complete series of content pieces from one mythology story"""
    base_myth: str
    mythology_category: str
    total_pieces: int
    content_pieces: List[MythContent]
    estimated_total_duration: int  # Total minutes of content
    series_description: str
    playlist_title: str

class MinuteMythsMultiplier:
    """
    Transforms single mythology stories into comprehensive content series.
    
    Strategy: Each myth becomes 10-20 pieces of content:
    - 1 main story
    - 2-3 character backstories
    - 1 origin/cultural context
    - 1-2 modern parallels
    - 1 symbols/meaning analysis
    - 1 moral lesson
    - 2-3 interesting facts
    - 1-2 variant versions
    - 1 aftermath/consequences
    
    Result: 84 base myths → 1000+ individual shorts
    """
    
    def __init__(self, output_dir: str = "content/minute-myths"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Create subdirectories
        self.scripts_dir = self.output_dir / "scripts"
        self.audio_dir = self.output_dir / "audio"  
        self.images_dir = self.output_dir / "images"
        self.videos_dir = self.output_dir / "videos"
        
        for dir_path in [self.scripts_dir, self.audio_dir, self.images_dir, self.videos_dir]:
            dir_path.mkdir(exist_ok=True)
        
        # Audio pipeline for 1-minute content
        self.audio_pipeline = AudioPipeline()
        
        # Voice configuration optimized for engaging shorts
        self.voice_config = VoiceConfig(
            provider=TTSProvider.OPENAI,
            voice_id="nova",  # Engaging and dynamic for shorts
            language_code="en-US",
            speed=1.05,  # Slightly faster for engagement
            pitch=0.0,
            volume_gain_db=2.0,  # Slightly louder for mobile
            audio_format=AudioFormat.MP3,
            sample_rate_hertz=44100  # High quality for mobile
        )
        
        # Video specs for mobile-first content
        self.video_config = {
            "resolution": "1080x1920",  # 9:16 vertical for mobile
            "fps": 30,
            "format": "mp4", 
            "quality": "high",
            "duration_target": 60,  # 1 minute exactly
            "background_style": "dynamic_mythology",
            "text_overlay": True,
            "mobile_optimized": True,
            "engagement_features": ["hooks", "visual_effects", "clear_text"]
        }
        
        # Content generation templates
        self.content_templates = self._load_content_templates()
        
        logger.info("Minute Myths Multiplier initialized for 1000+ shorts generation")

    def _load_content_templates(self) -> Dict[ContentType, Dict]:
        """Load templates for different content types"""
        return {
            ContentType.MAIN_STORY: {
                "duration": 60,
                "word_count": 150,
                "structure": "hook → setup → conflict → resolution → lesson",
                "style": "dramatic_storytelling"
            },
            ContentType.CHARACTER_BACKSTORY: {
                "duration": 60,
                "word_count": 150,
                "structure": "introduction → backstory → motivation → significance",
                "style": "character_focus"
            },
            ContentType.CULTURAL_CONTEXT: {
                "duration": 60,
                "word_count": 150,
                "structure": "historical_setting → cultural_beliefs → myth_purpose → legacy",
                "style": "educational_documentary"
            },
            ContentType.MODERN_PARALLEL: {
                "duration": 60,
                "word_count": 150,
                "structure": "myth_theme → modern_example → comparison → relevance",
                "style": "contemporary_connection"
            },
            ContentType.SYMBOLS_MEANING: {
                "duration": 60,
                "word_count": 150,
                "structure": "symbol_introduction → deeper_meaning → cultural_significance → interpretation",
                "style": "analytical_deep_dive"
            }
        }

    async def multiply_myth_content(self, myth_name: str, mythology_category: str, base_story: str) -> MythSeries:
        """
        Transform a single myth into a complete content series.
        
        Args:
            myth_name: Name of the myth (e.g., "Perseus and Medusa")
            mythology_category: Category (e.g., "Greek Mythology")
            base_story: The base mythology story text
            
        Returns:
            MythSeries with 10-20 individual content pieces
        """
        logger.info(f"Multiplying content for: {myth_name} ({mythology_category})")
        
        content_pieces = []
        
        # 1. Main Story (required)
        main_story = await self._generate_main_story(myth_name, mythology_category, base_story)
        content_pieces.append(main_story)
        
        # 2. Character Backstories (2-3 pieces)
        characters = await self._extract_characters(base_story)
        for character in characters[:3]:  # Top 3 characters
            backstory = await self._generate_character_backstory(myth_name, mythology_category, character, base_story)
            content_pieces.append(backstory)
        
        # 3. Cultural Context
        cultural_context = await self._generate_cultural_context(myth_name, mythology_category, base_story)
        content_pieces.append(cultural_context)
        
        # 4. Modern Parallels (1-2 pieces)
        modern_parallels = await self._generate_modern_parallels(myth_name, mythology_category, base_story)
        content_pieces.extend(modern_parallels)
        
        # 5. Symbols and Meaning
        symbols_analysis = await self._generate_symbols_analysis(myth_name, mythology_category, base_story)
        content_pieces.append(symbols_analysis)
        
        # 6. Moral Lessons
        moral_lesson = await self._generate_moral_lesson(myth_name, mythology_category, base_story)
        content_pieces.append(moral_lesson)
        
        # 7. Historical Facts (2-3 pieces)
        historical_facts = await self._generate_historical_facts(myth_name, mythology_category, base_story)
        content_pieces.extend(historical_facts)
        
        # 8. Variant Versions (if applicable)
        variants = await self._generate_variant_versions(myth_name, mythology_category, base_story)
        content_pieces.extend(variants)
        
        # 9. Aftermath/Consequences
        aftermath = await self._generate_aftermath(myth_name, mythology_category, base_story)
        content_pieces.append(aftermath)
        
        # Create series metadata
        series = MythSeries(
            base_myth=myth_name,
            mythology_category=mythology_category,
            total_pieces=len(content_pieces),
            content_pieces=content_pieces,
            estimated_total_duration=len(content_pieces),  # ~1 min each
            series_description=f"Complete {myth_name} series - {len(content_pieces)} parts exploring every aspect of this {mythology_category.lower()} myth",
            playlist_title=f"{myth_name} - Complete Mythology Series"
        )
        
        logger.info(f"Generated {len(content_pieces)} content pieces for {myth_name}")
        return series

    async def _generate_main_story(self, myth_name: str, category: str, base_story: str) -> MythContent:
        """Generate the main 1-minute story"""
        
        # Extract key elements for engaging retelling
        script = await self._create_engaging_script(
            myth_name, 
            base_story, 
            ContentType.MAIN_STORY,
            "Tell the complete myth in exactly 60 seconds with maximum engagement"
        )
        
        return MythContent(
            myth_name=myth_name,
            mythology_category=category,
            content_type=ContentType.MAIN_STORY,
            title=f"{myth_name} - The Complete Story",
            script=script,
            description=f"The complete story of {myth_name} from {category} in exactly one minute. Learn this fascinating myth quickly and easily!",
            tags=[myth_name.lower(), category.lower().replace(" ", ""), "mythology", "myths", "stories", "education"],
            image_prompt=f"Epic illustration of {myth_name}, {category} mythology style, dramatic and engaging, mobile-optimized vertical composition",
            educational_facts=[
                f"Origin: {category}",
                "Type: Heroic myth" if "hero" in base_story.lower() else "Classic myth",
                f"Main theme: {self._extract_theme(base_story)}"
            ],
            engagement_hook="What if I told you that...",
            call_to_action="Want to learn more? Check out the character breakdowns in our series!",
            series_number=1,
            duration_seconds=60,
            complexity_level="beginner"
        )

    async def _generate_character_backstory(self, myth_name: str, category: str, character: str, base_story: str) -> MythContent:
        """Generate character-focused content"""
        
        script = await self._create_engaging_script(
            f"{character} from {myth_name}",
            base_story,
            ContentType.CHARACTER_BACKSTORY,
            f"Focus entirely on {character}'s background, motivations, and role in the myth"
        )
        
        return MythContent(
            myth_name=myth_name,
            mythology_category=category,
            content_type=ContentType.CHARACTER_BACKSTORY,
            title=f"{character} - The Untold Story",
            script=script,
            description=f"Deep dive into {character} from {myth_name}. Discover their backstory, motivations, and significance in {category}.",
            tags=[character.lower(), myth_name.lower(), category.lower().replace(" ", ""), "character", "backstory"],
            image_prompt=f"Detailed portrait of {character} from {category} mythology, character-focused, dramatic lighting, vertical mobile format",
            educational_facts=[
                f"Character: {character}",
                f"Role: {self._determine_character_role(character, base_story)}",
                f"Significance: Key figure in {myth_name}"
            ],
            engagement_hook=f"You think you know {character}? Think again...",
            call_to_action="Which character should we explore next?",
            series_number=len([c for c in base_story if c == character]) + 1,
            duration_seconds=60,
            complexity_level="intermediate"
        )

    async def _create_engaging_script(self, title: str, source_content: str, content_type: ContentType, instruction: str) -> str:
        """
        Create an engaging 1-minute script optimized for mobile viewing.
        
        This would use AI to generate the actual script.
        For now, return a structured template.
        """
        template = self.content_templates.get(content_type, self.content_templates[ContentType.MAIN_STORY])
        
        # This would be replaced with actual AI script generation
        script = f"""
        [HOOK - 5 seconds]
        Attention-grabbing opening about {title}
        
        [MAIN CONTENT - 45 seconds]  
        {instruction}
        Based on: {source_content[:200]}...
        
        [WRAP-UP - 10 seconds]
        Key takeaway and engagement question
        
        Total: ~150 words for 60-second delivery
        """
        
        return script.strip()

    async def _extract_characters(self, story: str) -> List[str]:
        """Extract main characters from the story"""
        # This would use NLP to identify characters
        # For now, return common mythology characters
        common_characters = ["Zeus", "Athena", "Perseus", "Medusa", "Hermes", "Hades", "Poseidon"]
        found_characters = [char for char in common_characters if char.lower() in story.lower()]
        return found_characters[:3]  # Return top 3

    async def _generate_cultural_context(self, myth_name: str, category: str, base_story: str) -> MythContent:
        """Generate cultural context content"""
        script = f"The cultural significance of {myth_name} in ancient {category.split()[0]} society..."
        
        return MythContent(
            myth_name=myth_name,
            mythology_category=category,
            content_type=ContentType.CULTURAL_CONTEXT,
            title=f"{myth_name} - Cultural Significance",
            script=script,
            description=f"Discover why {myth_name} was important to ancient {category.split()[0]} culture and what it meant to people of that time.",
            tags=[myth_name.lower(), "culture", "history", category.lower().replace(" ", "")],
            image_prompt=f"Ancient {category.split()[0]} cultural scene depicting {myth_name}, historical accuracy, educational illustration",
            educational_facts=[f"Cultural origin: {category}", "Historical importance: High", "Modern relevance: Significant"],
            engagement_hook="Ever wonder why ancient people told this story?",
            call_to_action="What other cultural insights interest you?",
            series_number=99,  # Cultural context gets high number
            duration_seconds=60,
            complexity_level="intermediate"
        )

    # Placeholder methods for other content types
    async def _generate_modern_parallels(self, myth_name: str, category: str, base_story: str) -> List[MythContent]:
        """Generate modern parallel content"""
        return []  # Would generate 1-2 modern parallel pieces

    async def _generate_symbols_analysis(self, myth_name: str, category: str, base_story: str) -> MythContent:
        """Generate symbols analysis content"""
        return MythContent(
            myth_name=myth_name,
            mythology_category=category,
            content_type=ContentType.SYMBOLS_MEANING,
            title=f"{myth_name} - Hidden Meanings",
            script=f"The deeper symbolism in {myth_name}...",
            description=f"Uncover the hidden meanings and symbols in {myth_name}",
            tags=[myth_name.lower(), "symbolism", "meaning", "analysis"],
            image_prompt=f"Symbolic representation of {myth_name}, abstract and meaningful",
            educational_facts=["Deep symbolism present", "Multiple interpretations possible"],
            engagement_hook="This myth is deeper than you think...",
            call_to_action="What symbols did you notice?",
            series_number=50,
            duration_seconds=60,
            complexity_level="advanced"
        )

    async def _generate_moral_lesson(self, myth_name: str, category: str, base_story: str) -> MythContent:
        """Generate moral lesson content"""
        return MythContent(
            myth_name=myth_name,
            mythology_category=category,
            content_type=ContentType.MORAL_LESSON,
            title=f"{myth_name} - Life Lessons",
            script=f"What {myth_name} teaches us about life...",
            description=f"The timeless life lessons from {myth_name}",
            tags=[myth_name.lower(), "lessons", "wisdom", "morals"],
            image_prompt=f"Inspirational representation of lessons from {myth_name}",
            educational_facts=["Timeless wisdom", "Applicable today"],
            engagement_hook="This ancient story has modern wisdom...",
            call_to_action="How do you apply this lesson?",
            series_number=75,
            duration_seconds=60,
            complexity_level="beginner"
        )

    async def _generate_historical_facts(self, myth_name: str, category: str, base_story: str) -> List[MythContent]:
        """Generate historical facts content"""
        return []  # Would generate 2-3 fact pieces

    async def _generate_variant_versions(self, myth_name: str, category: str, base_story: str) -> List[MythContent]:
        """Generate variant versions content"""
        return []  # Would generate different cultural versions

    async def _generate_aftermath(self, myth_name: str, category: str, base_story: str) -> MythContent:
        """Generate aftermath content"""
        return MythContent(
            myth_name=myth_name,
            mythology_category=category,
            content_type=ContentType.AFTERMATH,
            title=f"{myth_name} - What Happened Next",
            script=f"After {myth_name}, what happened to the characters...",
            description=f"The aftermath and consequences of {myth_name}",
            tags=[myth_name.lower(), "aftermath", "consequences", "sequel"],
            image_prompt=f"Aftermath scene of {myth_name}, what happened next",
            educational_facts=["Consequences explored", "Extended storyline"],
            engagement_hook="But wait, there's more to the story...",
            call_to_action="Want to explore more myths?",
            series_number=100,
            duration_seconds=60,
            complexity_level="intermediate"
        )

    def _extract_theme(self, story: str) -> str:
        """Extract main theme from story"""
        return "heroism and courage"  # Placeholder

    def _determine_character_role(self, character: str, story: str) -> str:
        """Determine character's role in the story"""
        return "protagonist"  # Placeholder

    async def generate_video_for_content(self, content: MythContent) -> Dict:
        """
        Generate complete video for a single myth content piece.
        
        Returns video generation result with mobile optimization.
        """
        try:
            # Generate audio
            audio_path = self.audio_dir / f"{content.myth_name}_{content.content_type.value}_{content.series_number:02d}.mp3"
            
            await self.audio_pipeline.generate_audio(
                text=content.script,
                voice_config=self.voice_config,
                output_path=str(audio_path)
            )
            
            # Generate image with DALL-E 3
            image_filename = f"{content.myth_name}_{content.content_type.value}_{content.series_number:02d}.jpg"
            image_path = self.images_dir / image_filename
            
            # Generate actual image using DALL-E 3
            try:
                from packages.core.video.ai_image_generator import AIImageGenerator
                image_generator = AIImageGenerator()
                
                metadata = {
                    "title": content.title,
                    "myth_name": content.myth_name,
                    "mythology_category": content.mythology_category,
                    "content_type": content.content_type.value,
                    "series_number": content.series_number
                }
                
                logger.info(f"🎨 Generating Minute Myths image: {image_filename}")
                
                generated_path, stats = await image_generator.generate_episode_image(
                    story_content=content.script,
                    metadata=metadata,
                    pipeline="minute-myths",
                    custom_prompt=content.image_prompt,
                    output_filename=image_filename
                )
                
                image_path = generated_path
                logger.info(f"✅ Generated: {generated_path} ({stats['generation_time_seconds']:.1f}s)")
                
            except ImportError:
                logger.error("AI Image Generator not available - using placeholder")
            except Exception as e:
                logger.error(f"❌ Image generation failed: {e}")
            
            # Generate video composition data
            video_data = {
                "title": content.title,
                "script": content.script,
                "audio_path": str(audio_path),
                "image_path": str(image_path),
                "video_config": self.video_config,
                "metadata": {
                    "myth_name": content.myth_name,
                    "content_type": content.content_type.value,
                    "series_number": content.series_number,
                    "educational_facts": content.educational_facts,
                    "tags": content.tags
                }
            }
            
            # Save composition for Remotion
            composition_path = self.videos_dir / f"{content.myth_name}_{content.content_type.value}_{content.series_number:02d}_composition.json"
            with open(composition_path, 'w') as f:
                json.dump(video_data, f, indent=2)
            
            logger.info(f"Content generated: {content.title}")
            
            return {
                "success": True,
                "content_title": content.title,
                "audio_path": str(audio_path),
                "composition_path": str(composition_path),
                "duration": content.duration_seconds,
                "series_info": f"Part {content.series_number} of {content.myth_name} series"
            }
            
        except Exception as e:
            logger.error(f"Content generation failed for {content.title}: {e}")
            return {
                "success": False,
                "error": str(e)
            }

# Integration function for Underground Stories API
async def multiply_myth_into_series(myth_name: str, mythology_category: str, base_story: str) -> Dict:
    """
    Main entry point for Minute Myths content multiplication.
    
    Args:
        myth_name: Name of the myth
        mythology_category: Category (Greek, Norse, etc.)
        base_story: Base mythology story
        
    Returns:
        Series generation result with all content pieces
    """
    try:
        multiplier = MinuteMythsMultiplier()
        series = await multiplier.multiply_myth_content(myth_name, mythology_category, base_story)
        
        # Generate videos for all content pieces
        results = []
        for content in series.content_pieces:
            result = await multiplier.generate_video_for_content(content)
            results.append(result)
        
        return {
            "success": True,
            "series_title": series.playlist_title,
            "total_pieces": series.total_pieces,
            "estimated_duration": series.estimated_total_duration,
            "content_results": results,
            "multiplication_factor": f"1 myth → {series.total_pieces} videos"
        }
        
    except Exception as e:
        logger.error(f"Myth multiplication failed: {e}")
        return {
            "success": False,
            "error": str(e)
        }

if __name__ == "__main__":
    # Test content multiplication
    async def test():
        myth_name = "Perseus and Medusa"
        category = "Greek Mythology"
        base_story = """Perseus, son of Zeus, must slay the deadly Gorgon Medusa whose gaze turns men to stone. 
        Armed with a mirrored shield from Athena, winged sandals from Hermes, and an invisible helmet from Hades, 
        he approaches her lair backwards, watching only her reflection. With one swift stroke, he beheads the 
        sleeping monster, her blood giving birth to the winged horse Pegasus."""
        
        result = await multiply_myth_into_series(myth_name, category, base_story)
        print(f"Multiplication result: {result}")
    
    asyncio.run(test())