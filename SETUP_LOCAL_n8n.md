# 🚀 Local n8n Setup Guide for Living AuDHD

Complete step-by-step guide to set up n8n locally with all 5 automation workflows.

## Prerequisites

- Docker installed: https://docs.docker.com/get-docker/
- Docker Compose (usually included with Docker Desktop)
- Port 5678 available (n8n default)
- Text editor for `.env` files

---

## Step 1: Start n8n with Docker

### Option A: Simple (Recommended for Testing)

```bash
docker run -it --rm \
  -p 5678:5678 \
  -v ~/.n8n:/home/node/.n8n \
  n8nio/n8n
```

**Output**:
```
n8n ready on http://localhost:5678
```

### Option B: Docker Compose (Persistent)

Create `docker-compose.yml`:

```yaml
version: '3'

services:
  n8n:
    image: n8nio/n8n
    ports:
      - "5678:5678"
    environment:
      - N8N_HOST=localhost
      - N8N_PORT=5678
      - N8N_PROTOCOL=http
      - NODE_ENV=production
      - GENERIC_TIMEZONE=America/Chicago
    volumes:
      - n8n_data:/home/node/.n8n
    networks:
      - n8n-network

volumes:
  n8n_data:

networks:
  n8n-network:
    driver: bridge
```

Start:
```bash
docker-compose up -d
# Check logs
docker-compose logs -f
```

---

## Step 2: Access n8n Web Interface

1. Open browser: **http://localhost:5678**
2. First time setup:
   - Create admin user
   - Set username/password
   - Complete setup wizard

3. You should see dashboard with **Create Workflow** button

---

## Step 3: Set Environment Variables

### In n8n Settings

1. Click **Settings** (gear icon, bottom left)
2. Click **Environment Variables**
3. Click **New** for each variable:

```
Name: MASTER_DASHBOARD_ID
Value: (leave empty for now, add later)

Name: OPENAI_API_KEY
Value: (leave empty for now)

Name: YOUTUBE_API_KEY
Value: (leave empty for now)

Name: NOTIFICATION_EMAIL
Value: your_email@gmail.com

Name: CHANNEL_ID
Value: (leave empty for now)
```

Click **Save** after each entry.

---

## Step 4: Import First Workflow (Test)

We'll start with **Content Generation** (doesn't need YouTube API for testing).

### 4.1 Download Workflow File

```bash
# From your living-audhd repo:
cd n8n_workflows
# Copy the JSON file content
```

### 4.2 Import in n8n

1. Click **+ New** → **Create from file**
2. Select: `04_Content_Generation.json`
3. Click **Import**

You'll see the workflow with these nodes:
- Webhook Trigger
- Parse Input
- Generate Title (GPT-4)
- Generate Description (GPT-4)
- Generate Tags (GPT-4)
- Combine Metadata
- Save to SEO Library
- Return Generated Metadata
- Send Notification

---

## Step 5: Connect OpenAI (For AI Testing)

### 5.1 Get OpenAI API Key

