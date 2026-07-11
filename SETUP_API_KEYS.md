# 🔑 API Keys & Credentials Setup Guide

Complete step-by-step guide to obtain all credentials needed for Living AuDHD automation.

---

## 📋 Credentials Checklist

```
Priority 1 (Get First):
☐ OpenAI API Key           (5 min) - For content generation
☐ Google Cloud Project     (10 min) - For YouTube & Sheets
☐ Gmail App Password       (5 min) - For email notifications

Priority 2 (After Testing):
☐ YouTube Data API Key     (5 min) - For video operations
☐ Google Sheets Service Account (10 min) - For Dashboard sync
☐ YouTube Channel ID       (2 min) - Your channel identifier
```

---

## 1️⃣ OpenAI API Key (⏱️ 5 minutes)

### Step 1: Create Account

1. Go to: https://platform.openai.com
2. Click **Sign up**
3. Create account with email
4. Verify email
5. Add phone number (required)

### Step 2: Set Up Billing

1. Go to: https://platform.openai.com/account/billing/overview
2. Click **Set up paid account**
3. Add payment method (credit/debit card)
4. Set usage limits (optional, recommended: $5/month for testing)

⚠️ **Important**: Even with free trial credits, you need a payment method on file.

### Step 3: Generate API Key

1. Go to: https://platform.openai.com/api-keys
2. Click **+ Create new secret key**
3. Choose name: `Living-AuDHD`
4. Click **Create secret key**
5. **Copy immediately** (won't show again!)

```
Example: sk-proj-AbC1234567890DEF...
```

### Step 4: Save Securely

```bash
# Create .env file in your project
echo "OPENAI_API_KEY=sk-proj-YOUR_KEY_HERE" >> .env

# Verify (should show your key)
grep OPENAI .env
```

✅ **Test**: Use this key in n8n to generate content

---

## 2️⃣ Google Cloud Project Setup (⏱️ 10 minutes)

This gives you access to YouTube API and Google Sheets API.

### Step 1: Create Google Cloud Project

1. Go to: https://console.cloud.google.com/
2. Click **Select a Project** (top left)
3. Click **NEW PROJECT**
4. Project name: `Living-AuDHD`
5. Click **CREATE**
6. Wait for project to initialize (1-2 min)

### Step 2: Enable Required APIs

#### Enable YouTube Data API v3

1. Search box: type `YouTube Data API v3`
2. Click **YouTube Data API v3**
3. Click **ENABLE**
4. Wait for enabling (takes ~30 seconds)

#### Enable Google Sheets API

1. Search box: type `Google Sheets API`
2. Click **Google Sheets API**
3. Click **ENABLE**
4. Wait for enabling

#### Enable Google Drive API

1. Search box: type `Google Drive API`
2. Click **Google Drive API**
3. Click **ENABLE**

**Verify**: You should see checkmarks next to all 3 APIs

### Step 3: Create YouTube API Key

1. Go to: https://console.cloud.google.com/apis/credentials
2. Click **+ CREATE CREDENTIALS**
3. Select: **API Key**
4. Copy the key (looks like: `AIzaSyD...`)

```bash
# Add to .env
echo "YOUTUBE_API_KEY=AIzaSyD_YOUR_KEY_HERE" >> .env
```

---

## 3️⃣ YouTube OAuth2 Credentials (⏱️ 10 minutes)

For uploading videos and accessing your channel, you need OAuth2 credentials.

### Step 1: Create OAuth2 Credentials

1. In Google Cloud Console: https://console.cloud.google.com/apis/credentials
2. Click **+ CREATE CREDENTIALS**
3. Select: **OAuth client ID**
4. If prompted: Click **CONFIGURE CONSENT SCREEN**

### Step 2: Configure OAuth Consent Screen

1. Choose: **External**
2. Click **CREATE**

Fill in:
- **App name**: `Living AuDHD`
- **User support email**: your_email@gmail.com
- **Developer contact**: your_email@gmail.com

3. Click **SAVE AND CONTINUE**

Skip scopes section, click **SAVE AND CONTINUE**

Skip test users, click **SAVE AND CONTINUE**

4. Review and click **BACK TO DASHBOARD**

### Step 3: Create OAuth2 Desktop Application

1. Back to Credentials page: https://console.cloud.google.com/apis/credentials
2. Click **+ CREATE CREDENTIALS**
3. Select: **OAuth client ID**
4. Application type: **Desktop application**
5. Name: `Living AuDHD`
6. Click **CREATE**

You'll see a popup with:
- **Client ID**: (copy this)
- **Client Secret**: (copy this)

### Step 4: Download Credentials JSON

1. In Credentials page, find your OAuth2 credential
2. Click the **download icon** (⬇️)
3. Save as: `credentials.json`
4. Move to project root: `living-audhd/credentials.json`

```bash
# Verify file exists
ls -la credentials.json
# Should show: credentials.json (size ~700 bytes)
```

⚠️ **Security**: Never commit `credentials.json` to git!

Add to `.gitignore`:
```bash
echo "credentials.json" >> .gitignore
echo "token.pickle" >> .gitignore
```

---

## 4️⃣ Google Sheets Service Account (⏱️ 10 minutes)

For programmatic access to Google Sheets (Master Dashboard, Topic Database, etc.)

### Step 1: Create Service Account

1. In Google Cloud Console: https://console.cloud.google.com/iam-admin/serviceaccounts
2. Click **CREATE SERVICE ACCOUNT**
3. Service account name: `living-audhd-automation`
4. Service account ID: (auto-filled)
5. Click **CREATE AND CONTINUE**

### Step 2: Grant Permissions

1. Role: Select **Editor** (or **Sheets Editor** for sheets only)
2. Click **CONTINUE**
3. Click **DONE**

### Step 3: Create Key

1. Find the service account you just created
2. Click the email address
3. Go to **KEYS** tab
4. Click **ADD KEY** → **Create new key**
5. Select: **JSON**
6. Click **CREATE**

A JSON file downloads automatically. Save as: `service-account.json`

Move to project:
```bash
mv ~/Downloads/service-account.json living-audhd/
chmod 600 service-account.json
```

### Step 4: Share Sheets with Service Account

1. Open your Master Dashboard Google Sheet
2. Click **Share**
3. In the JSON file, find `"client_email"` value
4. Paste that email in Share dialog
5. Grant **Editor** access
6. Click **Share**

Repeat for:
- Topic Database sheet
- SEO Library sheet
- Analytics sheet

---

## 5️⃣ Gmail App Password (⏱️ 5 minutes)

For sending email notifications.

### Step 1: Enable 2-Factor Authentication

1. Go to: https://myaccount.google.com/security
2. Look for **2-Step Verification**
3. If not enabled:
   - Click **Enable**
   - Follow prompts with phone
   - Verify

### Step 2: Generate App Password

1. Go to: https://myaccount.google.com/apppasswords
2. Select:
   - **Mail**
   - **Windows Computer** (or your device type)
3. Click **GENERATE**
4. Google shows 16-character password

```
Example: abcd efgh ijkl mnop
```

5. Copy immediately (won't show again)

### Step 3: Save App Password

```bash
# Add to .env (remove spaces)
echo "GMAIL_PASSWORD=abcdefghijklmnop" >> .env

# Also add your email
echo "NOTIFICATION_EMAIL=your_email@gmail.com" >> .env
```

---

## 6️⃣ YouTube Channel ID (⏱️ 2 minutes)

Needed to target your specific channel.

### Step 1: Find Channel ID

1. Go to: https://www.youtube.com/@your_channel
2. Click your profile icon → **Settings**
3. Go to **Basic Info** or **Channel**
4. Look for **Channel ID** (starts with UC...)

Or:

1. Go to your channel
2. Right-click → **View page source** (Ctrl+U)
3. Search for: `"channel_id":"UC`
4. Copy the full ID

### Step 2: Save Channel ID

```bash
echo "CHANNEL_ID=UC_YOUR_CHANNEL_ID_HERE" >> .env
```

---

## 7️⃣ Google Sheets ID (⏱️ 2 minutes)

The unique identifier for your Master Dashboard sheet.

### Step 1: Get Sheet ID

1. Open your Master Dashboard in Google Sheets
2. Look at URL: `https://docs.google.com/spreadsheets/d/{SHEET_ID}/edit`
3. Copy the long ID between `/d/` and `/edit`

```
Example: 1A2b3C4d5E6f7G8h9I0j1K2l3M4n5O6p7Q8r9S0t
```

### Step 2: Save to .env

```bash
echo "MASTER_DASHBOARD_ID=1A2b3C4d5E6f7G8h9I0j1K2l3M4n5O6p7Q8r9S0t" >> .env
echo "TOPIC_DATABASE_ID=YOUR_SECOND_SHEET_ID" >> .env
echo "SEO_LIBRARY_ID=YOUR_THIRD_SHEET_ID" >> .env
```

---

## 📝 Complete .env File Template

Create `living-audhd/.env`:

```bash
# OpenAI Configuration
OPENAI_API_KEY=sk-proj-YOUR_OPENAI_KEY_HERE

# YouTube Configuration
YOUTUBE_API_KEY=AIzaSyD_YOUR_YOUTUBE_API_KEY_HERE
CHANNEL_ID=UC_YOUR_CHANNEL_ID_HERE

# Google Sheets Configuration
MASTER_DASHBOARD_ID=1A2b3C4d5E6f7G8h9I0j1K2l3M4n5O6p7Q8r9S0t
TOPIC_DATABASE_ID=1A2b3C4d5E6f7G8h9I0j1K2l3M4n5O6p7Q8r9S0t
SEO_LIBRARY_ID=1A2b3C4d5E6f7G8h9I0j1K2l3M4n5O6p7Q8r9S0t

# Gmail Configuration
NOTIFICATION_EMAIL=your_email@gmail.com
GMAIL_PASSWORD=abcdefghijklmnop

# File Paths
CREDENTIALS_FILE=credentials.json
SERVICE_ACCOUNT_FILE=service-account.json
TOKEN_FILE=token.pickle

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/audhd_automation.log

# n8n Configuration
N8N_HOST=localhost
N8N_PORT=5678
```

---

## ✅ Verification Checklist

After creating all credentials:

```bash
# 1. Check .env file exists
ls -la .env

# 2. Verify OpenAI key works
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer sk-proj-YOUR_KEY_HERE" | head -20

# 3. Verify YouTube API key works
curl "https://www.googleapis.com/youtube/v3/channels?part=statistics&mine=true&key=AIzaSyD_YOUR_KEY_HERE"
# Should return: "error" if not authenticated (expected without OAuth)

# 4. Check credentials.json exists
ls -la credentials.json

# 5. Check service-account.json exists
ls -la service-account.json
```

---

## 🔒 Security Best Practices

### DO:
✅ Store keys in `.env` file (not in code)  
✅ Add `.env` to `.gitignore`  
✅ Use different keys for dev/prod  
✅ Rotate keys periodically  
✅ Set API usage limits  
✅ Use service accounts (not personal account)  

### DON'T:
❌ Commit `.env` to git  
❌ Share API keys  
❌ Use personal Gmail for automation  
❌ Hardcode secrets in code  
❌ Post keys in public issues/forums  

---

## 💸 Cost Estimates

| Service | Free Tier | Typical Monthly |
|---------|-----------|-----------------|
| OpenAI | $5 credits | $5-20 (content generation) |
| YouTube API | 10K units/day | Free (unless >1M calls) |
| Google Sheets | Unlimited | Free |
| Google Cloud | Free tier | Free (under limits) |
| Gmail | Unlimited | Free |

**Total Monthly Cost**: ~$10-20 (mostly OpenAI)

---

## 🚨 Troubleshooting

### "Invalid API Key"
- Verify you copied entire key (including `sk-` prefix)
- Check key hasn't been regenerated
- Verify billing enabled on OpenAI account

### "Unauthorized"
- Verify credentials.json in correct location
- Check service account has sheet access
- Re-authenticate OAuth

### "Rate limit exceeded"
- Lower API call frequency
- Set billing limits in Google Cloud
- Check for infinite loops in workflows

### "Sheet not found"
- Verify sheet ID is correct
- Check service account email is shared on sheet
- Verify sheet tab names match workflow ranges

---

## 📚 Documentation Links

| Service | Documentation |
|---------|---|
| OpenAI | https://platform.openai.com/docs |
| YouTube API | https://developers.google.com/youtube/v3 |
| Google Sheets API | https://developers.google.com/sheets |
| Google Cloud | https://cloud.google.com/docs |
| Gmail API | https://developers.google.com/gmail/api |

---

## ✨ Next Steps

### After Collecting Credentials:

1. ✅ Create `.env` file with all keys
2. ✅ Verify each credential works
3. ✅ Start local n8n: `docker run -it --rm -p 5678:5678 -v ~/.n8n:/home/node/.n8n n8nio/n8n`
4. ✅ Add credentials to n8n Settings → Environment Variables
5. ✅ Test Content Generation workflow
6. ✅ Activate all workflows

### Ready to Deploy:

1. ✅ Test all workflows locally
2. ✅ Export workflows to production
3. ✅ Monitor logs and performance
4. ✅ Start automating your YouTube channel!

---

## 🎯 Time Breakdown

| Task | Duration | Status |
|------|----------|--------|
| OpenAI | 5 min | ⏱️ |
| Google Cloud Project | 10 min | ⏱️ |
| YouTube OAuth | 10 min | ⏱️ |
| Service Account | 10 min | ⏱️ |
| Gmail App Password | 5 min | ⏱️ |
| Channel ID | 2 min | ⏱️ |
| Sheet IDs | 5 min | ⏱️ |
| **Total** | **47 minutes** | ⏱️ |

**Fastest path**: ~30 minutes if you know where to find everything

---

## 🎉 You're Ready!

Once you have all credentials:

1. ✅ You can test n8n locally
2. ✅ You can generate content with AI
3. ✅ You can schedule videos
4. ✅ You can sync analytics
5. ✅ You can automate your entire YouTube workflow

**Next**: Go back to `SETUP_LOCAL_n8n.md` and start testing! 🚀

---

## ❓ Questions?

If you get stuck:

1. Check **Troubleshooting** section above
2. Read the official documentation links
3. Check n8n logs for error messages
4. Review .env file for typos

**You've got this! 💪**
