"""
Living AuDHD YouTube Automation System
Setup and Installation Script
"""

from setuptools import setup, find_packages

setup(
    name="living-audhd-youtube-automation",
    version="1.0.0",
    description="Complete YouTube automation system for Living AuDHD channel",
    author="Living AuDHD",
    packages=find_packages(),
    install_requires=[
        "google-auth-oauthlib==1.1.0",
        "google-auth-httplib2==0.2.0",
        "google-api-python-client==2.100.0",
        "python-dotenv==1.0.0",
        "openpyxl==3.10.0",
        "requests==2.31.0",
        "python-dateutil==2.8.2",
        "colorama==0.4.6",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "audhd-youtube=youtube_automation.cli:main",
        ],
    },
)
