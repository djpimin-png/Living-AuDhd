# Living AuDHD YouTube Automation System

Complete Python automation suite for the Living AuDHD YouTube channel.

## Features

### Core Capabilities
- **Video Upload** - Automated uploads with full metadata
- **Scheduling** - Queue and schedule video publishing
- **Analytics** - Track views, likes, comments, engagement
- **Metadata Generation** - AI-optimized titles, descriptions, tags, chapters
- **Spreadsheet Sync** - Auto-sync with Master Dashboard and Topic Database
- **Publishing Queue** - Manage video publishing workflow

## Installation

### Prerequisites
- Python 3.8+
- Google Cloud project with YouTube Data API enabled
- OAuth2 credentials JSON file

### Setup Steps

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/living-audhd.git
cd living-audhd
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up Google OAuth2**
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create new project or select existing
   - Enable YouTube Data API v3
   - Create OAuth2 credentials (Desktop application)
   - Download JSON and save as `credentials.json`

4. **Configure environment**
```bash
cp .env.example .env
# Edit .env with your settings
```

5. **Create logs directory**
```bash
mkdir logs
```

## Usage

### Command Line Interface

```bash
python -m youtube_automation.cli
```

This opens interactive menu with options:
- 📤 Upload Video
- 📅 Schedule Video
- 📊 View Analytics
- 🔧 Generate Metadata
- 📈 Get Channel Stats
- 🎯 View Publishing Queue

### Python API Usage

#### Upload a Video
```python
from youtube_automation.auth import setup_authentication
from youtube_automation.uploader import YouTubeUploader

youtube = setup_authentication()
uploader = YouTubeUploader(youtube)

video_id = uploader.upload_video(
    file_path='video.mp4',
    title='My ADHD Productivity System',
    description='Here\'s how I organize my life...',
    tags=['ADHD', 'Productivity', 'AI'],
    privacy_status='unlisted'
)
```

#### Schedule a Video
```python
from youtube_automation.scheduler import PublishScheduler
from datetime import datetime

scheduler = PublishScheduler()
publish_time = datetime(2024, 7, 15, 12, 0)

scheduler.add_to_queue(
    video_id='abc123',
    title='My Video',
    publish_date=publish_time,
    priority=3
)
```

#### Get Analytics
```python
from youtube_automation.analytics import AnalyticsTracker

analytics = AnalyticsTracker(youtube)

# Get channel stats
channel_stats = analytics.get_channel_analytics()
print(f"Subscribers: {channel_stats['subscribers']:,}")

# Get recent videos
videos = analytics.get_recent_videos(10)
for video in videos:
    analytics.print_stats(video)
```

#### Generate Metadata
```python
from youtube_automation.metadata_generator import MetadataGenerator

generator = MetadataGenerator()

title = generator.optimize_title('ADHD Productivity')
description = generator.generate_description(
    title=title,
    topic='ADHD Systems',
    keywords=['automation', 'productivity', 'ADHD']
)
tags = generator.generate_tags(title, 'ADHD', ['AI', 'automation'])
```

#### Sync to Google Sheets
```python
from youtube_automation.spreadsheet_sync import SpreadsheetSync

sync = SpreadsheetSync(creds)

video_data = {
    'video_id': 'abc123',
    'title': 'My Video',
    'category': 'Productivity',
    'views': 1250,
    'likes': 45,
    'comments': 12
}

sync.append_video_row(
    spreadsheet_id='your_sheet_id',
    sheet_name='Analytics',
    video_data=video_data
)
```

## Configuration

### Environment Variables (.env)

```env
# YouTube API
YOUTUBE_CLIENT_ID=your_client_id
YOUTUBE_CLIENT_SECRET=your_secret

# Google Sheets
MASTER_DASHBOARD_ID=your_sheet_id
TOPIC_DATABASE_ID=your_sheet_id
SEO_LIBRARY_ID=your_sheet_id

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/audhd_automation.log
```

## File Structure

```
living-audhd/
├── youtube_automation/
│   ├── __init__.py
│   ├── auth.py              # OAuth2 authentication
│   ├── uploader.py          # Video upload logic
│   ├── scheduler.py         # Publishing scheduler
│   ├── metadata_generator.py # SEO metadata generation
│   ├── analytics.py         # Analytics tracking
│   ├── spreadsheet_sync.py  # Google Sheets integration
│   └── cli.py               # Command-line interface
├── .env.example             # Environment template
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## Workflow Examples

### Complete Upload + Schedule Workflow
```python
from youtube_automation.auth import setup_authentication
from youtube_automation.uploader import YouTubeUploader
from youtube_automation.scheduler import PublishScheduler
from youtube_automation.metadata_generator import MetadataGenerator
from datetime import datetime

# Setup
youtube = setup_authentication()
uploader = YouTubeUploader(youtube)
scheduler = PublishScheduler()
generator = MetadataGenerator()

# Generate metadata
title = generator.optimize_title('ADHD Productivity Systems')
description = generator.generate_description(
    title, 'ADHD Systems', ['AI', 'Automation', 'Productivity']
)
tags = generator.generate_tags(title, 'ADHD', ['AI'])

# Upload video
video_id = uploader.upload_video(
    file_path='my_video.mp4',
    title=title,
    description=description,
    tags=tags,
    privacy_status='private'
)

# Schedule for publishing
if video_id:
    scheduler.add_to_queue(
        video_id=video_id,
        title=title,
        publish_date=datetime(2024, 7, 20, 12, 0),
        priority=3
    )
```

## Troubleshooting

### Authentication Issues
- Ensure `credentials.json` is in the correct location
- Check that YouTube API is enabled in Google Cloud Console
- Verify OAuth2 scopes include video upload

### Upload Failures
- Check video file format (MP4 recommended)
- Ensure file size < 256GB
- Verify sufficient quota in Google Cloud

### Spreadsheet Sync Issues
- Confirm sheet IDs in .env are correct
- Verify service account has sheet access
- Check sheet tab names match configuration

## Next Steps

### Future Enhancements
- [ ] Batch video processing
- [ ] Automated thumbnail generation
- [ ] AI-powered script generation
- [ ] Advanced analytics dashboard
- [ ] Automatic shorts creation
- [ ] Social media cross-posting
- [ ] Email notification system
- [ ] Dashboard web UI

## Support

For issues or questions:
1. Check logs in `logs/audhd_automation.log`
2. Review error messages in console output
3. Consult YouTube API documentation
4. Open an issue on GitHub

## License

MIT License - See LICENSE file for details

## Author

Living AuDHD Channel Automation System

---

**Happy automating! 🚀**