1. Go to: https://platform.openai.com/api-keys
2. Click **+ Create new secret key**
3. Copy the key (looks like: `sk-...`)
4. Click **Save** (you won't see it again)

### 5.2 Add Credential in n8n

1. In workflow, find **Generate Title** node
2. Click **+ Add New Credential**
3. Select **OpenAI**
4. Paste API key
5. Click **Create & Select**

Repeat for **Generate Description** and **Generate Tags** nodes.

---

## Step 6: Test Content Generation Workflow

### 6.1 Configure Webhook

1. In workflow editor, click **Webhook** node
2. In right panel, copy the **Webhook URL**
   - Format: `http://localhost:5678/webhook/...`

### 6.2 Activate Workflow

1. Click **Activate** toggle (top right)
2. Turn it **ON**
3. You should see: **Workflow is active**

### 6.3 Test with cURL

```bash
# Copy your webhook URL and paste below:
WEBHOOK_URL="http://localhost:5678/webhook/..."

curl -X POST $WEBHOOK_URL \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "ADHD Productivity Systems",
    "keywords": "time blocking, AI tools, automation"
  }'
```

**Expected Response**:
```json
{
  "title": "How to Build Your ADHD Productivity System",
  "description": "In this video, we explore ADHD Productivity Systems...",
  "tags": ["ADHD", "Productivity", "Time Management", ...],
  "generated_at": "2026-07-11T21:30:45.123Z"
}
```

### 6.4 Check Execution

1. Click **Executions** tab
2. You should see your test run
3. Look for **Success** status (green checkmark)
4. Click on execution to see output

---

## Step 7: Import Analytics Workflow (No Credentials Needed Yet)

Now import **03_Analytics_Sync.json**:

1. Click **+ New** → **Create from file**
2. Select: `03_Analytics_Sync.json`
3. Click **Import**

This workflow runs on a **timer** (every 1 hour):
- Fetches YouTube channel stats
- Updates Dashboard
- Checks for milestones

**Note**: Will fail without YouTube API credentials (that's OK for now).

---

## Step 8: Set Up Email Notifications (Optional)

To actually receive emails:

### 8.1 Gmail Setup

1. Go to: https://myaccount.google.com/apppasswords
2. Select **Mail** and **Windows Computer** (or your device)
3. Copy the **16-character password**

### 8.2 Add Email Credential in n8n

1. In any workflow, find **Send Notification** email node
2. Click **+ Add New Credential**
3. Select **Gmail (SMTP)**
4. Enter:
   - **Email**: your_email@gmail.com
   - **Password**: 16-char app password from step 1
5. Click **Create & Select**

---

## Step 9: Import All 5 Workflows

Now import remaining workflows one by one:

```
✓ 04_Content_Generation.json (done)
✓ 03_Analytics_Sync.json (done)
- 01_Video_Upload_Automation.json
- 02_Scheduled_Publishing.json  
- 05_Shorts_Creator.json
```

For each:
1. Click **+ New** → **Create from file**
2. Select JSON file
3. Click **Import**
4. Review structure
5. **Don't activate yet** (missing YouTube credentials)

---

## Step 10: View All Workflows

Click **Workflows** (left sidebar) to see all imported:

```
📋 Workflows
├── Living AuDHD - Video Upload Automation
├── Living AuDHD - Scheduled Publishing
├── Living AuDHD - Analytics Sync
├── Living AuDHD - Content Generation      ✓ ACTIVE
└── Living AuDHD - Shorts Creator
```

---

## 🧪 Testing Scenarios

### Scenario 1: Generate Metadata (WORKS NOW)

```bash
curl -X POST http://localhost:5678/webhook/content-generation-trigger \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "ADHD Meeting Strategies",
    "keywords": "meetings, communication, ADHD workplace"
  }'
```

✅ **Result**: Get AI-generated title, description, 30 tags

---

### Scenario 2: Schedule Publishing (Needs YouTube)

1. In `02_Scheduled_Publishing.json`, click **Activate**
2. Workflow runs every 5 minutes
3. Checks `Publishing Calendar` sheet in Google Sheets
4. Publishes due videos

**To test**: Need Google Sheets + YouTube API configured

---

### Scenario 3: Video Upload (Needs YouTube)

1. In `01_Video_Upload_Automation.json`, click **Activate**
2. Send webhook request with video file
3. Uploads to YouTube
4. Updates Dashboard

**To test**: Need YouTube OAuth + Google Sheets configured

---

## 📊 n8n Dashboard Overview

```
Left Sidebar:
├── Dashboard (home)
├── Workflows (all imported)
├── Executions (run history)
├── Settings
└── Documentation

Top Right:
├── Help (?)
├── Settings (gear)
└── User menu
```

---

## 🔍 Debugging

### View Workflow Logs

1. Open workflow
2. Click **Executions** tab
3. Click on any execution to expand
4. See input/output for each node
5. Scroll down to see **error messages**

### Common Errors

**"Invalid API Key"**
- Verify OpenAI key is correct
- Check in OpenAI dashboard usage

**"Unauthorized"**
- YouTube credentials expired
- Re-authenticate

**"Sheet not found"**
- Verify sheet ID in environment variables
- Check sheet exists in Google Drive

---

## 🚀 Next Steps

### After Local Testing

1. **Test all 5 workflows** with sample data
2. **Check execution logs** for any issues
3. **Verify email notifications** work
4. **Add YouTube credentials** (when ready)
5. **Test with production YouTube channel** (optional)

### Go to Production

1. Set up cloud n8n: https://n8n.cloud
2. Export workflows from local
3. Import to cloud instance
4. Configure credentials
5. Activate all workflows

---

## 📞 Troubleshooting

### Docker Issues

**Container won't start**:
```bash
# Check port availability
lsof -i :5678

# Stop container
docker stop <container_id>

# Try different port
docker run -it --rm -p 5679:5678 n8nio/n8n
```

**Can't access interface**:
- Try: http://localhost:5678
- Check docker logs: `docker logs <container_id>`
- Verify port 5678 not blocked by firewall

### n8n Issues

**Workflows not executing**:
1. Check workflow is **Activated** (toggle on)
2. Check for error messages in Executions
3. Review node configuration

**Credentials not working**:
1. Re-authenticate
2. Check environment variables set
3. Verify API keys valid

---

## 📋 Quick Reference

| Task | Steps |
|------|-------|
| Start n8n | `docker run ... n8nio/n8n` |
| Access | http://localhost:5678 |
| Import workflow | **+ New** → **Create from file** |
| Activate workflow | Click **Activate** toggle |
| Test webhook | `curl -X POST <URL>` |
| View logs | Click **Executions** tab |
| Add credential | Click node → **+ Add New Credential** |

---

## ✅ Setup Complete!

When you see all 5 workflows in your Workflows list and Content Generation test succeeds, you're ready!

**Next**: Add YouTube & Google Sheets credentials to activate all workflows.

---

## 📚 Resources

- n8n Docs: https://docs.n8n.io
- n8n Community: https://community.n8n.io
- YouTube API Docs: https://developers.google.com/youtube
- OpenAI API Docs: https://platform.openai.com/docs

---

**Your local n8n automation hub is ready! 🎉**
