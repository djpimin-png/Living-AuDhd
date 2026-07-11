"""
Video Publishing Scheduler
Automates video publishing based on calendar and queue
"""

from datetime import datetime, timedelta
import json
import logging
from colorama import Fore, Style

logger = logging.getLogger(__name__)

class PublishScheduler:
    """
    Manages video publishing schedule
    """
    
    def __init__(self):
        """
        Initialize scheduler
        """
        self.queue = []
        self.published = []
    
    def add_to_queue(self, video_id, title, publish_date, priority=1):
        """
        Add video to publishing queue
        
        Args:
            video_id: YouTube video ID
            title: Video title
            publish_date: datetime object
            priority: Priority level (1-5, higher = earlier)
        """
        item = {
            'video_id': video_id,
            'title': title,
            'publish_date': publish_date.isoformat(),
            'priority': priority,
            'status': 'queued',
            'created_at': datetime.now().isoformat()
        }
        
        self.queue.append(item)
        self.queue.sort(key=lambda x: (-x['priority'], x['publish_date']))
        
        print(f"{Fore.GREEN}✓ Added to queue: {title}{Style.RESET_ALL}")
        logger.info(f"Added to queue: {video_id}")
    
    def get_next_scheduled(self):
        """
        Get next video to publish
        
        Returns:
            Next scheduled video or None
        """
        if not self.queue:
            return None
        
        # Sort by priority and publish date
        pending = [v for v in self.queue if v['status'] == 'queued']
        
        if pending:
            return pending[0]
        
        return None
    
    def get_daily_schedule(self, date):
        """
        Get videos scheduled for specific date
        
        Args:
            date: datetime object
        
        Returns:
            List of videos scheduled for that day
        """
        target_date = date.date()
        scheduled = []
        
        for video in self.queue:
            video_date = datetime.fromisoformat(video['publish_date']).date()
            if video_date == target_date and video['status'] == 'queued':
                scheduled.append(video)
        
        return sorted(scheduled, key=lambda x: (-x['priority'], x['publish_date']))
    
    def mark_published(self, video_id):
        """
        Mark video as published
        
        Args:
            video_id: YouTube video ID
        """
        for video in self.queue:
            if video['video_id'] == video_id:
                video['status'] = 'published'
                video['published_at'] = datetime.now().isoformat()
                self.published.append(video)
                print(f"{Fore.GREEN}✓ Marked as published: {video['title']}{Style.RESET_ALL}")
                logger.info(f"Video published: {video_id}")
                return True
        
        return False
    
    def get_upcoming_week(self):
        """
        Get videos scheduled for upcoming 7 days
        
        Returns:
            List of upcoming videos
        """
        today = datetime.now()
        week_end = today + timedelta(days=7)
        
        upcoming = []
        for video in self.queue:
            if video['status'] == 'queued':
                pub_date = datetime.fromisoformat(video['publish_date'])
                if today <= pub_date <= week_end:
                    upcoming.append(video)
        
        return sorted(upcoming, key=lambda x: x['publish_date'])
    
    def export_schedule(self, filepath):
        """
        Export schedule to JSON file
        
        Args:
            filepath: Path to save schedule
        """
        data = {
            'exported_at': datetime.now().isoformat(),
            'queue': self.queue,
            'published': self.published
        }
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"{Fore.GREEN}✓ Schedule exported: {filepath}{Style.RESET_ALL}")
        logger.info(f"Schedule exported to {filepath}")
    
    def load_schedule(self, filepath):
        """
        Load schedule from JSON file
        
        Args:
            filepath: Path to schedule file
        """
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
            
            self.queue = data.get('queue', [])
            self.published = data.get('published', [])
            
            print(f"{Fore.GREEN}✓ Schedule loaded: {len(self.queue)} items{Style.RESET_ALL}")
            logger.info(f"Loaded {len(self.queue)} scheduled items")
            return True
        
        except Exception as e:
            print(f"{Fore.RED}✗ Failed to load schedule: {e}{Style.RESET_ALL}")
            logger.error(f"Schedule load error: {e}")
            return False
