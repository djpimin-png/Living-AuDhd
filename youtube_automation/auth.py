"""
YouTube API Authentication Module
Handles OAuth2 setup and token management
"""

import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from colorama import Fore, Style
import logging

logger = logging.getLogger(__name__)

# YouTube API scopes
SCOPES = [
    'https://www.googleapis.com/auth/youtube.upload',
    'https://www.googleapis.com/auth/youtube',
    'https://www.googleapis.com/auth/youtube.readonly',
]

class YouTubeAuthenticator:
    """
    Handles YouTube API authentication and token refresh
    """
    
    def __init__(self, credentials_file='credentials.json', token_file='token.pickle'):
        """
        Initialize authenticator
        
        Args:
            credentials_file: Path to OAuth2 credentials JSON
            token_file: Path to store/retrieve OAuth token
        """
        self.credentials_file = credentials_file
        self.token_file = token_file
        self.creds = None
    
    def authenticate(self):
        """
        Authenticate with YouTube API
        Returns valid credentials object
        """
        # Load existing token
        if os.path.exists(self.token_file):
            print(f"{Fore.CYAN}Loading existing token...{Style.RESET_ALL}")
            with open(self.token_file, 'rb') as token:
                self.creds = pickle.load(token)
                logger.info("Loaded existing credentials")
        
        # Refresh token if expired
        if self.creds and self.creds.expired and self.creds.refresh_token:
            print(f"{Fore.YELLOW}Refreshing expired token...{Style.RESET_ALL}")
            self.creds.refresh(Request())
            logger.info("Token refreshed")
        
        # Request new credentials if needed
        if not self.creds or not self.creds.valid:
            if not os.path.exists(self.credentials_file):
                raise FileNotFoundError(
                    f"{Fore.RED}credentials.json not found!{Style.RESET_ALL}\n"
                    "Please download OAuth2 credentials from Google Cloud Console."
                )
            
            print(f"{Fore.CYAN}Starting OAuth2 flow...{Style.RESET_ALL}")
            flow = InstalledAppFlow.from_client_secrets_file(
                self.credentials_file, SCOPES)
            self.creds = flow.run_local_server(port=8080)
            logger.info("New credentials obtained")
            
            # Save token for future use
            with open(self.token_file, 'wb') as token:
                pickle.dump(self.creds, token)
                print(f"{Fore.GREEN}Token saved for future use{Style.RESET_ALL}")
        
        print(f"{Fore.GREEN}✓ Authentication successful{Style.RESET_ALL}")
        return self.creds

def setup_authentication():
    """
    Main authentication setup function
    Returns YouTube API service object
    """
    from googleapiclient.discovery import build
    
    authenticator = YouTubeAuthenticator()
    creds = authenticator.authenticate()
    
    youtube = build('youtube', 'v3', credentials=creds)
    logger.info("YouTube API service created")
    
    return youtube
