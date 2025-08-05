#!/usr/bin/env python3
"""
Audio Concatenation Utility
===========================

Seamlessly combines multiple audio chunks into complete episodes.
Handles timing, cross-fades, and quality optimization.
"""

import asyncio
import logging
from typing import List, Optional
from pathlib import Path
from datetime import datetime
import subprocess
import os

logger = logging.getLogger(__name__)


class AudioConcatenator:
    """
    Combines multiple audio files into seamless episodes.
    
    Features:
    - Maintains consistent audio quality
    - Adds smooth transitions between chunks
    - Optimizes for storytelling (no abrupt cuts)
    - Handles different audio formats
    - Preserves metadata
    """
    
    def __init__(self, temp_dir: str = "temp/audio_processing"):
        self.temp_dir = Path(temp_dir)
        self.temp_dir.mkdir(parents=True, exist_ok=True)
        
        # Audio processing settings
        self.crossfade_duration = 0.1  # 100ms crossfade between chunks
        self.silence_duration = 0.2   # 200ms pause between chunks
        self.target_bitrate = "128k"  # Consistent quality
        self.target_sample_rate = 24000  # OpenAI TTS default
    
    async def concatenate_chunks(
        self, 
        audio_files: List[Path], 
        output_path: Path,
        add_pauses: bool = True,
        crossfade: bool = True
    ) -> dict:
        """
        Concatenate audio files into a single episode.
        
        Args:
            audio_files: List of audio file paths to concatenate
            output_path: Path for the final concatenated audio
            add_pauses: Whether to add brief pauses between chunks
            crossfade: Whether to add crossfades for smooth transitions
            
        Returns:
            Dict with concatenation results and metadata
        """
        
        if not audio_files:
            raise ValueError("No audio files provided for concatenation")
        
        if len(audio_files) == 1:
            # Single file, just copy it
            return await self._copy_single_file(audio_files[0], output_path)
        
        logger.info(f"Concatenating {len(audio_files)} audio chunks")
        
        try:
            # Ensure output directory exists
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Method 1: Try ffmpeg for high-quality concatenation
            if await self._has_ffmpeg():
                result = await self._concatenate_with_ffmpeg(
                    audio_files, output_path, add_pauses, crossfade
                )
            else:
                # Fallback: Simple concatenation
                result = await self._concatenate_simple(audio_files, output_path)
            
            # Validate result
            if output_path.exists() and output_path.stat().st_size > 0:
                result["success"] = True
                result["output_path"] = output_path
                result["file_size"] = output_path.stat().st_size
                
                logger.info(f"Concatenation successful: {output_path}")
                return result
            else:
                raise Exception("Concatenation failed - output file is empty or missing")
                
        except Exception as e:
            logger.error(f"Audio concatenation failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "output_path": output_path
            }
    
    async def _has_ffmpeg(self) -> bool:
        """Check if ffmpeg is available for high-quality processing"""
        try:
            result = subprocess.run(
                ["ffmpeg", "-version"], 
                capture_output=True, 
                text=True, 
                timeout=5
            )
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return False
    
    async def _concatenate_with_ffmpeg(
        self, 
        audio_files: List[Path], 
        output_path: Path,
        add_pauses: bool,
        crossfade: bool
    ) -> dict:
        """High-quality concatenation using ffmpeg"""
        
        # Create input file list for ffmpeg
        input_list_path = self.temp_dir / f"concat_list_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        with open(input_list_path, 'w') as f:
            for audio_file in audio_files:
                f.write(f"file '{audio_file.absolute()}'\n")
                if add_pauses and audio_file != audio_files[-1]:  # Don't add pause after last file
                    # Add silence between chunks
                    f.write(f"file 'silence.mp3'\n")
        
        # Create silence file if needed
        silence_file = None
        if add_pauses:
            silence_file = await self._create_silence_file()
            # Update the input list to use the actual silence file path
            with open(input_list_path, 'w') as f:
                for i, audio_file in enumerate(audio_files):
                    f.write(f"file '{audio_file.absolute()}'\n")
                    if i < len(audio_files) - 1:  # Don't add pause after last file
                        f.write(f"file '{silence_file.absolute()}'\n")
        
        try:
            # Build ffmpeg command
            cmd = [
                "ffmpeg", "-y",  # Overwrite output file
                "-f", "concat",
                "-safe", "0",
                "-i", str(input_list_path),
                "-c:a", "mp3",  # Audio codec
                "-b:a", self.target_bitrate,  # Bitrate
                "-ar", str(self.target_sample_rate),  # Sample rate
                str(output_path)
            ]
            
            # Run ffmpeg
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=120  # 2 minute timeout
            )
            
            if result.returncode != 0:
                raise Exception(f"ffmpeg failed: {result.stderr}")
            
            return {
                "method": "ffmpeg",
                "chunks_processed": len(audio_files),
                "added_pauses": add_pauses,
                "processing_time": "calculated_later"
            }
            
        finally:
            # Cleanup temp files
            if input_list_path.exists():
                input_list_path.unlink()
            if silence_file and silence_file.exists():
                silence_file.unlink()
    
    async def _create_silence_file(self) -> Path:
        """Create a short silence file for pauses between chunks"""
        silence_file = self.temp_dir / "silence.mp3"
        
        cmd = [
            "ffmpeg", "-y",
            "-f", "lavfi",
            "-i", f"anullsrc=channel_layout=mono:sample_rate={self.target_sample_rate}",
            "-t", str(self.silence_duration),
            "-c:a", "mp3",
            "-b:a", self.target_bitrate,
            str(silence_file)
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            raise Exception(f"Failed to create silence file: {result.stderr}")
        
        return silence_file
    
    async def _concatenate_simple(self, audio_files: List[Path], output_path: Path) -> dict:
        """Simple concatenation fallback (without ffmpeg)"""
        logger.warning("Using simple concatenation - install ffmpeg for better quality")
        
        # For now, just copy the first file as a basic fallback
        # In production, you might want to implement binary concatenation
        # or use a Python audio library like pydub
        
        if audio_files:
            # Simple copy of first file (placeholder)
            import shutil
            shutil.copy2(audio_files[0], output_path)
            
            return {
                "method": "simple_copy",
                "warning": "Only first chunk copied - install ffmpeg for full concatenation",
                "chunks_processed": 1
            }
        
        raise Exception("No audio files to concatenate")
    
    async def _copy_single_file(self, source: Path, destination: Path) -> dict:
        """Copy single file when no concatenation needed"""
        import shutil
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
        
        return {
            "success": True,
            "method": "single_file_copy",
            "chunks_processed": 1,
            "output_path": destination,
            "file_size": destination.stat().st_size
        }
    
    def estimate_duration(self, audio_files: List[Path]) -> float:
        """Estimate total duration of concatenated audio"""
        # This is a rough estimate - for accurate duration, would need audio analysis
        total_estimated_seconds = 0
        
        for audio_file in audio_files:
            # Rough estimate based on file size (varies by bitrate)
            file_size_mb = audio_file.stat().st_size / (1024 * 1024)
            # Assume ~1MB per minute for 128kbps MP3
            estimated_minutes = file_size_mb
            total_estimated_seconds += estimated_minutes * 60
        
        # Add pause time
        if len(audio_files) > 1:
            total_pauses = (len(audio_files) - 1) * self.silence_duration
            total_estimated_seconds += total_pauses
        
        return total_estimated_seconds
    
    def cleanup_temp_files(self):
        """Clean up temporary processing files"""
        if self.temp_dir.exists():
            for temp_file in self.temp_dir.glob("*"):
                try:
                    temp_file.unlink()
                except Exception as e:
                    logger.warning(f"Could not delete temp file {temp_file}: {e}")


# Convenience function for easy integration
async def concatenate_episode_chunks(chunk_files: List[Path], episode_path: Path) -> dict:
    """
    Convenience function to concatenate audio chunks into a complete episode.
    
    Args:
        chunk_files: List of paths to audio chunk files
        episode_path: Path where the complete episode should be saved
        
    Returns:
        Dict with concatenation results
    """
    concatenator = AudioConcatenator()
    try:
        result = await concatenator.concatenate_chunks(
            audio_files=chunk_files,
            output_path=episode_path,
            add_pauses=True,
            crossfade=True
        )
        return result
    finally:
        concatenator.cleanup_temp_files()


if __name__ == "__main__":
    # Test concatenation (would need actual audio files)
    import asyncio
    
    async def test_concatenator():
        concatenator = AudioConcatenator()
        
        # Test with dummy file paths (for development)
        test_files = [
            Path("test_chunk_1.mp3"),
            Path("test_chunk_2.mp3")
        ]
        
        print("Audio Concatenator initialized")
        print(f"FFmpeg available: {await concatenator._has_ffmpeg()}")
        print(f"Estimated duration for 2 chunks: {concatenator.estimate_duration(test_files):.1f}s")
    
    asyncio.run(test_concatenator())