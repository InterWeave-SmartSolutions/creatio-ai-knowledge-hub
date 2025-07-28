#!/usr/bin/env python3
"""
Video transcription script for Creatio Academy content.
Downloads videos, extracts audio, and transcribes using OpenAI Whisper.
"""

import os
import json
import subprocess
import time
import logging
from pathlib import Path
from urllib.parse import urlparse, parse_qs
import tempfile
import re
from typing import Dict, List, Optional

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def setup_directories():
    """Create necessary directories for transcription"""
    directories = [
        'videos/downloaded',
        'audio_extracted',
        'transcripts/text',
        'transcripts/json'
    ]
    
    for dir_path in directories:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        logger.info(f"Created directory: {dir_path}")

def extract_video_id_from_youtube_url(url: str) -> Optional[str]:
    """Extract video ID from various YouTube URL formats"""
    patterns = [
        r'(?:youtube\.com/watch\?v=|youtu\.be/|youtube\.com/embed/)([a-zA-Z0-9_-]{11})',
        r'youtube\.com/.*[?&]v=([a-zA-Z0-9_-]{11})'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    
    return None

def sanitize_filename(filename: str) -> str:
    """Sanitize filename for safe filesystem usage"""
    # Replace problematic characters
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    # Remove multiple consecutive underscores
    filename = re.sub(r'_{2,}', '_', filename)
    # Truncate if too long
    if len(filename) > 200:
        filename = filename[:200]
    return filename.strip('_')

def download_video(url: str, output_dir: str, video_name: str) -> Optional[str]:
    """Download video using yt-dlp"""
    try:
        video_id = extract_video_id_from_youtube_url(url)
        if not video_id:
            logger.error(f"Could not extract video ID from URL: {url}")
            return None
        
        safe_name = sanitize_filename(video_name)
        output_path = Path(output_dir) / f"{safe_name}_{video_id}.%(ext)s"
        
        # Check if video already exists
        existing_files = list(Path(output_dir).glob(f"{safe_name}_{video_id}.*"))
        video_files = [f for f in existing_files if f.suffix in ['.mp4', '.webm', '.mkv', '.avi']]
        if video_files:
            logger.info(f"Video already downloaded: {video_files[0]}")
            return str(video_files[0])
        
        cmd = [
            'yt-dlp',
            '--format', 'best[ext=mp4]/best[ext=webm]/best',
            '--output', str(output_path),
            '--no-playlist',
            '--write-info-json',
            '--write-description',
            '--write-thumbnail',
            url
        ]
        
        logger.info(f"Downloading video: {video_name} from {url}")
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        
        # Find the downloaded file
        downloaded_files = list(Path(output_dir).glob(f"{safe_name}_{video_id}.*"))
        video_files = [f for f in downloaded_files if f.suffix in ['.mp4', '.webm', '.mkv', '.avi']]
        
        if video_files:
            logger.info(f"Successfully downloaded: {video_files[0]}")
            return str(video_files[0])
        else:
            logger.error(f"No video file found after download for {url}")
            return None
            
    except subprocess.CalledProcessError as e:
        logger.error(f"yt-dlp failed for {url}: {e.stderr}")
        return None
    except Exception as e:
        logger.error(f"Error downloading {url}: {e}")
        return None

def extract_audio(video_path: str, audio_output_dir: str) -> Optional[str]:
    """Extract audio from video using ffmpeg"""
    try:
        video_file = Path(video_path)
        audio_file = Path(audio_output_dir) / f"{video_file.stem}.wav"
        
        # Check if audio already exists
        if audio_file.exists():
            logger.info(f"Audio already exists: {audio_file}")
            return str(audio_file)
        
        cmd = [
            'ffmpeg',
            '-i', video_path,
            '-vn',  # No video
            '-acodec', 'pcm_s16le',  # PCM 16-bit little-endian
            '-ar', '16000',  # 16kHz sample rate (optimal for Whisper)
            '-ac', '1',  # Mono
            str(audio_file)
        ]
        
        logger.info(f"Extracting audio from: {video_file.name}")
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        
        if audio_file.exists():
            logger.info(f"Audio extracted successfully: {audio_file}")
            return str(audio_file)
        else:
            logger.error(f"Audio file not created: {audio_file}")
            return None
            
    except subprocess.CalledProcessError as e:
        logger.error(f"ffmpeg failed for {video_path}: {e.stderr}")
        return None
    except Exception as e:
        logger.error(f"Error extracting audio from {video_path}: {e}")
        return None

def transcribe_audio(audio_path: str, text_output_dir: str, json_output_dir: str, video_name: str) -> Dict:
    """Transcribe audio using Whisper with detailed output"""
    try:
        audio_file = Path(audio_path)
        safe_name = sanitize_filename(video_name)
        
        text_file = Path(text_output_dir) / f"{safe_name}.txt"
        json_file = Path(json_output_dir) / f"{safe_name}.json"
        
        # Check if transcripts already exist
        if text_file.exists() and json_file.exists():
            logger.info(f"Transcripts already exist for: {safe_name}")
            with open(json_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        logger.info(f"Transcribing audio: {audio_file.name}")
        
        # Use whisper command line tool for better control
        cmd = [
            'whisper',
            audio_path,
            '--model', 'large',  # Use large model for accuracy
            '--language', 'en',  # Assume English
            '--output_format', 'json',
            '--output_format', 'txt', 
            '--output_dir', str(Path(text_output_dir).parent),  # Parent dir since whisper creates subdirs
            '--verbose', 'False'
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        
        # Whisper creates files with the audio filename
        whisper_json = Path(text_output_dir).parent / f"{audio_file.stem}.json"
        whisper_txt = Path(text_output_dir).parent / f"{audio_file.stem}.txt"
        
        transcript_data = {}
        
        if whisper_json.exists():
            with open(whisper_json, 'r', encoding='utf-8') as f:
                transcript_data = json.load(f)
            
            # Move to our organized structure
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(transcript_data, f, indent=2, ensure_ascii=False)
            
            # Clean up original file
            whisper_json.unlink()
        
        if whisper_txt.exists():
            # Process text file for better formatting
            with open(whisper_txt, 'r', encoding='utf-8') as f:
                text_content = f.read()
            
            # Add paragraph breaks and improve formatting
            formatted_text = format_transcript_text(text_content, transcript_data)
            
            with open(text_file, 'w', encoding='utf-8') as f:
                f.write(formatted_text)
            
            # Clean up original file
            whisper_txt.unlink()
        
        logger.info(f"Transcription completed for: {safe_name}")
        return transcript_data
        
    except subprocess.CalledProcessError as e:
        logger.error(f"Whisper failed for {audio_path}: {e.stderr}")
        return {}
    except Exception as e:
        logger.error(f"Error transcribing {audio_path}: {e}")
        return {}

def format_transcript_text(text: str, transcript_data: Dict) -> str:
    """Format transcript text with paragraph breaks and speaker detection"""
    if not transcript_data or 'segments' not in transcript_data:
        return text
    
    formatted_lines = []
    current_paragraph = []
    last_end_time = 0
    
    for segment in transcript_data['segments']:
        start_time = segment.get('start', 0)
        text_segment = segment.get('text', '').strip()
        
        if not text_segment:
            continue
        
        # Add paragraph break if there's a significant pause (more than 3 seconds)
        if start_time - last_end_time > 3.0 and current_paragraph:
            formatted_lines.append(' '.join(current_paragraph))
            current_paragraph = []
        
        current_paragraph.append(text_segment)
        last_end_time = segment.get('end', start_time + 1)
    
    # Add remaining paragraph
    if current_paragraph:
        formatted_lines.append(' '.join(current_paragraph))
    
    # Join paragraphs with double newlines
    formatted_text = '\n\n'.join(formatted_lines)
    
    # Clean up extra whitespace
    formatted_text = re.sub(r'\n{3,}', '\n\n', formatted_text)
    formatted_text = re.sub(r'[ \t]+', ' ', formatted_text)
    
    return formatted_text.strip()

def create_transcript_index(video_index_path: str, transcripts_dir: str) -> Dict:
    """Create index linking transcripts to videos"""
    transcript_index = {}
    
    with open(video_index_path, 'r', encoding='utf-8') as f:
        video_index = json.load(f)
    
    text_dir = Path(transcripts_dir) / 'text'
    json_dir = Path(transcripts_dir) / 'json'
    
    for file_key, video_data in video_index.items():
        metadata = video_data.get('metadata', {})
        title = metadata.get('title', f'Video {file_key}')
        safe_name = sanitize_filename(title)
        
        text_file = text_dir / f"{safe_name}.txt"
        json_file = json_dir / f"{safe_name}.json"
        
        if text_file.exists() and json_file.exists():
            transcript_index[file_key] = {
                'title': title,
                'description': metadata.get('description', ''),
                'type': metadata.get('type', 'Unknown'),
                'videos': video_data.get('videos', []),
                'transcripts': {
                    'text': str(text_file.relative_to(Path.cwd())),
                    'json': str(json_file.relative_to(Path.cwd()))
                },
                'created_at': time.time()
            }
    
    return transcript_index

def main():
    """Main transcription workflow"""
    logger.info("Starting video transcription workflow")
    
    # Check if video_index.json exists
    video_index_path = 'video_index.json'
    if not os.path.exists(video_index_path):
        logger.error(f"Video index not found: {video_index_path}")
        logger.info("Please run the video extraction script first to create the video index")
        return
    
    # Setup directories
    setup_directories()
    
    # Load video index
    with open(video_index_path, 'r', encoding='utf-8') as f:
        video_index = json.load(f)
    
    logger.info(f"Found {len(video_index)} video entries to process")
    
    # Process each video entry
    processed_count = 0
    transcript_results = {}
    
    for file_key, video_data in video_index.items():
        metadata = video_data.get('metadata', {})
        title = metadata.get('title', f'Video {file_key}')
        videos = video_data.get('videos', [])
        
        if not videos:
            logger.warning(f"No videos found for: {title}")
            continue
        
        logger.info(f"\nProcessing: {title}")
        logger.info(f"Videos: {len(videos)} found")
        
        # For now, process only the first video URL to avoid duplicates
        # In the future, we might want to handle multiple videos per entry
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
            transcript_results[file_key] = {
                'title': title,
                'video_url': video_url,
                'transcript_data': transcript_data
            }
            processed_count += 1
            logger.info(f"Successfully processed: {title}")
        
        # Small delay to avoid overwhelming the system
        time.sleep(1)
    
    # Create transcript index
    logger.info("\nCreating transcript index...")
    transcript_index = create_transcript_index(video_index_path, 'transcripts')
    
    with open('transcript_index.json', 'w', encoding='utf-8') as f:
        json.dump(transcript_index, f, indent=2, ensure_ascii=False)
    
    logger.info(f"\nTranscription workflow completed!")
    logger.info(f"Successfully processed: {processed_count} videos")
    logger.info(f"Transcript index saved to: transcript_index.json")
    logger.info(f"Text transcripts: transcripts/text/")
    logger.info(f"JSON transcripts: transcripts/json/")

if __name__ == "__main__":
    main()
