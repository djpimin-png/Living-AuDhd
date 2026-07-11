"""
Command-line Interface
Main entry point for YouTube automation
"""

import os
import sys
import logging
from datetime import datetime
from colorama import Fore, Style, init
from dotenv import load_dotenv

from .auth import setup_authentication
from .uploader import YouTubeUploader
from .scheduler import PublishScheduler
from .metadata_generator import MetadataGenerator
from .analytics import AnalyticsTracker
from .spreadsheet_sync import SpreadsheetSync

# Initialize colorama
init(autoreset=True)

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(
    level=os.getenv('LOG_LEVEL', 'INFO'),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.getenv('LOG_FILE', 'logs/audhd_automation.log')),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def print_header():
    """
    Print welcome header
    """
    print(f"""
{Fore.CYAN}╔════════════════════════════════════════════════════╗{Style.RESET_ALL}
{Fore.CYAN}║     Living AuDHD YouTube Automation System          ║{Style.RESET_ALL}
{Fore.CYAN}║     Version 1.0.0                                   ║{Style.RESET_ALL}
{Fore.CYAN}╚════════════════════════════════════════════════════╝{Style.RESET_ALL}
    """)

def show_menu():
    """
    Display main menu
    """
    print(f"""{Fore.YELLOW}
📺 YOUTUBE AUTOMATION MENU
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{Style.RESET_ALL}
1. 📤 Upload Video
2. 📅 Schedule Video
3. 📊 View Analytics
4. 🔧 Generate Metadata
5. 📈 Get Channel Stats
6. 🎯 View Publishing Queue
7. ⚙️  Settings
8. ❌ Exit

{Fore.YELLOW}Select an option (1-8):{Style.RESET_ALL} """)

def upload_video(uploader):
    """
    Interactive video upload
    """
    print(f"{Fore.CYAN}\n📤 VIDEO UPLOAD{Style.RESET_ALL}")
    print("="*50)
    
    file_path = input(f"{Fore.YELLOW}Video file path: {Style.RESET_ALL}")
    title = input(f"{Fore.YELLOW}Video title: {Style.RESET_ALL}")
    description = input(f"{Fore.YELLOW}Description: {Style.RESET_ALL}")
    tags = input(f"{Fore.YELLOW}Tags (comma-separated): {Style.RESET_ALL}").split(',')
    privacy = input(f"{Fore.YELLOW}Privacy (public/unlisted/private): {Style.RESET_ALL}") or 'private'
    
    print(f"\n{Fore.CYAN}Processing upload...{Style.RESET_ALL}")
    video_id = uploader.upload_video(
        file_path=file_path,
        title=title,
        description=description,
        tags=tags,
        privacy_status=privacy
    )
    
    if video_id:
        print(f"\n{Fore.GREEN}✓ Upload complete!{Style.RESET_ALL}")
        print(f"{Fore.GREEN}Video ID: {video_id}{Style.RESET_ALL}")
        logger.info(f"Upload completed: {video_id}")

def schedule_video(scheduler):
    """
    Interactive video scheduling
    """
    print(f"{Fore.CYAN}\n📅 SCHEDULE VIDEO{Style.RESET_ALL}")
    print("="*50)
    
    video_id = input(f"{Fore.YELLOW}Video ID: {Style.RESET_ALL}")
    title = input(f"{Fore.YELLOW}Video title: {Style.RESET_ALL}")
    date_str = input(f"{Fore.YELLOW}Publish date (YYYY-MM-DD): {Style.RESET_ALL}")
    time_str = input(f"{Fore.YELLOW}Publish time (HH:MM): {Style.RESET_ALL}") or "12:00"
    priority = int(input(f"{Fore.YELLOW}Priority (1-5): {Style.RESET_ALL}") or "3")
    
    try:
        publish_datetime = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
        scheduler.add_to_queue(video_id, title, publish_datetime, priority)
        print(f"\n{Fore.GREEN}✓ Video scheduled!{Style.RESET_ALL}")
        logger.info(f"Scheduled: {title}")
    except ValueError:
        print(f"{Fore.RED}✗ Invalid date/time format{Style.RESET_ALL}")

