# n8n Automation Workflows Setup Guide

## Overview

This folder contains 5 production-ready n8n workflows for automating the Living AuDHD YouTube channel. These workflows integrate with:

- **YouTube API** - Video uploads, publishing, analytics
- **Google Sheets** - Master Dashboard, Topic Database, Analytics tracking
- **OpenAI API** - Content generation (titles, descriptions, tags, scripts)
- **Email** - Notifications and reports

## Workflows Included

### 1. **Video Upload Automation** (`01_Video_Upload_Automation.json`)
**Trigger**: Webhook (manual trigger or external system)  
**Flow**: Upload → Log to Dashboard → Send Notification  
**Features**:
- Accepts video file and metadata
- Uploads to YouTube
- Logs to Master Dashboard
- Sends email confirmation

**Input JSON**:
```json
{
  "file_path": "/videos/my_video.mp4",
  "title": "My ADHD Productivity System",
  "description": "How I manage...",
  "tags": ["ADHD", "Productivity"],
  "category": "ADHD"
}
```

---

### 2. **Scheduled Publishing** (`02_Scheduled_Publishing.json`)
**Trigger**: Every 5 minutes  
**Flow**: Check Queue → Filter Due Videos → Publish → Update Dashboard  
**Features**:
- Automatically publishes videos at scheduled times
- Updates Master Dashboard status
- Sends publish confirmation email
- Queue status reports

**Setup**:
- Add publish schedule to `Publishing Calendar` sheet
- Videos must have `publish_date` column (ISO timestamp)
- Status automatically updates to "published"

---

### 3. **Analytics Sync** (`03_Analytics_Sync.json`)
**Trigger**: Every 1 hour  
**Flow**: Fetch Stats → Process → Update Dashboard → Check Milestones  
**Features**:
- Fetches channel subscribers, total views, video count
- Gets recent 10 videos stats
- Updates Dashboard KPIs in real-time
- Alerts on subscriber milestones (1K, 10K, 100K)
- Hourly sync reports

**Dashboard Updates**:
- Subscribers count → `Dashboard!B2`
- Total videos → `Dashboard!C2`
- Total views → `Dashboard!D2`

---

### 4. **Content Generation** (`04_Content_Generation.json`)
**Trigger**: Webhook (POST request)  
**Flow**: Parse Input → Generate Title/Description/Tags → Save to Library → Notify  
**Features**:
- AI-generated SEO titles (ChatGPT/GPT-4)
- Full YouTube descriptions with formatting
- 25-30 optimized tags
- Saves to SEO Library sheet

**Input JSON**:
```json
{
  "topic": "ADHD Productivity Systems",
  "keywords": "ADHD, AI, automation, productivity",
  "audience": "neurodivergent_creators",
  "style": "conversational"
}
```

**Output**: Saved to `SEO Library` sheet, ready to copy-paste

---

### 5. **Shorts Creator** (`05_Shorts_Creator.json`)
**Trigger**: Webhook (new video uploaded)  
**Flow**: Analyze Video → Generate Titles/Scripts → Create Queue → Publish Daily  
**Features**:
- Extracts 5 Short-worthy segments from long-form videos
- AI-generated hooks and scripts (15-60 seconds)
- Auto-schedules one Short per day for 5 days
- Daily publishing automation
- Tracks Shorts status in dashboard

**Input JSON**:
```json
{
  "video_id": "abc123def456",
  "video_title": "My ADHD Productivity System"
}
```

**Outputs**: 
- 5 Shorts titles with emojis
- 5 ready-to-use scripts
- Automatic scheduling for daily publication

---

## Installation & Setup

### Step 1: Set Up n8n Instance

**Option A: Self-Hosted**
```bash
docker run -it --rm \
  -p 5678:5678 \
  -v ~/.n8n:/home/node/.n8n \
  n8nio/n8n
```
Access at `http://localhost:5678`

**Option B: Cloud (n8n.cloud)**
1. Sign up at https://n8n.cloud
2. Create new account
3. Access dashboard

### Step 2: Set Environment Variables

In n8n Settings → Environment Variables, add:

```env
MASTER_DASHBOARD_ID=your_google_sheet_id
TOPIC_DATABASE_ID=your_google_sheet_id
SEO_LIBRARY_ID=your_google_sheet_id
NOTIFICATION_EMAIL=your_email@gmail.com
YOUTUBE_API_KEY=your_youtube_api_key
OPENAI_API_KEY=your_openai_api_key
CHANNEL_ID=your_channel_id
```

### Step 3: Connect Credentials

**YouTube OAuth2**:
1. Go to Google Cloud Console
2. Create OAuth2 credentials
3. In n8n: Create new credential → YouTube (OAuth2)
4. Authenticate

