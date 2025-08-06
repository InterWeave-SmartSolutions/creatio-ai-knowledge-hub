#!/usr/bin/env python3
"""
Comprehensive Creatio Solutions Hub Scraper V2
Discovers and processes ALL available solutions pages from knowledge-hub.creatio.com/solutions/
Includes content from /general, /industry-specific, and all other solution categories
"""

import requests
from bs4 import BeautifulSoup
import json
import os
import sqlite3
import hashlib
import time
import re
from urllib.parse import urljoin, urlparse
from pathlib import Path
import logging
from datetime import datetime
import html2text
import random

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('comprehensive_solutions_scraping_v2.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class ComprehensiveSolutionsScraper:
    def __init__(self, base_url="https://knowledge-hub.creatio.com", output_dir="ai_knowledge_hub"):
        self.base_url = base_url
        self.output_dir = Path(output_dir)
        self.scraped_urls = set()
        self.discovered_solutions = set()
        
        # Known solution endpoints to discover and try
        self.solution_endpoints = [
            "/solutions/",
            "/solutions/general",
            "/solutions/industry-specific", 
            "/solutions/crm",
            "/solutions/service",
            "/solutions/marketing",
            "/solutions/sales",
            "/solutions/customer-service",
            "/solutions/field-service",
            "/solutions/commerce",
            "/solutions/digital-commerce",
            "/solutions/financial-services",
            "/solutions/healthcare",
            "/solutions/education",
            "/solutions/manufacturing",
            "/solutions/real-estate",
            "/solutions/non-profit",
            "/solutions/government",
            "/solutions/retail",
            "/solutions/telecommunications",
            "/solutions/energy",
            "/solutions/logistics",
            "/solutions/professional-services"
        ]
        
        self.download_stats = {
            'solution_pages': 0,
            'articles_discovered': 0,
            'content_processed': 0,
            'images': 0,
            'documents': 0,
            'errors': 0
        }
        
        # Setup directories
        self.setup_directories()
        
        # Setup database
        self.setup_database()
        
        # Session with rotating headers
        self.session = requests.Session()
        self.user_agents = [
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        ]
        
        self.update_session_headers()
        
        # HTML to text converter
        self.h = html2text.HTML2Text()
        self.h.ignore_links = False
        self.h.body_width = 0
        
    def setup_directories(self):
        """Create directory structure for solutions content"""
        dirs = [
            'solutions_hub',
            'solutions_hub/discovered_pages',
            'solutions_hub/solution_articles',
            'solutions_hub/images',
            'solutions_hub/documents',
            'solutions_hub/structured_data',
            'solutions_hub/search_data'
        ]
        
        for dir_name in dirs:
            (self.output_dir / dir_name).mkdir(parents=True, exist_ok=True)
            
    def setup_database(self):
        """Setup database for solutions content"""
        self.db_path = self.output_dir / 'solutions_comprehensive.db'
        self.conn = sqlite3.connect(str(self.db_path), check_same_thread=False)
        
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS solutions_content (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT UNIQUE,
                title TEXT,
                category TEXT,
                solution_type TEXT,
                description TEXT,
                content TEXT,
                markdown_content TEXT,
                word_count INTEGER,
                scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                file_size INTEGER,
                checksum TEXT
            )
        ''')
        
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS discovered_links (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source_url TEXT,
                target_url TEXT,
                link_text TEXT,
                link_type TEXT,
                discovered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        self.conn.commit()
        
    def update_session_headers(self):
        """Update session headers"""
        self.session.headers.update({
            'User-Agent': random.choice(self.user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Referer': 'https://www.google.com/',
            'DNT': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'max-age=0'
        })

    def clean_filename(self, filename):
        """Clean filename for filesystem"""
        filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
        filename = re.sub(r'\s+', '_', filename)
        return filename.strip('._')[:200]

    def extract_content_from_page(self, soup, url):
        """Extract main content from solutions page"""
        content_data = {
            'title': '',
            'description': '',
            'main_content': '',
            'articles': [],
            'links': []
        }
        
        # Extract title
        title_elem = soup.find('title')
        if title_elem:
            content_data['title'] = title_elem.get_text().strip()
        
        # Extract description
        desc_elem = soup.find('meta', attrs={'name': 'description'})
        if desc_elem:
            content_data['description'] = desc_elem.get('content', '')
            
        # Try to find main content areas
        content_selectors = [
            '.main-content', '.content', '#content', 'main', 'article',
            '.page-content', '.solution-content', '.hub-content'
        ]
        
        main_content = None
        for selector in content_selectors:
            main_content = soup.select_one(selector)
            if main_content:
                break
                
        if not main_content:
            main_content = soup.find('body')
            
        if main_content:
            # Remove navigation, headers, footers
            for unwanted in main_content.find_all(['nav', 'header', 'footer', 'script', 'style', 'aside']):
                unwanted.decompose()
                
            content_data['main_content'] = main_content.get_text(strip=True, separator=' ')
            
        # Find solution articles and case studies
        article_selectors = [
            '.solution-item', '.case-study', '.article-item', '.solution-card',
            '.content-item', '.hub-article', 'article'
        ]
        
        for selector in article_selectors:
            articles = soup.select(selector)
            for article in articles:
                article_data = self.extract_article_info(article, url)
                if article_data:
                    content_data['articles'].append(article_data)
        
        # Extract all internal links
        links = soup.find_all('a', href=True)
        for link in links:
            href = link.get('href')
            if href and ('creatio.com' in href or href.startswith('/')):
                full_url = urljoin(url, href)
                link_text = link.get_text().strip()
                
                content_data['links'].append({
                    'url': full_url,
                    'text': link_text,
                    'internal': 'creatio.com' in full_url
                })
                
                # Store in database
                self.conn.execute('''
                    INSERT OR IGNORE INTO discovered_links 
                    (source_url, target_url, link_text, link_type)
                    VALUES (?, ?, ?, ?)
                ''', (url, full_url, link_text, 'solution_link'))
        
        return content_data

    def extract_article_info(self, article_elem, base_url):
        """Extract information from individual article elements"""
        article_data = {}
        
        # Try to find title
        title_selectors = ['h1', 'h2', 'h3', '.title', '.article-title', '.solution-title']
        for selector in title_selectors:
            title_elem = article_elem.select_one(selector)
            if title_elem:
                article_data['title'] = title_elem.get_text().strip()
                break
                
        # Try to find description/summary
        desc_selectors = ['.description', '.summary', '.excerpt', 'p']
        for selector in desc_selectors:
            desc_elem = article_elem.select_one(selector)
            if desc_elem:
                article_data['description'] = desc_elem.get_text().strip()
                break
                
        # Try to find link
        link_elem = article_elem.find('a', href=True)
        if link_elem:
            article_data['url'] = urljoin(base_url, link_elem.get('href'))
            
        # Get all text content
        article_data['content'] = article_elem.get_text(strip=True, separator=' ')
        
        return article_data if article_data.get('title') or article_data.get('content') else None

    def discover_solution_pages(self):
        """Discover all available solution pages"""
        logger.info("Discovering solution pages...")
        discovered_urls = set()
        
        for endpoint in self.solution_endpoints:
            url = self.base_url + endpoint
            
            try:
                logger.info(f"Checking endpoint: {url}")
                
                # Add random delay
                time.sleep(random.uniform(1, 3))
                
                # Update headers for each request
                self.update_session_headers()
                
                response = self.session.get(url, timeout=30, allow_redirects=True)
                
                # Check various success conditions
                if response.status_code == 200:
                    logger.info(f"✓ Accessible: {url}")
                    discovered_urls.add(url)
                    
                    # Parse for additional solution links
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # Look for more solution links
                    solution_links = soup.find_all('a', href=True)
                    for link in solution_links:
                        href = link.get('href')
                        if href and '/solutions/' in href:
                            full_url = urljoin(url, href)
                            if full_url not in discovered_urls:
                                discovered_urls.add(full_url)
                                logger.info(f"  → Found solution link: {full_url}")
                    
                elif response.status_code == 403:
                    logger.warning(f"403 Forbidden: {url} (might require authentication)")
                elif response.status_code == 404:
                    logger.debug(f"404 Not Found: {url}")
                else:
                    logger.warning(f"HTTP {response.status_code}: {url}")
                    
            except Exception as e:
                logger.error(f"Error checking {url}: {str(e)}")
                self.download_stats['errors'] += 1
        
        logger.info(f"Discovered {len(discovered_urls)} solution pages")
        self.discovered_solutions.update(discovered_urls)
        return list(discovered_urls)

    def scrape_solution_page(self, url):
        """Scrape a single solution page"""
        if url in self.scraped_urls:
            return
            
        logger.info(f"Scraping solution page: {url}")
        
        try:
            # Update headers
            self.update_session_headers()
            
            # Add delay
            time.sleep(random.uniform(2, 4))
            
            response = self.session.get(url, timeout=30)
            
            if response.status_code != 200:
                logger.warning(f"HTTP {response.status_code} for {url}")
                return
                
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract content
            content_data = self.extract_content_from_page(soup, url)
            
            # Determine solution category and type
            category = self.categorize_solution(url, content_data['title'])
            solution_type = self.determine_solution_type(content_data)
            
            # Clean and process content
            main_content = content_data['main_content']
            markdown_content = self.h.handle(str(soup))
            word_count = len(main_content.split()) if main_content else 0
            
            # Generate checksum
            checksum = hashlib.md5(main_content.encode()).hexdigest()
            
            # Save to database
            cursor = self.conn.execute('''
                INSERT OR REPLACE INTO solutions_content 
                (url, title, category, solution_type, description, content, 
                 markdown_content, word_count, file_size, checksum)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (url, content_data['title'], category, solution_type,
                  content_data['description'], main_content, markdown_content,
                  word_count, len(main_content.encode()), checksum))
            
            content_id = cursor.lastrowid
            
            # Save structured files
            self.save_solution_content(content_id, url, content_data, category)
            
            # Process articles found on the page
            for article in content_data['articles']:
                self.download_stats['articles_discovered'] += 1
                
                # If article has its own URL, add to scraping queue
                if article.get('url') and article['url'] not in self.scraped_urls:
                    self.discovered_solutions.add(article['url'])
            
            self.scraped_urls.add(url)
            self.download_stats['solution_pages'] += 1
            self.download_stats['content_processed'] += 1
            
            logger.info(f"Successfully scraped: {content_data['title']}")
            
        except Exception as e:
            logger.error(f"Error scraping {url}: {str(e)}")
            self.download_stats['errors'] += 1

    def categorize_solution(self, url, title):
        """Categorize solution based on URL and title"""
        url_lower = url.lower()
        title_lower = title.lower() if title else ""
        
        category_patterns = {
            'crm': ['crm', 'customer-relationship', 'sales', 'lead', 'opportunity'],
            'service': ['service', 'support', 'ticket', 'case', 'help-desk'],
            'marketing': ['marketing', 'campaign', 'email', 'lead-generation'],
            'commerce': ['commerce', 'e-commerce', 'retail', 'online-store'],
            'field-service': ['field-service', 'field', 'mobile', 'technician'],
            'financial-services': ['financial', 'banking', 'insurance', 'loan'],
            'healthcare': ['healthcare', 'medical', 'patient', 'clinical'],
            'manufacturing': ['manufacturing', 'production', 'supply-chain'],
            'education': ['education', 'school', 'university', 'student'],
            'non-profit': ['non-profit', 'nonprofit', 'charity', 'donation'],
            'government': ['government', 'public', 'civic', 'municipal'],
            'real-estate': ['real-estate', 'property', 'mortgage', 'listing']
        }
        
        for category, patterns in category_patterns.items():
            if any(pattern in url_lower or pattern in title_lower for pattern in patterns):
                return category
                
        return 'general'

    def determine_solution_type(self, content_data):
        """Determine the type of solution"""
        content = content_data.get('main_content', '').lower()
        title = content_data.get('title', '').lower()
        
        if 'case study' in title or 'case study' in content:
            return 'case_study'
        elif 'best practice' in title or 'best practice' in content:
            return 'best_practice'
        elif 'implementation' in title or 'implementation' in content:
            return 'implementation_guide'
        elif 'template' in title or 'template' in content:
            return 'template'
        else:
            return 'solution_overview'

    def save_solution_content(self, content_id, url, content_data, category):
        """Save structured solution content"""
        try:
            # Create category directory
            category_dir = self.output_dir / 'solutions_hub' / 'solution_articles' / category
            category_dir.mkdir(parents=True, exist_ok=True)
            
            # Clean filename
            filename = self.clean_filename(content_data['title']) or f"solution_{content_id}"
            
            # Save as JSON
            structured_data = {
                'id': content_id,
                'url': url,
                'title': content_data['title'],
                'category': category,
                'description': content_data['description'],
                'content': content_data['main_content'],
                'articles': content_data['articles'],
                'links': content_data['links'][:20],  # Limit links
                'scraped_at': datetime.now().isoformat(),
                'word_count': len(content_data['main_content'].split())
            }
            
            json_path = category_dir / f"{content_id}_{filename}.json"
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(structured_data, f, indent=2, ensure_ascii=False)
                
            # Save as markdown
            md_path = category_dir / f"{content_id}_{filename}.md"
            with open(md_path, 'w', encoding='utf-8') as f:
                f.write(f"# {content_data['title']}\n\n")
                f.write(f"**URL:** {url}\n")
                f.write(f"**Category:** {category}\n")
                f.write(f"**Description:** {content_data['description']}\n\n")
                f.write("## Content\n\n")
                f.write(content_data['main_content'])
                
                if content_data['articles']:
                    f.write("\n\n## Related Articles\n\n")
                    for article in content_data['articles']:
                        f.write(f"- **{article.get('title', 'Untitled')}**\n")
                        if article.get('description'):
                            f.write(f"  {article['description']}\n")
                        if article.get('url'):
                            f.write(f"  URL: {article['url']}\n")
                        f.write("\n")
                        
        except Exception as e:
            logger.error(f"Error saving content: {str(e)}")

    def create_solutions_search_index(self):
        """Create search index for solutions content"""
        logger.info("Creating solutions search index...")
        
        try:
            cursor = self.conn.execute('''
                SELECT id, url, title, category, solution_type, description, content, word_count
                FROM solutions_content
                ORDER BY title
            ''')
            
            search_index = []
            for row in cursor:
                (id, url, title, category, solution_type, description, content, word_count) = row
                
                search_entry = {
                    'id': id,
                    'url': url,
                    'title': title,
                    'category': category,
                    'solution_type': solution_type,
                    'description': description,
                    'content_preview': content[:500] if content else "",
                    'word_count': word_count,
                    'searchable_text': f"{title} {description} {content[:1000] if content else ''}"
                }
                
                search_index.append(search_entry)
            
            # Save main search index
            search_index_path = self.output_dir / 'solutions_hub' / 'search_data' / 'solutions_search_index.json'
            with open(search_index_path, 'w', encoding='utf-8') as f:
                json.dump(search_index, f, indent=2, ensure_ascii=False)
                
            # Create category indices
            categories = {}
            for entry in search_index:
                category = entry['category']
                if category not in categories:
                    categories[category] = []
                categories[category].append(entry)
                
            for category, entries in categories.items():
                category_index_path = self.output_dir / 'solutions_hub' / 'search_data' / f'solutions_{category}_index.json'
                with open(category_index_path, 'w', encoding='utf-8') as f:
                    json.dump(entries, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Created search index with {len(search_index)} solutions")
            
        except Exception as e:
            logger.error(f"Error creating search index: {str(e)}")

    def generate_comprehensive_report(self):
        """Generate comprehensive scraping report"""
        # Get database statistics
        cursor = self.conn.execute('SELECT COUNT(*) FROM solutions_content')
        total_solutions = cursor.fetchone()[0]
        
        cursor = self.conn.execute('SELECT category, COUNT(*) FROM solutions_content GROUP BY category')
        category_stats = dict(cursor.fetchall())
        
        cursor = self.conn.execute('SELECT solution_type, COUNT(*) FROM solutions_content GROUP BY solution_type')
        type_stats = dict(cursor.fetchall())
        
        report = {
            'scraping_session': {
                'completed_at': datetime.now().isoformat(),
                'base_url': self.base_url,
                'discovered_solutions': len(self.discovered_solutions),
                'scraped_pages': len(self.scraped_urls)
            },
            'statistics': self.download_stats,
            'content_analysis': {
                'total_solutions': total_solutions,
                'category_distribution': category_stats,
                'solution_type_distribution': type_stats
            },
            'discovered_endpoints': list(self.discovered_solutions),
            'recommendations': [
                "Solutions content has been comprehensively scraped and structured",
                "Use solutions_search_index.json for fast content discovery",
                "Category-specific indices available for targeted queries",
                "Database contains full content and metadata for AI consumption"
            ]
        }
        
        # Save report
        report_path = self.output_dir / 'solutions_hub' / 'comprehensive_solutions_report.json'
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
            
        return report

    def run_comprehensive_scraping(self):
        """Main comprehensive scraping process"""
        logger.info("Starting comprehensive solutions scraping...")
        
        try:
            # Step 1: Discover all solution pages
            discovered_urls = self.discover_solution_pages()
            
            if not discovered_urls:
                logger.warning("No accessible solution pages found")
                return None
            
            # Step 2: Scrape each discovered page
            for url in discovered_urls:
                self.scrape_solution_page(url)
                
                # Check for newly discovered URLs and scrape them too
                new_urls = [u for u in self.discovered_solutions if u not in self.scraped_urls]
                for new_url in new_urls[:10]:  # Limit to prevent infinite expansion
                    if 'solutions/' in new_url:
                        self.scrape_solution_page(new_url)
            
            # Step 3: Commit database changes
            self.conn.commit()
            
            # Step 4: Create search indices
            self.create_solutions_search_index()
            
            # Step 5: Generate report
            report = self.generate_comprehensive_report()
            
            logger.info("Comprehensive solutions scraping completed!")
            logger.info(f"Final Statistics: {self.download_stats}")
            
            return report
            
        except Exception as e:
            logger.error(f"Comprehensive scraping failed: {str(e)}")
            raise
        finally:
            self.conn.close()

if __name__ == "__main__":
    scraper = ComprehensiveSolutionsScraper()
    report = scraper.run_comprehensive_scraping()
    
    if report:
        print("\n" + "="*60)
        print("COMPREHENSIVE SOLUTIONS SCRAPING COMPLETED")
        print("="*60)
        print(f"Solution pages scraped: {report['statistics']['solution_pages']}")
        print(f"Articles discovered: {report['statistics']['articles_discovered']}")
        print(f"Content pieces processed: {report['statistics']['content_processed']}")
        print(f"Total solutions in database: {report['content_analysis']['total_solutions']}")
        print(f"Categories found: {len(report['content_analysis']['category_distribution'])}")
        print(f"Errors encountered: {report['statistics']['errors']}")
        print(f"\nSolutions content stored in: ai_knowledge_hub/solutions_hub/solution_articles/")
        print(f"Search index: ai_knowledge_hub/solutions_hub/search_data/solutions_search_index.json")
        print(f"Database: ai_knowledge_hub/solutions_comprehensive.db")
    else:
        print("No solutions content could be accessed. Check authentication requirements.")
