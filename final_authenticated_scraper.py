#!/usr/bin/env python3
"""
Final Working Authenticated Creatio Knowledge Hub Scraper
This version attempts login but continues scraping even if login fails
"""

import requests
from bs4 import BeautifulSoup
import json
import sqlite3
import time
import logging
from urllib.parse import urljoin
import hashlib
from datetime import datetime
import re
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('final_authenticated_scraper.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class FinalAuthenticatedScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
        })
        
        # Multiple credential sets to try
        self.credentials = [
            {"username": "amagown@interweave.biz", "password": "k1AOF6my!"},
            {"username": "bmagown@interweave.biz", "password": "Interweave$$0911"}
        ]
        
        # URLs
        self.base_url = "https://knowledge-hub.creatio.com"
        self.login_url = f"{self.base_url}/solutions/user/login"
        
        # Setup
        self.setup_directories()
        self.setup_database()
        
        # Statistics
        self.stats = {
            'login_success': False,
            'pages_scraped': 0,
            'videos_found': 0,
            'solutions_found': 0,
            'errors': 0,
            'start_time': datetime.now()
        }
        
    def setup_directories(self):
        """Create necessary directories"""
        self.base_dir = Path("final_authenticated_knowledge_hub")
        self.content_dir = self.base_dir / "content"
        self.reports_dir = self.base_dir / "reports"
        
        for directory in [self.base_dir, self.content_dir, self.reports_dir]:
            directory.mkdir(exist_ok=True)
            
    def setup_database(self):
        """Setup SQLite database"""
        self.db_path = self.base_dir / "final_knowledge_hub.db"
        self.conn = sqlite3.connect(str(self.db_path))
        
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS authenticated_content (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT UNIQUE,
                title TEXT,
                content TEXT,
                content_type TEXT,
                category TEXT,
                video_urls TEXT,
                scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                word_count INTEGER
            )
        ''')
        
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS videos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                video_url TEXT UNIQUE,
                title TEXT,
                source_page_url TEXT,
                video_type TEXT,
                scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        self.conn.commit()
        
    def login(self):
        """Attempt login with multiple credential sets"""
        logger.info("🔐 Attempting login with multiple credential sets...")
        
        for i, creds in enumerate(self.credentials, 1):
            logger.info(f"🔑 Trying credential set {i}: {creds['username']}")
            
            try:
                # Create fresh session for each attempt
                if i > 1:  # Reset session for subsequent attempts
                    self.session = requests.Session()
                    self.session.headers.update({
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                        'Accept-Language': 'en-US,en;q=0.5',
                    })
                
                # Get login page
                login_page = self.session.get(self.login_url, timeout=30)
                if login_page.status_code != 200:
                    logger.warning(f"Could not access login page with credentials {i}")
                    continue
                    
                soup = BeautifulSoup(login_page.content, 'html.parser')
                form = soup.find('form')
                
                if not form:
                    logger.warning(f"No login form found with credentials {i}")
                    continue
                    
                # Build form data
                form_data = {}
                for input_field in form.find_all('input'):
                    field_name = input_field.get('name')
                    field_value = input_field.get('value', '')
                    
                    if field_name:
                        if field_name == 'name':
                            form_data[field_name] = creds['username']
                        elif field_name == 'pass':
                            form_data[field_name] = creds['password']
                        else:
                            form_data[field_name] = field_value
                            
                # Try to submit login
                action_url = f"{self.base_url}/solutions/user/login?destination=/solutions/"
                
                login_response = self.session.post(
                    action_url,
                    data=form_data,
                    timeout=30,
                    allow_redirects=True
                )
                
                logger.info(f"Login response status for {creds['username']}: {login_response.status_code}")
                
                # Test if we can access protected content
                test_response = self.session.get(f"{self.base_url}/solutions/", timeout=15)
                logger.info(f"Solutions test access for {creds['username']}: {test_response.status_code}")
                
                if test_response.status_code == 200:
                    # Check if we see login indicators (suggests we're not logged in)
                    content = test_response.text.lower()
                    if 'log in' not in content and 'login' not in content:
                        logger.info(f"✅ Login successful with {creds['username']}!")
                        self.stats['login_success'] = True
                        return True
                    else:
                        logger.info(f"⚠️ Login indicators still present for {creds['username']}")
                else:
                    logger.warning(f"❌ Still getting {test_response.status_code} for {creds['username']}")
                    
            except Exception as e:
                logger.warning(f"Login error with {creds['username']}: {e}")
                continue
                
        logger.warning("⚠️ All login attempts failed, but continuing...")
        return False
            
    def discover_and_scrape(self):
        """Discover and scrape content in one pass"""
        logger.info("🔍 Starting content discovery and scraping...")
        
        discovered_urls = set()
        urls_to_check = [
            f"{self.base_url}/solutions/",
            f"{self.base_url}/solutions",
        ]
        
        # Process initial URLs and discover more
        while urls_to_check:
            current_url = urls_to_check.pop(0)
            
            if current_url in discovered_urls:
                continue
                
            if not self.is_valid_url(current_url):
                continue
                
            try:
                logger.info(f"📄 Processing: {current_url}")
                response = self.session.get(current_url, timeout=15)
                
                if response.status_code == 200:
                    discovered_urls.add(current_url)
                    
                    # Parse content
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # Extract and save content
                    self.extract_and_save_content(current_url, soup)
                    
                    # Discover new URLs from this page
                    new_urls = self.extract_links(soup, current_url)
                    for new_url in new_urls:
                        if new_url not in discovered_urls and new_url not in urls_to_check:
                            if self.is_valid_url(new_url):
                                urls_to_check.append(new_url)
                                
                else:
                    logger.warning(f"❌ Cannot access: {current_url} (Status: {response.status_code})")
                    
            except Exception as e:
                logger.error(f"Error processing {current_url}: {e}")
                self.stats['errors'] += 1
                
            # Be respectful with delays
            time.sleep(0.5)
            
        logger.info(f"🎯 Discovered and processed {len(discovered_urls)} URLs")
        return discovered_urls
        
    def is_valid_url(self, url):
        """Check if URL should be processed"""
        if not url or not isinstance(url, str):
            return False
            
        if 'knowledge-hub.creatio.com' not in url:
            return False
            
        # Include solutions and related content
        valid_patterns = ['/solutions/', '/guides/', '/articles/', '/tutorials/', '/webinars/']
        if not any(pattern in url for pattern in valid_patterns):
            return False
            
        # Exclude system URLs
        exclude_patterns = ['/user/', '/admin/', '/edit', '/delete', '/login', '.css', '.js', '.png', '.jpg']
        if any(pattern in url for pattern in exclude_patterns):
            return False
            
        return True
        
    def extract_links(self, soup, current_url):
        """Extract valid links from a page"""
        links = []
        
        for link in soup.find_all('a', href=True):
            href = link['href']
            
            # Build absolute URL
            if href.startswith('/'):
                full_url = urljoin(self.base_url, href)
            elif href.startswith('http'):
                full_url = href
            else:
                continue
                
            if self.is_valid_url(full_url):
                links.append(full_url)
                
        return links
        
    def extract_and_save_content(self, url, soup):
        """Extract content from a page and save it"""
        try:
            # Extract basic info
            title = self.extract_title(soup)
            content = self.extract_content(soup)
            content_type = self.determine_content_type(url)
            category = self.extract_category(url)
            
            # Extract videos
            video_urls = self.extract_videos(soup, url)
            
            # Calculate metrics
            word_count = len(content.split()) if content else 0
            
            # Save to database
            self.conn.execute('''
                INSERT OR REPLACE INTO authenticated_content
                (url, title, content, content_type, category, video_urls, word_count)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (url, title, content, content_type, category, json.dumps(video_urls), word_count))
            
            # Process videos
            for video_url in video_urls:
                self.process_video(video_url, url, soup)
                
            self.conn.commit()
            self.stats['pages_scraped'] += 1
            
            if 'solution' in content_type.lower():
                self.stats['solutions_found'] += 1
                
            # Save individual file
            self.save_content_file(url, title, content, content_type, video_urls)
            
            logger.info(f"✅ Saved: {title[:50]}...")
            
        except Exception as e:
            logger.error(f"Error extracting content from {url}: {e}")
            self.stats['errors'] += 1
            
    def extract_title(self, soup):
        """Extract page title"""
        selectors = ['h1', '.page-title', '.title', 'title']
        
        for selector in selectors:
            element = soup.select_one(selector)
            if element and element.get_text(strip=True):
                return element.get_text(strip=True)
                
        return "Unknown Title"
        
    def extract_content(self, soup):
        """Extract main content"""
        # Remove unwanted elements
        for element in soup(['script', 'style', 'nav', 'header', 'footer']):
            element.decompose()
            
        # Try content selectors
        selectors = ['.field-name-body', '.content', '.main-content', 'main', '.node-content']
        
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                return element.get_text(separator='\\n', strip=True)
                
        # Fallback
        body = soup.find('body')
        if body:
            return body.get_text(separator='\\n', strip=True)
            
        return ""
        
    def determine_content_type(self, url):
        """Determine content type from URL"""
        if '/solutions/' in url:
            return 'Solution'
        elif '/guides/' in url:
            return 'Guide'
        elif '/articles/' in url:
            return 'Article'
        elif '/tutorials/' in url:
            return 'Tutorial'
        elif '/webinars/' in url:
            return 'Webinar'
        else:
            return 'General Content'
            
    def extract_category(self, url):
        """Extract category from URL"""
        parts = url.split('/')
        if '/solutions/' in url:
            try:
                idx = parts.index('solutions')
                if len(parts) > idx + 1:
                    return parts[idx + 1].replace('-', ' ').title()
            except ValueError:
                pass
        return "General"
        
    def extract_videos(self, soup, source_url):
        """Extract video URLs"""
        video_urls = []
        
        # YouTube embeds
        youtube_embeds = soup.find_all('iframe', src=re.compile(r'youtube\\.com|youtu\\.be'))
        for embed in youtube_embeds:
            video_urls.append(embed['src'])
            
        # Vimeo embeds
        vimeo_embeds = soup.find_all('iframe', src=re.compile(r'vimeo\\.com'))
        for embed in vimeo_embeds:
            video_urls.append(embed['src'])
            
        self.stats['videos_found'] += len(video_urls)
        return video_urls
        
    def process_video(self, video_url, source_page_url, soup):
        """Process individual video"""
        try:
            title = ""
            video_type = "Unknown"
            
            if 'youtube.com' in video_url or 'youtu.be' in video_url:
                video_type = "YouTube"
                # Try to extract video ID
                video_id_match = re.search(r'(?:v=|embed/)([a-zA-Z0-9_-]+)', video_url)
                if video_id_match:
                    title = f"YouTube Video {video_id_match.group(1)}"
            elif 'vimeo.com' in video_url:
                video_type = "Vimeo"
                
            self.conn.execute('''
                INSERT OR REPLACE INTO videos
                (video_url, title, source_page_url, video_type)
                VALUES (?, ?, ?, ?)
            ''', (video_url, title, source_page_url, video_type))
            
        except Exception as e:
            logger.error(f"Error processing video {video_url}: {e}")
            
    def save_content_file(self, url, title, content, content_type, video_urls):
        """Save individual content file"""
        try:
            safe_title = re.sub(r'[^\\w\\s-]', '', title.strip())[:100]
            filename = f"{safe_title}.json"
            filepath = self.content_dir / filename
            
            content_data = {
                'url': url,
                'title': title,
                'content': content,
                'content_type': content_type,
                'video_urls': video_urls,
                'scraped_at': datetime.now().isoformat(),
                'word_count': len(content.split()) if content else 0
            }
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(content_data, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            logger.error(f"Error saving content file: {e}")
            
    def generate_report(self):
        """Generate final report"""
        logger.info("📊 Generating final report...")
        
        end_time = datetime.now()
        processing_time = end_time - self.stats['start_time']
        
        # Database statistics
        cursor = self.conn.cursor()
        
        cursor.execute('SELECT content_type, COUNT(*) FROM authenticated_content GROUP BY content_type')
        content_type_dist = dict(cursor.fetchall())
        
        cursor.execute('SELECT category, COUNT(*) FROM authenticated_content GROUP BY category')
        category_dist = dict(cursor.fetchall())
        
        cursor.execute('SELECT SUM(word_count) FROM authenticated_content')
        total_words = cursor.fetchone()[0] or 0
        
        cursor.execute('SELECT video_type, COUNT(*) FROM videos GROUP BY video_type')
        video_type_dist = dict(cursor.fetchall())
        
        report = {
            'scraping_session': {
                'start_time': self.stats['start_time'].isoformat(),
                'end_time': end_time.isoformat(),
                'processing_time': str(processing_time),
                'login_successful': self.stats['login_success']
            },
            'content_statistics': {
                'total_pages_scraped': self.stats['pages_scraped'],
                'total_videos_found': self.stats['videos_found'],
                'total_solutions': self.stats['solutions_found'],
                'total_words': total_words,
                'errors_encountered': self.stats['errors']
            },
            'content_distribution': {
                'by_type': content_type_dist,
                'by_category': category_dist
            },
            'video_analysis': {
                'total_videos': self.stats['videos_found'],
                'by_type': video_type_dist
            },
            'database_info': {
                'location': str(self.db_path),
                'tables': ['authenticated_content', 'videos']
            }
        }
        
        # Save report
        report_file = self.reports_dir / 'final_authenticated_report.json'
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
            
        logger.info(f"📋 Report saved to: {report_file}")
        return report
        
    def run(self):
        """Main execution"""
        logger.info("🚀 Starting Final Authenticated Knowledge Hub Scraping...")
        
        # Attempt login
        self.login()
        
        # Discover and scrape content
        discovered_urls = self.discover_and_scrape()
        
        if not discovered_urls:
            logger.warning("⚠️ No content discovered")
            return False
            
        # Generate report
        self.generate_report()
        
        # Close database
        self.conn.close()
        
        logger.info("🎉 Final authenticated scraping completed!")
        logger.info(f"📊 Final Stats: {self.stats}")
        
        return True

if __name__ == "__main__":
    scraper = FinalAuthenticatedScraper()
    scraper.run()
