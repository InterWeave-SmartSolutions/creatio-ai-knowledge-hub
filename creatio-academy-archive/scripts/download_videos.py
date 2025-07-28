#!/usr/bin/env python3
"""
Creatio Academy Video Downloader

This script extracts video URLs from the archived HTML files and downloads them using yt-dlp.
It handles various video platforms and provides comprehensive logging and metadata generation.

Usage:
    python download_videos.py

Requirements:
    - yt-dlp (install with: pip install yt-dlp)
    - Python 3.6+
"""

import os
import subprocess
import json
import re
import glob
from urllib.parse import urljoin, urlparse
from datetime import datetime

# Directories and files
VIDEO_DIR = "videos/"
LOG_FILE = "download_errors.log"
VIDEO_METADATA_FILE = "video_metadata.json"
URL_EXTRACTION_LOG = "url_extraction.log"

# Ensure directories exist
os.makedirs(VIDEO_DIR, exist_ok=True)

def extract_urls_from_html_files():
    """Extract all potential video URLs from HTML files"""
    all_urls = set()
    
    # Read all HTML files in raw pages directory
    html_files = glob.glob("pages/raw/*.html")
    
    with open(URL_EXTRACTION_LOG, "w") as extraction_log:
        extraction_log.write(f"Starting URL extraction from {len(html_files)} HTML files\n")
        
        for html_file in html_files:
            try:
                with open(html_file, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                # Extract various URL patterns
                patterns = [
                    # YouTube URLs
                    r'https?://(?:www\.)?youtube\.com/watch\?v=[\w-]+',
                    r'https?://(?:www\.)?youtube\.com/embed/[\w-]+',
                    r'https?://youtu\.be/[\w-]+',
                    
                    # Vimeo URLs  
                    r'https?://(?:www\.)?vimeo\.com/\d+',
                    r'https?://player\.vimeo\.com/video/\d+',
                    
                    # Wistia URLs
                    r'https?://[\w-]+\.wistia\.com/medias/[\w-]+',
                    
                    # Academy module/lesson URLs that might contain videos
                    r'https?://academy\.creatio\.com/[\w/-]+/module/\d+[\w/-]*',
                    r'https?://academy\.creatio\.com/[\w/-]+/lesson/\d+[\w/-]*',
                    r'https?://academy\.creatio\.com/[\w/-]+/video/\d+[\w/-]*',
                    r'https?://academy\.creatio\.com/group/\d+/module/\d+[\w/-]*',
                    r'https?://academy\.creatio\.com/[\w/-]+/answer/\d+[\w/-]*',
                    
                    # Direct video file URLs
                    r'https?://[\w.-]+/[\w/.-]+\.(mp4|webm|avi|mov|mkv|flv|wmv)',
                    
                    # Generic video player URLs
                    r'https?://[\w.-]+/[\w/.-]*(?:player|video|embed)[\w/.-]*',
                ]
                
                # Also search for iframe and video tags that might contain embedded content
                iframe_pattern = r'<iframe[^>]+src=["\']([^"\'>]+)["\'][^>]*>'
                video_pattern = r'<video[^>]+src=["\']([^"\'>]+)["\'][^>]*>'
                source_pattern = r'<source[^>]+src=["\']([^"\'>]+)["\'][^>]*>'
                
                # Extract iframe sources
                iframe_matches = re.findall(iframe_pattern, content, re.IGNORECASE)
                for match in iframe_matches:
                    if any(platform in match.lower() for platform in ['youtube', 'vimeo', 'wistia']) or 'academy.creatio.com' in match:
                        all_urls.add(match)
                        extraction_log.write(f"Found iframe URL: {match} in {html_file}\n")
                
                # Extract video/source URLs
                for pattern in [video_pattern, source_pattern]:
                    matches = re.findall(pattern, content, re.IGNORECASE)
                    for match in matches:
                        if match.startswith('http'):
                            all_urls.add(match)
                            extraction_log.write(f"Found video/source URL: {match} in {html_file}\n")
                
                # Extract standard URL patterns
                for pattern in patterns:
                    matches = re.findall(pattern, content, re.IGNORECASE)
                    for match in matches:
                        if isinstance(match, tuple):  # For patterns with groups
                            url = match[0] if match[0] else ''
                        else:
                            url = match
                            
                        if url and ('academy.creatio.com' in url or any(platform in url.lower() for platform in ['youtube', 'vimeo', 'wistia'])):
                            all_urls.add(url)
                            extraction_log.write(f"Found URL: {url} in {html_file}\n")
                            
            except Exception as e:
                extraction_log.write(f"Error processing {html_file}: {str(e)}\n")
        
        extraction_log.write(f"\nTotal unique URLs extracted: {len(all_urls)}\n")
    
    return list(all_urls)

def download_video_content(urls):
    """Download video content using yt-dlp"""
    metadata = []
    
    with open(LOG_FILE, "w") as log_file:
        log_file.write(f"Starting video download process at {datetime.now()}\n")
        log_file.write(f"Total URLs to process: {len(urls)}\n\n")
        
        for i, url in enumerate(urls, 1):
            log_file.write(f"Processing {i}/{len(urls)}: {url}\n")
            
            try:
                # Create structured directory and filename from URL
                parsed_url = urlparse(url)
                path_parts = parsed_url.path.strip('/').split('/')
                
                # Extract course/module information from URL path for organization
                course_name = "general"
                lesson_info = ""
                
                if 'group' in path_parts and 'module' in path_parts:
                    try:
                        group_idx = path_parts.index('group')
                        module_idx = path_parts.index('module')
                        if group_idx + 1 < len(path_parts) and module_idx + 1 < len(path_parts):
                            group_id = path_parts[group_idx + 1]
                            module_id = path_parts[module_idx + 1]
                            course_name = f"group_{group_id}"
                            lesson_info = f"module_{module_id}"
                            if 'answer' in path_parts:
                                answer_idx = path_parts.index('answer')
                                if answer_idx + 1 < len(path_parts):
                                    lesson_info += f"_answer_{path_parts[answer_idx + 1]}"
                    except (ValueError, IndexError):
                        pass
                
                # Create course directory
                course_dir = os.path.join(VIDEO_DIR, course_name)
                os.makedirs(course_dir, exist_ok=True)
                
                # Create safe filename
                safe_filename = re.sub(r'[^\w\-_.]', '_', lesson_info or f"video_{i}")
                output_template = os.path.join(course_dir, f"{safe_filename}_%(title)s.%(ext)s")
                
                # Try to download with yt-dlp using authentication credentials
                command = [
                    "yt-dlp",
                    url,
                    "-o", output_template,
                    "--format", "best[height<=720]/best",
                    "--write-info-json",
                    "--write-description", 
                    "--write-thumbnail",
                    "--continue",
                    "--retries", "3",
                    "--fragment-retries", "3",
                    "--ignore-errors",
                    "--no-check-certificate",  # Skip SSL certificate verification
                    "--username", "amagown@interweave.biz",
                    "--password", "k1AOF6my!",
                ]
                
                result = subprocess.run(command, capture_output=True, text=True, timeout=300)
                
                if result.returncode == 0:
                    log_file.write(f"✓ Successfully downloaded: {url}\n")
                    
                    # Look for generated info files to extract metadata
                    info_files = glob.glob(os.path.join(course_dir, f"{safe_filename}_*.info.json"))
                    
                    for info_file in info_files:
                        try:
                            with open(info_file, 'r', encoding='utf-8') as f:
                                video_info = json.load(f)
                                
                            metadata.append({
                                "title": video_info.get("title", "Unknown"),
                                "duration": video_info.get("duration"),
                                "resolution": f"{video_info.get('width', 0)}x{video_info.get('height', 0)}",
                                "format": video_info.get("ext", "unknown"),
                                "filesize": video_info.get("filesize"),
                                "upload_date": video_info.get("upload_date"),
                                "uploader": video_info.get("uploader"),
                                "source_url": url,
                                "download_date": datetime.now().isoformat(),
                                "local_file": info_file.replace(".info.json", f".{video_info.get('ext', 'mp4')}")
                            })
                        except Exception as e:
                            log_file.write(f"  Warning: Could not read metadata from {info_file}: {str(e)}\n")
                            
                else:
                    error_msg = result.stderr.strip() if result.stderr else "Unknown error"
                    log_file.write(f"✗ Failed to download {url}: {error_msg}\n")
                    
            except subprocess.TimeoutExpired:
                log_file.write(f"✗ Timeout downloading {url}\n")
            except Exception as e:
                log_file.write(f"✗ Error downloading {url}: {str(e)}\n")
            
            log_file.write("\n")
    
    return metadata

def main():
    """Main function to extract URLs and download videos"""
    print("Step 1: Extracting URLs from HTML files...")
    urls = extract_urls_from_html_files()
    
    if not urls:
        print("No video URLs found in HTML files.")
        return
    
    print(f"Step 2: Found {len(urls)} URLs. Starting download process...")
    metadata = download_video_content(urls)
    
    print(f"Step 3: Saving metadata for {len(metadata)} downloaded videos...")
    
    # Save comprehensive metadata
    with open(VIDEO_METADATA_FILE, "w", encoding='utf-8') as f:
        json.dump({
            "extraction_date": datetime.now().isoformat(),
            "total_urls_found": len(urls),
            "total_videos_downloaded": len(metadata),
            "videos": metadata
        }, f, indent=2, ensure_ascii=False)
    
    print(f"\nDownload process completed!")
    print(f"- URLs extracted: {len(urls)}")
    print(f"- Videos downloaded: {len(metadata)}")
    print(f"- Check '{LOG_FILE}' for detailed download logs")
    print(f"- Check '{URL_EXTRACTION_LOG}' for URL extraction details")
    print(f"- Check '{VIDEO_METADATA_FILE}' for video metadata")
    print(f"- Videos saved to '{VIDEO_DIR}' directory")

if __name__ == "__main__":
    main()
