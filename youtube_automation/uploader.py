"""
YouTube Video Upload Module
Handles automated video uploads with metadata
"""

import os
import time
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from colorama import Fore, Style
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class YouTubeUploader:
    """
    Handles video uploads to YouTube with full metadata
    """
    
    def __init__(self, youtube_service):
        """
        Initialize uploader
        
        Args:
            youtube_service: Authenticated YouTube API service
        """
        self.youtube = youtube_service
    
    def upload_video(self, file_path, title, description, tags, category_id='22',
                    privacy_status='private', playlist_id=None, thumbnail_path=None):
        """
        Upload video to YouTube with metadata
        
        Args:
            file_path: Path to video file
            title: Video title
            description: Video description
            tags: List of tags
            category_id: YouTube category ID (default: 22 = People & Blogs)
            privacy_status: 'public', 'unlisted', or 'private'
            playlist_id: Optional playlist to add video to
            thumbnail_path: Optional custom thumbnail file path
        
        Returns:
            Video ID if successful
        """
        
        if not os.path.exists(file_path):
            print(f"{Fore.RED}✗ File not found: {file_path}{Style.RESET_ALL}")
            logger.error(f"File not found: {file_path}")
            return None
        
        print(f"{Fore.CYAN}Preparing upload: {title}{Style.RESET_ALL}")
        
        # Build request body
        request_body = {
            'snippet': {
                'title': title,
                'description': description,
                'tags': tags if isinstance(tags, list) else tags.split(',')
                'categoryId': str(category_id),
            },
            'status': {
                'privacyStatus': privacy_status,
                'madeForKids': False,
            },
        }
        
        # Build media upload
        media = MediaFileUpload(
            file_path,
            chunksize=1024*1024,  # 1MB chunks
            resumable=True
        )
        
        try:
            # Execute upload
            print(f"{Fore.YELLOW}Uploading video...{Style.RESET_ALL}")
            request = self.youtube.videos().insert(
                part='snippet,status',
                body=request_body,
                media_body=media
            )
            
            response = self._resumable_upload(request)
            video_id = response['id']
            
            print(f"{Fore.GREEN}✓ Video uploaded successfully{Style.RESET_ALL}")
            print(f"{Fore.GREEN}Video ID: {video_id}{Style.RESET_ALL}")
            logger.info(f"Video uploaded: {video_id}")
            
            # Upload thumbnail if provided
            if thumbnail_path:
                self.upload_thumbnail(video_id, thumbnail_path)
            
            # Add to playlist if specified
            if playlist_id:
                self.add_to_playlist(video_id, playlist_id)
            
            return video_id
        
        except HttpError as e:
            print(f"{Fore.RED}✗ Upload failed: {e}{Style.RESET_ALL}")
            logger.error(f"Upload error: {e}")
            return None
    
    def _resumable_upload(self, request, max_retries=5):
        """
        Handle resumable upload with retry logic
        
        Args:
            request: YouTube API request object
            max_retries: Maximum retry attempts
        
        Returns:
            Response object
        """
        response = None
        error = None
        retry = 0
        
        while response is None:
            try:
                status, response = request.next_chunk()
                if status:
                    percent = int(status.progress() * 100)
                    print(f"{Fore.CYAN}Upload progress: {percent}%{Style.RESET_ALL}", end='\r')
            
            except HttpError as e:
                if e.resp.status in [500, 502, 503, 504]:
                    error = e
                    retry += 1
                    if retry < max_retries:
                        print(f"\n{Fore.YELLOW}Retry {retry}/{max_retries}...{Style.RESET_ALL}")
                        time.sleep(2 ** retry)
                    else:
                        raise
                else:
                    raise
        
        print()  # New line after progress
        return response
    
    def upload_thumbnail(self, video_id, thumbnail_path):
        """
        Upload custom thumbnail for video
        
        Args:
            video_id: YouTube video ID
            thumbnail_path: Path to thumbnail file
        
        Returns:
            True if successful
        """
        if not os.path.exists(thumbnail_path):
            print(f"{Fore.YELLOW}⚠ Thumbnail not found: {thumbnail_path}{Style.RESET_ALL}")
            return False
        
        try:
            print(f"{Fore.CYAN}Uploading thumbnail...{Style.RESET_ALL}")
            
            media = MediaFileUpload(
                thumbnail_path,
                mimetype='image/jpeg',
                chunksize=-1,
                resumable=False
            )
            
            request = self.youtube.thumbnails().set(
                videoId=video_id,
                media_body=media
            )
            
            request.execute()
            print(f"{Fore.GREEN}✓ Thumbnail uploaded{Style.RESET_ALL}")
            logger.info(f"Thumbnail uploaded for {video_id}")
            return True
        
        except HttpError as e:
            print(f"{Fore.YELLOW}⚠ Thumbnail upload failed: {e}{Style.RESET_ALL}")
            logger.warning(f"Thumbnail upload error: {e}")
            return False
    
    def add_to_playlist(self, video_id, playlist_id):
        """
        Add video to playlist
        
        Args:
            video_id: YouTube video ID
            playlist_id: Playlist ID to add to
        
        Returns:
            True if successful
        """
        try:
            print(f"{Fore.CYAN}Adding to playlist...{Style.RESET_ALL}")
            
            request = self.youtube.playlistItems().insert(
                part='snippet',
                body={
                    'snippet': {
                        'playlistId': playlist_id,
                        'resourceId': {
                            'kind': 'youtube#video',
                            'videoId': video_id
                        }
                    }
                }
            )
            
            request.execute()
            print(f"{Fore.GREEN}✓ Added to playlist{Style.RESET_ALL}")
            logger.info(f"Video {video_id} added to playlist {playlist_id}")
            return True
        
        except HttpError as e:
            print(f"{Fore.YELLOW}⚠ Playlist add failed: {e}{Style.RESET_ALL}")
            logger.warning(f"Playlist error: {e}")
            return False
    
    def schedule_publish(self, video_id, publish_time):
        """
        Schedule video for future publishing
        
        Args:
            video_id: YouTube video ID
            publish_time: datetime object for publication
        
        Returns:
            True if successful
        """
        try:
            print(f"{Fore.CYAN}Scheduling publish: {publish_time}{Style.RESET_ALL}")
            
            request = self.youtube.videos().update(
                part='status',
                body={
                    'id': video_id,
                    'status': {
                        'privacyStatus': 'private',
                        'publishAt': publish_time.isoformat() + 'Z'
                    }
                }
            )
            
            request.execute()
            print(f"{Fore.GREEN}✓ Scheduled for {publish_time}{Style.RESET_ALL}")
            logger.info(f"Video {video_id} scheduled for {publish_time}")
            return True
        
        except HttpError as e:
            print(f"{Fore.RED}✗ Scheduling failed: {e}{Style.RESET_ALL}")
            logger.error(f"Scheduling error: {e}")
            return False
