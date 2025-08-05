"""
YouTube API Integration for Underground Stories
Automated video uploading with metadata, thumbnails, and scheduling.
"""

import os
import json
import pickle
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

class YouTubeUploader:
    """
    Handles YouTube API operations for Underground Stories video uploads.
    
    Features:
    - OAuth2 authentication with token refresh
    - Video upload with metadata (title, description, tags, thumbnail)
    - Scheduled publishing with release dates
    - Playlist management for series organization
    - Error handling and retry logic
    - Batch operations for multiple videos
    """
    
    # YouTube API scopes
    SCOPES = [
        'https://www.googleapis.com/auth/youtube.upload',
        'https://www.googleapis.com/auth/youtube',
        'https://www.googleapis.com/auth/youtube.force-ssl'
    ]
    
    def __init__(self, credentials_path: str = "config/youtube-credentials.json"):
        """
        Initialize YouTube uploader.
        
        Args:
            credentials_path: Path to YouTube API credentials JSON file
        """
        self.credentials_path = Path(credentials_path)
        self.token_path = Path("config/youtube-token.pickle")
        self.service = None
        
        # Underground Stories channel configuration
        self.channel_config = {
            'fairer-tales': {
                'playlist_title': 'Underground Stories: Fairer Tales',
                'category_id': '24',  # Entertainment
                'default_language': 'en',
                'default_region': 'US'
            },
            'timeless-retold': {
                'playlist_title': 'Underground Stories: Timeless Retold',
                'category_id': '24',
                'default_language': 'en',
                'default_region': 'US'
            },
            'minute-myths': {
                'playlist_title': 'Underground Stories: Minute Myths',
                'category_id': '24',
                'default_language': 'en',
                'default_region': 'US'
            }
        }
        
        self.authenticate()
    
    def authenticate(self) -> None:
        """
        Authenticate with YouTube API using OAuth2.
        Handles token refresh and initial authentication flow.
        """
        creds = None
        
        # Load existing token
        if self.token_path.exists():
            with open(self.token_path, 'rb') as token:
                creds = pickle.load(token)
        
        # If no valid credentials, authenticate
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                    print("✅ YouTube API token refreshed successfully")
                except Exception as e:
                    print(f"⚠️ Token refresh failed: {e}")
                    creds = None
            
            if not creds:
                if not self.credentials_path.exists():
                    raise FileNotFoundError(
                        f"YouTube API credentials not found at {self.credentials_path}. "
                        "Please download from Google Cloud Console."
                    )
                
                flow = InstalledAppFlow.from_client_secrets_file(
                    str(self.credentials_path), self.SCOPES
                )
                creds = flow.run_local_server(port=0)
                print("✅ YouTube API authentication completed")
            
            # Save credentials for next run
            with open(self.token_path, 'wb') as token:
                pickle.dump(creds, token)
        
        # Build YouTube service
        self.service = build('youtube', 'v3', credentials=creds)
        print("✅ YouTube API service initialized")
    
    def upload_video(
        self,
        video_path: str,
        title: str,
        description: str,
        tags: List[str],
        pipeline: str,
        thumbnail_path: Optional[str] = None,
        privacy_status: str = 'private',
        scheduled_time: Optional[datetime] = None,
        playlist_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Upload video to YouTube with full metadata.
        
        Args:
            video_path: Path to video file
            title: Video title
            description: Video description
            tags: List of tags
            pipeline: Pipeline name (fairer-tales, etc.)
            thumbnail_path: Optional custom thumbnail
            privacy_status: 'private', 'unlisted', 'public'
            scheduled_time: Future datetime for scheduled publishing
            playlist_id: Add to specific playlist
            
        Returns:
            Dict with video ID, URL, and upload status
        """
        try:
            video_path = Path(video_path)
            if not video_path.exists():
                raise FileNotFoundError(f"Video file not found: {video_path}")
            
            # Prepare video metadata
            snippet = {
                'title': title,
                'description': description,
                'tags': tags,
                'categoryId': self.channel_config[pipeline]['category_id'],
                'defaultLanguage': self.channel_config[pipeline]['default_language']
            }
            
            status = {
                'privacyStatus': privacy_status,
                'selfDeclaredMadeForKids': False
            }
            
            # Handle scheduled publishing
            if scheduled_time and privacy_status == 'private':
                status['publishAt'] = scheduled_time.isoformat() + 'Z'
                status['privacyStatus'] = 'private'  # Will auto-publish at scheduled time
            
            body = {
                'snippet': snippet,
                'status': status
            }
            
            # Create media upload
            media = MediaFileUpload(
                str(video_path), 
                chunksize=-1, 
                resumable=True,
                mimetype='video/*'
            )
            
            print(f"🎬 Uploading video: {title}")
            print(f"📁 File: {video_path.name} ({video_path.stat().st_size / 1024 / 1024:.1f}MB)")
            
            # Execute upload
            insert_request = self.service.videos().insert(
                part=','.join(body.keys()),
                body=body,
                media_body=media
            )
            
            response = self._resumable_upload(insert_request)
            video_id = response['id']
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            
            print(f"✅ Video uploaded successfully!")
            print(f"🆔 Video ID: {video_id}")
            print(f"🔗 URL: {video_url}")
            
            # Upload custom thumbnail if provided
            if thumbnail_path and Path(thumbnail_path).exists():
                self._upload_thumbnail(video_id, thumbnail_path)
            
            # Add to playlist if specified
            if playlist_id:
                self._add_to_playlist(video_id, playlist_id)
            
            return {
                'video_id': video_id,
                'url': video_url,
                'title': title,
                'upload_time': datetime.now().isoformat(),
                'scheduled_time': scheduled_time.isoformat() if scheduled_time else None,
                'privacy_status': privacy_status,
                'status': 'success'
            }
            
        except HttpError as e:
            error_msg = f"YouTube API error: {e}"
            print(f"❌ {error_msg}")
            return {
                'status': 'error',
                'error': error_msg,
                'title': title
            }
        except Exception as e:
            error_msg = f"Upload error: {e}"
            print(f"❌ {error_msg}")
            return {
                'status': 'error',
                'error': error_msg,
                'title': title
            }
    
    def _resumable_upload(self, insert_request) -> Dict[str, Any]:
        """
        Handle resumable upload with progress tracking.
        """
        response = None
        error = None
        retry = 0
        
        while response is None:
            try:
                status, response = insert_request.next_chunk()
                if status:
                    progress = int(status.progress() * 100)
                    print(f"📤 Upload progress: {progress}%")
            except HttpError as e:
                if e.resp.status in [500, 502, 503, 504]:
                    # Retriable errors
                    retry += 1
                    if retry > 3:
                        raise e
                    print(f"⚠️ Retriable error {e.resp.status}, retrying...")
                    continue
                else:
                    raise e
        
        return response
    
    def _upload_thumbnail(self, video_id: str, thumbnail_path: str) -> bool:
        """
        Upload custom thumbnail for video.
        """
        try:
            thumbnail_path = Path(thumbnail_path)
            if not thumbnail_path.exists():
                print(f"⚠️ Thumbnail not found: {thumbnail_path}")
                return False
            
            media = MediaFileUpload(str(thumbnail_path), mimetype='image/*')
            
            self.service.thumbnails().set(
                videoId=video_id,
                media_body=media
            ).execute()
            
            print(f"✅ Thumbnail uploaded: {thumbnail_path.name}")
            return True
            
        except Exception as e:
            print(f"⚠️ Thumbnail upload failed: {e}")
            return False
    
    def _add_to_playlist(self, video_id: str, playlist_id: str) -> bool:
        """
        Add video to specified playlist.
        """
        try:
            body = {
                'snippet': {
                    'playlistId': playlist_id,
                    'resourceId': {
                        'kind': 'youtube#video',
                        'videoId': video_id
                    }
                }
            }
            
            self.service.playlistItems().insert(
                part='snippet',
                body=body
            ).execute()
            
            print(f"✅ Added to playlist: {playlist_id}")
            return True
            
        except Exception as e:
            print(f"⚠️ Playlist addition failed: {e}")
            return False
    
    def create_playlist(self, title: str, description: str, privacy: str = 'public') -> str:
        """
        Create a new playlist.
        
        Returns:
            Playlist ID
        """
        try:
            body = {
                'snippet': {
                    'title': title,
                    'description': description
                },
                'status': {
                    'privacyStatus': privacy
                }
            }
            
            response = self.service.playlists().insert(
                part='snippet,status',
                body=body
            ).execute()
            
            playlist_id = response['id']
            print(f"✅ Playlist created: {title} (ID: {playlist_id})")
            return playlist_id
            
        except Exception as e:
            print(f"❌ Playlist creation failed: {e}")
            raise e
    
    def batch_upload(
        self,
        videos: List[Dict[str, Any]],
        pipeline: str,
        delay_between_uploads: int = 60
    ) -> List[Dict[str, Any]]:
        """
        Upload multiple videos with delay between uploads.
        
        Args:
            videos: List of video metadata dicts
            pipeline: Pipeline name
            delay_between_uploads: Seconds between uploads
            
        Returns:
            List of upload results
        """
        results = []
        
        for i, video_data in enumerate(videos):
            print(f"\n📤 Uploading video {i+1}/{len(videos)}")
            
            result = self.upload_video(
                video_path=video_data['video_path'],
                title=video_data['title'],
                description=video_data['description'],
                tags=video_data['tags'],
                pipeline=pipeline,
                thumbnail_path=video_data.get('thumbnail_path'),
                privacy_status=video_data.get('privacy_status', 'private'),
                scheduled_time=video_data.get('scheduled_time'),
                playlist_id=video_data.get('playlist_id')
            )
            
            results.append(result)
            
            # Delay between uploads to avoid rate limits
            if i < len(videos) - 1:
                print(f"⏳ Waiting {delay_between_uploads}s before next upload...")
                import time
                time.sleep(delay_between_uploads)
        
        return results
    
    def get_channel_info(self) -> Dict[str, Any]:
        """
        Get authenticated channel information.
        """
        try:
            response = self.service.channels().list(
                part='snippet,statistics,contentDetails',
                mine=True
            ).execute()
            
            if response['items']:
                channel = response['items'][0]
                return {
                    'channel_id': channel['id'],
                    'title': channel['snippet']['title'],
                    'subscriber_count': channel['statistics']['subscriberCount'],
                    'video_count': channel['statistics']['videoCount'],
                    'view_count': channel['statistics']['viewCount']
                }
        except Exception as e:
            print(f"❌ Failed to get channel info: {e}")
            return {}
    
    def schedule_series_release(
        self,
        videos: List[Dict[str, Any]],
        start_date: datetime,
        release_pattern: List[int]  # Days of week: [0=Monday, 1=Tuesday, etc.]
    ) -> List[Dict[str, Any]]:
        """
        Schedule a series release with specific pattern.
        
        Args:
            videos: List of video metadata
            start_date: First release date
            release_pattern: Days of week for releases (e.g., [0, 2, 4] for Mon/Wed/Fri)
            
        Returns:
            Updated video list with scheduled times
        """
        scheduled_videos = []
        current_date = start_date
        
        for video in videos:
            # Find next valid release day
            while current_date.weekday() not in release_pattern:
                current_date += timedelta(days=1)
            
            video_copy = video.copy()
            video_copy['scheduled_time'] = current_date.replace(hour=9, minute=0, second=0)  # 9 AM release
            scheduled_videos.append(video_copy)
            
            # Move to next week for next video
            current_date += timedelta(days=1)
            while current_date.weekday() not in release_pattern:
                current_date += timedelta(days=1)
        
        return scheduled_videos

# Helper function for easy usage
def create_youtube_uploader() -> YouTubeUploader:
    """
    Create YouTubeUploader instance with standard configuration.
    """
    return YouTubeUploader()

if __name__ == "__main__":
    # Test authentication
    uploader = YouTubeUploader()
    channel_info = uploader.get_channel_info()
    print(f"✅ Connected to channel: {channel_info.get('title', 'Unknown')}")