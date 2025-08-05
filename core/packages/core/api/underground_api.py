#!/usr/bin/env python3
"""
Underground Stories API Layer
============================

Central API for integrating Underground Stories backend with Streamlit frontend.
Provides unified interface for all content pipelines and production management.
"""

import json
import time
import asyncio
from typing import Dict, List, Optional, Any, Union
from pathlib import Path
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
import sys
import os
import logging

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

from packages.core.blueprint.blueprint_generator import BlueprintGenerator, CompleteBlueprint
from packages.core.data.data_manager import get_data_manager

# Optional imports - fail gracefully if not available
try:
    from packages.core.youtube.youtube_uploader import YouTubeUploader
    YOUTUBE_AVAILABLE = True
except ImportError:
    YouTubeUploader = None
    YOUTUBE_AVAILABLE = False

try:
    from weekly_production_scheduler import WeeklyProductionScheduler
    SCHEDULER_AVAILABLE = True
except ImportError:
    WeeklyProductionScheduler = None
    SCHEDULER_AVAILABLE = False

# Video generation imports  
try:
    from packages.timeless_retold.video_generator import generate_timeless_video
    from packages.minute_myths.video_generator import generate_minute_myth_video
    VIDEO_GENERATION_AVAILABLE = True
except ImportError:
    VIDEO_GENERATION_AVAILABLE = False

@dataclass
class ProductionStatus:
    """Current production status across all pipelines"""
    current_week: int
    current_story: str
    total_stories: int
    completed_stories: List[str]
    failed_stories: List[str]
    next_scheduled_run: str
    progress_percentage: float
    youtube_connected: bool
    last_generation: Optional[str] = None

@dataclass
class StoryGenerationResult:
    """Result of story generation process"""
    success: bool
    story_title: str
    story_id: Optional[str] = None
    filepath: Optional[str] = None
    word_count: Optional[int] = None
    error: Optional[str] = None
    generation_time: Optional[str] = None

@dataclass
class VideoGenerationResult:
    """Result of video generation process"""
    success: bool
    video_path: Optional[str] = None
    file_size_mb: Optional[float] = None
    duration_seconds: Optional[int] = None
    error: Optional[str] = None
    generation_time: Optional[str] = None

@dataclass
class YouTubeUploadResult:
    """Result of YouTube upload process"""
    success: bool
    video_id: Optional[str] = None
    video_url: Optional[str] = None
    scheduled_time: Optional[str] = None
    error: Optional[str] = None

