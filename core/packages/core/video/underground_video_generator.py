#!/usr/bin/env python3
"""
Underground Stories Video Generator
==================================

Creates actual video files with synchronized text, waveforms, and atmospheric backgrounds.
Implements the complete visual design system for Underground Stories.
"""

import asyncio
import logging
import subprocess
import re
from typing import List, Dict, Tuple
from pathlib import Path
from datetime import datetime
import json
import math

# For video generation
try:
    import numpy as np
    from PIL import Image, ImageDraw, ImageFont, ImageFilter
    import librosa
    DEPENDENCIES_AVAILABLE = True
except ImportError:
    DEPENDENCIES_AVAILABLE = False

logger = logging.getLogger(__name__)


class TextTimingEngine:
    """Calculates precise timing for text synchronization with audio"""
    
    def __init__(self, words_per_minute: float = 150):
        self.words_per_minute = words_per_minute
        self.words_per_second = words_per_minute / 60
        
    def calculate_text_timing(self, text: str, audio_duration_seconds: float) -> List[Dict]:
        """
        Calculate precise timing for text display.
        
        Args:
            text: Complete episode text
            audio_duration_seconds: Actual audio duration
            
        Returns:
            List of timing segments with start/end times
        """
        # Split text into sentences
        sentences = self._split_into_sentences(text)
        total_words = sum(len(sentence.split()) for sentence in sentences)
        
        # Calculate scaling factor based on actual audio duration
        estimated_duration = total_words / self.words_per_second
        time_scale = audio_duration_seconds / estimated_duration
        
        timing_segments = []
        current_time = 0
        
        for i, sentence in enumerate(sentences):
            word_count = len(sentence.split())
            natural_duration = word_count / self.words_per_second
            scaled_duration = natural_duration * time_scale
            
            # Group sentences into 2-3 sentence segments for readability
            segment_text = sentence
            if i < len(sentences) - 1 and len(sentence.split()) < 8:
                # Add next sentence if current is short
                segment_text += " " + sentences[i + 1]
                word_count += len(sentences[i + 1].split())
                scaled_duration += (len(sentences[i + 1].split()) / self.words_per_second) * time_scale
                sentences[i + 1] = ""  # Mark as used
            
            if segment_text and segment_text.strip():  # Skip empty segments
                timing_segments.append({
                    "text": segment_text.strip(),
                    "start_time": current_time,
                    "end_time": current_time + scaled_duration,
                    "duration": scaled_duration,
                    "word_count": word_count
                })
                
                current_time += scaled_duration
        
        return [seg for seg in timing_segments if seg["text"]]  # Remove empty segments
    
    def _split_into_sentences(self, text: str) -> List[str]:
        """Split text into sentences using smart sentence detection"""
        # Handle dialogue and complex punctuation
        sentences = re.split(r'(?<=[.!?])\s+(?=[A-Z])', text)
        # Clean up sentences
        return [s.strip() for s in sentences if s.strip()]


class WaveformGenerator:
    """Generates audio waveform visualizations"""
    
    def __init__(self, width: int = 1920, height: int = 200):
        self.width = width
        self.height = height
    
    def generate_waveform_data(self, audio_path: Path, style: str = "underground") -> Dict:
        """
        Generate waveform visualization data from audio file.
        
        Args:
            audio_path: Path to audio file
            style: Visual style (underground, classical, energetic)
            
        Returns:
            Dict with waveform data and styling
        """
        if not DEPENDENCIES_AVAILABLE:
            logger.warning("Audio analysis dependencies not available, using placeholder")
            return self._generate_placeholder_waveform()
        
        try:
            # Load audio file
            y, sr = librosa.load(str(audio_path))
            
            # Calculate frame-based waveform for video synchronization
            frame_rate = 30  # 30 FPS
            hop_length = len(y) // (len(y) * frame_rate // sr)
            
            # Extract amplitude envelope
            amplitude = np.abs(y)
            
            # Downsample to video frame rate
            frames_total = int(len(y) / sr * frame_rate)
            samples_per_frame = len(amplitude) // frames_total
            
            waveform_frames = []
            for i in range(frames_total):
                start_idx = i * samples_per_frame
                end_idx = min(start_idx + samples_per_frame, len(amplitude))
                frame_amplitude = np.mean(amplitude[start_idx:end_idx])
                waveform_frames.append(float(frame_amplitude))
            
            return {
                "frames": waveform_frames,
                "duration": len(y) / sr,
                "sample_rate": sr,
                "style": style,
                "max_amplitude": float(np.max(amplitude))
            }
            
        except Exception as e:
            logger.error(f"Waveform generation failed: {e}")
            return self._generate_placeholder_waveform()
    
    def _generate_placeholder_waveform(self) -> Dict:
        """Generate placeholder waveform for testing"""
        frames = [0.3 + 0.7 * math.sin(i * 0.1) * (0.5 + 0.5 * math.sin(i * 0.01)) for i in range(19800)]  # 11 minutes at 30fps
        return {
            "frames": frames,
            "duration": 660,  # 11 minutes
            "sample_rate": 22050,
            "style": "underground",
            "max_amplitude": 1.0
        }


