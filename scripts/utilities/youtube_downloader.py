#!/usr/bin/env python3
"""
Creatio Academy YouTube Video Downloader
A comprehensive script to download all videos from Creatio Academy YouTube channel
with rate limiting, retry logic, progress tracking, and integrity verification.
"""

import os
import sys
import json
import time
import logging
import subprocess
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import hashlib
import re

class CreatioYouTubeDownloader:
    def __init__(self, output_dir: str = "downloads", max_retries: int = 3, 
                 rate_limit: str = "1M", concurrent_downloads: int = 1):
        """
        Initialize the downloader with configuration options.
        
        Args:
            output_dir: Base directory for downloads
            max_retries: Maximum retry attempts for failed downloads
            rate_limit: Rate limit for downloads (e.g., '1M' for 1MB/s)
            concurrent_downloads: Number of concurrent downloads
        """
        self.output_dir = Path(output_dir)
        self.max_retries = max_retries
        self.rate_limit = rate_limit
        self.concurrent_downloads = concurrent_downloads
        
        # Create output directory
        self.output_dir.mkdir(exist_ok=True)
        
        # Setup logging
        self.setup_logging()
        
        # Progress tracking
        self.progress_file = self.output_dir / "download_progress.json"
        self.completed_videos = self.load_progress()
        
        # Channel URL
        self.channel_url = "https://www.youtube.com/@CreatioAcademy"
        
    def setup_logging(self):
        """Setup logging configuration."""
        log_file = self.output_dir / "download.log"
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def load_progress(self) -> Dict:
        """Load download progress from file."""
        if self.progress_file.exists():
            try:
                with open(self.progress_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                self.logger.warning("Could not load progress file, starting fresh")
        return {
            "completed": {},
            "failed": {},
            "total_videos": 0,
            "downloaded_count": 0,
            "failed_count": 0,
            "last_updated": datetime.now().isoformat()
        }
        
    def save_progress(self):
        """Save current progress to file."""
        self.completed_videos["last_updated"] = datetime.now().isoformat()
        with open(self.progress_file, 'w') as f:
            json.dump(self.completed_videos, f, indent=2)
            
    def get_channel_videos(self) -> List[Dict]:
        """
        Get list of all videos from the channel.
        Returns list of video metadata dictionaries.
        """
        self.logger.info("Fetching channel video list...")
        
        cmd = [
            "yt-dlp",
            "--flat-playlist",
            "--print", "%(id)s|%(title)s|%(uploader)s|%(duration)s|%(upload_date)s|%(playlist_title)s",
            self.channel_url
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            videos = []
            
            for line in result.stdout.strip().split('\n'):
                if '|' in line:
                    parts = line.split('|', 5)
                    if len(parts) >= 5:
                        video_info = {
                            'id': parts[0],
                            'title': parts[1],
                            'uploader': parts[2],
                            'duration': parts[3],
                            'upload_date': parts[4],
                            'playlist_title': parts[5] if len(parts) > 5 else 'General'
                        }
                        videos.append(video_info)
                        
            self.logger.info(f"Found {len(videos)} videos in channel")
            return videos
            
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Failed to get channel videos: {e}")
            return []
            
    def sanitize_filename(self, filename: str) -> str:
        """Sanitize filename for filesystem compatibility."""
        # Remove or replace invalid characters
        filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
        filename = re.sub(r'\s+', ' ', filename).strip()
        return filename[:200]  # Limit length
        
    def get_video_output_path(self, video_info: Dict) -> Path:
        """
        Determine output path for video based on playlist/category.
        Organizes videos into subdirectories.
        """
        playlist_title = video_info.get('playlist_title', 'General')
        category_dir = self.sanitize_filename(playlist_title)
        
        # Create category subdirectory
        category_path = self.output_dir / category_dir
        category_path.mkdir(exist_ok=True)
        
        # Generate safe filename
        safe_title = self.sanitize_filename(video_info['title'])
        filename = f"{video_info['id']}_{safe_title}.%(ext)s"
        
        return category_path / filename
        
    def download_video(self, video_info: Dict) -> bool:
        """
        Download a single video with retry logic.
        
        Args:
            video_info: Video metadata dictionary
            
        Returns:
            True if download successful, False otherwise
        """
        video_id = video_info['id']
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        
        # Check if already downloaded
        if video_id in self.completed_videos.get("completed", {}):
            self.logger.info(f"Video {video_id} already downloaded, skipping")
            return True
            
        output_path = self.get_video_output_path(video_info)
        
        # yt-dlp command with comprehensive options
        cmd = [
            "yt-dlp",
            "--format", "best[height<=1080]/best",  # Prefer 1080p or best available
            "--output", str(output_path),
            "--write-info-json",  # Save metadata
            "--write-thumbnail",  # Save thumbnail
            "--write-subs",  # Download subtitles if available
            "--write-auto-subs",  # Download auto-generated subs
            "--sub-langs", "en,en-US",  # Prefer English subtitles
            "--embed-subs",  # Embed subtitles in video
            "--rate-limit", self.rate_limit,
            "--retries", str(self.max_retries),
            "--fragment-retries", str(self.max_retries),
            "--abort-on-unavailable-fragment",
            "--keep-fragments",  # Keep fragments for debugging
            "--no-overwrites",  # Don't overwrite existing files
            "--continue",  # Resume partial downloads
            video_url
        ]
        
        for attempt in range(self.max_retries):
            try:
                self.logger.info(f"Downloading {video_info['title']} (attempt {attempt + 1}/{self.max_retries})")
                
                result = subprocess.run(cmd, capture_output=True, text=True, check=True)
                
                # Verify download
                if self.verify_download(output_path, video_info):
                    self.completed_videos["completed"][video_id] = {
                        "title": video_info["title"],
                        "download_date": datetime.now().isoformat(),
                        "file_path": str(output_path),
                        "verified": True
                    }
                    self.completed_videos["downloaded_count"] = self.completed_videos.get("downloaded_count", 0) + 1
                    self.save_progress()
                    self.logger.info(f"Successfully downloaded: {video_info['title']}")
                    return True
                else:
                    self.logger.error(f"Download verification failed for {video_id}")
                    
            except subprocess.CalledProcessError as e:
                self.logger.warning(f"Download attempt {attempt + 1} failed for {video_id}: {e}")
                if "rate" in str(e).lower() or "quota" in str(e).lower():
                    # Rate limiting detected, wait longer
                    wait_time = min(300, (attempt + 1) * 60)  # Up to 5 minutes
                    self.logger.info(f"Rate limit detected, waiting {wait_time} seconds...")
                    time.sleep(wait_time)
                else:
                    # Generic error, shorter wait
                    time.sleep(30)
                    
        # All attempts failed
        self.completed_videos["failed"][video_id] = {
            "title": video_info["title"],
            "failed_date": datetime.now().isoformat(),
            "attempts": self.max_retries
        }
        self.completed_videos["failed_count"] = self.completed_videos.get("failed_count", 0) + 1
        self.save_progress()
        self.logger.error(f"Failed to download after {self.max_retries} attempts: {video_info['title']}")
        return False
        
    def verify_download(self, output_path: Path, video_info: Dict) -> bool:
        """
        Verify download integrity and completeness.
        
        Args:
            output_path: Expected output path (template)
            video_info: Video metadata
            
        Returns:
            True if download is valid, False otherwise
        """
        try:
            # Find actual downloaded files (yt-dlp replaces %(ext)s)
            parent_dir = output_path.parent
            base_name = output_path.stem  # Remove .%(ext)s
            
            video_files = list(parent_dir.glob(f"{base_name}.*"))
            video_files = [f for f in video_files if f.suffix in ['.mp4', '.webm', '.mkv', '.avi']]
            
            if not video_files:
                self.logger.error(f"No video file found for {video_info['id']}")
                return False
                
            video_file = video_files[0]  # Take first match
            
            # Check file size (should be > 1KB for a real video)
            if video_file.stat().st_size < 1024:
                self.logger.error(f"Video file too small: {video_file}")
                return False
                
            # Check if info.json exists (metadata verification)
            info_file = parent_dir / f"{base_name}.info.json"
            if info_file.exists():
                try:
                    with open(info_file, 'r') as f:
                        info_data = json.load(f)
                        # Verify video ID matches
                        if info_data.get('id') != video_info['id']:
                            self.logger.error(f"Video ID mismatch in metadata: {video_info['id']}")
                            return False
                except json.JSONDecodeError:
                    self.logger.warning(f"Could not parse info.json for {video_info['id']}")
                    
            self.logger.info(f"Download verified: {video_file}")
            return True
            
        except Exception as e:
            self.logger.error(f"Verification error for {video_info['id']}: {e}")
            return False
            
    def print_progress_summary(self):
        """Print current download progress summary."""
        total = self.completed_videos.get("total_videos", 0)
        downloaded = self.completed_videos.get("downloaded_count", 0)
        failed = self.completed_videos.get("failed_count", 0)
        
        print("\n" + "="*60)
        print("DOWNLOAD PROGRESS SUMMARY")
        print("="*60)
        print(f"Total videos found: {total}")
        print(f"Successfully downloaded: {downloaded}")
        print(f"Failed downloads: {failed}")
        print(f"Remaining: {total - downloaded - failed}")
        
        if total > 0:
            completion_rate = (downloaded / total) * 100
            print(f"Completion rate: {completion_rate:.1f}%")
            
        print("="*60)
        
    def run_batch_download(self):
        """
        Main method to run the batch download process.
        """
        self.logger.info("Starting Creatio Academy YouTube download process")
        
        # Get all videos from channel
        videos = self.get_channel_videos()
        
        if not videos:
            self.logger.error("No videos found or failed to fetch channel")
            return
            
        self.completed_videos["total_videos"] = len(videos)
        self.save_progress()
        
        self.logger.info(f"Starting download of {len(videos)} videos")
        
        # Download each video
        for i, video_info in enumerate(videos, 1):
            self.logger.info(f"Processing video {i}/{len(videos)}: {video_info['title']}")
            
            success = self.download_video(video_info)
            
            # Print periodic progress updates
            if i % 10 == 0 or not success:
                self.print_progress_summary()
                
            # Rate limiting between downloads
            if success:
                time.sleep(2)  # 2 second delay between successful downloads
            else:
                time.sleep(10)  # Longer delay after failures
                
        # Final summary
        self.print_progress_summary()
        self.logger.info("Batch download process completed")
        
        # Generate completion report
        self.generate_report()
        
    def generate_report(self):
        """Generate detailed download report."""
        report_file = self.output_dir / "download_report.txt"
        
        with open(report_file, 'w') as f:
            f.write("CREATIO ACADEMY YOUTUBE DOWNLOAD REPORT\n")
            f.write("="*50 + "\n")
            f.write(f"Report generated: {datetime.now().isoformat()}\n")
            f.write(f"Total videos: {self.completed_videos.get('total_videos', 0)}\n")
            f.write(f"Downloaded: {self.completed_videos.get('downloaded_count', 0)}\n")
            f.write(f"Failed: {self.completed_videos.get('failed_count', 0)}\n\n")
            
            # List successful downloads
            f.write("SUCCESSFUL DOWNLOADS:\n")
            f.write("-" * 30 + "\n")
            for video_id, info in self.completed_videos.get("completed", {}).items():
                f.write(f"{video_id}: {info['title']}\n")
                
            # List failed downloads
            f.write("\nFAILED DOWNLOADS:\n")
            f.write("-" * 30 + "\n")
            for video_id, info in self.completed_videos.get("failed", {}).items():
                f.write(f"{video_id}: {info['title']}\n")
                
        self.logger.info(f"Detailed report saved to: {report_file}")


def main():
    """Main entry point with command line argument parsing."""
    parser = argparse.ArgumentParser(description="Download Creatio Academy YouTube videos")
    parser.add_argument("--output-dir", default="downloads", 
                       help="Output directory for downloads")
    parser.add_argument("--max-retries", type=int, default=3,
                       help="Maximum retry attempts for failed downloads")
    parser.add_argument("--rate-limit", default="1M",
                       help="Rate limit for downloads (e.g., '1M' for 1MB/s)")
    parser.add_argument("--concurrent", type=int, default=1,
                       help="Number of concurrent downloads")
    
    args = parser.parse_args()
    
    # Create downloader and run
    downloader = CreatioYouTubeDownloader(
        output_dir=args.output_dir,
        max_retries=args.max_retries,
        rate_limit=args.rate_limit,
        concurrent_downloads=args.concurrent
    )
    
    try:
        downloader.run_batch_download()
    except KeyboardInterrupt:
        print("\nDownload interrupted by user")
        downloader.save_progress()
        sys.exit(1)
    except Exception as e:
        downloader.logger.error(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
