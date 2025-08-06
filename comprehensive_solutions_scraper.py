#!/usr/bin/env python3
"""
Comprehensive Creatio Solutions Hub Scraper
Scrapes https://knowledge-hub.creatio.com/solutions/ and all linked content
Downloads and processes all media, images, videos, documents
Structures data for AI/API consumption
"""
from utils.cli import base_parser
import argparse, json, sys

import requests
from bs4 import BeautifulSoup
import json
import os
import sqlite3
import hashlib
import time
import mimetypes
import re
from urllib.parse import urljoin, urlparse, unquote
from pathlib import Path
import logging
from datetime import datetime
import subprocess
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
import html2text
import base64
from PIL import Image
import cv2
import numpy as np

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('solutions_scraping.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class CreatioSolutionsScraper:
    def __init__(self, base_url="https://knowledge-hub.creatio.com/solutions/", output_dir="ai_knowledge_hub"):
        self.base_url = base_url
        self.output_dir = Path(output_dir)
        self.scraped_urls = set()
        self.download_stats = {
            'pages': 0,
            'images': 0,
            'videos': 0,
            'documents': 0,
            'gifs': 0,
            'errors': 0
        }

        # Create directory structure
        self.setup_directories()

        # Setup database
        self.setup_database()

        # Session with enhanced headers to mimic real browser
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Linux"',
            'Cache-Control': 'max-age=0',
            'DNT': '1'
        })

        # HTML to text converter
        self.h = html2text.HTML2Text()
        self.h.ignore_links = False
        self.h.body_width = 0

    def setup_directories(self):
        """Create the directory structure for organized content storage"""
        dirs = [
            'solutions_hub',
            'solutions_hub/pages',
            'solutions_hub/images',
            'solutions_hub/videos',
            'solutions_hub/documents',
            'solutions_hub/gifs',
            'solutions_hub/screenshots',
            'solutions_hub/transcripts',
            'solutions_hub/metadata',
            'solutions_hub/search_data'
        ]

        for dir_name in dirs:
            (self.output_dir / dir_name).mkdir(parents=True, exist_ok=True)

    def setup_database(self):
        """Setup SQLite database for storing scraped content metadata"""
        self.db_path = self.output_dir / 'solutions_knowledge.db'
        self.conn = sqlite3.connect(str(self.db_path), check_same_thread=False)

        # Create tables
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS scraped_content (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT UNIQUE,
                title TEXT,
                content_type TEXT,
                file_path TEXT,
                description TEXT,
                tags TEXT,
                scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                file_size INTEGER,
                checksum TEXT
            )
        ''')

        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS media_files (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT UNIQUE,
                local_path TEXT,
                media_type TEXT,
                file_size INTEGER,
                duration REAL,
                dimensions TEXT,
                checksum TEXT,
                transcription TEXT,
                scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS page_links (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source_url TEXT,
                target_url TEXT,
                link_text TEXT,
                link_type TEXT,
                scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        self.conn.commit()

    def get_file_hash(self, file_path):
        """Generate MD5 hash of file for deduplication"""
        hash_md5 = hashlib.md5()
        try:
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
        except:
            return None

    def clean_filename(self, filename):
        """Clean filename for filesystem compatibility"""
        # Remove/replace problematic characters
        filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
        filename = re.sub(r'\s+', '_', filename)
        filename = filename.strip('._')
        return filename[:200]  # Limit length

    def download_file(self, url, local_path, timeout=30):
        """Download a file with proper error handling"""
        try:
            # Check if file already exists
            if os.path.exists(local_path):
                logger.info(f"File already exists: {local_path}")
                return True

            response = self.session.get(url, timeout=timeout, stream=True)
            response.raise_for_status()

            os.makedirs(os.path.dirname(local_path), exist_ok=True)

            with open(local_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)

            logger.info(f"Downloaded: {url} -> {local_path}")
            return True

        except Exception as e:
            logger.error(f"Failed to download {url}: {str(e)}")
            self.download_stats['errors'] += 1
            return False

    def extract_media_info(self, file_path):
        """Extract metadata from media files"""
        info = {}

        try:
            if file_path.suffix.lower() in ['.mp4', '.avi', '.mov', '.wmv', '.flv']:
                # Video file
                cap = cv2.VideoCapture(str(file_path))
                if cap.isOpened():
                    fps = cap.get(cv2.CAP_PROP_FPS)
                    frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
                    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

                    info['duration'] = frame_count / fps if fps > 0 else 0
                    info['dimensions'] = f"{width}x{height}"
                    info['fps'] = fps
                    cap.release()

            elif file_path.suffix.lower() in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']:
                # Image file
                try:
                    with Image.open(file_path) as img:
                        info['dimensions'] = f"{img.width}x{img.height}"
                        info['format'] = img.format
                        if hasattr(img, 'is_animated'):
                            info['animated'] = img.is_animated
                except:
                    pass

        except Exception as e:
            logger.warning(f"Could not extract media info for {file_path}: {str(e)}")

        return info

    def transcribe_video(self, video_path):
        """Extract and transcribe audio from video files"""
        try:
            # Extract audio using ffmpeg
            audio_path = video_path.with_suffix('.wav')
            cmd = [
                'ffmpeg', '-i', str(video_path),
                '-vn', '-acodec', 'pcm_s16le',
                '-ar', '16000', '-ac', '1',
                str(audio_path), '-y'
            ]

            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)

            if result.returncode == 0 and audio_path.exists():
                # Here you would integrate with a speech-to-text service
                # For now, we'll create a placeholder
                transcript_path = video_path.with_suffix('.transcript.txt')
                with open(transcript_path, 'w', encoding='utf-8') as f:
                    f.write(f"[Transcript placeholder for {video_path.name}]\n")
                    f.write("To enable transcription, integrate with Whisper API or similar service.\n")

                # Clean up audio file
                if audio_path.exists():
                    os.remove(audio_path)

                return str(transcript_path)

        except Exception as e:
            logger.error(f"Failed to transcribe {video_path}: {str(e)}")

        return None

    def take_screenshot(self, url, output_path):
        """Take screenshot of webpage using selenium (optional)"""
        try:
            # Placeholder for screenshot functionality
            # You would need to install selenium and a webdriver
            logger.info(f"Screenshot placeholder for {url}")
            return None
        except Exception as e:
            logger.error(f"Failed to take screenshot of {url}: {str(e)}")
            return None

    def process_images(self, soup, page_url, page_dir):
        """Download and process all images from a page"""
        images = soup.find_all(['img', 'picture', 'source'])

        for img in images:
            img_url = None

            # Get image URL from various attributes
            for attr in ['src', 'data-src', 'srcset']:
                if img.get(attr):
                    img_url = img.get(attr)
                    break

            if not img_url:
                continue

            # Handle srcset (take first URL)
            if 'srcset' in img_url:
                img_url = img_url.split(',')[0].split()[0]

            img_url = urljoin(page_url, img_url)

            if img_url in self.scraped_urls:
                continue

            self.scraped_urls.add(img_url)

            # Generate filename
            parsed_url = urlparse(img_url)
            filename = os.path.basename(parsed_url.path)
            if not filename or '.' not in filename:
                filename = f"image_{len(self.scraped_urls)}.jpg"

            filename = self.clean_filename(filename)

            # Determine if it's a GIF or regular image
            if filename.lower().endswith('.gif'):
                local_path = self.output_dir / 'solutions_hub' / 'gifs' / filename
                media_type = 'gif'
                self.download_stats['gifs'] += 1
            else:
                local_path = self.output_dir / 'solutions_hub' / 'images' / filename
                media_type = 'image'
                self.download_stats['images'] += 1

            if self.download_file(img_url, local_path):
                # Extract metadata
                info = self.extract_media_info(local_path)
                file_size = local_path.stat().st_size if local_path.exists() else 0
                checksum = self.get_file_hash(local_path)

                # Store in database
                self.conn.execute('''
                    INSERT OR REPLACE INTO media_files
                    (url, local_path, media_type, file_size, dimensions, checksum)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (img_url, str(local_path), media_type, file_size,
                      info.get('dimensions', ''), checksum))

    def process_videos(self, soup, page_url, page_dir):
        """Download and process all videos from a page"""
        # Find video elements
        videos = soup.find_all(['video', 'source'])

        # Also look for embedded videos (YouTube, Vimeo, etc.)
        embeds = soup.find_all(['iframe', 'embed'])

        for video in videos:
            video_url = video.get('src') or video.get('data-src')
            if not video_url:
                continue

            video_url = urljoin(page_url, video_url)

            if video_url in self.scraped_urls:
                continue

            self.scraped_urls.add(video_url)

            # Generate filename
            parsed_url = urlparse(video_url)
            filename = os.path.basename(parsed_url.path)
            if not filename or '.' not in filename:
                filename = f"video_{len(self.scraped_urls)}.mp4"

            filename = self.clean_filename(filename)
            local_path = self.output_dir / 'solutions_hub' / 'videos' / filename

            if self.download_file(video_url, local_path):
                # Extract video metadata
                info = self.extract_media_info(local_path)
                file_size = local_path.stat().st_size if local_path.exists() else 0
                checksum = self.get_file_hash(local_path)

                # Transcribe video
                transcript_path = self.transcribe_video(local_path)

                # Store in database
                self.conn.execute('''
                    INSERT OR REPLACE INTO media_files
                    (url, local_path, media_type, file_size, duration, dimensions, checksum, transcription)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (video_url, str(local_path), 'video', file_size,
                      info.get('duration', 0), info.get('dimensions', ''),
                      checksum, transcript_path))

                self.download_stats['videos'] += 1

        # Process embedded videos
        for embed in embeds:
            src = embed.get('src')
            if not src:
                continue

            # Check for YouTube, Vimeo, etc.
            if any(domain in src for domain in ['youtube.com', 'youtu.be', 'vimeo.com']):
                # Create metadata file for embedded video
                embed_data = {
                    'url': src,
                    'type': 'embedded_video',
                    'platform': 'youtube' if 'youtube' in src or 'youtu.be' in src else 'vimeo' if 'vimeo' in src else 'unknown',
                    'found_on': page_url,
                    'scraped_at': datetime.now().isoformat()
                }

                embed_filename = f"embed_{hashlib.md5(src.encode()).hexdigest()[:8]}.json"
                embed_path = self.output_dir / 'solutions_hub' / 'videos' / embed_filename

                with open(embed_path, 'w', encoding='utf-8') as f:
                    json.dump(embed_data, f, indent=2)

    def process_documents(self, soup, page_url, page_dir):
        """Download and process documents (PDFs, Word docs, etc.)"""
        # Find links to documents
        doc_extensions = ['.pdf', '.doc', '.docx', '.ppt', '.pptx', '.xls', '.xlsx', '.txt', '.rtf']

        links = soup.find_all('a', href=True)

        for link in links:
            href = link.get('href')
            if not href:
                continue

            # Check if it's a document
            if not any(ext in href.lower() for ext in doc_extensions):
                continue

            doc_url = urljoin(page_url, href)

            if doc_url in self.scraped_urls:
                continue

            self.scraped_urls.add(doc_url)

            # Generate filename
            parsed_url = urlparse(doc_url)
            filename = os.path.basename(parsed_url.path)
            if not filename:
                filename = f"document_{len(self.scraped_urls)}.pdf"

            filename = self.clean_filename(filename)
            local_path = self.output_dir / 'solutions_hub' / 'documents' / filename

            if self.download_file(doc_url, local_path):
                file_size = local_path.stat().st_size if local_path.exists() else 0
                checksum = self.get_file_hash(local_path)

                # Store in database
                self.conn.execute('''
                    INSERT OR REPLACE INTO media_files
                    (url, local_path, media_type, file_size, checksum)
                    VALUES (?, ?, ?, ?, ?)
                ''', (doc_url, str(local_path), 'document', file_size, checksum))

                self.download_stats['documents'] += 1

    def extract_text_content(self, soup):
        """Extract clean text content from HTML"""
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()

        # Get text
        text = soup.get_text()

        # Clean up whitespace
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)

        return text

    def scrape_page(self, url, depth=0, max_depth=3, retry_count=0):
        """Scrape a single page and all its content"""
        if url in self.scraped_urls or depth > max_depth:
            return

        self.scraped_urls.add(url)

        try:
            logger.info(f"Scraping page (depth {depth}, attempt {retry_count + 1}): {url}")

            # Add random delay to seem more human-like
            import random
            time.sleep(random.uniform(1, 3))

            # Try different approaches for 403 errors
            response = None
            for attempt in range(3):
                try:
                    if attempt > 0:
                        # Change user agent on retry
                        user_agents = [
                            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                            'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/121.0'
                        ]
                        self.session.headers['User-Agent'] = random.choice(user_agents)

                    response = self.session.get(url, timeout=30, allow_redirects=True)

                    if response.status_code == 403:
                        logger.warning(f"403 Forbidden on attempt {attempt + 1}, trying alternative approach...")
                        # Try with different headers
                        headers = self.session.headers.copy()
                        headers.update({
                            'Referer': 'https://www.google.com/',
                            'X-Forwarded-For': f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}"
                        })
                        response = requests.get(url, headers=headers, timeout=30)

                    if response.status_code == 200:
                        break
                    elif response.status_code == 403 and attempt < 2:
                        time.sleep(random.uniform(2, 5))  # Wait before retry
                        continue
                    else:
                        response.raise_for_status()
                except requests.exceptions.RequestException as e:
                    if attempt == 2:  # Last attempt
                        raise e
                    time.sleep(random.uniform(1, 3))
                    continue

            if not response or response.status_code != 200:
                logger.error(f"Failed to get valid response after all attempts for {url}")
                return

            soup = BeautifulSoup(response.content, 'html.parser')

            # Extract page metadata
            title = soup.find('title')
            title = title.get_text().strip() if title else 'Untitled'

            description = soup.find('meta', attrs={'name': 'description'})
            description = description.get('content', '') if description else ''

            # Create page directory
            page_name = self.clean_filename(title) or f"page_{len(self.scraped_urls)}"
            page_dir = self.output_dir / 'solutions_hub' / 'pages' / page_name
            page_dir.mkdir(parents=True, exist_ok=True)

            # Save HTML content
            html_path = page_dir / 'content.html'
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(str(soup))

            # Convert to markdown for AI consumption
            markdown_content = self.h.handle(str(soup))
            markdown_path = page_dir / 'content.md'
            with open(markdown_path, 'w', encoding='utf-8') as f:
                f.write(markdown_content)

            # Extract clean text
            text_content = self.extract_text_content(soup)
            text_path = page_dir / 'content.txt'
            with open(text_path, 'w', encoding='utf-8') as f:
                f.write(text_content)

            # Create structured data for AI/API consumption
            structured_data = {
                'url': url,
                'title': title,
                'description': description,
                'scraped_at': datetime.now().isoformat(),
                'word_count': len(text_content.split()),
                'content': text_content,
                'markdown': markdown_content,
                'links': [],
                'media': {
                    'images': [],
                    'videos': [],
                    'documents': []
                }
            }

            # Process all media
            self.process_images(soup, url, page_dir)
            self.process_videos(soup, url, page_dir)
            self.process_documents(soup, url, page_dir)

            # Extract and follow links
            links = soup.find_all('a', href=True)
            for link in links:
                href = link.get('href')
                link_text = link.get_text().strip()

                if not href:
                    continue

                full_url = urljoin(url, href)

                # Store link information
                structured_data['links'].append({
                    'url': full_url,
                    'text': link_text,
                    'internal': 'creatio.com' in full_url
                })

                # Store in database
                self.conn.execute('''
                    INSERT OR REPLACE INTO page_links
                    (source_url, target_url, link_text, link_type)
                    VALUES (?, ?, ?, ?)
                ''', (url, full_url, link_text,
                      'internal' if 'creatio.com' in full_url else 'external'))

                # Follow internal links
                if ('creatio.com' in full_url and
                    full_url not in self.scraped_urls and
                    depth < max_depth):

                    # Add to queue for processing
                    self.scrape_page(full_url, depth + 1, max_depth)

            # Save structured data
            json_path = page_dir / 'structured_data.json'
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(structured_data, f, indent=2, ensure_ascii=False)

            # Store page in database
            file_size = sum(f.stat().st_size for f in page_dir.rglob('*') if f.is_file())
            checksum = hashlib.md5(text_content.encode()).hexdigest()

            self.conn.execute('''
                INSERT OR REPLACE INTO scraped_content
                (url, title, content_type, file_path, description, file_size, checksum)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (url, title, 'webpage', str(page_dir), description, file_size, checksum))

            self.download_stats['pages'] += 1
            self.conn.commit()

            logger.info(f"Successfully scraped: {title}")

        except Exception as e:
            logger.error(f"Failed to scrape {url}: {str(e)}")
            self.download_stats['errors'] += 1

    def create_search_index(self):
        """Create search index for AI/API consumption"""
        logger.info("Creating search index...")

        search_data = []

        # Index all scraped content
        cursor = self.conn.execute('''
            SELECT url, title, content_type, file_path, description
            FROM scraped_content
        ''')

        for row in cursor:
            url, title, content_type, file_path, description = row

            # Read content files
            content_text = ""
            structured_path = Path(file_path) / 'structured_data.json'

            if structured_path.exists():
                with open(structured_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    content_text = data.get('content', '')

            search_data.append({
                'id': hashlib.md5(url.encode()).hexdigest(),
                'url': url,
                'title': title,
                'type': content_type,
                'description': description,
                'content': content_text[:1000],  # First 1000 chars for search
                'file_path': file_path
            })

        # Save search index
        search_index_path = self.output_dir / 'solutions_hub' / 'search_data' / 'search_index.json'
        with open(search_index_path, 'w', encoding='utf-8') as f:
            json.dump(search_data, f, indent=2, ensure_ascii=False)

        logger.info(f"Search index created with {len(search_data)} entries")

    def generate_report(self):
        """Generate comprehensive scraping report"""
        report = {
            'scraping_session': {
                'started_at': datetime.now().isoformat(),
                'base_url': self.base_url,
                'total_urls_processed': len(self.scraped_urls)
            },
            'statistics': self.download_stats,
            'database_stats': {},
            'file_structure': {},
            'recommendations': []
        }

        # Get database statistics
        cursor = self.conn.execute('SELECT COUNT(*) FROM scraped_content')
        report['database_stats']['total_pages'] = cursor.fetchone()[0]

        cursor = self.conn.execute('SELECT COUNT(*) FROM media_files')
        report['database_stats']['total_media_files'] = cursor.fetchone()[0]

        cursor = self.conn.execute('SELECT COUNT(*) FROM page_links')
        report['database_stats']['total_links'] = cursor.fetchone()[0]

        # Calculate directory sizes
        solutions_dir = self.output_dir / 'solutions_hub'
        for subdir in solutions_dir.iterdir():
            if subdir.is_dir():
                size = sum(f.stat().st_size for f in subdir.rglob('*') if f.is_file())
                report['file_structure'][subdir.name] = {
                    'size_bytes': size,
                    'size_mb': round(size / (1024 * 1024), 2),
                    'file_count': len(list(subdir.rglob('*')))
                }

        # Add recommendations
        if report['statistics']['errors'] > 0:
            report['recommendations'].append(
                f"Review {report['statistics']['errors']} failed downloads in the log file"
            )

        if report['statistics']['videos'] > 0:
            report['recommendations'].append(
                "Consider integrating Whisper or similar for video transcription"
            )

        report['recommendations'].append(
            "Use the search_index.json file for AI/API queries"
        )

        # Save report
        report_path = self.output_dir / 'solutions_hub' / 'scraping_report.json'
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)

        return report

    def run(self):
        """Main scraping process"""
        logger.info(f"Starting comprehensive scraping of {self.base_url}")

        try:
            # Start with the main solutions page
            self.scrape_page(self.base_url, depth=0, max_depth=2)

            # Create search index
            self.create_search_index()

            # Generate report
            report = self.generate_report()

            logger.info("Scraping completed successfully!")
            logger.info(f"Statistics: {self.download_stats}")

            return report

        except Exception as e:
            logger.error(f"Scraping failed: {str(e)}")
            raise
        finally:
            self.conn.close()

