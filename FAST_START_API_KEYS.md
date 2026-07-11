# ⚡ FASTEST PATH: Get API Keys in 30 Minutes

**Streamlined guide to collect all credentials in the shortest time possible.**

---

## 📊 Credential Priority Matrix

```
MUST HAVE (Testing Starts):
1. OpenAI API Key           ← Start HERE (5 min)
2. Gmail App Password       ← Then THIS (5 min)

THEN CAN TEST:
3. Google Cloud Project     ← Then THIS (10 min)

THEN FULL AUTOMATION:
4-7. YouTube + Sheets       ← Complete these (15 min total)
```

**Total: ~30 minutes to first working test**

---

## 🟢 STEP 1: OpenAI API Key (5 minutes)

### 1.1 Create Account
```
Go to: https://platform.openai.com
Click: Sign up
Complete: Email verification + phone number
```

### 1.2 Add Payment Method
```
Go to: https://platform.openai.com/account/billing/overview
Click: Set up paid account
Add: Credit/debit card
Budget: Set to $5 (optional, but recommended)
```

**⚠️ You need a payment method even with free credits**

### 1.3 Generate Key
```
Go to: https://platform.openai.com/api-keys
Click: + Create new secret key
Name: Living-AuDHD
Copy: The key immediately (won't show again!)
Example: sk-proj-AbC1234567890DEF...
```

### 1.4 Save It
```bash
# Create .env file
cat > .env << 'EOF'
OPENAI_API_KEY=sk-proj-YOUR_KEY_HERE
EOF

# Verify
cat .env
```

**✅ DONE - You can now test content generation!**

---

## 🟢 STEP 2: Gmail App Password (5 minutes)

### 2.1 Enable 2-Factor Auth
```
Go to: https://myaccount.google.com/security
Look for: 2-Step Verification
If not enabled:
  - Click Enable
  - Follow prompts with phone
```

### 2.2 Get App Password
```
Go to: https://myaccount.google.com/apppasswords
Select: Mail + Windows Computer (or your device)
Click: GENERATE
Copy: 16-character password (remove spaces)
Example: abcd efgh ijkl mnop  →  abcdefghijklmnop
```

### 2.3 Save It
```bash
# Add to .env
cat >> .env << 'EOF'
NOTIFICATION_EMAIL=your_email@gmail.com
GMAIL_PASSWORD=abcdefghijklmnop
EOF

# Verify
cat .env
```

**✅ DONE - Email notifications ready!**

---

## 🟡 STEP 3: Google Cloud Project (10 minutes)

### 3.1 Create Project
```
Go to: https://console.cloud.google.com/
Click: Select a Project (top left)
Click: NEW PROJECT
Name: Living-AuDHD
Click: CREATE
Wait: ~1 minute for initialization
```

### 3.2 Enable APIs (3 APIs, 1 minute each)

**Enable YouTube Data API v3:**
```
Search: YouTube Data API v3
Click: Result
Click: ENABLE
Wait: 30 seconds
```

**Enable Google Sheets API:**
```
Search: Google Sheets API
Click: Result
Click: ENABLE
```

**Enable Google Drive API:**
```
Search: Google Drive API
Click: Result
Click: ENABLE
```

### 3.3 Create API Key
```
Go to: https://console.cloud.google.com/apis/credentials
Click: + CREATE CREDENTIALS
Select: API Key
Copy: The key (AIzaSyD_...)
```

### 3.4 Save It
```bash
cat >> .env << 'EOF'
YOUTUBE_API_KEY=AIzaSyD_YOUR_KEY_HERE
EOF
```

**✅ DONE - YouTube API ready!**

---

## 🟠 STEP 4: YouTube OAuth2 Credentials (10 minutes)

### 4.1 Configure OAuth Consent
```
Go to: https://console.cloud.google.com/apis/credentials
Click: + CREATE CREDENTIALS
Select: OAuth client ID
If prompted: Click CONFIGURE CONSENT SCREEN
```

**Configure Screen:**
```
Choose: External
Click: CREATE
Fill in:
  - App name: Living AuDHD
  - User support email: your_email@gmail.com
  - Developer contact: your_email@gmail.com
Click: SAVE AND CONTINUE
Skip scopes: Click SAVE AND CONTINUE
Skip users: Click SAVE AND CONTINUE
Review: Click BACK TO DASHBOARD
```

