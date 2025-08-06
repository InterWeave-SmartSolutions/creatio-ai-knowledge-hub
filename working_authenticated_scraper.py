#!/usr/bin/env python3
"""
Working Authenticated Creatio Knowledge Hub Scraper
"""

import requests
from bs4 import BeautifulSoup
import json
import sqlite3
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
        logging.FileHandler('working_scraper.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class WorkingKnowledgeHubScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
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
        self.base_dir = Path("working_authenticated_knowledge_hub")
        self.content_dir = self.base_dir / "content"
        self.media_dir = self.base_dir / "media"
        self.reports_dir = self.base_dir / "reports"
        
        for directory in [self.base_dir, self.content_dir, self.media_dir, self.reports_dir]:
            directory.mkdir(exist_ok=True)
            
    def setup_database(self):
        """Setup SQLite database for authenticated content"""
        self.db_path = self.base_dir / "working_knowledge_hub.db"
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
        """Authenticate with Knowledge Hub using proper form handling"""
        logger.info("🔐 Attempting to login to Knowledge Hub...")
        
        try:
            # Step 1: Get login page with fresh session
            logger.info("📄 Getting fresh login page...")
            login_page = self.session.get(self.login_url, timeout=30)
            login_page.raise_for_status()
            
            soup = BeautifulSoup(login_page.content, 'html.parser')
            
            # Step 2: Find and analyze login form
            login_form = soup.find('form')
            if not login_form:
                logger.error("Could not find login form")
                return False
                
            # Step 3: Extract form data properly
            form_data = {}
            
            for input_field in login_form.find_all('input'):
                field_name = input_field.get('name')
                field_value = input_field.get('value', '')
                
                if field_name:
                    if field_name == 'name':
                        form_data[field_name] = self.username
                    elif field_name == 'pass':
                        form_data[field_name] = self.password
                    else:
                        # Include all hidden fields (form_build_id, form_id, etc.)
                        form_data[field_name] = field_value
                        
            logger.info(f"Form fields: {list(form_data.keys())}")
            
            # Step 4: Build proper action URL
            form_action = login_form.get('action', '/user/login')\n            
            # The action seems to be relative, build the full URL manually
            action_url = f"{self.base_url}/solutions/user/login?destination=/solutions/"
            
            logger.info(f"Submitting login to: {action_url}")
            
            # Step 5: Submit login form
            login_response = self.session.post(
                action_url,
                data=form_data,
                timeout=30,
                allow_redirects=True
            )
            
            logger.info(f"Login response status: {login_response.status_code}")
            
            # Step 6: Verify login success
            if login_response.status_code == 200:
                # Check final URL to see if we're logged in
                final_url = login_response.url
                logger.info(f"Final URL after login: {final_url}")
                
                # Test access to solutions page
                test_response = self.session.get(f"{self.base_url}/solutions/", timeout=15)
                logger.info(f"Solutions test access: {test_response.status_code}")
                
                if test_response.status_code == 200:
                    # Check if we're actually logged in (not seeing login form)
                    test_content = test_response.text.lower()
                    if 'log in' not in test_content and 'login' not in test_content:
                        logger.info("✅ Login successful!")
                        self.stats['login_success'] = True
                        return True
                        
            # Alternative: Check for specific success indicators
            response_text = login_response.text.lower()
            if 'dashboard' in response_text or 'welcome' in response_text:
                logger.info("✅ Login successful (dashboard detected)!")
                self.stats['login_success'] = True
                return True
                
            logger.warning("⚠️ Login may have failed - proceeding anyway...")
            return False
            
        except Exception as e:
            logger.error(f"Login error: {str(e)}")
            return False
            
    def discover_content_urls(self):
        """Discover all accessible content URLs after authentication"""
        logger.info("🔍 Discovering authenticated content URLs...")
        
        content_urls = set()
        
        # Start with main solutions page
        main_urls = [
            f"{self.base_url}/solutions/",
            f"{self.base_url}/solutions/general",
            f"{self.base_url}/solutions"
        ]
        
        for main_url in main_urls:
            try:
                logger.info(f"Checking main URL: {main_url}")
                response = self.session.get(main_url, timeout=15)
                
                if response.status_code == 200:
                    logger.info(f"✅ Accessible: {main_url}")
                    content_urls.add(main_url)
                    
                    # Extract all internal links from this page
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # Find all links
                    for link in soup.find_all('a', href=True):\n                        href = link['href']\n                        \n                        # Build full URL\n                        if href.startswith('/'):\n                            full_url = urljoin(self.base_url, href)\n                        elif href.startswith('http'):\n                            full_url = href\n                        else:\n                            continue\n                            \n                        # Filter for knowledge content\n                        if self.is_knowledge_content_url(full_url):\n                            content_urls.add(full_url)\n                            \n                    # Look for specific content patterns\n                    content_patterns = [\n                        'article', 'solution', 'guide', 'tutorial', 'best-practice',\n                        'case-study', 'implementation', 'webinar', 'video'\n                    ]\n                    \n                    for pattern in content_patterns:\n                        pattern_links = soup.find_all('a', href=re.compile(pattern, re.I))\n                        for link in pattern_links:\n                            href = link['href']\n                            if href.startswith('/'):\n                                full_url = urljoin(self.base_url, href)\n                            elif href.startswith('http'):\n                                full_url = href\n                            else:\n                                continue\n                            content_urls.add(full_url)\n                            \n                else:\n                    logger.warning(f"❌ Not accessible: {main_url} (Status: {response.status_code})")\n                    \n            except Exception as e:\n                logger.error(f"Error checking {main_url}: {str(e)}")\n                self.stats['errors'] += 1\n                \n        # Discover more URLs through navigation/sitemap patterns\n        discovery_patterns = [\n            '/solutions/general',\n            '/solutions/industry', \n            '/solutions/crm',\n            '/solutions/marketing',\n            '/solutions/sales',\n            '/solutions/service'\n        ]\n        \n        for pattern in discovery_patterns:\n            try:\n                url = f"{self.base_url}{pattern}"\n                response = self.session.get(url, timeout=10)\n                if response.status_code == 200:\n                    content_urls.add(url)\n                    # Extract more links from these pages too\n                    soup = BeautifulSoup(response.content, 'html.parser')\n                    for link in soup.find_all('a', href=True):\n                        href = link['href']\n                        if href.startswith('/solutions/') or href.startswith('/guides/') or href.startswith('/articles/'):\n                            full_url = urljoin(self.base_url, href)\n                            content_urls.add(full_url)\n            except:\n                continue\n                \n        # Filter out non-content URLs\n        filtered_urls = [url for url in content_urls if self.is_valid_content_url(url)]\n        \n        logger.info(f"🎯 Discovered {len(filtered_urls)} content URLs")\n        return filtered_urls\n        \n    def is_knowledge_content_url(self, url):\n        """Check if URL is a knowledge content URL"""        \n        if not url or not isinstance(url, str):\n            return False\n            \n        # Must be from the knowledge hub domain\n        if 'knowledge-hub.creatio.com' not in url:\n            return False\n            \n        knowledge_patterns = [\n            '/solutions/',\n            '/guides/',\n            '/articles/',\n            '/best-practices/',\n            '/tutorials/',\n            '/webinars/',\n            '/videos/',\n            '/case-studies/', \n            '/implementations/'\n        ]\n        \n        return any(pattern in url for pattern in knowledge_patterns)\n        \n    def is_valid_content_url(self, url):\n        """Additional validation for content URLs"""        \n        if not self.is_knowledge_content_url(url):\n            return False\n            \n        # Exclude user/admin URLs\n        exclude_patterns = [\n            '/user/', '/admin/', '/edit', '/delete', '/login', '/logout',\n            '.css', '.js', '.png', '.jpg', '.gif', '.pdf', '#'\n        ]\n        \n        return not any(pattern in url for pattern in exclude_patterns)\n        \n    def scrape_content(self, url):\n        """Scrape content from a specific URL"""        \n        try:\n            logger.info(f"📄 Scraping: {url}")\n            response = self.session.get(url, timeout=30)\n            response.raise_for_status()\n            \n            soup = BeautifulSoup(response.content, 'html.parser')\n            \n            # Extract basic information\n            title = self.extract_title(soup)\n            content = self.extract_content(soup)\n            content_type = self.determine_content_type(url, soup)\n            category, subcategory = self.extract_categories(url, soup)\n            tags = self.extract_tags(soup)\n            \n            # Extract media\n            video_urls = self.extract_videos(soup, url)\n            image_urls = self.extract_images(soup, url)\n            download_links = self.extract_downloads(soup, url)\n            \n            # Calculate metrics\n            word_count = len(content.split()) if content else 0\n            content_hash = hashlib.md5(content.encode() if content else b"").hexdigest()\n            difficulty_level = self.determine_difficulty(content, tags)\n            estimated_read_time = max(1, word_count // 200)\n            \n            # Store in database\n            self.conn.execute('''\n                INSERT OR REPLACE INTO authenticated_content\n                (url, title, content, content_type, category, subcategory, tags,\n                 video_urls, image_urls, download_links, content_hash, word_count,\n                 difficulty_level, estimated_read_time)\n                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)\n            ''', (\n                url, title, content, content_type, category, subcategory,\n                json.dumps(tags), json.dumps(video_urls), json.dumps(image_urls),\n                json.dumps(download_links), content_hash, word_count,\n                difficulty_level, estimated_read_time\n            ))\n            \n            # Process videos separately\n            for video_url in video_urls:\n                self.process_video(video_url, url, soup)\n                \n            self.conn.commit()\n            self.stats['pages_scraped'] += 1\n            \n            # Update content type stats\n            content_type_lower = content_type.lower()\n            if 'solution' in content_type_lower:\n                self.stats['solutions_found'] += 1\n            elif 'guide' in content_type_lower:\n                self.stats['guides_found'] += 1\n            elif 'article' in content_type_lower:\n                self.stats['articles_found'] += 1\n                \n            # Save individual content file\n            self.save_content_file(url, title, content, content_type, video_urls, image_urls)\n            \n            # Small delay to be respectful\n            time.sleep(0.5)\n            \n        except Exception as e:\n            logger.error(f"Error scraping {url}: {str(e)}")\n            self.stats['errors'] += 1\n            \n    def extract_title(self, soup):\n        """Extract title from page"""        \n        title_selectors = [\n            'h1.page-title',\n            'h1',\n            '.title',\n            '.page-title',\n            '.article-title',\n            '.solution-title',\n            'title'\n        ]\n        \n        for selector in title_selectors:\n            element = soup.select_one(selector)\n            if element and element.get_text(strip=True):\n                return element.get_text(strip=True)\n                \n        return "Unknown Title"\n        \n    def extract_content(self, soup):\n        """Extract main content from page"""        \n        # Remove unwanted elements\n        for element in soup(['script', 'style', 'nav', 'header', 'footer', '.menu']):\n            element.decompose()\n            \n        # Try content selectors in order of preference\n        content_selectors = [\n            '.field-name-body',\n            '.content',\n            '.article-content', \n            '.solution-content',\n            '.main-content',\n            'main',\n            '.page-content',\n            '.node-content'\n        ]\n        \n        for selector in content_selectors:\n            element = soup.select_one(selector)\n            if element:\n                return element.get_text(separator='\\n', strip=True)\n                \n        # Fallback to body content (less navigation)\n        body = soup.find('body')\n        if body:\n            # Remove more navigation elements\n            for nav_element in body(['nav', '.menu', '.navigation', '.breadcrumb']):\n                nav_element.decompose()\n            return body.get_text(separator='\\n', strip=True)\n            \n        return ""\n        \n    def determine_content_type(self, url, soup):\n        """Determine content type based on URL and content"""        \n        url_lower = url.lower()\n        \n        type_mapping = {\n            '/solutions/': 'Solution',\n            '/guides/': 'Guide', \n            '/articles/': 'Article',\n            '/best-practices/': 'Best Practice',\n            '/tutorials/': 'Tutorial',\n            '/webinars/': 'Webinar',\n            '/videos/': 'Video',\n            '/case-studies/': 'Case Study',\n            '/implementations/': 'Implementation'\n        }\n        \n        for pattern, content_type in type_mapping.items():\n            if pattern in url_lower:\n                return content_type\n                \n        return 'General Content'\n        \n    def extract_categories(self, url, soup):\n        """Extract category and subcategory"""        \n        url_parts = url.split('/')\n        \n        category = "General"\n        subcategory = ""\n        \n        # Extract from URL structure\n        if '/solutions/' in url:\n            try:\n                idx = url_parts.index('solutions')\n                if len(url_parts) > idx + 1:\n                    category = url_parts[idx + 1].replace('-', ' ').title()\n                if len(url_parts) > idx + 2:\n                    subcategory = url_parts[idx + 2].replace('-', ' ').title()\n            except ValueError:\n                pass\n        elif '/guides/' in url:\n            category = "Guides"\n        elif '/articles/' in url:\n            category = "Articles"\n            \n        # Try to extract from breadcrumbs\n        breadcrumbs = soup.select('.breadcrumb a, .breadcrumbs a')\n        if breadcrumbs and len(breadcrumbs) > 1:\n            category = breadcrumbs[-2].get_text(strip=True)\n            if len(breadcrumbs) > 2:\n                subcategory = breadcrumbs[-1].get_text(strip=True)\n                \n        return category, subcategory\n        \n    def extract_tags(self, soup):\n        """Extract tags or keywords"""        \n        tags = []\n        \n        # Look for tag elements\n        tag_selectors = [\n            '.field-name-field-tags a',\n            '.tags a',\n            '.keywords a', \n            '.categories a',\n            '[data-tag]'\n        ]\n        \n        for selector in tag_selectors:\n            elements = soup.select(selector)\n            for element in elements:\n                tag = element.get_text(strip=True)\n                if tag and tag not in tags and len(tag) > 2:\n                    tags.append(tag)\n                    \n        # Extract from meta keywords\n        meta_keywords = soup.find('meta', attrs={'name': 'keywords'})\n        if meta_keywords:\n            keywords = meta_keywords.get('content', '').split(',')\n            for keyword in keywords:\n                keyword = keyword.strip()\n                if keyword and keyword not in tags and len(keyword) > 2:\n                    tags.append(keyword)\n                    \n        return tags[:10]  # Limit to 10 most relevant tags\n        \n    def extract_videos(self, soup, source_url):\n        """Extract video URLs from page"""        \n        video_urls = []\n        \n        # YouTube embeds\n        youtube_embeds = soup.find_all('iframe', src=re.compile(r'youtube\\.com|youtu\\.be'))\n        for embed in youtube_embeds:\n            video_urls.append(embed['src'])\n            \n        # Vimeo embeds\n        vimeo_embeds = soup.find_all('iframe', src=re.compile(r'vimeo\\.com'))\n        for embed in vimeo_embeds:\n            video_urls.append(embed['src'])\n            \n        # HTML5 videos\n        video_elements = soup.find_all('video')\n        for video in video_elements:\n            src = video.get('src')\n            if src:\n                if not src.startswith('http'):\n                    src = urljoin(source_url, src)\n                video_urls.append(src)\n                \n        # Video links\n        video_links = soup.find_all('a', href=re.compile(r'\\.(mp4|avi|mov|wmv|flv|webm)$'))\n        for link in video_links:\n            href = link['href']\n            if not href.startswith('http'):\n                href = urljoin(source_url, href)\n            video_urls.append(href)\n            \n        self.stats['videos_found'] += len(video_urls)\n        return video_urls\n        \n    def extract_images(self, soup, source_url):\n        """Extract image URLs from page"""        \n        image_urls = []\n        \n        images = soup.find_all('img', src=True)\n        for img in images:\n            src = img['src']\n            if not src.startswith('http'):\n                src = urljoin(source_url, src)\n            # Filter out tiny images (likely icons)\n            if not any(skip in src for skip in ['icon', 'logo', 'sprite']) and 'data:' not in src:\n                image_urls.append(src)\n                \n        return image_urls[:20]  # Limit to 20 images per page\n        \n    def extract_downloads(self, soup, source_url):\n        """Extract download links"""        \n        download_links = []\n        \n        # Common download file extensions\n        download_pattern = re.compile(r'\\.(pdf|doc|docx|xls|xlsx|ppt|pptx|zip|rar)$', re.I)\n        \n        download_link_elements = soup.find_all('a', href=download_pattern)\n        for link in download_link_elements:\n            href = link['href']\n            if not href.startswith('http'):\n                href = urljoin(source_url, href)\n            download_links.append({\n                'url': href,\n                'text': link.get_text(strip=True),\n                'type': href.split('.')[-1].lower()\n            })\n            \n        return download_links\n        \n    def determine_difficulty(self, content, tags):\n        """Determine content difficulty level"""        \n        if not content:\n            return "beginner"\n            \n        # Technical indicators for advanced content\n        advanced_indicators = [\n            'api', 'development', 'code', 'script', 'database', 'sql',\n            'configuration', 'advanced', 'technical', 'integration',\n            'custom', 'development', 'programming'\n        ]\n        \n        # Beginner indicators\n        beginner_indicators = [\n            'introduction', 'basic', 'getting started', 'overview',\n            'beginner', 'simple', 'easy', 'first steps', 'quick start'\n        ]\n        \n        content_lower = content.lower()\n        tags_lower = [tag.lower() for tag in tags]\n        \n        advanced_score = sum(1 for indicator in advanced_indicators \n                           if indicator in content_lower or indicator in tags_lower)\n        beginner_score = sum(1 for indicator in beginner_indicators \n                           if indicator in content_lower or indicator in tags_lower)\n        \n        if advanced_score > beginner_score and advanced_score >= 3:\n            return "advanced"\n        elif beginner_score > advanced_score and beginner_score >= 2:\n            return "beginner"\n        else:\n            return "intermediate"\n            \n    def process_video(self, video_url, source_page_url, soup):\n        """Process individual video details"""        \n        try:\n            title = ""\n            description = ""\n            duration = ""\n            thumbnail_url = ""\n            \n            # Try to find video metadata from the page\n            if 'youtube.com' in video_url:\n                # Extract YouTube video ID and metadata if possible\n                video_id_match = re.search(r'(?:v=|embed/)([a-zA-Z0-9_-]+)', video_url)\n                if video_id_match:\n                    video_id = video_id_match.group(1)\n                    title = f"YouTube Video {video_id}"\n                    \n            # Try to find title from surrounding elements\n            iframe = soup.find('iframe', src=video_url)\n            if iframe:\n                container = iframe.find_parent()\n                if container:\n                    title_element = container.find(['h1', 'h2', 'h3', '.video-title'])\n                    if title_element:\n                        title = title_element.get_text(strip=True)\n                        \n            # Determine video type\n            video_type = "Unknown"\n            if 'youtube.com' in video_url or 'youtu.be' in video_url:\n                video_type = "YouTube"\n            elif 'vimeo.com' in video_url:\n                video_type = "Vimeo" \n            elif video_url.endswith(('.mp4', '.avi', '.mov', '.wmv', '.flv', '.webm')):\n                video_type = "Direct Video"\n                \n            # Store video information\n            self.conn.execute('''\n                INSERT OR REPLACE INTO videos\n                (video_url, title, description, duration, thumbnail_url,\n                 source_page_url, video_type)\n                VALUES (?, ?, ?, ?, ?, ?, ?)\n            ''', (video_url, title, description, duration, thumbnail_url,\n                  source_page_url, video_type))\n                  \n        except Exception as e:\n            logger.error(f"Error processing video {video_url}: {str(e)}")\n            \n    def save_content_file(self, url, title, content, content_type, video_urls, image_urls):\n        """Save individual content file"""        \n        try:\n            # Create safe filename\n            safe_title = re.sub(r'[^\\w\\s-]', '', title.strip())[:100]\n            filename = f"{safe_title}.json"\n            filepath = self.content_dir / filename\n            \n            content_data = {\n                'url': url,\n                'title': title,\n                'content': content,\n                'content_type': content_type,\n                'video_urls': video_urls,\n                'image_urls': image_urls,\n                'scraped_at': datetime.now().isoformat(),\n                'word_count': len(content.split()) if content else 0\n            }\n            \n            with open(filepath, 'w', encoding='utf-8') as f:\n                json.dump(content_data, f, indent=2, ensure_ascii=False)\n                \n        except Exception as e:\n            logger.error(f"Error saving content file for {url}: {str(e)}")\n            \n    def generate_report(self):\n        """Generate comprehensive scraping report"""        \n        logger.info("📊 Generating comprehensive report...")\n        \n        end_time = datetime.now()\n        processing_time = end_time - self.stats['start_time']\n        \n        # Query database for detailed statistics\n        cursor = self.conn.cursor()\n        \n        # Content type distribution\n        cursor.execute('''\n            SELECT content_type, COUNT(*) \n            FROM authenticated_content \n            GROUP BY content_type\n        ''')\n        content_type_dist = dict(cursor.fetchall())\n        \n        # Category distribution\n        cursor.execute('''\n            SELECT category, COUNT(*) \n            FROM authenticated_content \n            GROUP BY category\n        ''')\n        category_dist = dict(cursor.fetchall())\n        \n        # Difficulty distribution\n        cursor.execute('''\n            SELECT difficulty_level, COUNT(*)  \n            FROM authenticated_content \n            GROUP BY difficulty_level\n        ''')\n        difficulty_dist = dict(cursor.fetchall())\n        \n        # Total word count\n        cursor.execute('SELECT SUM(word_count) FROM authenticated_content')\n        total_words = cursor.fetchone()[0] or 0\n        \n        # Video statistics\n        cursor.execute('SELECT video_type, COUNT(*) FROM videos GROUP BY video_type')\n        video_type_dist = dict(cursor.fetchall())\n        \n        report = {\n            'scraping_session': {\n                'start_time': self.stats['start_time'].isoformat(),\n                'end_time': end_time.isoformat(),\n                'processing_time': str(processing_time),\n                'login_successful': self.stats['login_success']\n            },\n            'content_statistics': {\n                'total_pages_scraped': self.stats['pages_scraped'],\n                'total_videos_found': self.stats['videos_found'],\n                'total_solutions': self.stats['solutions_found'],\n                'total_guides': self.stats['guides_found'],\n                'total_articles': self.stats['articles_found'],\n                'total_words': total_words,\n                'errors_encountered': self.stats['errors']\n            },\n            'content_distribution': {\n                'by_type': content_type_dist,\n                'by_category': category_dist,\n                'by_difficulty': difficulty_dist\n            },\n            'video_analysis': {\n                'total_videos': self.stats['videos_found'],\n                'by_type': video_type_dist\n            },\n            'database_info': {\n                'location': str(self.db_path),\n                'tables': ['authenticated_content', 'videos']\n            },\n            'output_directories': {\n                'content_files': str(self.content_dir),\n                'media_files': str(self.media_dir),\n                'reports': str(self.reports_dir)\n            }\n        }\n        \n        # Save report\n        report_file = self.reports_dir / 'working_scraping_report.json'\n        with open(report_file, 'w', encoding='utf-8') as f:\n            json.dump(report, f, indent=2, ensure_ascii=False)\n            \n        logger.info(f"📋 Report saved to: {report_file}")\n        return report\n        \n    def run(self):\n        """Main execution method"""        \n        logger.info("🚀 Starting Working Authenticated Knowledge Hub Scraping...")\n        \n        # Step 1: Login (optional - proceed even if it fails)\n        login_success = self.login()\n        if not login_success:\n            logger.warning("⚠️ Login failed, but proceeding to try scraping anyway...")\n            \n        # Step 2: Discover content URLs\n        content_urls = self.discover_content_urls()\n        if not content_urls:\n            logger.warning("⚠️ No content URLs discovered")\n            return False\n            \n        # Step 3: Scrape all discovered content\n        logger.info(f"📥 Scraping {len(content_urls)} content URLs...")\n        for i, url in enumerate(content_urls, 1):\n            logger.info(f"Progress: {i}/{len(content_urls)}")\n            self.scrape_content(url)\n            \n        # Step 4: Generate report\n        report = self.generate_report()\n        \n        # Step 5: Close database connection\n        self.conn.close()\n        \n        logger.info("🎉 Working Authenticated Knowledge Hub scraping completed!")\n        logger.info(f"📊 Final Stats: {self.stats}")\n        \n        return True\n\nif __name__ == "__main__":\n    scraper = WorkingKnowledgeHubScraper()\n    scraper.run()
