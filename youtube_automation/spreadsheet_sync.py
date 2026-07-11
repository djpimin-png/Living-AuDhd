"""
Google Sheets Integration
Syncs video data with Master Dashboard and Topic Database
"""

import logging
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import pickle
from colorama import Fore, Style

logger = logging.getLogger(__name__)

class SpreadsheetSync:
    """
    Syncs video data with Google Sheets
    """
    
    def __init__(self, creds):
        """
        Initialize sheets sync
        
        Args:
            creds: Google OAuth credentials
        """
        self.sheets = build('sheets', 'v4', credentials=creds)
        self.drive = build('drive', 'v3', credentials=creds)
    
    def append_video_row(self, spreadsheet_id, sheet_name, video_data):
        """
        Append video row to spreadsheet
        
        Args:
            spreadsheet_id: Google Sheets ID
            sheet_name: Sheet name to append to
            video_data: Dictionary with video information
        
        Returns:
            True if successful
        """
        try:
            values = [
                [
                    video_data.get('video_id', ''),
                    video_data.get('title', ''),
                    video_data.get('category', ''),
                    video_data.get('status', 'published'),
                    video_data.get('publish_date', ''),
                    video_data.get('views', 0),
                    video_data.get('likes', 0),
                    video_data.get('comments', 0),
                ]
            ]
            
            body = {'values': values}
            result = self.sheets.spreadsheets().values().append(
                spreadsheetId=spreadsheet_id,
                range=f"{sheet_name}!A:H",
                valueInputOption='USER_ENTERED',
                body=body
            ).execute()
            
            print(f"{Fore.GREEN}✓ Video logged to spreadsheet{Style.RESET_ALL}")
            logger.info(f"Video appended to {sheet_name}")
            return True
        
        except Exception as e:
            print(f"{Fore.RED}✗ Failed to append to spreadsheet: {e}{Style.RESET_ALL}")
            logger.error(f"Spreadsheet error: {e}")
            return False
    
    def update_cell(self, spreadsheet_id, sheet_name, cell_ref, value):
        """
        Update specific cell in spreadsheet
        
        Args:
            spreadsheet_id: Google Sheets ID
            sheet_name: Sheet name
            cell_ref: Cell reference (e.g., 'A1')
            value: Value to set
        
        Returns:
            True if successful
        """
        try:
            range_name = f"{sheet_name}!{cell_ref}"
            values = [[value]]
            body = {'values': values}
            
            self.sheets.spreadsheets().values().update(
                spreadsheetId=spreadsheet_id,
                range=range_name,
                valueInputOption='USER_ENTERED',
                body=body
            ).execute()
            
            logger.info(f"Updated {cell_ref} in {sheet_name}")
            return True
        
        except Exception as e:
            logger.error(f"Update error: {e}")
            return False
    
    def read_sheet(self, spreadsheet_id, sheet_range):
        """
        Read data from spreadsheet
        
        Args:
            spreadsheet_id: Google Sheets ID
            sheet_range: Range to read (e.g., 'Sheet1!A1:Z100')
        
        Returns:
            List of rows
        """
        try:
            result = self.sheets.spreadsheets().values().get(
                spreadsheetId=spreadsheet_id,
                range=sheet_range
            ).execute()
            
            values = result.get('values', [])
            logger.info(f"Read {len(values)} rows from spreadsheet")
            return values
        
        except Exception as e:
            logger.error(f"Read error: {e}")
            return []
    
    def sync_analytics_to_sheet(self, spreadsheet_id, sheet_name, videos):
        """
        Sync analytics data for multiple videos to sheet
        
        Args:
            spreadsheet_id: Google Sheets ID
            sheet_name: Sheet to update
            videos: List of video data dictionaries
        
        Returns:
            True if successful
        """
        try:
            print(f"{Fore.CYAN}Syncing {len(videos)} videos to sheet...{Style.RESET_ALL}")
            
            for video in videos:
                self.append_video_row(spreadsheet_id, sheet_name, video)
            
            print(f"{Fore.GREEN}✓ Analytics synced to spreadsheet{Style.RESET_ALL}")
            logger.info("All analytics synced")
            return True
        
        except Exception as e:
            print(f"{Fore.RED}✗ Sync failed: {e}{Style.RESET_ALL}")
            logger.error(f"Sync error: {e}")
            return False