### 4.2 Create OAuth2 Credentials
```
Go to: https://console.cloud.google.com/apis/credentials
Click: + CREATE CREDENTIALS
Select: OAuth client ID
Application type: Desktop application
Name: Living AuDHD
Click: CREATE
```

**You'll see a popup with:**
```
Client ID: (copy this)
Client Secret: (copy this)
```

### 4.3 Download JSON
```
In Credentials page, find your OAuth2 credential
Click: Download icon (⬇️)
Save as: credentials.json
Move to: living-audhd/credentials.json
```

### 4.4 Secure It
```bash
# Add to .gitignore
echo "credentials.json" >> .gitignore
echo "token.pickle" >> .gitignore

# Verify file
ls -la credentials.json
```

**✅ DONE - YouTube auth ready!**

---

## 🟠 STEP 5: Service Account (10 minutes)

### 5.1 Create Service Account
```
Go to: https://console.cloud.google.com/iam-admin/serviceaccounts
Click: CREATE SERVICE ACCOUNT
Service account name: living-audhd-automation
Service account ID: (auto-filled)
Click: CREATE AND CONTINUE
```

### 5.2 Grant Permissions
```
Role: Select Editor
Click: CONTINUE
Click: DONE
```

### 5.3 Create Key
```
Find: Your service account in the list
Click: Its email address
Go to: KEYS tab
Click: ADD KEY → Create new key
Select: JSON
Click: CREATE
(JSON file downloads automatically)
```

### 5.4 Move File
```bash
mv ~/Downloads/service-account.json living-audhd/
chmod 600 service-account.json
ls -la service-account.json
```

**✅ DONE - Sheets automation ready!**

---

## 🔵 STEP 6: Get IDs (5 minutes)

### 6.1 YouTube Channel ID
```
Go to: https://www.youtube.com/@your_channel
Click: Profile icon → Settings
Look for: Channel ID (starts with UC...)
Copy it
```

