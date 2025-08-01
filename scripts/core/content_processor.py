#!/usr/bin/env python3
"""
Comprehensive Creatio Academy Content Processor
- Crawls all web pages
- Extracts video URLs from all pages
- Downloads videos and resources
- Transcribes video content
- Creates AI-readable index
"""

import os
import sys
import json
import re
import subprocess
import logging
import requests
from pathlib import Path
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from datetime import datetime
import whisper
import hashlib
import mimetypes
from typing import Dict, List, Set, Optional

# Import our document processor
sys.path.append(str(Path(__file__).parent.parent / "utilities"))
from document_processor import DocumentProcessor

class CreatioContentProcessor:
    def __init__(self, base_url: str = "https://academy.creatio.com", output_dir: str = "processed_content"):
        self.base_url = base_url
        self.output_dir = Path(output_dir)
        self.crawled_dir = Path("crawler_output") 
        self.videos_dir = self.output_dir / "videos"
        self.transcripts_dir = self.output_dir / "transcripts"
        self.resources_dir = self.output_dir / "resources"
        self.pages_dir = self.output_dir / "pages"
        self.documents_dir = self.output_dir / "documents"
        
        # Create directories
        for dir_path in [self.output_dir, self.videos_dir, self.transcripts_dir, 
                        self.resources_dir, self.pages_dir, self.documents_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)
            
        # Initialize document processor
        self.doc_processor = DocumentProcessor(output_dir=str(self.documents_dir))
            
        # Setup logging
        self.setup_logging()
        
        # Initialize video URLs set and processed files
        self.video_urls = set()
        self.processed_files = {}
        self.load_progress()
        
        # Initialize whisper for transcription
        try:
            self.whisper_model = whisper.load_model("base")
        except Exception as e:
            self.logger.warning(f"Could not load Whisper model: {e}")
            self.whisper_model = None
            
    def setup_logging(self):
        """Setup comprehensive logging."""
        log_file = self.output_dir / "content_processor.log"
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def load_progress(self):
        """Load processing progress."""
        progress_file = self.output_dir / "processing_progress.json"
        if progress_file.exists():
            try:
                with open(progress_file, 'r') as f:
                    self.processed_files = json.load(f)
            except Exception as e:
                self.logger.warning(f"Could not load progress: {e}")
                self.processed_files = {}
        else:
            self.processed_files = {
                "pages": {},
                "videos": {},
                "resources": {},
                "last_updated": datetime.now().isoformat()
            }
    
    def save_progress(self):
        """Save processing progress."""
        progress_file = self.output_dir / "processing_progress.json"
        self.processed_files["last_updated"] = datetime.now().isoformat()
        with open(progress_file, 'w') as f:
            json.dump(self.processed_files, f, indent=2)
            
    def crawl_website(self):
        """Crawl the entire website using wget."""
        self.logger.info("Starting website crawl...")
        
        cmd = [
            "wget",
            "--recursive",
            "--no-clobber", 
            "--page-requisites",
            "--html-extension",
            "--convert-links",
            f"--domains={urlparse(self.base_url).netloc}",
            "--restrict-file-names=windows",
            "--no-parent",
            "-e", "robots=off",
            "--wait=1",
            "--random-wait",
            "--directory-prefix=crawler_output",
            "--user-agent=Mozilla/5.0 (compatible; CreatioBot/1.0)",
            self.base_url
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=3600)
            self.logger.info(f"Website crawl completed with return code: {result.returncode}")
            if result.stderr:
                self.logger.warning(f"Crawl warnings: {result.stderr}")
        except subprocess.TimeoutExpired:
            self.logger.warning("Website crawl timed out after 1 hour")
        except Exception as e:
            self.logger.error(f"Website crawl failed: {e}")
            
    def extract_urls_from_pages(self):
        """Extract all video URLs and resource URLs from crawled pages."""
        self.logger.info("Extracting URLs from crawled pages...")
        
        html_files = list(self.crawled_dir.rglob("*.html")) + list(self.crawled_dir.rglob("*.htm"))
        self.logger.info(f"Found {len(html_files)} HTML files to process")
        
        for html_file in html_files:
            try:
                self.process_html_file(html_file)
            except Exception as e:
                self.logger.error(f"Error processing {html_file}: {e}")
                
        self.logger.info(f"Found {len(self.video_urls)} unique video URLs")
        
    def process_html_file(self, html_file: Path):
        """Process a single HTML file to extract URLs and content."""
        try:
            with open(html_file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                
            soup = BeautifulSoup(content, 'html.parser')
            
            # Extract video URLs (YouTube, Vimeo, etc.)
            video_patterns = [
                r'https?://(?:www\.)?youtube\.com/watch\?v=[\w-]+',
                r'https?://youtu\.be/[\w-]+',
                r'https?://(?:www\.)?vimeo\.com/\d+',
                r'https?://player\.vimeo\.com/video/\d+',
                r'https?://.*\.mp4',
                r'https?://.*\.webm',
                r'https?://.*\.mov'
            ]
            
            for pattern in video_patterns:
                matches = re.findall(pattern, content, re.IGNORECASE)
                self.video_urls.update(matches)
                
            # Extract from iframe sources
            iframes = soup.find_all('iframe')
            for iframe in iframes:
                src = iframe.get('src', '')
                if any(domain in src for domain in ['youtube.com', 'youtu.be', 'vimeo.com']):
                    self.video_urls.add(src)
                    
            # Extract from video tags
            videos = soup.find_all('video')
            for video in videos:
                src = video.get('src', '')
                if src:
                    self.video_urls.add(urljoin(self.base_url, src))
                    
            # Extract downloadable resources
            self.extract_resources_from_soup(soup, html_file)
            
            # Save processed page content as markdown
            self.save_page_as_markdown(soup, html_file)
            
        except Exception as e:
            self.logger.error(f"Error processing HTML file {html_file}: {e}")
            
    def extract_resources_from_soup(self, soup: BeautifulSoup, html_file: Path):
        """Extract downloadable resources from HTML soup."""
        resource_extensions = {'.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', 
                             '.zip', '.rar', '.tar', '.gz', '.png', '.jpg', '.jpeg', '.gif'}
        
        # Extract from links
        links = soup.find_all('a', href=True)
        for link in links:
            href = link['href']
            if any(href.lower().endswith(ext) for ext in resource_extensions):
                full_url = urljoin(self.base_url, href)
                self.download_resource(full_url, link.get_text(strip=True))
                
    def save_page_as_markdown(self, soup: BeautifulSoup, html_file: Path):
        """Convert HTML page to markdown for AI readability."""
        try:
            # Extract main content
            title = soup.find('title')
            title_text = title.get_text(strip=True) if title else html_file.stem
            
            # Get main content areas
            main_content = soup.find('main') or soup.find('article') or soup.find('div', class_=re.compile(r'content|main'))
            if not main_content:
                main_content = soup.find('body')
                
            # Extract text content
            text_content = []
            if main_content:
                # Remove script and style elements
                for script in main_content(["script", "style"]):
                    script.decompose()
                    
                # Extract text
                text = main_content.get_text()
                # Clean up whitespace
                lines = (line.strip() for line in text.splitlines())
                text_content = [line for line in lines if line]
                
            # Create markdown file
            md_file = self.pages_dir / f"{html_file.stem}.md"
            with open(md_file, 'w', encoding='utf-8') as f:
                f.write(f"# {title_text}\n\n")
                f.write(f"**Source:** {html_file}\n")
                f.write(f"**Processed:** {datetime.now().isoformat()}\n\n")
                f.write("---\n\n")
                f.write('\n'.join(text_content))
                
            self.processed_files["pages"][str(html_file)] = {
                "markdown_file": str(md_file),
                "title": title_text,
                "processed_date": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error converting {html_file} to markdown: {e}")
            
    def download_resource(self, url: str, description: str = ""):
        """Download a resource file."""
        try:
            response = requests.get(url, stream=True, timeout=30)
            response.raise_for_status()
            
            # Generate filename
            parsed_url = urlparse(url)
            filename = Path(parsed_url.path).name
            if not filename or '.' not in filename:
                # Generate filename based on content type
                content_type = response.headers.get('content-type', '')
                extension = mimetypes.guess_extension(content_type) or '.bin'
                filename = f"resource_{hashlib.md5(url.encode()).hexdigest()[:8]}{extension}"
                
            resource_path = self.resources_dir / filename
            
            # Skip if already downloaded
            if resource_path.exists():
                return
                
            # Download file
            with open(resource_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
                    
            self.logger.info(f"Downloaded resource: {filename}")
            
            # Save metadata
            self.processed_files.setdefault("resources", {})[url] = {
                "filename": filename,
                "description": description,
                "download_date": datetime.now().isoformat(),
                "size": resource_path.stat().st_size
            }
            
        except Exception as e:
            self.logger.error(f"Error downloading resource {url}: {e}")
            
    def download_videos(self):
        """Download all extracted videos using yt-dlp."""
        self.logger.info(f"Starting download of {len(self.video_urls)} videos...")
        
        for i, video_url in enumerate(self.video_urls, 1):
            try:
                self.logger.info(f"Downloading video {i}/{len(self.video_urls)}: {video_url}")
                self.download_single_video(video_url)
            except Exception as e:
                self.logger.error(f"Error downloading video {video_url}: {e}")
                
        self.save_progress()
        
    def download_single_video(self, video_url: str):
        """Download a single video and extract metadata."""
        # Generate safe filename
        video_id = hashlib.md5(video_url.encode()).hexdigest()[:12]
        output_template = str(self.videos_dir / f"{video_id}_%(title)s.%(ext)s")
        
        cmd = [
            "yt-dlp",
            "--format", "best[height<=1080]/best",
            "--output", output_template,
            "--write-info-json",
            "--write-thumbnail", 
            "--write-subs",
            "--write-auto-subs",
            "--sub-langs", "en,en-US",
            "--no-overwrites",
            "--ignore-errors",
            video_url
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
            
            if result.returncode == 0:
                self.logger.info(f"Successfully downloaded: {video_url}")
                
                # Find downloaded files
                video_files = list(self.videos_dir.glob(f"{video_id}_*"))
                video_file = None
                for file in video_files:
                    if file.suffix in ['.mp4', '.webm', '.mkv']:
                        video_file = file
                        break
                        
                if video_file:
                    self.processed_files.setdefault("videos", {})[video_url] = {
                        "video_file": str(video_file),
                        "video_id": video_id,
                        "download_date": datetime.now().isoformat(),
                        "transcribed": False
                    }
                    
                    # Schedule for transcription
                    self.transcribe_video(video_file, video_url)
                    
            else:
                self.logger.warning(f"Failed to download {video_url}: {result.stderr}")
                
        except subprocess.TimeoutExpired:
            self.logger.error(f"Download timeout for {video_url}")
        except Exception as e:
            self.logger.error(f"Download error for {video_url}: {e}")
            
    def transcribe_video(self, video_file: Path, video_url: str):
        """Transcribe video to text using Whisper."""
        if not self.whisper_model:
            self.logger.warning(f"Whisper not available, skipping transcription of {video_file}")
            return
            
        try:
            self.logger.info(f"Transcribing video: {video_file}")
            
            # Extract audio if needed
            audio_file = video_file.with_suffix('.wav')
            if not audio_file.exists():
                cmd = [
                    "ffmpeg", "-i", str(video_file),
                    "-acodec", "pcm_s16le", "-ac", "1", "-ar", "16000",
                    str(audio_file), "-y"
                ]
                subprocess.run(cmd, capture_output=True, check=True)
                
            # Transcribe with Whisper
            result = self.whisper_model.transcribe(str(audio_file))
            
            # Save transcript
            transcript_file = self.transcripts_dir / f"{video_file.stem}_transcript.txt"
            with open(transcript_file, 'w', encoding='utf-8') as f:
                f.write(f"# Transcript: {video_file.name}\n")
                f.write(f"**Source:** {video_url}\n")
                f.write(f"**Transcribed:** {datetime.now().isoformat()}\n\n")
                f.write("---\n\n")
                f.write(result['text'])
                
            # Save detailed transcript with timestamps
            detailed_transcript_file = self.transcripts_dir / f"{video_file.stem}_detailed_transcript.json"
            with open(detailed_transcript_file, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2)
                
            # Update progress
            if video_url in self.processed_files.get("videos", {}):
                self.processed_files["videos"][video_url]["transcribed"] = True
                self.processed_files["videos"][video_url]["transcript_file"] = str(transcript_file)
                
            # Clean up audio file if it was created
            if audio_file.exists() and audio_file != video_file:
                audio_file.unlink()
                
            self.logger.info(f"Transcription completed: {transcript_file}")
            
        except Exception as e:
            self.logger.error(f"Transcription error for {video_file}: {e}")
            
    def process_documents(self):
        """Process all downloaded documents using the document processor."""
        self.logger.info("Processing downloaded documents...")
        
        # Process documents in resources directory
        result = self.doc_processor.process_directory(self.resources_dir, recursive=False)
        
        if result.get('success'):
            self.logger.info(f"Successfully processed {result.get('files_processed', 0)} documents")
            
            # Store document processing results
            self.processed_files.setdefault("documents", {})
            for file_result in result.get('results', []):
                file_path = file_result['file']
                processing_result = file_result['result']
                
                if processing_result.get('success'):
                    self.processed_files["documents"][file_path] = {
                        "markdown_file": processing_result.get('output_file'),
                        "method": processing_result.get('method'),
                        "processed_date": datetime.now().isoformat(),
                        "character_count": processing_result.get('character_count', 0)
                    }
                    
            # Save processing statistics
            doc_stats = self.doc_processor.get_statistics()
            self.logger.info(f"Document processing statistics: {doc_stats}")
            
        else:
            self.logger.error(f"Document processing failed: {result.get('error', 'Unknown error')}")
            
    def create_ai_index(self):
        """Create comprehensive AI-readable index of all content."""
        self.logger.info("Creating AI-readable index...")
        
        index_data = {
            "created": datetime.now().isoformat(),
            "base_url": self.base_url,
            "summary": {
                "total_pages": len(self.processed_files.get("pages", {})),
                "total_videos": len(self.processed_files.get("videos", {})),
                "total_resources": len(self.processed_files.get("resources", {})),
                "total_documents": len(self.processed_files.get("documents", {})),
                "total_transcripts": len([v for v in self.processed_files.get("videos", {}).values() if v.get("transcribed")])
            },
            "content": {
                "pages": self.processed_files.get("pages", {}),
                "videos": self.processed_files.get("videos", {}),
                "resources": self.processed_files.get("resources", {}),
                "documents": self.processed_files.get("documents", {})
            }
        }
        
        # Save main index
        index_file = self.output_dir / "ai_content_index.json"
        with open(index_file, 'w', encoding='utf-8') as f:
            json.dump(index_data, f, indent=2)
            
        # Create searchable text index
        search_index_file = self.output_dir / "searchable_content.txt"
        with open(search_index_file, 'w', encoding='utf-8') as f:
            f.write("# Creatio Academy - Complete Content Index\n")
            f.write(f"Generated: {datetime.now().isoformat()}\n\n")
            
            # Add page content
            f.write("## Web Pages\n\n")
            for page_path, page_data in self.processed_files.get("pages", {}).items():
                f.write(f"### {page_data.get('title', 'Untitled')}\n")
                f.write(f"**Source:** {page_path}\n")
                if Path(page_data.get('markdown_file', '')).exists():
                    try:
                        with open(page_data['markdown_file'], 'r', encoding='utf-8') as md_file:
                            f.write(md_file.read())
                    except Exception as e:
                        f.write(f"Error reading markdown: {e}")
                f.write("\n\n---\n\n")
                
            # Add video transcripts
            f.write("## Video Transcripts\n\n")
            for video_url, video_data in self.processed_files.get("videos", {}).items():
                if video_data.get("transcribed") and video_data.get("transcript_file"):
                    f.write(f"### Video: {Path(video_data['video_file']).stem}\n")
                    f.write(f"**Source:** {video_url}\n")
                    try:
                        with open(video_data['transcript_file'], 'r', encoding='utf-8') as trans_file:
                            f.write(trans_file.read())
                    except Exception as e:
                        f.write(f"Error reading transcript: {e}")
                    f.write("\n\n---\n\n")
            
            # Add processed documents
            f.write("## Processed Documents\n\n")
            for document_path, document_data in self.processed_files.get("documents", {}).items():
                f.write(f"### Document: {Path(document_path).name}\n")
                f.write(f"**Source:** {document_path}\n")
                f.write(f"**Processing Method:** {document_data.get('method', 'Unknown')}\n")
                if Path(document_data.get('markdown_file', '')).exists():
                    try:
                        with open(document_data['markdown_file'], 'r', encoding='utf-8') as doc_file:
                            f.write(doc_file.read())
                    except Exception as e:
                        f.write(f"Error reading document: {e}")
                f.write("\n\n---\n\n")
                    
        self.logger.info(f"AI-readable index created: {index_file}")
        self.logger.info(f"Searchable content created: {search_index_file}")
        
    def generate_report(self):
        """Generate comprehensive processing report."""
        report_file = self.output_dir / "processing_report.md"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("# Creatio Academy Content Processing Report\n\n")
            f.write(f"**Generated:** {datetime.now().isoformat()}\n")
            f.write(f"**Base URL:** {self.base_url}\n\n")
            
            # Summary statistics
            f.write("## Summary\n\n")
            f.write(f"- **Web Pages Processed:** {len(self.processed_files.get('pages', {}))}\n")
            f.write(f"- **Videos Downloaded:** {len(self.processed_files.get('videos', {}))}\n")
            f.write(f"- **Videos Transcribed:** {len([v for v in self.processed_files.get('videos', {}).values() if v.get('transcribed')])}\n")
            f.write(f"- **Resources Downloaded:** {len(self.processed_files.get('resources', {}))}\n\n")
            
            # Directory structure
            f.write("## Directory Structure\n\n")
            f.write("```\n")
            f.write(f"{self.output_dir}/\n")
            f.write("├── videos/           # Downloaded video files\n")
            f.write("├── transcripts/      # Video transcriptions\n")
            f.write("├── resources/        # Downloaded resources (PDFs, images, etc.)\n")
            f.write("├── pages/            # Web pages converted to markdown\n")
            f.write("├── ai_content_index.json      # Structured content index\n")
            f.write("├── searchable_content.txt     # AI-readable full content\n")
            f.write("└── processing_report.md       # This report\n")
            f.write("```\n\n")
            
            # Content details
            f.write("## Processed Content Details\n\n")
            
            # Videos
            f.write("### Videos\n\n")
            for video_url, video_data in self.processed_files.get("videos", {}).items():
                f.write(f"- **{Path(video_data.get('video_file', '')).name}**\n")
                f.write(f"  - Source: {video_url}\n")
                f.write(f"  - Transcribed: {'Yes' if video_data.get('transcribed') else 'No'}\n")
                f.write(f"  - Downloaded: {video_data.get('download_date', 'Unknown')}\n\n")
                
        self.logger.info(f"Processing report created: {report_file}")
        
    def run_full_pipeline(self):
        """Run the complete content processing pipeline."""
        self.logger.info("Starting complete Creatio Academy content processing pipeline...")
        
        try:
            # Step 1: Crawl website
            self.crawl_website()
            
            # Step 2: Extract URLs from pages
            self.extract_urls_from_pages()
            
            # Step 3: Download videos
            self.download_videos()
            
            # Step 4: Process downloaded documents
            self.process_documents()
            
            # Step 5: Create AI index
            self.create_ai_index()
            
            # Step 5: Generate report
            self.generate_report()
            
            # Save final progress
            self.save_progress()
            
            self.logger.info("Content processing pipeline completed successfully!")
            
        except Exception as e:
            self.logger.error(f"Pipeline failed: {e}")
            self.save_progress()
            raise


def main():
    """Main entry point."""
    processor = CreatioContentProcessor()
    processor.run_full_pipeline()


if __name__ == "__main__":
    main()