class UndergroundVideoGenerator:
    """
    Complete video generation system for Underground Stories.
    Creates professional videos with synchronized text and atmospheric visuals.
    """
    
    def __init__(self, output_dir: str = "content/underground_videos"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.timing_engine = TextTimingEngine()
        self.waveform_generator = WaveformGenerator()
        
        # Video settings
        self.video_settings = {
            "resolution": (1920, 1080),
            "fps": 30,
            "bitrate": "2M",
            "audio_bitrate": "128k"
        }
        
        # Visual themes
        self.themes = {
            "underground_fairer_tales": {
                "background_color": (44, 44, 44),      # #2C2C2C
                "accent_color": (184, 115, 51),        # #B87333
                "text_color": (245, 245, 245),         # #F5F5F5
                "highlight_color": (0, 191, 255),      # #00BFFF
                "font_size": 32,
                "waveform_style": "circular"
            },
            "underground_timeless": {
                "background_color": (44, 24, 16),      # #2C1810
                "accent_color": (139, 69, 19),         # #8B4513
                "text_color": (244, 241, 222),         # #F4F1DE
                "highlight_color": (184, 115, 51),     # #B87333
                "font_size": 30,
                "waveform_style": "linear"
            },
            "underground_myths": {
                "background_color": (13, 17, 23),      # #0D1117
                "accent_color": (88, 166, 255),        # #58A6FF
                "text_color": (240, 246, 252),         # #F0F6FC
                "highlight_color": (0, 191, 255),      # #00BFFF
                "font_size": 34,
                "waveform_style": "energetic"
            }
        }
    
    async def create_video(
        self, 
        audio_path: Path, 
        text: str, 
        metadata: Dict,
        theme: str = "underground_fairer_tales"
    ) -> Path:
        """
        Create complete video with synchronized text and visuals.
        
        Args:
            audio_path: Path to audio file
            text: Complete episode text
            metadata: Video metadata
            theme: Visual theme to use
            
        Returns:
            Path to generated video file
        """
        
        logger.info(f"Creating Underground Stories video: {metadata.get('title', 'Unknown')}")
        
        # Step 1: Analyze audio for timing and waveform
        logger.info("Analyzing audio...")
        audio_duration = self._get_audio_duration(audio_path)
        waveform_data = self.waveform_generator.generate_waveform_data(audio_path, theme)
        
        # Step 2: Calculate text timing
        logger.info("Calculating text timing...")
        text_segments = self.timing_engine.calculate_text_timing(text, audio_duration)
        
        # Step 3: Generate video components
        logger.info("Generating visual components...")
        
        # Create output path
        safe_title = re.sub(r'[^\w\-_\.]', '_', metadata.get('title', 'video'))
        output_path = self.output_dir / f"{safe_title}.mp4"
        
        # Step 4: Create video using FFmpeg
        success = await self._create_video_with_ffmpeg(
            audio_path=audio_path,
            text_segments=text_segments,
            waveform_data=waveform_data,
            theme=theme,
            output_path=output_path,
            metadata=metadata
        )
        
        if success:
            logger.info(f"Video created successfully: {output_path}")
            return output_path
        else:
            raise Exception("Video creation failed")
    
    async def _create_video_with_ffmpeg(
        self,
        audio_path: Path,
        text_segments: List[Dict],
        waveform_data: Dict,
        theme: str,
        output_path: Path,
        metadata: Dict
    ) -> bool:
        """Create video using FFmpeg with synchronized text and visuals"""
        
        theme_config = self.themes.get(theme, self.themes["underground_fairer_tales"])
        
        try:
            # Create subtitle file for text synchronization
            subtitle_path = await self._create_subtitle_file(text_segments, theme_config)
            
            # Create waveform visualization
            waveform_path = await self._create_waveform_video(waveform_data, theme_config)
            
            # Create atmospheric background
            background_path = await self._create_atmospheric_background(theme_config, waveform_data["duration"])
            
            logger.info("Creating video with synchronized text and visuals...")
            
            # Enhanced FFmpeg command with text overlay and waveform
            cmd = [
                "ffmpeg", "-y",
                # Input files
                "-i", str(background_path),    # Background video
                "-i", str(waveform_path),      # Waveform visualization
                "-i", str(audio_path),         # Audio
                
                # Complex filter for layered composition
                "-filter_complex", 
                f"[0:v][1:v]overlay=0:860[bg_wave];"  # Add waveform at bottom
                f"[bg_wave]subtitles={subtitle_path}:force_style='"
                f"FontName=Arial,FontSize={theme_config['font_size']},"
                f"PrimaryColour=&H{self._rgb_to_bgr_hex(theme_config['text_color'])},"
                f"BackColour=&H80000000,"  # Semi-transparent background
                f"BorderStyle=1,Outline=2,Shadow=1,"
                f"Alignment=2,MarginV=180'[final]",  # Bottom-middle positioning
                
                # Output mapping
                "-map", "[final]",
                "-map", "2:a",  # Audio from input 2
                
                # Encoding settings
                "-c:v", "libx264",
                "-c:a", "aac",
                "-b:v", self.video_settings["bitrate"],
                "-b:a", self.video_settings["audio_bitrate"],
                "-r", str(self.video_settings["fps"]),
                "-pix_fmt", "yuv420p",  # YouTube compatibility
                
                str(output_path)
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                # Save generation info
                info = {
                    "video_path": str(output_path),
                    "audio_source": str(audio_path),
                    "theme": theme,
                    "text_segments": len(text_segments),
                    "duration": waveform_data["duration"],
                    "features": ["synchronized_text", "waveform_visualization", "atmospheric_background"],
                    "created_at": datetime.now().isoformat(),
                    "metadata": metadata
                }
                
                info_path = output_path.with_suffix('.info.json')
                with open(info_path, 'w') as f:
                    json.dump(info, f, indent=2)
                
                # Cleanup temporary files
                self._cleanup_temp_files([subtitle_path, waveform_path, background_path])
                
                return True
            else:
                logger.error(f"FFmpeg failed: {result.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"Video creation failed: {e}")
            return False
    
    async def _create_subtitle_file(self, text_segments: List[Dict], theme_config: Dict) -> Path:
        """Create SRT subtitle file for text synchronization"""
        srt_path = self.output_dir / "temp_subtitles.srt"
        
        with open(srt_path, 'w', encoding='utf-8') as f:
            for i, segment in enumerate(text_segments, 1):
                start_time = self._seconds_to_srt_time(segment["start_time"])
                end_time = self._seconds_to_srt_time(segment["end_time"])
                
                f.write(f"{i}\n")
                f.write(f"{start_time} --> {end_time}\n")
                f.write(f"{segment['text']}\n\n")
        
        return srt_path
    
    async def _create_waveform_video(self, waveform_data: Dict, theme_config: Dict) -> Path:
        """Create waveform visualization video"""
        waveform_path = self.output_dir / "temp_waveform.mp4"
        
        # Create a simple waveform visualization using FFmpeg
        color = self._rgb_to_hex(theme_config['accent_color'])
        duration = waveform_data["duration"]
        
        cmd = [
            "ffmpeg", "-y",
            "-f", "lavfi",
            "-i", f"color=c=black@0.0:size=1920x220:duration={duration}",  # Transparent background
            "-f", "lavfi", 
            "-i", f"sine=frequency=1000:duration={duration}",  # Dummy audio for waveform
            "-filter_complex",
            f"[1:a]showwaves=s=1920x220:mode=line:colors={color}:scale=lin[wave];"
            f"[0:v][wave]overlay[out]",
            "-map", "[out]",
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            "-t", str(duration),
            str(waveform_path)
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            logger.warning(f"Waveform creation failed, using placeholder: {result.stderr}")
            # Create simple colored bar as fallback
            await self._create_simple_waveform_placeholder(waveform_path, theme_config, duration)
        
        return waveform_path
    
    async def _create_simple_waveform_placeholder(self, output_path: Path, theme_config: Dict, duration: float):
        """Create simple colored bar as waveform placeholder"""
        color = self._rgb_to_hex(theme_config['accent_color'])
        cmd = [
            "ffmpeg", "-y",
            "-f", "lavfi",
            "-i", f"color=c={color}@0.7:size=1920x220:duration={duration}",
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            str(output_path)
        ]
        subprocess.run(cmd, capture_output=True, text=True)
    
    async def _create_atmospheric_background(self, theme_config: Dict, duration: float) -> Path:
        """Create atmospheric background video"""
        bg_path = self.output_dir / "temp_background.mp4"
        
        # Create animated gradient background
        bg_color = self._rgb_to_hex(theme_config['background_color'])
        accent_color = self._rgb_to_hex(theme_config['accent_color'])
        
        cmd = [
            "ffmpeg", "-y",
            "-f", "lavfi",
            "-i", f"color=c={bg_color}:size=1920x1080:duration={duration}",
            # Add subtle gradient overlay
            "-f", "lavfi",
            "-i", f"gradients=s=1920x1080:c0={bg_color}:c1={accent_color}@0.1:duration={duration}",
            "-filter_complex",
            "[0:v][1:v]overlay=0:0:eval=frame:eof_action=repeat[bg];"
            # Add subtle animation with noise
            "[bg]noise=alls=20:allf=t+u:c=1[final]",
            "-map", "[final]",
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            str(bg_path)
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            logger.warning(f"Atmospheric background creation failed, using simple background: {result.stderr}")
            # Fallback to simple colored background
            await self._create_simple_background(bg_path, theme_config, duration)
        
        return bg_path
    
    async def _create_simple_background(self, output_path: Path, theme_config: Dict, duration: float):
        """Create simple colored background as fallback"""
        color = self._rgb_to_hex(theme_config['background_color'])
        cmd = [
            "ffmpeg", "-y",
            "-f", "lavfi",
            "-i", f"color=c={color}:size=1920x1080:duration={duration}",
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            str(output_path)
        ]
        subprocess.run(cmd, capture_output=True, text=True)
    
    def _seconds_to_srt_time(self, seconds: float) -> str:
        """Convert seconds to SRT time format"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millisecs = int((seconds % 1) * 1000)
        return f"{hours:02d}:{minutes:02d}:{secs:02d},{millisecs:03d}"
    
    def _rgb_to_hex(self, rgb: Tuple[int, int, int]) -> str:
        """Convert RGB tuple to hex string"""
        return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"
    
    def _rgb_to_bgr_hex(self, rgb: Tuple[int, int, int]) -> str:
        """Convert RGB tuple to BGR hex string (for FFmpeg subtitles)"""
        # FFmpeg expects BGR format for subtitle colors
        return f"{rgb[2]:02x}{rgb[1]:02x}{rgb[0]:02x}"
    
    def _cleanup_temp_files(self, file_paths: List[Path]):
        """Clean up temporary files"""
        for path in file_paths:
            try:
                if path.exists():
                    path.unlink()
                    logger.debug(f"Cleaned up temp file: {path}")
            except Exception as e:
                logger.warning(f"Failed to cleanup {path}: {e}")
    
    def _get_audio_duration(self, audio_path: Path) -> float:
        """Get audio duration using FFprobe"""
        try:
            cmd = [
                "ffprobe", "-v", "quiet", "-show_entries", "format=duration",
                "-of", "csv=p=0", str(audio_path)
            ]
            result = subprocess.run(cmd, capture_output=True, text=True)
            return float(result.stdout.strip())
        except:
            # Fallback estimation based on file size
            file_size_mb = audio_path.stat().st_size / (1024 * 1024)
            return file_size_mb * 60  # Rough estimate: 1MB per minute
    
    def get_text_timing_preview(self, text: str, duration: float) -> List[Dict]:
        """Preview text timing without creating video"""
        return self.timing_engine.calculate_text_timing(text, duration)


# Convenience function for easy integration
async def create_underground_video(
    audio_path: Path,
    text: str,
    metadata: Dict,
    theme: str = "underground_fairer_tales"
) -> Path:
    """
    Convenience function to create Underground Stories video.
    
    Args:
        audio_path: Path to audio file
        text: Complete episode text
        metadata: Video metadata
        theme: Visual theme
        
    Returns:
        Path to created video file
    """
    generator = UndergroundVideoGenerator()
    return await generator.create_video(audio_path, text, metadata, theme)


if __name__ == "__main__":
    # Test the video generator
    async def test_generator():
        generator = UndergroundVideoGenerator()
        
        # Test text timing
        sample_text = "Dr. Lupus Grimm sat in his forest sanctuary. The therapy circle was an unlikely gathering. Today, we practice the breathing technique."
        timing = generator.get_text_timing_preview(sample_text, 30)
        
        print("Text Timing Preview:")
        for i, segment in enumerate(timing, 1):
            print(f"{i}. {segment['start_time']:.1f}s-{segment['end_time']:.1f}s: {segment['text'][:50]}...")
    
    asyncio.run(test_generator())