class UndergroundStoriesAPI:
    """
    Central API for all Underground Stories operations.
    Integrates blueprint generation, story creation, video production, and YouTube publishing.
    """
    
    def __init__(self):
        self.project_root = Path(__file__).parent.parent.parent
        self.data_dir = self.project_root / "data" / "underground_api"
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize components
        self.blueprint_generator = BlueprintGenerator()
        self.data_manager = get_data_manager(use_supabase=False)  # JSON mode for now
        self.youtube_uploader = None
        self.scheduler = None
        
        # Setup logging
        self._setup_logging()
        
        # Initialize YouTube if credentials available
        self._init_youtube()
        
        # Initialize scheduler
        self._init_scheduler()
        
        self.logger.info("🚀 Underground Stories API initialized")
    
    def _setup_logging(self):
        """Setup API logging"""
        log_dir = self.project_root / "logs"
        log_dir.mkdir(exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_dir / f"underground_api_{datetime.now().strftime('%Y%m%d')}.log"),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger("UndergroundAPI")
    
    def _init_youtube(self):
        """Initialize YouTube uploader if credentials available"""
        if not YOUTUBE_AVAILABLE:
            self.logger.info("⚠️ YouTube uploader not available (missing dependencies)")
            self.youtube_uploader = None
            return
            
        try:
            self.youtube_uploader = YouTubeUploader()
            self.logger.info("✅ YouTube API connected")
        except Exception as e:
            self.logger.warning(f"⚠️ YouTube API not available: {e}")
            self.youtube_uploader = None
    
    def _init_scheduler(self):
        """Initialize weekly production scheduler"""
        if not SCHEDULER_AVAILABLE:
            self.logger.info("⚠️ Weekly scheduler not available (missing dependencies)")
            self.scheduler = None
            return
            
        try:
            self.scheduler = WeeklyProductionScheduler()
            self.logger.info("✅ Weekly scheduler initialized")
        except Exception as e:
            self.logger.error(f"❌ Scheduler initialization failed: {e}")
            self.scheduler = None
    
    # ========================================
    # Blueprint Generation APIs
    # ========================================
    
    def generate_blueprint(self, story_concept: str, base_fairy_tale: str = None) -> Dict[str, Any]:
        """
        Generate detailed blueprint from story concept.
        
        Args:
            story_concept: Basic story idea or title
            base_fairy_tale: Optional fairy tale to base it on
            
        Returns:
            Blueprint generation result
        """
        try:
            self.logger.info(f"🎨 Generating blueprint for: {story_concept}")
            
            blueprint = self.blueprint_generator.generate_blueprint_from_concept(
                story_concept, base_fairy_tale
            )
            
            filepath = self.blueprint_generator.save_blueprint(blueprint)
            flipside_format = self.blueprint_generator.export_to_flipside_format(blueprint)
            
            return {
                "success": True,
                "blueprint": asdict(blueprint),
                "filepath": filepath,
                "flipside_format": flipside_format,
                "story_title": blueprint.new.title,
                "genre": blueprint.new.genre,
                "generated_at": blueprint.generated_at
            }
            
        except Exception as e:
            self.logger.error(f"❌ Blueprint generation failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_available_blueprints(self) -> List[Dict[str, Any]]:
        """Get list of all available blueprints"""
        try:
            return self.data_manager.list_blueprints()
        except Exception as e:
            self.logger.error(f"❌ Error getting blueprints: {e}")
            return []
    
    def load_blueprint(self, story_id: int) -> Optional[Dict[str, Any]]:
        """Load specific blueprint by story ID"""
        try:
            return self.data_manager.load_blueprint(story_id)
        except Exception as e:
            self.logger.error(f"❌ Error loading blueprint {story_id}: {e}")
            return None
    
    # ========================================
    # Production Management APIs  
    # ========================================
    
    def get_production_status(self) -> ProductionStatus:
        """Get current production status across all pipelines"""
        try:
            if self.scheduler:
                status = self.scheduler.get_status()
                
                return ProductionStatus(
                    current_week=status["current_week"],
                    current_story=status["current_story"],
                    total_stories=status["total_weeks"],
                    completed_stories=status["completed_stories"],
                    failed_stories=[f["story"] for f in status["failed_stories"]],
                    next_scheduled_run=status["next_scheduled_run"],
                    progress_percentage=status["progress_percentage"],
                    youtube_connected=self.youtube_uploader is not None,
                    last_generation=status["last_generation"]
                )
            else:
                return ProductionStatus(
                    current_week=0,
                    current_story="Not initialized",
                    total_stories=11,
                    completed_stories=[],
                    failed_stories=[],
                    next_scheduled_run="Scheduler not available",
                    progress_percentage=0.0,
                    youtube_connected=self.youtube_uploader is not None
                )
                
        except Exception as e:
            self.logger.error(f"❌ Error getting production status: {e}")
            return ProductionStatus(
                current_week=0,
                current_story="Error",
                total_stories=11,
                completed_stories=[],
                failed_stories=[],
                next_scheduled_run="Error",
                progress_percentage=0.0,
                youtube_connected=False
            )
    
    def trigger_manual_production(self) -> Dict[str, Any]:
        """Trigger manual production run"""
        try:
            if not self.scheduler:
                return {
                    "success": False,
                    "error": "Scheduler not initialized"
                }
            
            self.logger.info("🔧 Running manual production cycle...")
            result = self.scheduler.run_manual_production()
            
            return {
                "success": result.get("overall_success", False),
                "result": result,
                "message": "Manual production completed" if result.get("overall_success") else "Manual production failed"
            }
            
        except Exception as e:
            self.logger.error(f"❌ Manual production failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def generate_single_story_video(self, story_title: str, part: int) -> VideoGenerationResult:
        """Generate single video for testing"""
        try:
            self.logger.info(f"🎬 Generating video: {story_title} Part {part}")
            
            if not VIDEO_GENERATION_AVAILABLE:
                return VideoGenerationResult(
                    success=False,
                    error="Video generation system not available"
                )
            
            # Use scheduler's video generation method if available
            if self.scheduler:
                story_slug = story_title.lower().replace(" ", "-").replace("&", "and")
                output_path = self.project_root / "output" / "test" / f"{story_slug}-part{part}-test.mp4"
                output_path.parent.mkdir(parents=True, exist_ok=True)
                
                success = self.scheduler._generate_single_video(story_title, part, str(output_path))
                
                if success and output_path.exists():
                    file_size = output_path.stat().st_size / 1024 / 1024  # MB
                    
                    return VideoGenerationResult(
                        success=True,
                        video_path=str(output_path),
                        file_size_mb=round(file_size, 2),
                        generation_time=datetime.now().isoformat()
                    )
            
            return VideoGenerationResult(
                success=False,
                error="Video generation failed - scheduler not available"
            )
                
        except Exception as e:
            self.logger.error(f"❌ Video generation failed: {e}")
            return VideoGenerationResult(
                success=False,
                error=str(e)
            )
    
    async def generate_timeless_retold_video(self, book_title: str, chapter_path: str) -> Dict[str, Any]:
        """Generate Timeless Retold video from chapter"""
        try:
            if not VIDEO_GENERATION_AVAILABLE:
                return {
                    "success": False,
                    "error": "Video generation system not available"
                }
            
            self.logger.info(f"🎬 Generating Timeless Retold video: {book_title}")
            
            result = await generate_timeless_video(book_title, chapter_path)
            return result
            
        except Exception as e:
            self.logger.error(f"❌ Timeless Retold video generation failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def generate_minute_myths_video(self, myth_name: str, mythology_category: str, video_format: str, narration_style: str) -> Dict[str, Any]:
        """Generate Minute Myths video"""
        try:
            if not VIDEO_GENERATION_AVAILABLE:
                return {
                    "success": False,
                    "error": "Video generation system not available"
                }
            
            self.logger.info(f"⚡ Generating Minute Myths video: {myth_name}")
            
            result = await generate_minute_myth_video(myth_name, mythology_category, video_format, narration_style)
            return result
            
        except Exception as e:
            self.logger.error(f"❌ Minute Myths video generation failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    # ========================================
    # YouTube Integration APIs
    # ========================================
    
    def test_youtube_connection(self) -> Dict[str, Any]:
        """Test YouTube API connection"""
        try:
            if not self.youtube_uploader:
                return {
                    "connected": False,
                    "error": "YouTube API not initialized"
                }
            
            channel_info = self.youtube_uploader.get_channel_info()
            
            if channel_info:
                return {
                    "connected": True,
                    "channel_info": channel_info
                }
            else:
                return {
                    "connected": False,
                    "error": "Failed to get channel info"
                }
                
        except Exception as e:
            self.logger.error(f"❌ YouTube connection test failed: {e}")
            return {
                "connected": False,
                "error": str(e)
            }
    
    def upload_video_to_youtube(
        self,
        video_path: str,
        title: str,
        description: str,
        tags: List[str],
        privacy_status: str = "private",
        scheduled_time: Optional[datetime] = None
    ) -> YouTubeUploadResult:
        """Upload video to YouTube"""
        try:
            if not self.youtube_uploader:
                return YouTubeUploadResult(
                    success=False,
                    error="YouTube API not initialized"
                )
            
            self.logger.info(f"📤 Uploading to YouTube: {title}")
            
            result = self.youtube_uploader.upload_video(
                video_path=video_path,
                title=title,
                description=description,
                tags=tags,
                pipeline="fairer-tales",
                privacy_status=privacy_status,
                scheduled_time=scheduled_time
            )
            
            if result.get("status") == "success":
                return YouTubeUploadResult(
                    success=True,
                    video_id=result["video_id"],
                    video_url=result["url"],
                    scheduled_time=result.get("scheduled_time")
                )
            else:
                return YouTubeUploadResult(
                    success=False,
                    error=result.get("error", "Upload failed")
                )
                
        except Exception as e:
            self.logger.error(f"❌ YouTube upload failed: {e}")
            return YouTubeUploadResult(
                success=False,
                error=str(e)
            )
    
    # ========================================
    # Content Pipeline APIs
    # ========================================
    
    def get_pipeline_status(self, pipeline: str) -> Dict[str, Any]:
        """Get status of specific content pipeline"""
        try:
            if pipeline == "fairer-tales":
                return self._get_fairer_tales_status()
            elif pipeline == "timeless-retold":
                return self._get_timeless_retold_status()
            elif pipeline == "minute-myths":
                return self._get_minute_myths_status()
            else:
                return {
                    "error": f"Unknown pipeline: {pipeline}"
                }
                
        except Exception as e:
            self.logger.error(f"❌ Error getting pipeline status: {e}")
            return {
                "error": str(e)
            }
    
    def _get_fairer_tales_status(self) -> Dict[str, Any]:
        """Get Fairer Tales pipeline status"""
        production_status = self.get_production_status()
        
        return {
            "pipeline": "fairer-tales",
            "status": "active",
            "current_week": production_status.current_week,
            "current_story": production_status.current_story,
            "total_stories": production_status.total_stories,
            "completed": production_status.completed_stories,
            "failed": production_status.failed_stories,
            "progress": production_status.progress_percentage,
            "next_run": production_status.next_scheduled_run,
            "automation": "weekly_scheduler"
        }
    
    def _get_timeless_retold_status(self) -> Dict[str, Any]:
        """Get Timeless Retold pipeline status"""
        return {
            "pipeline": "timeless-retold", 
            "status": "development",
            "description": "Full book processing system",
            "features": [
                "Book upload and processing",
                "Chapter extraction",
                "Modernization engine",
                "Multi-part audio generation"
            ],
            "implementation_stage": "planning"
        }
    
    def _get_minute_myths_status(self) -> Dict[str, Any]:
        """Get Minute Myths pipeline status"""
        return {
            "pipeline": "minute-myths",
            "status": "development", 
            "description": "Short mythology retellings",
            "features": [
                "Myth database integration",
                "Quick generation system",
                "Cultural research automation",
                "1-minute audio format"
            ],
            "implementation_stage": "planning"
        }
    
    # ========================================
    # Data Management APIs
    # ========================================
    
    def save_session_data(self, session_id: str, data: Dict[str, Any]) -> bool:
        """Save session data for persistence"""
        try:
            return self.data_manager.save_session(session_id, data)
        except Exception as e:
            self.logger.error(f"❌ Error saving session data: {e}")
            return False
    
    def load_session_data(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Load session data"""
        try:
            return self.data_manager.load_session(session_id)
        except Exception as e:
            self.logger.error(f"❌ Error loading session data: {e}")
            return None
    
    def get_system_health(self) -> Dict[str, Any]:
        """Get overall system health status"""
        try:
            return {
                "api_status": "healthy",
                "blueprint_generator": "available",
                "data_manager": "json_mode" if not self.data_manager.use_supabase else "supabase_mode",
                "youtube_api": "connected" if self.youtube_uploader else "disconnected",
                "scheduler": "available" if self.scheduler else "unavailable",
                "project_root": str(self.project_root),
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"❌ Error getting system health: {e}")
            return {
                "api_status": "error",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def create_data_backup(self) -> Dict[str, Any]:
        """Create backup of all system data"""
        try:
            backup_path = self.data_manager.backup_data()
            return {
                "success": True,
                "backup_path": backup_path,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            self.logger.error(f"❌ Error creating backup: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def migrate_to_supabase(self) -> Dict[str, Any]:
        """Migrate data from JSON to Supabase (future implementation)"""
        try:
            if self.data_manager.use_supabase:
                return {
                    "success": False,
                    "error": "Already using Supabase mode"
                }
            
            # This will be implemented when Supabase is reactivated
            success = self.data_manager.migrate_to_supabase()
            return {
                "success": success,
                "message": "Migration to Supabase (placeholder - not yet implemented)",
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            self.logger.error(f"❌ Error migrating to Supabase: {e}")
            return {
                "success": False,
                "error": str(e)
            }

# Singleton instance for Streamlit integration
_api_instance = None

def get_underground_api() -> UndergroundStoriesAPI:
    """Get singleton API instance"""
    global _api_instance
    if _api_instance is None:
        _api_instance = UndergroundStoriesAPI()
    return _api_instance

# Test the API
if __name__ == "__main__":
    api = UndergroundStoriesAPI()
    
    # Test system health
    health = api.get_system_health()
    print(f"🏥 System Health: {health}")
    
    # Test production status
    status = api.get_production_status()
    print(f"📊 Production Status: {asdict(status)}")
    
    # Test blueprint generation
    result = api.generate_blueprint("Test Story")
    print(f"🎨 Blueprint Result: {result['success']}")
    
    print("✅ API test complete!")