**Or (if above doesn't work):**
```
Go to: Your channel
Right-click: View page source (Ctrl+U)
Search: "channel_id":"UC
Copy: The full ID
```

### 6.2 Get Sheet IDs
```
For each of your Google Sheets:
  1. Open the sheet
  2. Look at URL: docs.google.com/spreadsheets/d/{SHEET_ID}/edit
  3. Copy the long ID between /d/ and /edit
  4. Save it
```

### 6.3 Save All IDs
```bash
cat >> .env << 'EOF'
CHANNEL_ID=UC_YOUR_CHANNEL_ID_HERE
MASTER_DASHBOARD_ID=1A2b3C4d5E6f7G8h9I0j1K2l3M4n5O6p7Q8r9S0t
TOPIC_DATABASE_ID=1A2b3C4d5E6f7G8h9I0j1K2l3M4n5O6p7Q8r9S0t
SEO_LIBRARY_ID=1A2b3C4d5E6f7G8h9I0j1K2l3M4n5O6p7Q8r9S0t
EOF
```

**✅ DONE - IDs configured!**

---

## 🟣 STEP 7: Share Sheets with Service Account (5 minutes)

### 7.1 Get Service Account Email
```bash
# Extract from the JSON file
grep "client_email" service-account.json
# Output: "client_email": "living-audhd@project.iam.gserviceaccount.com"
# Copy the email address
```

### 7.2 Share Each Sheet
```
For EACH sheet (Dashboard, Database, Library):
  1. Open the sheet
  2. Click Share
  3. Paste service account email
  4. Grant: Editor access
  5. Click Share
  6. Close
```

**✅ DONE - Service account has access!**

---

## 📋 Final .env File

```bash
# Your complete .env should look like:

# OpenAI
OPENAI_API_KEY=sk-proj-YOUR_KEY_HERE

# YouTube
YOUTUBE_API_KEY=AIzaSyD_YOUR_KEY_HERE
CHANNEL_ID=UC_YOUR_CHANNEL_ID_HERE

# Google Sheets
MASTER_DASHBOARD_ID=1A2b3C4d5E6f7G8h9I0j1K2l3M4n5O6p7Q8r9S0t
TOPIC_DATABASE_ID=1A2b3C4d5E6f7G8h9I0j1K2l3M4n5O6p7Q8r9S0t
SEO_LIBRARY_ID=1A2b3C4d5E6f7G8h9I0j1K2l3M4n5O6p7Q8r9S0t

# Gmail
NOTIFICATION_EMAIL=your_email@gmail.com
GMAIL_PASSWORD=abcdefghijklmnop

# Files
CREDENTIALS_FILE=credentials.json
SERVICE_ACCOUNT_FILE=service-account.json
```

---

## ✅ Verification (2 minutes)

### Check Files
```bash
# Verify files exist
ls -la .env
ls -la credentials.json
ls -la service-account.json
ls -la .gitignore
```

### Check .env Content
```bash
# Should show all variables
cat .env

# Count lines (should be ~10+)
wc -l .env
```

### Test OpenAI Key
```bash
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer $(grep OPENAI_API_KEY .env | cut -d'=' -f2)" | head

# Should return: {"object":"list","data":[...
```

**✅ ALL CREDENTIALS READY!**

---

## 🎯 Time Breakdown

```
Step 1: OpenAI              5 min
Step 2: Gmail              5 min
Step 3: Google Cloud       10 min
Step 4: YouTube OAuth      10 min
Step 5: Service Account    10 min
Step 6: Get IDs            5 min
Step 7: Share Sheets       5 min
─────────────────────────────────
TOTAL:                     50 min

But if you're fast:        ~30 min
```

---

## 🚀 Next: Start Testing!

Once you have .env file:

```bash
# 1. Start n8n
docker run -it --rm -p 5678:5678 -v ~/.n8n:/home/node/.n8n n8nio/n8n

# 2. Open browser
# http://localhost:5678

# 3. Follow: SETUP_LOCAL_n8n.md
# Steps 1-6 (about 15 minutes)

# 4. Test Content Generation
# curl -X POST http://localhost:5678/webhook/content-generation-trigger \
#   -H "Content-Type: application/json" \
#   -d '{"topic": "ADHD Productivity", "keywords": "AI, automation"}'

# ✅ You'll get AI-generated metadata in seconds!
```

---

## 🔒 Security Checklist

```
✅ Added .env to .gitignore
✅ Never committed .env to git
✅ credentials.json is secure (chmod 600)
✅ service-account.json is secure (chmod 600)
✅ All API keys unique
✅ No secrets in code
✅ Payment method added for OpenAI
```

---

## ❌ Common Mistakes (Avoid These!)

```
❌ Committing .env to git
❌ Forgetting to add payment method to OpenAI
❌ Not sharing sheets with service account
❌ Typos in API keys
❌ Using personal email for automation
❌ Copying key with extra spaces
❌ Forgetting file permissions (chmod 600)
```

---

## ✨ Success Indicators

```
✅ .env file created with all variables
✅ credentials.json in project root
✅ service-account.json in project root
✅ All files in .gitignore
✅ OpenAI test passed
✅ Google Sheets shared with service account
✅ Ready to test n8n!
```

---

## 📞 If You Get Stuck

**Common Issues:**

| Problem | Solution |
|---------|----------|
| "Invalid API Key" | Copy entire key including `sk-` prefix |
| "Unauthorized" | Re-verify service account email |
| "Sheet not found" | Check sheet ID is correct (between /d/ and /edit) |
| "2-factor not enabled" | Enable it at myaccount.google.com/security |
| "App password not working" | Ensure spaces removed from password |

---

## 🎉 You're Done!

**You now have:**
- ✅ OpenAI API for content generation
- ✅ Gmail setup for notifications
- ✅ Google Cloud Project configured
- ✅ YouTube API enabled
- ✅ OAuth2 credentials downloaded
- ✅ Service account created
- ✅ All sheet IDs configured
- ✅ All credentials saved to .env

**Next Step:** Open `SETUP_LOCAL_n8n.md` and start testing! 🚀

---

## 📊 What You Can Do After This

```
Immediately (Right Now):
✅ Test content generation with AI

After Getting YouTube Credentials:
✅ Upload videos to YouTube
✅ Schedule publishing
✅ Track analytics
✅ Create Shorts automatically

Full Automation:
✅ Everything automated 24/7
✅ YouTube running on autopilot
✅ Emails on key milestones
✅ Dashboard always updated
```

---

**Ready to get your credentials? Start with Step 1! ⏱️**