def view_analytics(analytics):
    """
    View channel analytics
    """
    print(f"{Fore.CYAN}\n📊 ANALYTICS{Style.RESET_ALL}")
    print("="*50)
    
    channel_stats = analytics.get_channel_analytics()
    if channel_stats:
        print(f"\n{Fore.GREEN}Channel: {channel_stats['channel_name']}{Style.RESET_ALL}")
        print(f"Subscribers: {channel_stats['subscribers']:,}")
        print(f"Total Videos: {channel_stats['total_videos']}")
        print(f"Total Views: {channel_stats['total_views']:,}")
    
    print(f"\n{Fore.CYAN}Recent Videos:{Style.RESET_ALL}")
    videos = analytics.get_recent_videos(5)
    for video in videos:
        analytics.print_stats(video)

def generate_metadata():
    """
    Generate video metadata
    """
    print(f"{Fore.CYAN}\n🔧 GENERATE METADATA{Style.RESET_ALL}")
    print("="*50)
    
    generator = MetadataGenerator()
    
    topic = input(f"{Fore.YELLOW}Video topic: {Style.RESET_ALL}")
    keywords = input(f"{Fore.YELLOW}Keywords (comma-separated): {Style.RESET_ALL}").split(',')
    
    title = generator.optimize_title(topic)
    description = generator.generate_description(title, topic, keywords)
    tags = generator.generate_tags(title, topic, keywords)
    
    print(f"\n{Fore.GREEN}Generated Metadata:{Style.RESET_ALL}")
    print(f"\n📌 Title:\n{title}")
    print(f"\n📝 Description:\n{description[:200]}...")
    print(f"\n🏷️  Tags ({len(tags)}):\n{', '.join(tags)}")

def main():
    """
    Main CLI application loop
    """
    print_header()
    
    try:
        # Setup authentication
        print(f"{Fore.CYAN}Setting up authentication...{Style.RESET_ALL}")
        youtube = setup_authentication()
        
        # Initialize components
        uploader = YouTubeUploader(youtube)
        scheduler = PublishScheduler()
        analytics = AnalyticsTracker(youtube)
        metadata = MetadataGenerator()
        
        logger.info("Application started")
        
        # Main loop
        while True:
            try:
                show_menu()
                choice = input().strip()
                
                if choice == '1':
                    upload_video(uploader)
                elif choice == '2':
                    schedule_video(scheduler)
                elif choice == '3':
                    view_analytics(analytics)
                elif choice == '4':
                    generate_metadata()
                elif choice == '5':
                    stats = analytics.get_channel_analytics()
                    if stats:
                        analytics.print_stats(stats)
                elif choice == '6':
                    upcoming = scheduler.get_upcoming_week()
                    if upcoming:
                        print(f"\n{Fore.CYAN}Upcoming Videos (7 days):{Style.RESET_ALL}")
                        for video in upcoming:
                            print(f"  • {video['title']} - {video['publish_date']}")
                    else:
                        print(f"{Fore.YELLOW}No videos scheduled{Style.RESET_ALL}")
                elif choice == '7':
                    print(f"{Fore.CYAN}Settings (not yet implemented){Style.RESET_ALL}")
                elif choice == '8':
                    print(f"{Fore.GREEN}Thank you for using Living AuDHD Automation!{Style.RESET_ALL}")
                    logger.info("Application closed")
                    sys.exit(0)
                else:
                    print(f"{Fore.RED}Invalid option{Style.RESET_ALL}")
            
            except KeyboardInterrupt:
                print(f"\n{Fore.YELLOW}Exit (Ctrl+C){Style.RESET_ALL}")
                sys.exit(0)
            except Exception as e:
                print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
                logger.error(f"Error: {e}", exc_info=True)
    
    except Exception as e:
        print(f"{Fore.RED}Fatal error: {e}{Style.RESET_ALL}")
        logger.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)

if __name__ == '__main__':
    main()
