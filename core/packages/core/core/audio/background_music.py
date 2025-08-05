#!/usr/bin/env python3
"""
Background Music System - Classical Audio Mixing
===============================================

Adds low-volume classical music to Underground Stories audio content.
Supports public domain classical MP3s with intelligent volume balancing.
"""

import asyncio
import logging
import os
import random
from pathlib import Path
from typing import Dict, List, Optional, Union
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class MusicTrack:
    """Represents a background music track"""
    file_path: Path
    title: str
    composer: str
    duration_seconds: float
    genre: str  # baroque, classical, romantic, modern
    mood: str   # peaceful, dramatic, mysterious, uplifting
    intensity: str  # low, medium, high


class BackgroundMusicManager:
    """
    Manages background music for Underground Stories content.
    
    Features:
    - Intelligent music selection based on story genre
    - Volume balancing to ensure voice clarity
    - Seamless audio mixing and crossfading
    - Public domain classical music support
    """
    
    def __init__(self, music_library_path: str = "assets/music/classical"):
        self.music_library = Path(music_library_path)
        self.music_library.mkdir(parents=True, exist_ok=True)
        
        # Audio mixing settings
        self.background_volume = -18  # dB reduction for background music
        self.voice_boost = 2         # dB boost for voice clarity
        self.crossfade_duration = 2000  # ms for smooth transitions
        
        # Music catalog (will be auto-populated from files)
        self.music_catalog: List[MusicTrack] = []
        self._load_music_catalog()
        
        logger.info(f"🎵 Background Music Manager initialized with {len(self.music_catalog)} tracks")
    
    def _load_music_catalog(self):
        """Load music catalog from library directory"""
        
        # Sample classical music database (you'll add actual files)
        sample_tracks = [
            {
                "filename": "bach_air_on_g_string.mp3",
                "title": "Air on the G String",
                "composer": "Johann Sebastian Bach",
                "genre": "baroque",
                "mood": "peaceful",
                "intensity": "low"
            },
            {
                "filename": "mozart_eine_kleine_nachtmusik.mp3", 
                "title": "Eine kleine Nachtmusik",
                "composer": "Wolfgang Amadeus Mozart",
                "genre": "classical",
                "mood": "uplifting", 
                "intensity": "medium"
            },
            {
                "filename": "beethoven_moonlight_sonata.mp3",
                "title": "Moonlight Sonata",
                "composer": "Ludwig van Beethoven", 
                "genre": "classical",
                "mood": "mysterious",
                "intensity": "low"
            },
            {
                "filename": "vivaldi_four_seasons_spring.mp3",
                "title": "The Four Seasons - Spring",
                "composer": "Antonio Vivaldi",
                "genre": "baroque",
                "mood": "uplifting",
                "intensity": "medium"
            },
            {
                "filename": "chopin_nocturne_op9_no2.mp3",
                "title": "Nocturne in E-flat major",
                "composer": "Frédéric Chopin",
                "genre": "romantic",
                "mood": "peaceful",
                "intensity": "low"
            }
        ]
        
        # Load actual files that exist
        for track_info in sample_tracks:
            file_path = self.music_library / track_info["filename"]
            
            if file_path.exists():
                try:
                    # Get duration from actual file
                    audio = AudioSegment.from_mp3(str(file_path))
                    duration = len(audio) / 1000.0  # Convert to seconds
                    
                    track = MusicTrack(
                        file_path=file_path,
                        title=track_info["title"],
                        composer=track_info["composer"],
                        duration_seconds=duration,
                        genre=track_info["genre"],
                        mood=track_info["mood"],
                        intensity=track_info["intensity"]
                    )
                    
                    self.music_catalog.append(track)
                    logger.info(f"📀 Loaded: {track.composer} - {track.title} ({duration:.1f}s)")
                    
                except Exception as e:
                    logger.warning(f"⚠️ Failed to load {file_path}: {e}")
            else:
                logger.debug(f"📂 Music file not found: {file_path}")
    
    def select_music_for_story(self, story_type: str, story_mood: str = "neutral", 
                              duration_seconds: float = 0) -> Optional[MusicTrack]:
        """
        Intelligently select background music based on story characteristics.
        
        Args:
            story_type: timeless_retold, minute_myths, flipside
            story_mood: peaceful, dramatic, mysterious, uplifting, epic
            duration_seconds: Target duration for the story
        """
        
        if not self.music_catalog:
            logger.warning("🚫 No music tracks available in catalog")
            return None
        
        # Story type to music mapping
        story_preferences = {
            "timeless_retold": {
                "preferred_genres": ["classical", "romantic"],
                "preferred_moods": ["peaceful", "mysterious"],
                "preferred_intensity": ["low", "medium"]
            },
            "minute_myths": {
                "preferred_genres": ["baroque", "classical"],
                "preferred_moods": ["dramatic", "mysterious", "uplifting"],
                "preferred_intensity": ["medium", "high"]
            },
            "flipside": {
                "preferred_genres": ["classical", "romantic"],
                "preferred_moods": ["dramatic", "mysterious"],
                "preferred_intensity": ["medium", "high"]
            }
        }
        
        preferences = story_preferences.get(story_type, {
            "preferred_genres": ["classical"],
            "preferred_moods": ["peaceful"],
            "preferred_intensity": ["low"]
        })
        
        # Score tracks based on preferences
        scored_tracks = []
        for track in self.music_catalog:
            score = 0
            
            # Genre match
            if track.genre in preferences.get("preferred_genres", []):
                score += 3
            
            # Mood match
            target_mood = story_mood if story_mood != "neutral" else "peaceful"
            if track.mood == target_mood:
                score += 2
            elif track.mood in preferences.get("preferred_moods", []):
                score += 1
            
            # Intensity match
            if track.intensity in preferences.get("preferred_intensity", []):
                score += 1
            
            # Duration preference (prefer tracks longer than story)
            if duration_seconds > 0 and track.duration_seconds >= duration_seconds:
                score += 1
            
            scored_tracks.append((track, score))
        
        # Sort by score and add some randomness
        scored_tracks.sort(key=lambda x: x[1], reverse=True)
        
        # Select from top 3 tracks for variety
        top_tracks = [track for track, score in scored_tracks[:3]]
        selected = random.choice(top_tracks) if top_tracks else random.choice(self.music_catalog)
        
        logger.info(f"🎼 Selected: {selected.composer} - {selected.title} for {story_type}")
        return selected
    
    async def mix_audio_with_background(self, voice_audio_path: Union[str, Path], 
                                      background_track: MusicTrack,
                                      output_path: Union[str, Path],
                                      story_type: str = "default") -> Dict:
        """
        Mix voice audio with background music.
        
        Args:
            voice_audio_path: Path to the generated voice audio
            background_track: Selected background music track
            output_path: Where to save the mixed audio
            story_type: Type of story for optimal mixing settings
        """
        
        try:
            logger.info(f"🎧 Mixing {Path(voice_audio_path).name} with {background_track.title}")
            
            # Load audio files
            voice_audio = AudioSegment.from_mp3(str(voice_audio_path))
            background_music = AudioSegment.from_mp3(str(background_track.file_path))
            
            # Normalize voice audio for clarity
            voice_audio = normalize(voice_audio)
            voice_audio = voice_audio + self.voice_boost  # Boost voice
            
            # Prepare background music
            background_music = background_music + self.background_volume  # Reduce volume
            
            # Adjust background music duration to match voice
            voice_duration = len(voice_audio)
            
            if len(background_music) < voice_duration:
                # Loop background music if too short
                loops_needed = (voice_duration // len(background_music)) + 1
                background_music = background_music * loops_needed
            
            # Trim background to match voice duration
            background_music = background_music[:voice_duration]
            
            # Apply fade in/out to background music
            fade_duration = min(self.crossfade_duration, voice_duration // 4)
            background_music = background_music.fade_in(fade_duration).fade_out(fade_duration)
            
            # Mix the audio tracks
            mixed_audio = voice_audio.overlay(background_music)
            
            # Export mixed audio
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            mixed_audio.export(str(output_path), format="mp3", bitrate="192k")
            
            # Calculate statistics
            original_size = Path(voice_audio_path).stat().st_size
            mixed_size = output_path.stat().st_size
            duration_seconds = len(mixed_audio) / 1000.0
            
            logger.info(f"✅ Mixed audio created:")
            logger.info(f"   Output: {output_path}")
            logger.info(f"   Duration: {duration_seconds:.1f} seconds")
            logger.info(f"   Size: {mixed_size} bytes ({mixed_size/original_size:.1%} of original)")
            logger.info(f"   Background: {background_track.composer} - {background_track.title}")
            
            return {
                "success": True,
                "mixed_audio_path": str(output_path),
                "original_audio_path": str(voice_audio_path),
                "background_track": {
                    "title": background_track.title,
                    "composer": background_track.composer,
                    "genre": background_track.genre,
                    "mood": background_track.mood
                },
                "duration_seconds": duration_seconds,
                "file_size_bytes": mixed_size,
                "mixing_settings": {
                    "background_volume_db": self.background_volume,
                    "voice_boost_db": self.voice_boost,
                    "crossfade_ms": fade_duration
                }
            }
            
        except Exception as e:
            logger.error(f"❌ Audio mixing failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "original_audio_path": str(voice_audio_path)
            }
    
    def get_music_recommendations(self) -> Dict[str, List[str]]:
        """Get recommendations for downloading classical music"""
        
        recommendations = {
            "public_domain_sources": [
                "IMSLP (International Music Score Library Project)",
                "Musopen.org - Free classical music",
                "Archive.org Classical Music Collection",
                "Wikipedia Commons Audio",
                "LibriVox Music Section"
            ],
            "recommended_pieces": {
                "Peaceful/Background": [
                    "Bach - Air on the G String",
                    "Pachelbel - Canon in D",
                    "Debussy - Clair de Lune", 
                    "Satie - Gymnopédie No. 1",
                    "Chopin - Nocturnes"
                ],
                "Dramatic/Epic": [
                    "Beethoven - Symphony No. 5",
                    "Wagner - Ride of the Valkyries",
                    "Grieg - In the Hall of the Mountain King",
                    "Tchaikovsky - 1812 Overture",
                    "Vivaldi - Four Seasons (Storm)"
                ],
                "Mysterious/Atmospheric": [
                    "Beethoven - Moonlight Sonata",
                    "Chopin - Funeral March",
                    "Liszt - Liebestraum",
                    "Bach - Toccata and Fugue in D minor",
                    "Mozart - Requiem"
                ]
            },
            "file_format_notes": [
                "Use MP3 format at 192kbps or higher",
                "Ensure consistent volume levels",
                "Prefer longer pieces (3+ minutes) for looping",
                "Avoid pieces with dramatic volume changes"
            ]
        }
        
        return recommendations


async def test_background_music():
    """Test the background music system"""
    
    logging.basicConfig(level=logging.INFO)
    logger.info("🎵 Testing Background Music System")
    
    music_manager = BackgroundMusicManager()
    
    # Test music selection
    for story_type in ["timeless_retold", "minute_myths", "flipside"]:
        selected = music_manager.select_music_for_story(
            story_type=story_type,
            story_mood="peaceful",
            duration_seconds=180
        )
        
        if selected:
            logger.info(f"🎼 {story_type}: {selected.composer} - {selected.title}")
        else:
            logger.info(f"🎼 {story_type}: No music available")
    
    # Show recommendations
    recommendations = music_manager.get_music_recommendations()
    
    logger.info("\n📚 Music Library Recommendations:")
    logger.info("Public Domain Sources:")
    for source in recommendations["public_domain_sources"]:
        logger.info(f"  • {source}")
    
    logger.info("\nRecommended Pieces by Category:")
    for category, pieces in recommendations["recommended_pieces"].items():
        logger.info(f"  {category}:")
        for piece in pieces[:3]:  # Show first 3
            logger.info(f"    • {piece}")


if __name__ == "__main__":
    asyncio.run(test_background_music())