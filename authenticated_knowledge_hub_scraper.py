#!/usr/bin/env python3
"""
Authenticated Creatio Knowledge Hub Scraper
Logs in and scrapes all restricted content including solutions, guides, and videos
"""

import requests
from bs4 import BeautifulSoup
import json
import sqlite3
import os
import time
import logging
from urllib.parse import urljoin, urlparse
import hashlib
from datetime import datetime
import re
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('authenticated_scraper.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class AuthenticatedKnowledgeHubScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # Credentials
        self.username = "amagown@interweave.biz"
        self.password = "k1AOF6my!"
        
        # Base URLs
        self.base_url = "https://knowledge-hub.creatio.com"
        self.login_url = f"{self.base_url}/solutions/user/login"
        
        # Setup directories
        self.setup_directories()
        
        # Setup database
        self.setup_database()
        
        # Statistics
        self.stats = {
            'login_success': False,
            'pages_scraped': 0,
            'videos_found': 0,
            'solutions_found': 0,
            'guides_found': 0,
            'articles_found': 0,
            'errors': 0,
            'start_time': datetime.now()
        }
        
    def setup_directories(self):
        """Create necessary directories"""
        self.base_dir = Path("authenticated_knowledge_hub")
        self.content_dir = self.base_dir / "content"
        self.media_dir = self.base_dir / "media"
        self.reports_dir = self.base_dir / "reports"
        
        for directory in [self.base_dir, self.content_dir, self.media_dir, self.reports_dir]:
            directory.mkdir(exist_ok=True)
            
    def setup_database(self):
        """Setup SQLite database for authenticated content"""
        self.db_path = self.base_dir / "authenticated_knowledge_hub.db"
        self.conn = sqlite3.connect(str(self.db_path))
        
        # Create tables
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS authenticated_content (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT UNIQUE,
                title TEXT,
                content TEXT,
                content_type TEXT,
                category TEXT,
                subcategory TEXT,
                tags TEXT,
                video_urls TEXT,
                image_urls TEXT,
                download_links TEXT,
                scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                content_hash TEXT,
                word_count INTEGER,
                difficulty_level TEXT,
                estimated_read_time INTEGER
            )
        ''')
        
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS videos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                video_url TEXT UNIQUE,
                title TEXT,
                description TEXT,
                duration TEXT,
                thumbnail_url TEXT,
                source_page_url TEXT,
                video_type TEXT,
                scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        self.conn.commit()
        
    def login(self):
        """Authenticate with Knowledge Hub"""
        logger.info("🔐 Attempting to login to Knowledge Hub...")
        
        try:
            # Get login page to extract any CSRF tokens or form data
            login_page = self.session.get(self.login_url, timeout=30)
            login_page.raise_for_status()
            
            soup = BeautifulSoup(login_page.content, 'html.parser')
            
            # Look for login form
            login_form = soup.find('form')
            if not login_form:
                logger.error("Could not find login form")
                return False
                
            # Extract form action and method
            form_action = login_form.get('action', self.login_url)
            if not form_action.startswith('http'):
                form_action = urljoin(self.base_url, form_action)
                
            # Prepare login data - try different field names
            login_data = {}
            
            # Look for all form fields and identify login fields
            username_field = None
            password_field = None
            
            for input_field in login_form.find_all('input'):
                field_name = input_field.get('name')
                field_value = input_field.get('value', '')
                field_type = input_field.get('type', 'text')
                
                if field_name:
                    # Identify username/email field
                    if field_type in ['email', 'text'] and any(x in field_name.lower() for x in ['mail', 'user', 'login', 'name']):
                        username_field = field_name
                        login_data[field_name] = self.username
                    # Identify password field
                    elif field_type == 'password':
                        password_field = field_name
                        login_data[field_name] = self.password
                    # Include hidden fields (CSRF tokens, etc.)
                    elif field_type == 'hidden':
                        login_data[field_name] = field_value
                        
            # Fallback field names if not detected
            if not username_field:
                login_data['name'] = self.username
                login_data['mail'] = self.username
                login_data['email'] = self.username
            
            if not password_field:
                login_data['pass'] = self.password
                login_data['password'] = self.password
                    
            logger.info(f"Submitting login form to: {form_action}")
            
            # Submit login form
            login_response = self.session.post(
                form_action,
                data=login_data,
                timeout=30,
                allow_redirects=True
            )
            
            # Check if login was successful
            if login_response.status_code == 200:
                # Check for successful login indicators
                response_text = login_response.text.lower()
                
                # Negative indicators (still on login page)
                if any(indicator in response_text for indicator in ['login', 'sign in', 'password', 'invalid credentials']):
                    # Try alternative login approach
                    return self.try_alternative_login()
                else:
                    logger.info("✅ Login successful!")
                    self.stats['login_success'] = True
                    return True
            else:
                logger.error(f"Login failed with status code: {login_response.status_code}")
                return self.try_alternative_login()
                
        except Exception as e:
            logger.error(f"Login error: {str(e)}")
            return self.try_alternative_login()
            
    def try_alternative_login(self):
        """Try alternative login methods"""
        logger.info("🔄 Trying alternative login approaches...")
        
        # Method 1: Direct POST to common login endpoints
        alternative_endpoints = [
            f"{self.base_url}/auth/login",
            f"{self.base_url}/api/login",
            f"{self.base_url}/user/login",
            f"{self.base_url}/account/login"
        ]
        
        for endpoint in alternative_endpoints:
            try:
                login_data = {
                    'username': self.username,
                    'password': self.password,
                    'email': self.username
                }
                
                response = self.session.post(endpoint, data=login_data, timeout=15)
                if response.status_code == 200 and 'error' not in response.text.lower():
                    logger.info(f"✅ Alternative login successful via: {endpoint}")
                    self.stats['login_success'] = True
                    return True
                    
            except Exception as e:
                continue
                
        # Method 2: Try with JSON payload
        try:
            json_login_data = {
                'email': self.username,
                'password': self.password
            }
            
            response = self.session.post(
                self.login_url,
                json=json_login_data,
                headers={'Content-Type': 'application/json'},
                timeout=15
            )
            
            if response.status_code in [200, 302]:
                logger.info("✅ JSON login successful!")
                self.stats['login_success'] = True
                return True
                
        except Exception as e:
            pass
            
        logger.warning("⚠️ All login methods failed. Proceeding with session cookies if any...")
        return False
        
    def discover_content_urls(self):
        """Discover all accessible content URLs after authentication"""
        logger.info("🔍 Discovering authenticated content URLs...")
        
        content_urls = set()
        
        # Main discovery endpoints
        discovery_urls = [
            f"{self.base_url}/solutions",
            f"{self.base_url}/solutions/general",
            f"{self.base_url}/solutions/industry",
            f"{self.base_url}/solutions/crm",
            f"{self.base_url}/solutions/marketing",
            f"{self.base_url}/solutions/sales",
            f"{self.base_url}/solutions/service",
            f"{self.base_url}/solutions/healthcare",
            f"{self.base_url}/solutions/financial",
            f"{self.base_url}/solutions/education",
            f"{self.base_url}/solutions/real-estate",
            f"{self.base_url}/guides",
            f"{self.base_url}/best-practices",
            f"{self.base_url}/articles",
            f"{self.base_url}/tutorials",
            f"{self.base_url}/webinars",
            f"{self.base_url}/videos"
        ]
        
        for url in discovery_urls:
            try:
                logger.info(f"Checking: {url}")
                response = self.session.get(url, timeout=15)
                
                if response.status_code == 200:
                    logger.info(f"✅ Accessible: {url}")
                    content_urls.add(url)
                    
                    # Extract links from this page
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # Find all internal links
                    for link in soup.find_all('a', href=True):
                        href = link['href']
                        if href.startswith('/'):
                            full_url = urljoin(self.base_url, href)
                            if self.is_knowledge_content_url(full_url):
                                content_urls.add(full_url)
                        elif href.startswith(self.base_url):
                            if self.is_knowledge_content_url(href):
                                content_urls.add(href)
                                
                else:
                    logger.warning(f"❌ Not accessible: {url} (Status: {response.status_code})")
                    
            except Exception as e:
                logger.error(f"Error checking {url}: {str(e)}")
                self.stats['errors'] += 1
                
        logger.info(f"🎯 Discovered {len(content_urls)} content URLs")
        return list(content_urls)
        
    def is_knowledge_content_url(self, url):
        """Check if URL is a knowledge content URL"""
        knowledge_patterns = [
            '/solutions/',
            '/guides/',
            '/articles/',
            '/best-practices/',
            '/tutorials/',
            '/webinars/',
            '/videos/',
            '/case-studies/',
            '/implementations/'
        ]
        
        return any(pattern in url for pattern in knowledge_patterns)
        
    def scrape_content(self, url):
        """Scrape content from a specific URL"""
        try:
            logger.info(f"📄 Scraping: {url}")
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract basic information
            title = self.extract_title(soup)
            content = self.extract_content(soup)
            content_type = self.determine_content_type(url, soup)
            category, subcategory = self.extract_categories(url, soup)
            tags = self.extract_tags(soup)
            
            # Extract media
            video_urls = self.extract_videos(soup, url)
            image_urls = self.extract_images(soup, url)
            download_links = self.extract_downloads(soup, url)
            
            # Calculate metrics
            word_count = len(content.split()) if content else 0
            content_hash = hashlib.md5(content.encode()).hexdigest() if content else ""
            difficulty_level = self.determine_difficulty(content, tags)
            estimated_read_time = max(1, word_count // 200)  # 200 words per minute
            
            # Store in database
            self.conn.execute('''
                INSERT OR REPLACE INTO authenticated_content
                (url, title, content, content_type, category, subcategory, tags,
                 video_urls, image_urls, download_links, content_hash, word_count,
                 difficulty_level, estimated_read_time)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                url, title, content, content_type, category, subcategory,
                json.dumps(tags), json.dumps(video_urls), json.dumps(image_urls),
                json.dumps(download_links), content_hash, word_count,
                difficulty_level, estimated_read_time
            ))
            
            # Process videos separately
            for video_url in video_urls:
                self.process_video(video_url, url, soup)
                
            self.conn.commit()
            self.stats['pages_scraped'] += 1
            
            # Update content type stats
            if 'solution' in content_type.lower():
                self.stats['solutions_found'] += 1
            elif 'guide' in content_type.lower():
                self.stats['guides_found'] += 1
            elif 'article' in content_type.lower():
                self.stats['articles_found'] += 1
                
            # Save individual content file
            self.save_content_file(url, title, content, content_type, video_urls, image_urls)
            
            # Small delay to be respectful
            time.sleep(1)
            
        except Exception as e:
            logger.error(f"Error scraping {url}: {str(e)}")
            self.stats['errors'] += 1
            
    def extract_title(self, soup):
        """Extract title from page"""
        # Try multiple title selectors
        title_selectors = [
            'h1',
            '.title',
            '.page-title',
            '.article-title',
            '.solution-title',
            'title'
        ]
        
        for selector in title_selectors:
            element = soup.select_one(selector)
            if element and element.get_text(strip=True):
                return element.get_text(strip=True)
                
        return "Unknown Title"
        
    def extract_content(self, soup):
        """Extract main content from page"""
        # Remove unwanted elements
        for element in soup(['script', 'style', 'nav', 'header', 'footer']):
            element.decompose()
            
        # Try content selectors
        content_selectors = [
            '.content',
            '.article-content',
            '.solution-content',
            '.main-content',
            'main',
            '.page-content'
        ]
        
        for selector in content_selectors:
            element = soup.select_one(selector)
            if element:
                return element.get_text(separator='\n', strip=True)
                
        # Fallback to body content
        body = soup.find('body')
        if body:
            return body.get_text(separator='\n', strip=True)
            
        return ""
        
    def determine_content_type(self, url, soup):
        """Determine content type based on URL and content"""
        url_lower = url.lower()
        
        if '/solutions/' in url_lower:
            return 'Solution'
        elif '/guides/' in url_lower:
            return 'Guide'
        elif '/articles/' in url_lower:
            return 'Article'
        elif '/best-practices/' in url_lower:
            return 'Best Practice'
        elif '/tutorials/' in url_lower:
            return 'Tutorial'
        elif '/webinars/' in url_lower:
            return 'Webinar'
        elif '/videos/' in url_lower:
            return 'Video'
        else:
            return 'General Content'
            
    def extract_categories(self, url, soup):
        """Extract category and subcategory"""
        url_parts = url.split('/')
        
        category = "General"
        subcategory = ""
        
        # Extract from URL structure
        if '/solutions/' in url:
            idx = url_parts.index('solutions')
            if len(url_parts) > idx + 1:
                category = url_parts[idx + 1].title()
            if len(url_parts) > idx + 2:
                subcategory = url_parts[idx + 2].title()
        elif '/guides/' in url:
            category = "Guides"
        elif '/articles/' in url:
            category = "Articles"
            
        # Try to extract from breadcrumbs or navigation
        breadcrumbs = soup.select('.breadcrumb a, .breadcrumbs a')
        if breadcrumbs and len(breadcrumbs) > 1:
            category = breadcrumbs[-2].get_text(strip=True)
            if len(breadcrumbs) > 2:
                subcategory = breadcrumbs[-1].get_text(strip=True)
                
        return category, subcategory
        
    def extract_tags(self, soup):
        """Extract tags or keywords"""
        tags = []
        
        # Look for tag elements
        tag_selectors = [
            '.tags a',
            '.keywords a',
            '.categories a',
            '[data-tag]'
        ]
        
        for selector in tag_selectors:
            elements = soup.select(selector)
            for element in elements:
                tag = element.get_text(strip=True)
                if tag and tag not in tags:
                    tags.append(tag)
                    
        # Extract from meta keywords
        meta_keywords = soup.find('meta', attrs={'name': 'keywords'})
        if meta_keywords:
            keywords = meta_keywords.get('content', '').split(',')
            for keyword in keywords:
                keyword = keyword.strip()
                if keyword and keyword not in tags:
                    tags.append(keyword)
                    
        return tags
        
    def extract_videos(self, soup, source_url):
        """Extract video URLs from page"""
        video_urls = []
        
        # YouTube embeds
        youtube_embeds = soup.find_all('iframe', src=re.compile(r'youtube\.com|youtu\.be'))
        for embed in youtube_embeds:
            video_urls.append(embed['src'])
            
        # Vimeo embeds
        vimeo_embeds = soup.find_all('iframe', src=re.compile(r'vimeo\.com'))
        for embed in vimeo_embeds:
            video_urls.append(embed['src'])
            
        # HTML5 videos
        video_elements = soup.find_all('video')
        for video in video_elements:
            src = video.get('src')
            if src:
                if not src.startswith('http'):
                    src = urljoin(source_url, src)
                video_urls.append(src)
                
        # Video links
        video_links = soup.find_all('a', href=re.compile(r'\.(mp4|avi|mov|wmv|flv|webm)$'))
        for link in video_links:
            href = link['href']
            if not href.startswith('http'):
                href = urljoin(source_url, href)
            video_urls.append(href)
            
        self.stats['videos_found'] += len(video_urls)
        return video_urls
        
    def extract_images(self, soup, source_url):
        """Extract image URLs from page"""
        image_urls = []
        
        images = soup.find_all('img', src=True)
        for img in images:
            src = img['src']
            if not src.startswith('http'):
                src = urljoin(source_url, src)
            image_urls.append(src)
            
        return image_urls
        
    def extract_downloads(self, soup, source_url):
        """Extract download links"""
        download_links = []
        
        # Common download file extensions
        download_pattern = re.compile(r'\.(pdf|doc|docx|xls|xlsx|ppt|pptx|zip|rar)$', re.I)
        
        download_links_elements = soup.find_all('a', href=download_pattern)
        for link in download_links_elements:
            href = link['href']
            if not href.startswith('http'):
                href = urljoin(source_url, href)
            download_links.append({
                'url': href,
                'text': link.get_text(strip=True),
                'type': href.split('.')[-1].lower()
            })
            
        return download_links
        
    def determine_difficulty(self, content, tags):
        """Determine content difficulty level"""
        if not content:
            return "beginner"
            
        # Technical indicators for advanced content
        advanced_indicators = [
            'api', 'development', 'code', 'script', 'database', 'sql',
            'configuration', 'advanced', 'technical', 'integration'
        ]
        
        # Beginner indicators
        beginner_indicators = [
            'introduction', 'basic', 'getting started', 'overview',
            'beginner', 'simple', 'easy', 'first steps'
        ]
        
        content_lower = content.lower()
        tags_lower = [tag.lower() for tag in tags]
        
        advanced_score = sum(1 for indicator in advanced_indicators 
                           if indicator in content_lower or indicator in tags_lower)
        beginner_score = sum(1 for indicator in beginner_indicators 
                           if indicator in content_lower or indicator in tags_lower)
        
        if advanced_score > beginner_score and advanced_score >= 2:
            return "advanced"
        elif beginner_score > advanced_score and beginner_score >= 2:
            return "beginner"
        else:
            return "intermediate"
            
    def process_video(self, video_url, source_page_url, soup):
        """Process individual video details"""
        try:
            # Extract video metadata from the page
            title = ""
            description = ""
            duration = ""
            thumbnail_url = ""
            
            # Try to find video title
            video_container = soup.find('div', {'data-video-url': video_url}) or \
                            soup.find('iframe', {'src': video_url}).find_parent()
            
            if video_container:
                title_element = video_container.find(['h1', 'h2', 'h3', '.video-title'])
                if title_element:
                    title = title_element.get_text(strip=True)
                    
                desc_element = video_container.find(['.video-description', '.description'])
                if desc_element:
                    description = desc_element.get_text(strip=True)
                    
            # Determine video type
            video_type = "Unknown"
            if 'youtube.com' in video_url or 'youtu.be' in video_url:
                video_type = "YouTube"
            elif 'vimeo.com' in video_url:
                video_type = "Vimeo"
            elif video_url.endswith(('.mp4', '.avi', '.mov', '.wmv', '.flv', '.webm')):
                video_type = "Direct Video"
                
            # Store video information
            self.conn.execute('''
                INSERT OR REPLACE INTO videos
                (video_url, title, description, duration, thumbnail_url,
                 source_page_url, video_type)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (video_url, title, description, duration, thumbnail_url,
                  source_page_url, video_type))
                  
        except Exception as e:
            logger.error(f"Error processing video {video_url}: {str(e)}")
            
    def save_content_file(self, url, title, content, content_type, video_urls, image_urls):
        """Save individual content file"""
        try:
            # Create safe filename
            safe_title = re.sub(r'[^\w\s-]', '', title.strip())[:100]
            filename = f"{safe_title}.json"
            filepath = self.content_dir / filename
            
            content_data = {
                'url': url,
                'title': title,
                'content': content,
                'content_type': content_type,
                'video_urls': video_urls,
                'image_urls': image_urls,
                'scraped_at': datetime.now().isoformat(),
                'word_count': len(content.split()) if content else 0
            }
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(content_data, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            logger.error(f"Error saving content file for {url}: {str(e)}")
            
    def generate_report(self):
        """Generate comprehensive scraping report"""
        logger.info("📊 Generating comprehensive report...")
        
        end_time = datetime.now()
        processing_time = end_time - self.stats['start_time']
        
        # Query database for detailed statistics
        cursor = self.conn.cursor()
        
        # Content type distribution
        cursor.execute('''
            SELECT content_type, COUNT(*) 
            FROM authenticated_content 
            GROUP BY content_type
        ''')
        content_type_dist = dict(cursor.fetchall())
        
        # Category distribution
        cursor.execute('''
            SELECT category, COUNT(*) 
            FROM authenticated_content 
            GROUP BY category
        ''')
        category_dist = dict(cursor.fetchall())
        
        # Difficulty distribution
        cursor.execute('''
            SELECT difficulty_level, COUNT(*) 
            FROM authenticated_content 
            GROUP BY difficulty_level
        ''')
        difficulty_dist = dict(cursor.fetchall())
        
        # Total word count
        cursor.execute('SELECT SUM(word_count) FROM authenticated_content')
        total_words = cursor.fetchone()[0] or 0
        
        # Video statistics
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
                'total_guides': self.stats['guides_found'],
                'total_articles': self.stats['articles_found'],
                'total_words': total_words,
                'errors_encountered': self.stats['errors']
            },
            'content_distribution': {
                'by_type': content_type_dist,
                'by_category': category_dist,
                'by_difficulty': difficulty_dist
            },
            'video_analysis': {
                'total_videos': self.stats['videos_found'],
                'by_type': video_type_dist
            },
            'database_info': {
                'location': str(self.db_path),
                'tables': ['authenticated_content', 'videos']
            },
            'output_directories': {
                'content_files': str(self.content_dir),
                'media_files': str(self.media_dir),
                'reports': str(self.reports_dir)
            }
        }
        
        # Save report
        report_file = self.reports_dir / 'authenticated_scraping_report.json'
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
            
        logger.info(f"📋 Report saved to: {report_file}")
        return report
        
    def run(self):
        """Main execution method"""
        logger.info("🚀 Starting Authenticated Knowledge Hub Scraping...")
        
        # Step 1: Login
        if not self.login():
            logger.error("❌ Failed to login. Exiting...")
            return False
            
        # Step 2: Discover content URLs
        content_urls = self.discover_content_urls()
        if not content_urls:
            logger.warning("⚠️ No content URLs discovered")
            return False
            
        # Step 3: Scrape all discovered content
        logger.info(f"📥 Scraping {len(content_urls)} content URLs...")
        for i, url in enumerate(content_urls, 1):
            logger.info(f"Progress: {i}/{len(content_urls)}")
            self.scrape_content(url)
            
        # Step 4: Generate report
        report = self.generate_report()
        
        # Step 5: Close database connection
        self.conn.close()
        
        logger.info("🎉 Authenticated Knowledge Hub scraping completed!")
        logger.info(f"📊 Final Stats: {self.stats}")
        
        return True

if __name__ == "__main__":
    scraper = AuthenticatedKnowledgeHubScraper()
    scraper.run()
