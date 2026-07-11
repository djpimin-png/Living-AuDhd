#!/usr/bin/env python3
"""
Create Google Sheets for Living AuDHD Automation
Run this script to automatically create Master Dashboard, Topic Database, and SEO Library sheets
"""

from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import json

# Configuration
SERVICE_ACCOUNT_FILE = 'service-account.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']

# Sheet configurations
SHEETS_TO_CREATE = [
    {
        'title': 'Living AuDHD - Master Dashboard',
        'tabs': ['Dashboard', 'Analytics', 'Publishing Calendar', 'Shorts']
    },
    {
        'title': 'Living AuDHD - Topic Database',
        'tabs': ['Topics', 'Keywords', 'Ideas', 'Research']
    },
    {
        'title': 'Living AuDHD - SEO Library',
        'tabs': ['SEO Library', 'Titles', 'Descriptions', 'Tags']
    }
]

def create_sheets():
    """Create all sheets and add tabs"""
    
    # Authenticate
    print("🔐 Authenticating with Google...")
    creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    sheets_service = build('sheets', 'v4', credentials=creds)
    drive_service = build('drive', 'v3', credentials=creds)
    
    sheet_ids = {}
    
    for sheet_config in SHEETS_TO_CREATE:
        print(f"\n📊 Creating: {sheet_config['title']}")
        
        # Create spreadsheet
        spreadsheet_body = {
            'properties': {
                'title': sheet_config['title']
            },
            'sheets': [
                {'properties': {'title': tab}} for tab in sheet_config['tabs']
            ]
        }
        
        spreadsheet = sheets_service.spreadsheets().create(
            body=spreadsheet_body,
            fields='spreadsheetId'
        ).execute()
        
        sheet_id = spreadsheet.get('spreadsheetId')
        sheet_ids[sheet_config['title']] = sheet_id
        
        print(f"   ✅ Created: {sheet_id}")
        print(f"   🔗 URL: https://docs.google.com/spreadsheets/d/{sheet_id}/edit")
        
        # Make it editable by the service account (it already is, but just in case)
        try:
            drive_service.permissions().create(
                fileId=sheet_id,
                body={
                    'kind': 'drive#permission',
                    'role': 'editor',
                    'type': 'serviceAccount'
                }
            ).execute()
            print(f"   ✅ Service account granted access")
        except:
            pass  # Already has access
    
    return sheet_ids

def save_sheet_ids_to_env(sheet_ids):
    """Save sheet IDs to .env file"""
    
    env_content = ""
    
    # Map titles to env variable names
    mapping = {
        'Living AuDHD - Master Dashboard': 'MASTER_DASHBOARD_ID',
        'Living AuDHD - Topic Database': 'TOPIC_DATABASE_ID',
        'Living AuDHD - SEO Library': 'SEO_LIBRARY_ID'
    }
    
    print("\n" + "="*50)
    print("📝 Add these to your .env file:")
    print("="*50)
    
    for title, env_var in mapping.items():
        if title in sheet_ids:
            sheet_id = sheet_ids[title]
            env_line = f"{env_var}={sheet_id}"
            env_content += env_line + "\n"
            print(env_line)
    
    print("\n" + "="*50)
    print("Or run this to append to .env:")
    print("="*50)
    print(f"""cat >> .env << 'EOF'
{env_content}EOF""")
    
    return env_content

if __name__ == '__main__':
    try:
        print("🚀 Living AuDHD - Google Sheets Creator\n")
        sheet_ids = create_sheets()
        save_sheet_ids_to_env(sheet_ids)
        print("\n✅ All sheets created successfully!")
        print("\n📝 Now add the sheet IDs to your .env file")
        
    except FileNotFoundError:
        print("❌ Error: service-account.json not found!")
        print("Make sure service-account.json is in the current directory")
    except Exception as e:
        print(f"❌ Error: {e}")
