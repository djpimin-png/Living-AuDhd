"""
Schedule Uploads Example
Schedule videos for automatic publishing
"""

from youtube_automation.scheduler import PublishScheduler
from datetime import datetime, timedelta
import json

def schedule_videos_from_calendar(calendar_file):
    """
    Load video schedule from JSON calendar file
    
    Args:
        calendar_file: Path to JSON file with schedule
    """
    scheduler = PublishScheduler()
    
    # Load calendar
    with open(calendar_file, 'r') as f:
        calendar = json.load(f)
    
    # Process each scheduled video
    for video in calendar['scheduled_videos']:
        publish_datetime = datetime.fromisoformat(video['publish_date'])
        
        scheduler.add_to_queue(
            video_id=video['video_id'],
            title=video['title'],
            publish_date=publish_datetime,
            priority=video.get('priority', 3)
        )
        
        print(f"Scheduled: {video['title']} for {publish_datetime}")
    
    # Export schedule
    scheduler.export_schedule('schedule_export.json')
    
    # Show upcoming week
    print("\nUpcoming videos (next 7 days):")
    for video in scheduler.get_upcoming_week():
        print(f"  • {video['title']} - {video['publish_date']}")

if __name__ == '__main__':
    schedule_videos_from_calendar('calendar.json')
