#!/usr/bin/env python3
"""
Remotion Video Renderer
======================

Python bridge to integrate Remotion.dev rendering with Underground Stories pipeline.
Provides progressive sketch drawing video generation for all three content pipelines.
"""

import asyncio
import subprocess
import json
import logging
from typing import Dict, Optional, List, Tuple
from pathlib import Path
from datetime import datetime
import shutil
import os

logger = logging.getLogger(__name__)


class RemotionRenderer:
    """
    Bridge between Python pipeline and Remotion.dev video generation.
    
    Handles:
    - Remotion rendering orchestration
    - Audio file preparation and validation
    - Progressive sketch drawing configuration
    - Underground Stories branding integration
    - Quality comparison with FFmpeg system
    """
    
    def __init__(self, project_root: Optional[Path] = None):
        self.project_root = project_root or Path(__file__).parent.parent.parent.parent
        self.output_dir = self.project_root / "content" / "remotion_videos"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Ensure Node.js and Remotion are available
        self._validate_dependencies()
        
        logger.info("Remotion renderer initialized")
    
    def _validate_dependencies(self) -> bool:
        """Validate that Node.js and Remotion are properly installed"""
        try:
            # Check Node.js
            result = subprocess.run(['node', '--version'], 
                                  capture_output=True, text=True, cwd=self.project_root)
            if result.returncode != 0:
                raise RuntimeError("Node.js not found")
            
            # Check npm and Remotion installation
            result = subprocess.run(['npm', 'list', 'remotion'], 
                                  capture_output=True, text=True, cwd=self.project_root)
            if result.returncode != 0:
                raise RuntimeError("Remotion not properly installed")
            
            logger.info("✅ Remotion dependencies validated")
            return True
            
        except Exception as e:
            logger.error(f"❌ Dependency validation failed: {e}")
            raise RuntimeError(f"Remotion setup incomplete: {e}")
    
    async def render_underground_video(
        self,
        audio_path: Path,
        metadata: Dict,
        pipeline: str = "fairer-tales",
        composition_id: Optional[str] = None,
        custom_props: Optional[Dict] = None
    ) -> Tuple[Path, Dict]:
        """
        Render a complete Underground Stories video using Remotion.
        
        Args:
            audio_path: Path to the audio file
            metadata: Video metadata (title, episode, etc.)
            pipeline: Content pipeline ('fairer-tales', 'timeless-retold', 'minute-myths')
            composition_id: Specific Remotion composition to render
            custom_props: Custom properties to pass to Remotion
            
        Returns:
            Tuple of (video_path, render_stats)
        """
        
        logger.info(f"🎬 Starting Remotion render for {metadata.get('title', 'Unknown')}")
        
        # Prepare audio file for Remotion
        prepared_audio = await self._prepare_audio_file(audio_path)
        
        # Calculate video duration from audio
        duration = await self._get_audio_duration(prepared_audio)
        
        # Set up composition props
        props = {
            "title": metadata.get("title", "Underground Stories"),
            "episode": metadata.get("episode_number", 1),
            "pipeline": pipeline,
            "audioPath": prepared_audio.name,  # Just the filename for staticFile()
            "duration": duration,
            **(custom_props or {})
        }
        
        # Determine composition ID
        comp_id = composition_id or self._get_composition_id(metadata, pipeline)
        
        # Generate output filename
        safe_title = "".join(c for c in metadata.get("title", "video") if c.isalnum() or c in (' ', '-', '_')).rstrip()
        safe_title = safe_title.replace(' ', '_')
        output_filename = f"{safe_title}_{pipeline}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
        output_path = self.output_dir / output_filename
        
        # Start rendering
        render_start = datetime.now()
        
        try:
            # Build Remotion render command
            cmd = [
                'npx', 'remotion', 'render',
                'src/remotion/Root.tsx',
                comp_id,
                str(output_path),
                '--props', json.dumps(props),
                '--concurrency', '2',  # Reasonable concurrency for most systems
                '--image-format', 'jpeg',
                '--crf', '18',  # High quality for YouTube
                '--pixel-format', 'yuv420p',
                '--codec', 'h264'
            ]
            
            logger.info(f"🚀 Executing Remotion render: {comp_id}")
            logger.info(f"📁 Output: {output_path}")
            
            # Execute render with real-time output
            process = await asyncio.create_subprocess_exec(
                *cmd,
                cwd=self.project_root,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            if process.returncode != 0:
                error_msg = stderr.decode() if stderr else "Unknown render error"
                logger.error(f"❌ Remotion render failed: {error_msg}")
                raise RuntimeError(f"Remotion render failed: {error_msg}")
            
            # Calculate render statistics
            render_end = datetime.now()
            render_duration = (render_end - render_start).total_seconds()
            
            if not output_path.exists():
                raise RuntimeError("Render completed but output file not found")
            
            file_size_mb = output_path.stat().st_size / (1024 * 1024)
            
            render_stats = {
                "render_duration_seconds": render_duration,
                "output_file_size_mb": round(file_size_mb, 2),
                "video_duration_seconds": duration,
                "compression_ratio": round(file_size_mb / (duration / 60), 2),  # MB per minute
                "render_speed_ratio": round(duration / render_duration, 2),  # How many seconds of video per second of render
                "composition_id": comp_id,
                "pipeline": pipeline,
                "props_used": props,
                "timestamp": render_end.isoformat()
            }
            
            logger.info(f"✅ Remotion render complete!")
            logger.info(f"   📹 Duration: {duration}s")
            logger.info(f"   📦 Size: {file_size_mb:.2f}MB")
            logger.info(f"   ⏱️ Render time: {render_duration:.1f}s")
            logger.info(f"   🚀 Speed ratio: {render_stats['render_speed_ratio']:.2f}x")
            
            return output_path, render_stats
            
        except Exception as e:
            logger.error(f"❌ Render failed: {e}")
            # Clean up partial files
            if output_path.exists():
                output_path.unlink()
            raise
    
    async def _prepare_audio_file(self, audio_path: Path) -> Path:
        """Prepare audio file for Remotion rendering"""
        
        if not audio_path.exists():
            raise FileNotFoundError(f"Audio file not found: {audio_path}")
        
        # For now, we'll use the audio file as-is
        # In the future, we might need format conversion or optimization
        
        # Ensure audio is accessible to Remotion (in public directory)
        public_dir = self.project_root / "public"
        public_dir.mkdir(exist_ok=True)
        
        public_audio_path = public_dir / audio_path.name
        
        # Copy audio to public directory if not already there
        if not public_audio_path.exists() or public_audio_path.stat().st_mtime < audio_path.stat().st_mtime:
            shutil.copy2(audio_path, public_audio_path)
            logger.info(f"📁 Audio prepared: {public_audio_path}")
        
        return public_audio_path
    
    async def _get_audio_duration(self, audio_path: Path) -> int:
        """Get audio duration in seconds using ffprobe"""
        try:
            cmd = [
                'ffprobe', '-v', 'quiet', '-print_format', 'json', 
                '-show_format', str(audio_path)
            ]
            
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            if process.returncode == 0:
                data = json.loads(stdout.decode())
                duration = float(data['format']['duration'])
                return int(duration)
            else:
                logger.warning(f"Could not get audio duration, using default: {stderr.decode()}")
                return 660  # Default to 11 minutes for Huff & Heal
                
        except Exception as e:
            logger.warning(f"Audio duration detection failed: {e}, using default")
            return 660
    
    def _get_composition_id(self, metadata: Dict, pipeline: str) -> str:
        """Determine appropriate Remotion composition ID"""
        
        # Check if this is the specific Huff & Heal episode
        title = metadata.get("title", "").lower()
        if "huff" in title and "heal" in title:
            return "huff-and-heal"
        
        # Use pipeline-specific template
        pipeline_compositions = {
            "fairer-tales": "fairer-tales-template",
            "timeless-retold": "timeless-retold-template", 
            "minute-myths": "minute-myths-template"
        }
        
        return pipeline_compositions.get(pipeline, "fairer-tales-template")
    
    async def preview_video(self, composition_id: str = "huff-and-heal") -> None:
        """Start Remotion preview server for development"""
        
        logger.info(f"🎬 Starting Remotion preview for: {composition_id}")
        
        cmd = ['npm', 'run', 'dev']
        
        process = await asyncio.create_subprocess_exec(
            *cmd,
            cwd=self.project_root
        )
        
        await process.wait()
    
    async def compare_with_ffmpeg(
        self,
        remotion_path: Path,
        ffmpeg_path: Path
    ) -> Dict:
        """Compare Remotion output with existing FFmpeg system"""
        
        logger.info("📊 Comparing Remotion vs FFmpeg quality...")
        
        try:
            # Get file stats
            remotion_stats = remotion_path.stat()
            ffmpeg_stats = ffmpeg_path.stat()
            
            comparison = {
                "remotion": {
                    "file_size_mb": round(remotion_stats.st_size / (1024 * 1024), 2),
                    "path": str(remotion_path)
                },
                "ffmpeg": {
                    "file_size_mb": round(ffmpeg_stats.st_size / (1024 * 1024), 2),
                    "path": str(ffmpeg_path)
                },
                "comparison": {
                    "size_difference_mb": round((remotion_stats.st_size - ffmpeg_stats.st_size) / (1024 * 1024), 2),
                    "size_ratio": round(remotion_stats.st_size / ffmpeg_stats.st_size, 2),
                    "remotion_advantage": remotion_stats.st_size < ffmpeg_stats.st_size
                }
            }
            
            logger.info(f"📊 Comparison complete:")
            logger.info(f"   Remotion: {comparison['remotion']['file_size_mb']}MB")
            logger.info(f"   FFmpeg: {comparison['ffmpeg']['file_size_mb']}MB")
            logger.info(f"   Ratio: {comparison['comparison']['size_ratio']:.2f}x")
            
            return comparison
            
        except Exception as e:
            logger.error(f"Comparison failed: {e}")
            return {"error": str(e)}
    
    def get_render_stats(self) -> Dict:
        """Get rendering statistics and capabilities"""
        return {
            "renderer": "Remotion.dev",
            "version": "4.0.331",
            "supported_formats": ["mp4", "mov", "webm"],
            "supported_pipelines": ["fairer-tales", "timeless-retold", "minute-myths"],
            "features": [
                "progressive_sketch_drawing",
                "svg_based_illustrations", 
                "audio_synchronization",
                "underground_stories_branding",
                "mobile_optimized_output",
                "typescript_based_components"
            ],
            "output_specs": {
                "resolution": "1920x1080",
                "fps": 30,
                "codec": "h264",
                "quality": "high (CRF 18)",
                "format": "mp4"
            },
            "estimated_render_time": "1-3 minutes per video minute"
        }


# Utility functions for integration

async def render_huff_and_heal() -> Tuple[Path, Dict]:
    """Quick render function for Huff & Heal episode"""
    
    renderer = RemotionRenderer()
    
    audio_path = Path("content/complete_episodes/Huff_and_Heal_Complete_Episode.mp3")
    
    metadata = {
        "title": "Underground: The Wolf's Truth - Huff & Heal",
        "episode_number": 1,
        "series": "Fairer Tales",
        "description": "The story they didn't want you to hear about the Big Bad Wolf."
    }
    
    return await renderer.render_underground_video(
        audio_path=audio_path,
        metadata=metadata,
        pipeline="fairer-tales"
    )


if __name__ == "__main__":
    # Direct execution for testing
    asyncio.run(render_huff_and_heal())