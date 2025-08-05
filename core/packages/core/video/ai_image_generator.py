#!/usr/bin/env python3
"""
AI Image Generator for Underground Stories
=========================================

Generates episode-specific images using OpenAI DALL-E or Google Imagen
for Underground Stories video content.
"""

import asyncio
import base64
import json
import logging
from pathlib import Path
from typing import Dict, Optional, Tuple, List
import hashlib
import os
from datetime import datetime

# OpenAI integration
import openai
from openai import AsyncOpenAI

# HTTP client for image downloads
import aiohttp

logger = logging.getLogger(__name__)


class AIImageGenerator:
    """
    Generate professional episode artwork using AI image generation.
    
    Supports:
    - OpenAI DALL-E 3 (high quality, expensive)
    - OpenAI DALL-E 2 (good quality, cheaper)
    - Future: Google Imagen integration
    """
    
    def __init__(self, project_root: Optional[Path] = None):
        self.project_root = project_root or Path(__file__).parent.parent.parent.parent
        self.images_dir = self.project_root / "content" / "episode_images"
        self.images_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize OpenAI client
        self.openai_client = None
        self._init_openai()
        
        logger.info("AI Image Generator initialized")
    
    def _init_openai(self):
        """Initialize OpenAI client if API key is available"""
        try:
            # Load environment variables from .env file
            from dotenv import load_dotenv
            load_dotenv()
            
            api_key = os.getenv('OPENAI_API_KEY')
            if api_key:
                self.openai_client = AsyncOpenAI(api_key=api_key)
                logger.info("✅ OpenAI DALL-E available")
            else:
                logger.warning("⚠️ OPENAI_API_KEY not found - DALL-E disabled")
        except Exception as e:
            logger.error(f"❌ OpenAI initialization failed: {e}")
    
    async def generate_episode_image(
        self,
        story_content: str,
        metadata: Dict,
        pipeline: str,
        force_regenerate: bool = False,
        custom_prompt: Optional[str] = None,
        output_filename: Optional[str] = None
    ) -> Tuple[Path, Dict]:
        """
        Generate or retrieve cached episode artwork.
        
        Args:
            story_content: The story text to base the image on
            metadata: Episode metadata (title, etc.)
            pipeline: Content pipeline ('fairer-tales', 'timeless-retold', 'minute-myths')
            force_regenerate: Force new generation even if cached image exists
            custom_prompt: Override default prompt generation
            output_filename: Custom filename (optional)
            
        Returns:
            Tuple of (image_path, generation_stats)
        """
        
        # Create filename - use custom filename if provided
        if output_filename:
            image_filename = output_filename
        else:
            # Create unique filename based on content hash
            content_hash = hashlib.md5(f"{story_content[:500]}{pipeline}".encode()).hexdigest()[:12]
            safe_title = "".join(c for c in metadata.get('title', 'episode') if c.isalnum() or c in (' ', '-', '_')).strip()
            safe_title = safe_title.replace(' ', '_')[:30]
            image_filename = f"{pipeline}_{safe_title}_{content_hash}.png"
        
        image_path = self.images_dir / image_filename
        
        # Check if we already have this image
        if image_path.exists() and not force_regenerate:
            logger.info(f"📁 Using cached image: {image_filename}")
            return image_path, {
                "method": "cached",
                "image_path": str(image_path),
                "generated_at": datetime.fromtimestamp(image_path.stat().st_mtime).isoformat()
            }
        
        logger.info(f"🎨 Generating new image for: {metadata.get('title', 'Unknown')}")
        
        # Generate the image
        if self.openai_client:
            return await self._generate_with_openai(
                story_content, metadata, pipeline, image_path, custom_prompt
            )
        else:
            raise RuntimeError("No AI image generation services available")
    
    async def _generate_with_openai(
        self,
        story_content: str,
        metadata: Dict,
        pipeline: str,
        output_path: Path,
        custom_prompt: Optional[str] = None
    ) -> Tuple[Path, Dict]:
        """Generate image using OpenAI DALL-E"""
        
        # Use custom prompt if provided, otherwise create pipeline-specific prompt
        if custom_prompt:
            base_prompt = custom_prompt
        else:
            base_prompt = self._create_image_prompt(story_content, metadata, pipeline)
        
        generation_start = datetime.now()
        
        try:
            logger.info(f"🎨 Generating with DALL-E 3...")
            logger.info(f"📝 Prompt: {base_prompt[:100]}...")
            
            # Determine size based on pipeline
            if pipeline == 'minute-myths':
                size = "1024x1792"  # 9:16 aspect ratio for mobile
                logger.info(f"📱 Using mobile 9:16 format for {pipeline}")
            else:
                size = "1792x1024"  # 16:9 aspect ratio for desktop
                logger.info(f"🖥️ Using desktop 16:9 format for {pipeline}")
            
            response = await self.openai_client.images.generate(
                model="dall-e-3",
                prompt=base_prompt,
                size=size,
                quality="hd",
                style="vivid",
                n=1
            )
            
            # Download the generated image
            image_url = response.data[0].url
            await self._download_image(image_url, output_path)
            
            generation_end = datetime.now()
            generation_time = (generation_end - generation_start).total_seconds()
            
            stats = {
                "method": "dall-e-3",
                "model": "dall-e-3",
                "prompt": base_prompt,
                "size": "1792x1024",
                "quality": "hd",
                "generation_time_seconds": generation_time,
                "image_path": str(output_path),
                "generated_at": generation_end.isoformat(),
                "revised_prompt": response.data[0].revised_prompt if hasattr(response.data[0], 'revised_prompt') else None
            }
            
            logger.info(f"✅ Image generated successfully!")
            logger.info(f"   📁 Saved to: {output_path}")
            logger.info(f"   ⏱️ Generation time: {generation_time:.1f}s")
            
            return output_path, stats
            
        except Exception as e:
            logger.error(f"❌ DALL-E generation failed: {e}")
            
            # Fallback to DALL-E 2 if DALL-E 3 fails
            logger.info("🔄 Falling back to DALL-E 2...")
            try:
                response = await self.openai_client.images.generate(
                    model="dall-e-2",
                    prompt=base_prompt[:1000],  # DALL-E 2 has shorter prompt limit
                    size="1024x1024",  # DALL-E 2 size options
                    n=1
                )
                
                image_url = response.data[0].url
                await self._download_image(image_url, output_path)
                
                generation_end = datetime.now()
                generation_time = (generation_end - generation_start).total_seconds()
                
                stats = {
                    "method": "dall-e-2-fallback",
                    "model": "dall-e-2",
                    "prompt": base_prompt[:1000],
                    "size": "1024x1024",
                    "generation_time_seconds": generation_time,
                    "image_path": str(output_path),
                    "generated_at": generation_end.isoformat()
                }
                
                logger.info(f"✅ Fallback image generated successfully!")
                return output_path, stats
                
            except Exception as e2:
                logger.error(f"❌ DALL-E 2 fallback also failed: {e2}")
                raise RuntimeError(f"Image generation failed: {e}")
    
    def _create_image_prompt(self, story_content: str, metadata: Dict, pipeline: str) -> str:
        """Create AI image generation prompt based on story content and pipeline"""
        
        title = metadata.get('title', 'Unknown Story')
        
        # Extract key story elements (first 500 characters for context)
        story_excerpt = story_content[:500] if story_content else ""
        
        # Pipeline-specific prompt templates
        pipeline_styles = {
            'fairer-tales': {
                'style': 'dark fantasy, gothic fairy tale, atmospheric lighting, rich textures',
                'mood': 'mysterious, atmospheric, slightly dark but not scary',
                'setting': 'fairy tale world with modern psychological depth'
            },
            'timeless-retold': {
                'style': 'classical literature, vintage illustration, elegant composition, literary aesthetic',
                'mood': 'timeless, sophisticated, literary elegance',
                'setting': 'classical literary world with timeless appeal'
            },
            'minute-myths': {
                'style': 'mythological, epic, dynamic composition, vibrant colors, mobile-optimized vertical format',
                'mood': 'epic, powerful, larger-than-life, instantly engaging',
                'setting': 'mythological realm with divine elements, perfect for mobile viewing'
            }
        }
        
        style_guide = pipeline_styles.get(pipeline, pipeline_styles['fairer-tales'])
        
        # Build the prompt with pipeline-specific requirements
        if pipeline == 'minute-myths':
            aspect_ratio = "9:16 vertical format perfect for mobile viewing and social media"
            platform_optimization = "TikTok/Instagram/YouTube Shorts optimized"
        else:
            aspect_ratio = "16:9 widescreen composition perfect for video thumbnails"
            platform_optimization = "YouTube optimized"
        
        prompt = f"""Create a high-quality, cinematic artwork for "{title}".

Story context: {story_excerpt}

Visual style: {style_guide['style']}
Mood: {style_guide['mood']}
Setting: {style_guide['setting']}

Requirements:
- {aspect_ratio}
- Professional, cinematic quality suitable for {platform_optimization}
- Rich detail and atmospheric lighting
- Focus on the main character or central scene
- No text or words in the image
- Underground Stories brand aesthetic: sophisticated, mysterious, high-quality
- Safe for all audiences but with mature storytelling depth

The image should capture the essence of the story and draw viewers into the Underground Stories world."""

        return prompt
    
    async def _download_image(self, url: str, output_path: Path) -> None:
        """Download image from URL to local file"""
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    content = await response.read()
                    with open(output_path, 'wb') as f:
                        f.write(content)
                    logger.info(f"📁 Image downloaded: {output_path}")
                else:
                    raise RuntimeError(f"Failed to download image: HTTP {response.status}")
    
    def get_cached_images(self) -> List[Dict]:
        """Get list of all cached episode images"""
        
        cached_images = []
        
        for image_file in self.images_dir.glob("*.png"):
            stats = image_file.stat()
            cached_images.append({
                "filename": image_file.name,
                "path": str(image_file),
                "size_mb": round(stats.st_size / (1024 * 1024), 2),
                "created": datetime.fromtimestamp(stats.st_ctime).isoformat(),
                "modified": datetime.fromtimestamp(stats.st_mtime).isoformat()
            })
        
        return sorted(cached_images, key=lambda x: x['modified'], reverse=True)
    
    def get_generator_stats(self) -> Dict:
        """Get generator capabilities and statistics"""
        
        cached_images = self.get_cached_images()
        
        return {
            "available_generators": {
                "dall-e-3": self.openai_client is not None,
                "dall-e-2": self.openai_client is not None,
                "google-imagen": False  # Future implementation
            },
            "supported_pipelines": ["fairer-tales", "timeless-retold", "minute-myths"],
            "output_format": "PNG",
            "output_size": "1792x1024 (16:9)",
            "cache_directory": str(self.images_dir),
            "cached_images_count": len(cached_images),
            "total_cache_size_mb": round(sum(img['size_mb'] for img in cached_images), 2)
        }


# Utility functions for integration

async def generate_huff_heal_image() -> Tuple[Path, Dict]:
    """Quick generation function for Huff & Heal episode"""
    
    generator = AIImageGenerator()
    
    # Read the Huff & Heal story
    story_path = Path("content/fairer-tales/stories/Huff & Heal.txt")
    
    if story_path.exists():
        with open(story_path, 'r', encoding='utf-8') as f:
            story_content = f.read()
    else:
        story_content = "Dr. Lupus Grimm, the Big Bad Wolf turned therapist, runs a forest sanctuary helping woodland creatures heal from trauma. When corporate developers threaten his sanctuary, he must choose between his peaceful nature and protecting those he's sworn to help."
    
    metadata = {
        "title": "Underground: The Wolf's Truth - Huff & Heal",
        "episode_number": 1,
        "series": "Fairer Tales"
    }
    
    return await generator.generate_episode_image(
        story_content=story_content,
        metadata=metadata,
        pipeline="fairer-tales"
    )


if __name__ == "__main__":
    # Direct execution for testing
    asyncio.run(generate_huff_heal_image())