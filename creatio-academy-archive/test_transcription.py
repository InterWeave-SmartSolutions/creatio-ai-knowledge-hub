#!/usr/bin/env python3
"""
Test script to transcribe a few videos first to validate the workflow
"""

import json
import subprocess
import logging
from pathlib import Path
from transcribe_videos import (
    setup_directories, download_video, extract_audio, transcribe_audio,
    create_transcript_index, sanitize_filename
)

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_transcription(max_videos=3):
    """Test transcription with a limited number of videos"""
    logger.info(f"Testing transcription workflow with {max_videos} videos")
    
    # Setup directories
    setup_directories()
    
    # Load video index
    with open('video_index.json', 'r', encoding='utf-8') as f:
        video_index = json.load(f)
    
    # Process only the first few videos
    processed_count = 0
    for file_key, video_data in list(video_index.items())[:max_videos]:
        metadata = video_data.get('metadata', {})
        title = metadata.get('title', f'Video {file_key}')
        videos = video_data.get('videos', [])
        
        if not videos:
            logger.warning(f"No videos found for: {title}")
            continue
        
        logger.info(f"\nTesting with: {title}")
        video_url = videos[0]
        
        # Download video
        video_path = download_video(video_url, 'videos/downloaded', title)
        if not video_path:
            logger.error(f"Failed to download video for: {title}")
            continue
        
        # Extract audio
        audio_path = extract_audio(video_path, 'audio_extracted')
        if not audio_path:
            logger.error(f"Failed to extract audio for: {title}")
            continue
        
        # Transcribe
        transcript_data = transcribe_audio(
            audio_path, 'transcripts/text', 'transcripts/json', title
        )
        
        if transcript_data:
            processed_count += 1
            logger.info(f"Successfully processed: {title}")
    
    logger.info(f"\nTest completed! Successfully processed: {processed_count} videos")
    return processed_count > 0

if __name__ == "__main__":
    success = test_transcription(3)
    if success:
        print("\nTest successful! You can now run the full transcription with:")
        print("python3 transcribe_videos.py")
    else:
        print("\nTest failed. Please check the logs and fix any issues.")