**Google Sheets**:
1. Create service account in Google Cloud
2. Download credentials JSON
3. In n8n: Create credential → Google Sheets
4. Paste JSON

**OpenAI**:
1. Get API key from https://platform.openai.com/api-keys
2. In n8n: Create credential → OpenAI (API Key)
3. Paste API key

**Email**:
1. In n8n: Create credential → Gmail/SMTP
2. Use your email account credentials

### Step 4: Import Workflows

1. In n8n Dashboard, click **Import Workflow**
2. Select JSON file from `n8n_workflows/` folder
3. Click **Import** (credentials will auto-link if configured)
4. Review and activate

**Import all 5 workflows**:
```bash
# If using CLI:
n8n import:workflow --input 01_Video_Upload_Automation.json
n8n import:workflow --input 02_Scheduled_Publishing.json
n8n import:workflow --input 03_Analytics_Sync.json
n8n import:workflow --input 04_Content_Generation.json
n8n import:workflow --input 05_Shorts_Creator.json
```

### Step 5: Activate Workflows

1. Open each workflow in n8n
2. Click **Activate** (toggle on)
3. Check **Logs** tab for any errors
4. Test with sample data

---

## Workflow Trigger URLs

Once activated, each webhook-triggered workflow has a unique URL:

**Video Upload**:
```
https://[your-n8n-domain]/webhook/upload-trigger
```

**Content Generation**:
```
https://[your-n8n-domain]/webhook/content-generation-trigger
```

**Shorts Creator**:
```
https://[your-n8n-domain]/webhook/shorts-trigger
```

---

## Testing Workflows

### Test Video Upload
```bash
curl -X POST https://[your-n8n-domain]/webhook/upload-trigger \
  -H "Content-Type: application/json" \
  -d '{
    "file_path": "/videos/test.mp4",
    "title": "Test Video",
    "description": "Test description",
    "tags": ["test", "ADHD"],
    "category": "Education"
  }'
```

### Test Content Generation
```bash
curl -X POST https://[your-n8n-domain]/webhook/content-generation-trigger \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "ADHD Time Management",
    "keywords": "time blocking, ADHD, productivity"
  }'
```

### Test Shorts Creator
```bash
curl -X POST https://[your-n8n-domain]/webhook/shorts-trigger \
  -H "Content-Type: application/json" \
  -d '{
    "video_id": "abc123",
    "video_title": "My ADHD System"
  }'
```

---

## Dashboard Integration

All workflows automatically update your Master Dashboard:

| Workflow | Sheet Updated | Data |  
|---|---|---|
| Video Upload | Analytics | video_id, title, status |
| Scheduled Publishing | Publishing Calendar | status → "published" |
| Analytics Sync | Dashboard | subscribers, views, video count |
| Content Generation | SEO Library | title, description, tags |
| Shorts Creator | Shorts | short_id, title, schedule |

---

## Troubleshooting

### Workflows Not Activating
- Check credentials are properly configured
- Verify API keys are valid
- Check n8n logs for error messages

### YouTube Upload Failing
- Verify OAuth2 token hasn't expired
- Check video file format (MP4 recommended)
- Ensure channel quota isn't exceeded

### Google Sheets Not Updating
- Verify sheet ID is correct
- Check service account has edit access
- Verify sheet tab names match workflow ranges

### OpenAI Generation Failing
- Check API key is valid
- Verify account has credits
- Check API usage limits

### Email Notifications Not Sending
- Verify SMTP credentials
- Check email address is valid
- Check Gmail app passwords (if using Gmail)

---

## Advanced Customization

### Modify Publishing Schedule
Edit `02_Scheduled_Publishing.json` → "Filter Due Videos" → Update time logic

### Add More Shorts per Video
Edit `05_Shorts_Creator.json` → "Create Shorts Queue" → Increase loop count

### Change Analytics Sync Interval
Edit `03_Analytics_Sync.json` → "Trigger Hourly" → Change interval

### Custom Email Templates
Edit any email node → Customize subject and textContent

---

## API Rate Limits

- **YouTube API**: 10,000 quota units/day
- **OpenAI API**: Based on plan
- **Google Sheets API**: 500 requests/100 seconds
- **n8n**: Depends on plan

Monitor usage in respective dashboards.

---

## Support

- n8n Docs: https://docs.n8n.io
- YouTube API: https://developers.google.com/youtube
- OpenAI API: https://platform.openai.com/docs
- Google Sheets API: https://developers.google.com/sheets

---

## Next Steps

1. ✅ Import all 5 workflows
2. ✅ Set up credentials
3. ✅ Activate workflows
4. ✅ Test each workflow
5. ✅ Connect to production YouTube channel
6. ✅ Monitor logs and performance

**Your YouTube channel is now automated! 🚀**