if __name__ == "__main__":
    try:
        parser = base_parser("Comprehensive Creatio Solutions Hub scraper")
    except Exception:
        parser = argparse.ArgumentParser(description="Comprehensive Creatio Solutions Hub scraper")
        parser.add_argument("-c","--config", type=str, default="config.yaml")
        parser.add_argument("--in", dest="input_dir", default=None)
        parser.add_argument("--out", dest="output_dir", default="out")
        parser.add_argument("--limit", type=int, default=0)
        parser.add_argument("--format", choices=["json","ndjson"], default="json")
    args = parser.parse_args()

    # Emit machine-readable invocation summary first
    print(json.dumps({
        "tool": "comprehensive_solutions_scraper",
        "config": getattr(args, "config", "config.yaml"),
        "input_dir": getattr(args, "input_dir", None),
        "output_dir": getattr(args, "output_dir", "out"),
        "limit": getattr(args, "limit", 0),
        "format": getattr(args, "format", "json")
    }), flush=True)

    scraper = CreatioSolutionsScraper()
    report = scraper.run()

    print("\n" + "="*60)
    print("SCRAPING COMPLETED")
    print("="*60)
    print(f"Pages scraped: {report['statistics']['pages']}")
    print(f"Images downloaded: {report['statistics']['images']}")
    print(f"Videos downloaded: {report['statistics']['videos']}")
    print(f"Documents downloaded: {report['statistics']['documents']}")
    print(f"GIFs downloaded: {report['statistics']['gifs']}")
    print(f"Errors encountered: {report['statistics']['errors']}")
    print(f"\nContent stored in: ai_knowledge_hub/solutions_hub/")
    print(f"Database: ai_knowledge_hub/solutions_knowledge.db")
    print(f"Search index: ai_knowledge_hub/solutions_hub/search_data/search_index.json")
