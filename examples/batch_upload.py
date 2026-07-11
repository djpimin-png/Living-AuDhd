"""
Batch Upload Example
Process and upload multiple videos from a folder
"""

import os
from youtube_automation.auth import setup_authentication
from youtube_automation.uploader import YouTubeUploader
from youtube_automation.metadata_generator import MetadataGenerator

def batch_upload_videos(videos_folder, metadata_file=None):
    """
    Upload all videos from a folder
    
    Args:
        videos_folder: Path to folder containing video files
        metadata_file: Optional JSON file with video metadata
    """
    # Setup
    youtube = setup_authentication()
    uploader = YouTubeUploader(youtube)
    generator = MetadataGenerator()
    
    # Load metadata if provided
    metadata_map = {}
    if metadata_file:
        import json
        with open(metadata_file, 'r') as f:
            metadata_map = json.load(f)
    
    # Process each video
    video_files = [f for f in os.listdir(videos_folder) if f.endswith('.mp4')]
    
    print(f"Found {len(video_files)} videos to upload")
    
    for video_file in video_files:
        video_path = os.path.join(videos_folder, video_file)
        video_name = os.path.splitext(video_file)[0]
        
        # Get metadata
        if video_name in metadata_map:
            meta = metadata_map[video_name]
            title = meta.get('title', video_name)
            description = meta.get('description', '')
            tags = meta.get('tags', [])
        else:
            title = video_name
            description = f"Video: {video_name}"
            tags = ['Living AuDHD']
        
        # Upload
        print(f"\nUploading: {title}")
        video_id = uploader.upload_video(
            file_path=video_path,
            title=title,
            description=description,
            tags=tags,
            privacy_status='private'
        )
        
        if video_id:
            print(f"Success! Video ID: {video_id}")
        else:
            print(f"Failed to upload {video_file}")

if __name__ == '__main__':
    # Example usage
    batch_upload_videos(
        videos_folder='./videos',
        metadata_file='./metadata.json'
    )
