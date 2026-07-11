"""
YouTube Analytics Module
Fetches and analyzes video performance metrics
"""

import logging
from colorama import Fore, Style
from googleapiclient.errors import HttpError
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class AnalyticsTracker:
    """
    Tracks and reports on video analytics
    """
    
    def __init__(self, youtube_service):
        """
        Initialize analytics tracker
        
        Args:
            youtube_service: Authenticated YouTube API service
        """
        self.youtube = youtube_service
    
    def get_video_stats(self, video_id):
        """
        Get statistics for a specific video
        
        Args:
            video_id: YouTube video ID
        
        Returns:
            Dictionary with view count, likes, comments, etc.
        """
        try:
            request = self.youtube.videos().list(
                part='statistics,snippet',
                id=video_id
            )
            
            response = request.execute()
            
            if response['items']:
                video = response['items'][0]
                stats = {
                    'title': video['snippet']['title'],
                    'views': int(video['statistics'].get('viewCount', 0)),
                    'likes': int(video['statistics'].get('likeCount', 0)),
                    'comments': int(video['statistics'].get('commentCount', 0)),
                    'video_id': video_id,
                }
                
                logger.info(f"Retrieved stats for {video_id}")
                return stats
        
        except HttpError as e:
            print(f"{Fore.RED}✗ Failed to fetch stats: {e}{Style.RESET_ALL}")
            logger.error(f"Analytics error: {e}")
            return None
    
    def get_channel_analytics(self):
        """
        Get channel-level statistics
        
        Returns:
            Dictionary with channel metrics
        """
        try:
            request = self.youtube.channels().list(
                part='statistics,snippet',
                mine=True
            )
            
            response = request.execute()
            
            if response['items']:
                channel = response['items'][0]
                analytics = {
                    'channel_name': channel['snippet']['title'],
                    'subscribers': int(channel['statistics'].get('subscriberCount', 0)),
                    'total_videos': int(channel['statistics'].get('videoCount', 0)),
                    'total_views': int(channel['statistics'].get('viewCount', 0)),
                }
                
                logger.info(f"Retrieved channel analytics")
                return analytics
        
        except HttpError as e:
            print(f"{Fore.RED}✗ Failed to fetch channel analytics: {e}{Style.RESET_ALL}")
            logger.error(f"Channel analytics error: {e}")
            return None
    
    def get_recent_videos(self, max_results=10):
        """
        Get recently uploaded videos
        
        Args:
            max_results: Maximum videos to retrieve
        
        Returns:
            List of recent videos with stats
        """
        try:
            request = self.youtube.search().list(
                part='snippet',
                forMine=True,
                order='date',
                type='video',
                maxResults=max_results
            )
            
            response = request.execute()
            
            videos = []
            for item in response.get('items', []):
                video_id = item['id']['videoId']
                stats = self.get_video_stats(video_id)
                if stats:
                    stats['published_at'] = item['snippet']['publishedAt']
                    videos.append(stats)
            
            logger.info(f"Retrieved {len(videos)} recent videos")
            return videos
        
        except HttpError as e:
            print(f"{Fore.RED}✗ Failed to fetch recent videos: {e}{Style.RESET_ALL}")
            logger.error(f"Recent videos error: {e}")
            return []
    
    def print_stats(self, stats):
        """
        Pretty print video statistics
        
        Args:
            stats: Statistics dictionary
        """
        print(f"\n{Fore.CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Style.RESET_ALL}")
        print(f"{Fore.GREEN}{stats.get('title', 'Video')}{Style.RESET_ALL}")
        print(f"\n📊 Views: {stats.get('views', 0):,}")
        print(f"👍 Likes: {stats.get('likes', 0):,}")
        print(f"💬 Comments: {stats.get('comments', 0):,}")
        
        views = stats.get('views', 1)
        like_rate = (stats.get('likes', 0) / views * 100) if views > 0 else 0
        print(f"\n📈 Like Rate: {like_rate:.2f}%")
        print(f"{Fore.CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Style.RESET_ALL}\n")
