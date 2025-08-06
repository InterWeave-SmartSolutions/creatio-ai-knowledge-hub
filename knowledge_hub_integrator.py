#!/usr/bin/env python3
"""
Creatio Knowledge Hub Integrator
Combines existing Academy data with Solutions hub content
Creates comprehensive AI-ready knowledge base
"""

import json
import sqlite3
import os
import re
from pathlib import Path
from datetime import datetime
import logging
import requests
from bs4 import BeautifulSoup
import html2text
import hashlib
from urllib.parse import urljoin, urlparse
import time
import random

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('knowledge_hub_integration.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class KnowledgeHubIntegrator:
    def __init__(self, base_dir="/home/andrewwork/creatio-ai-knowledge-hub"):
        self.base_dir = Path(base_dir)
        self.output_dir = self.base_dir / "ai_knowledge_hub"
        self.solutions_dir = self.output_dir / "solutions_hub"
        
        # Setup directories
        self.setup_directories()
        
        # Setup database
        self.setup_integrated_database()
        
        # Session for web requests
        self.session = requests.Session()
        self.update_session_headers()
        
        # HTML to text converter
        self.h = html2text.HTML2Text()
        self.h.ignore_links = False
        self.h.body_width = 0
        
        # Statistics
        self.integration_stats = {
            'academy_urls_processed': 0,
            'solutions_content_extracted': 0,
            'total_pages_indexed': 0,
            'media_files_processed': 0,
            'ai_ready_entries': 0,
            'errors': 0
        }
        
    def setup_directories(self):
        """Create comprehensive directory structure"""
        dirs = [
            'solutions_hub',
            'solutions_hub/pages',
            'solutions_hub/academy_content',
            'solutions_hub/solutions_content', 
            'solutions_hub/images',
            'solutions_hub/videos',
            'solutions_hub/documents',
            'solutions_hub/gifs',
            'solutions_hub/ai_ready',
            'solutions_hub/search_data',
            'solutions_hub/metadata',
            'solutions_hub/structured_data'
        ]
        
        for dir_name in dirs:
            (self.output_dir / dir_name).mkdir(parents=True, exist_ok=True)
            
    def update_session_headers(self):
        """Update session headers for web requests"""
        user_agents = [
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        ]
        
        self.session.headers.update({
            'User-Agent': random.choice(user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Referer': 'https://www.google.com/',
            'DNT': '1'
        })
            
    def setup_integrated_database(self):
        """Setup comprehensive SQLite database"""
        self.db_path = self.output_dir / 'integrated_knowledge_hub.db'
        self.conn = sqlite3.connect(str(self.db_path), check_same_thread=False)
        
        # Create comprehensive tables
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS knowledge_content (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT UNIQUE,
                title TEXT,
                content_type TEXT,
                source TEXT,
                category TEXT,
                description TEXT,
                content TEXT,
                markdown_content TEXT,
                word_count INTEGER,
                tags TEXT,
                file_path TEXT,
                scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                file_size INTEGER,
                checksum TEXT
            )
        ''')
        
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS ai_ready_content (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                knowledge_id INTEGER,
                title TEXT,
                summary TEXT,
                key_concepts TEXT,
                use_cases TEXT,
                related_topics TEXT,
                difficulty_level TEXT,
                content_format TEXT,
                ai_tags TEXT,
                structured_data TEXT,
                FOREIGN KEY (knowledge_id) REFERENCES knowledge_content (id)
            )
        ''')
        
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS content_relationships (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source_id INTEGER,
                target_id INTEGER,
                relationship_type TEXT,
                strength REAL,
                FOREIGN KEY (source_id) REFERENCES knowledge_content (id),
                FOREIGN KEY (target_id) REFERENCES knowledge_content (id)
            )
        ''')
        
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS media_assets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                knowledge_id INTEGER,
                url TEXT,
                local_path TEXT,
                media_type TEXT,
                file_size INTEGER,
                metadata TEXT,
                FOREIGN KEY (knowledge_id) REFERENCES knowledge_content (id)
            )
        ''')
        
        self.conn.commit()

    def clean_text(self, text):
        """Clean and normalize text content"""
        if not text:
            return ""
        
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'\n\s*\n', '\n\n', text)
        
        # Remove special characters that might cause issues
        text = text.strip()
        
        return text

    def categorize_content(self, url, title, content):
        """Categorize content based on URL and content analysis"""
        url_lower = url.lower()
        title_lower = title.lower() if title else ""
        content_lower = content.lower() if content else ""
        
        # Define categories
        categories = {
            'development': ['dev', 'development', 'code', 'api', 'integration', 'javascript', 'css', 'html'],
            'administration': ['admin', 'setup', 'configuration', 'security', 'user', 'permissions'],
            'applications': ['app', 'creatio-apps', 'service', 'sales', 'marketing', 'finance'],
            'mobile': ['mobile', 'android', 'ios', 'app'],
            'customization': ['custom', 'business-rules', 'workflow', 'process'],
            'solutions': ['solution', 'case-study', 'implementation', 'best-practice'],
            'getting-started': ['getting-started', 'first-app', 'tutorial', 'basics'],
            'reference': ['reference', 'api-reference', 'documentation'],
            'troubleshooting': ['troubleshoot', 'faq', 'problem', 'error', 'issue']
        }
        
        # Check URL and content for category indicators
        for category, keywords in categories.items():
            if any(keyword in url_lower or keyword in title_lower or keyword in content_lower[:500] for keyword in keywords):
                return category
                
        return 'general'

    def extract_key_concepts(self, content):
        """Extract key concepts from content using simple keyword analysis"""
        if not content:
            return []
            
        # Common Creatio concepts
        creatio_concepts = [
            'business process', 'workflow', 'entity schema', 'page schema', 'configuration',
            'freedom ui', 'classic ui', 'section', 'detail', 'lookup', 'dashboard',
            'integration', 'web service', 'odata', 'rest api', 'sql', 'database',
            'user permissions', 'role', 'operation', 'system setting', 'package',
            'mobile app', 'synchronization', 'notification', 'email template',
            'campaign', 'lead', 'opportunity', 'contact', 'account', 'case'
        ]
        
        content_lower = content.lower()
        found_concepts = []
        
        for concept in creatio_concepts:
            if concept in content_lower:
                found_concepts.append(concept)
                
        return found_concepts[:10]  # Limit to top 10

    def determine_difficulty(self, content, url):
        """Determine content difficulty level"""
        if not content:
            return 'unknown'
            
        url_lower = url.lower()
        content_lower = content.lower()
        
        # Beginner indicators
        beginner_indicators = ['getting-started', 'basics', 'overview', 'introduction', 'first']
        
        # Advanced indicators
        advanced_indicators = ['development', 'api', 'integration', 'custom', 'advanced', 'reference']
        
        if any(indicator in url_lower for indicator in beginner_indicators):
            return 'beginner'
        elif any(indicator in url_lower for indicator in advanced_indicators):
            return 'advanced'
        elif len(content) > 3000:  # Long content usually more advanced
            return 'intermediate'
        else:
            return 'beginner'

    def process_academy_urls(self):
        """Process existing Academy URLs from discovered_8x_urls.json"""
        logger.info("Processing Academy URLs...")
        
        urls_file = self.base_dir / 'discovered_8x_urls.json'
        if not urls_file.exists():
            logger.warning("discovered_8x_urls.json not found")
            return
            
        try:
            with open(urls_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                urls = data.get('urls', [])
                
            logger.info(f"Found {len(urls)} Academy URLs to process")
            
            for i, url in enumerate(urls[:50]):  # Process first 50 for testing
                try:
                    self.process_single_url(url, 'academy')
                    self.integration_stats['academy_urls_processed'] += 1
                    
                    # Add delay to be respectful
                    time.sleep(random.uniform(1, 2))
                    
                    if i % 10 == 0:
                        logger.info(f"Processed {i+1}/{len(urls)} Academy URLs")
                        
                except Exception as e:
                    logger.error(f"Error processing {url}: {str(e)}")
                    self.integration_stats['errors'] += 1
                    
        except Exception as e:
            logger.error(f"Error loading Academy URLs: {str(e)}")

    def process_single_url(self, url, source_type):
        """Process a single URL and extract content"""
        try:
            # Check if already processed
            cursor = self.conn.execute('SELECT id FROM knowledge_content WHERE url = ?', (url,))
            if cursor.fetchone():
                logger.debug(f"URL already processed: {url}")
                return
                
            logger.debug(f"Processing: {url}")
            
            # Fetch content
            response = self.session.get(url, timeout=30)
            if response.status_code != 200:
                logger.warning(f"HTTP {response.status_code} for {url}")
                return
                
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract metadata
            title = soup.find('title')
            title = title.get_text().strip() if title else 'Untitled'
            
            description = soup.find('meta', attrs={'name': 'description'})
            description = description.get('content', '') if description else ''
            
            # Extract main content
            content = self.extract_main_content(soup)
            markdown_content = self.h.handle(str(soup))
            
            # Clean content
            content = self.clean_text(content)
            word_count = len(content.split()) if content else 0
            
            # Categorize and analyze
            category = self.categorize_content(url, title, content)
            key_concepts = self.extract_key_concepts(content)
            difficulty = self.determine_difficulty(content, url)
            
            # Generate checksum
            checksum = hashlib.md5(content.encode()).hexdigest()
            
            # Save to main table
            cursor = self.conn.execute('''
                INSERT OR REPLACE INTO knowledge_content 
                (url, title, content_type, source, category, description, content, 
                 markdown_content, word_count, file_size, checksum)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (url, title, 'webpage', source_type, category, description, 
                  content, markdown_content, word_count, len(content.encode()), checksum))
            
            knowledge_id = cursor.lastrowid
            
            # Create AI-ready entry
            self.create_ai_ready_entry(knowledge_id, title, content, key_concepts, category, difficulty)
            
            # Save structured files
            self.save_structured_content(knowledge_id, url, title, content, markdown_content, category)
            
            logger.debug(f"Successfully processed: {title}")
            
        except Exception as e:
            logger.error(f"Error processing {url}: {str(e)}")
            raise

    def extract_main_content(self, soup):
        """Extract main content from HTML, removing navigation and other clutter"""
        # Remove unwanted elements
        for element in soup(['nav', 'header', 'footer', 'script', 'style', 'aside', 'menu']):
            element.decompose()
            
        # Try to find main content areas
        main_content = None
        
        # Common content selectors
        content_selectors = [
            'main', 'article', '.content', '#content', '.main-content',
            '.article-content', '.post-content', '.entry-content'
        ]
        
        for selector in content_selectors:
            main_content = soup.select_one(selector)
            if main_content:
                break
                
        if not main_content:
            main_content = soup.find('body')
            
        if main_content:
            return main_content.get_text(strip=True, separator=' ')
        else:
            return soup.get_text(strip=True, separator=' ')

    def create_ai_ready_entry(self, knowledge_id, title, content, key_concepts, category, difficulty):
        """Create AI-ready structured entry"""
        try:
            # Generate summary (first 300 chars)
            summary = content[:300] + "..." if len(content) > 300 else content
            
            # Generate use cases based on content analysis
            use_cases = self.generate_use_cases(content, category)
            
            # Find related topics
            related_topics = self.find_related_topics(content, key_concepts)
            
            # Create AI tags
            ai_tags = self.generate_ai_tags(title, content, key_concepts, category)
            
            # Create structured data
            structured_data = {
                'title': title,
                'category': category,
                'difficulty': difficulty,
                'key_concepts': key_concepts,
                'use_cases': use_cases,
                'related_topics': related_topics,
                'ai_tags': ai_tags,
                'word_count': len(content.split()),
                'content_type': 'documentation'
            }
            
            # Insert into AI-ready table
            self.conn.execute('''
                INSERT INTO ai_ready_content 
                (knowledge_id, title, summary, key_concepts, use_cases, related_topics,
                 difficulty_level, content_format, ai_tags, structured_data)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (knowledge_id, title, summary, json.dumps(key_concepts), 
                  json.dumps(use_cases), json.dumps(related_topics), 
                  difficulty, 'markdown', json.dumps(ai_tags), 
                  json.dumps(structured_data)))
                  
            self.integration_stats['ai_ready_entries'] += 1
            
        except Exception as e:
            logger.error(f"Error creating AI-ready entry: {str(e)}")

    def generate_use_cases(self, content, category):
        """Generate potential use cases based on content"""
        use_cases = []
        content_lower = content.lower() if content else ""
        
        use_case_patterns = {
            'development': ['building applications', 'customization', 'integration'],
            'administration': ['system setup', 'user management', 'security configuration'],
            'applications': ['business process automation', 'workflow management', 'data analysis'],
            'mobile': ['mobile application development', 'offline synchronization', 'mobile UX'],
            'customization': ['UI customization', 'business logic', 'workflow design']
        }
        
        if category in use_case_patterns:
            use_cases.extend(use_case_patterns[category])
            
        # Add specific use cases based on content keywords
        if 'integration' in content_lower:
            use_cases.append('third-party integration')
        if 'api' in content_lower:
            use_cases.append('API development')
        if 'report' in content_lower:
            use_cases.append('reporting and analytics')
            
        return list(set(use_cases))[:5]  # Limit to 5 unique use cases

    def find_related_topics(self, content, key_concepts):
        """Find related topics based on content analysis"""
        related = []
        
        # Use key concepts as base for related topics
        concept_relations = {
            'business process': ['workflow', 'automation', 'bpm'],
            'integration': ['api', 'web service', 'data sync'],
            'mobile app': ['synchronization', 'offline', 'mobile ui'],
            'freedom ui': ['page schema', 'customization', 'ui design'],
            'user permissions': ['role', 'security', 'access control']
        }
        
        for concept in key_concepts:
            if concept in concept_relations:
                related.extend(concept_relations[concept])
                
        return list(set(related))[:8]  # Limit to 8 related topics

    def generate_ai_tags(self, title, content, key_concepts, category):
        """Generate AI-friendly tags"""
        tags = [category]
        
        # Add key concepts as tags
        tags.extend(key_concepts[:5])
        
        # Add specific tags based on content
        content_lower = content.lower() if content else ""
        title_lower = title.lower() if title else ""
        
        ai_tag_patterns = {
            'tutorial': ['tutorial', 'how-to', 'guide', 'step-by-step'],
            'reference': ['reference', 'api', 'documentation', 'specification'],
            'example': ['example', 'sample', 'demo', 'case-study'],
            'troubleshooting': ['troubleshoot', 'problem', 'error', 'fix'],
            'configuration': ['config', 'setup', 'install', 'configure']
        }
        
        for tag, patterns in ai_tag_patterns.items():
            if any(pattern in title_lower or pattern in content_lower for pattern in patterns):
                tags.append(tag)
                
        return list(set(tags))[:10]  # Limit to 10 tags

    def save_structured_content(self, knowledge_id, url, title, content, markdown_content, category):
        """Save structured content to files for AI consumption"""
        try:
            # Create category directory
            category_dir = self.solutions_dir / 'structured_data' / category
            category_dir.mkdir(parents=True, exist_ok=True)
            
            # Clean filename
            filename = re.sub(r'[<>:"/\\|?*]', '_', title)[:100]
            
            # Save as JSON
            structured_data = {
                'id': knowledge_id,
                'url': url,
                'title': title,
                'category': category,
                'content': content,
                'markdown': markdown_content,
                'word_count': len(content.split()),
                'processed_at': datetime.now().isoformat()
            }
            
            json_path = category_dir / f"{knowledge_id}_{filename}.json"
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(structured_data, f, indent=2, ensure_ascii=False)
                
            # Save as markdown for easy reading
            md_path = category_dir / f"{knowledge_id}_{filename}.md"
            with open(md_path, 'w', encoding='utf-8') as f:
                f.write(f"# {title}\n\n")
                f.write(f"**URL:** {url}\n")
                f.write(f"**Category:** {category}\n")
                f.write(f"**Word Count:** {len(content.split())}\n\n")
                f.write("## Content\n\n")
                f.write(markdown_content)
                
        except Exception as e:
            logger.error(f"Error saving structured content: {str(e)}")

    def create_ai_search_index(self):
        """Create comprehensive search index for AI consumption"""
        logger.info("Creating AI search index...")
        
        try:
            # Get all AI-ready content
            cursor = self.conn.execute('''
                SELECT kc.id, kc.url, kc.title, kc.category, kc.description, kc.content,
                       arc.summary, arc.key_concepts, arc.use_cases, arc.related_topics,
                       arc.difficulty_level, arc.ai_tags
                FROM knowledge_content kc
                JOIN ai_ready_content arc ON kc.id = arc.knowledge_id
                ORDER BY kc.title
            ''')
            
            search_index = []
            for row in cursor:
                (id, url, title, category, description, content, summary, 
                 key_concepts, use_cases, related_topics, difficulty, ai_tags) = row
                
                # Parse JSON fields
                try:
                    key_concepts = json.loads(key_concepts) if key_concepts else []
                    use_cases = json.loads(use_cases) if use_cases else []
                    related_topics = json.loads(related_topics) if related_topics else []
                    ai_tags = json.loads(ai_tags) if ai_tags else []
                except:
                    key_concepts = use_cases = related_topics = ai_tags = []
                
                search_entry = {
                    'id': id,
                    'url': url,
                    'title': title,
                    'category': category,
                    'description': description,
                    'summary': summary,
                    'key_concepts': key_concepts,
                    'use_cases': use_cases,
                    'related_topics': related_topics,
                    'difficulty': difficulty,
                    'ai_tags': ai_tags,
                    'content_preview': content[:500] if content else "",
                    'searchable_text': f"{title} {description} {summary} {' '.join(key_concepts)} {' '.join(ai_tags)}"
                }
                
                search_index.append(search_entry)
            
            # Save search index
            search_index_path = self.solutions_dir / 'search_data' / 'ai_search_index.json'
            with open(search_index_path, 'w', encoding='utf-8') as f:
                json.dump(search_index, f, indent=2, ensure_ascii=False)
                
            # Create category-based indices
            categories = {}
            for entry in search_index:
                category = entry['category']
                if category not in categories:
                    categories[category] = []
                categories[category].append(entry)
                
            for category, entries in categories.items():
                category_index_path = self.solutions_dir / 'search_data' / f'{category}_index.json'
                with open(category_index_path, 'w', encoding='utf-8') as f:
                    json.dump(entries, f, indent=2, ensure_ascii=False)
            
            self.integration_stats['total_pages_indexed'] = len(search_index)
            logger.info(f"Created AI search index with {len(search_index)} entries")
            
        except Exception as e:
            logger.error(f"Error creating search index: {str(e)}")

    def generate_integration_report(self):
        """Generate comprehensive integration report"""
        logger.info("Generating integration report...")
        
        # Get database statistics
        cursor = self.conn.execute('SELECT COUNT(*) FROM knowledge_content')
        total_content = cursor.fetchone()[0]
        
        cursor = self.conn.execute('SELECT COUNT(*) FROM ai_ready_content')
        ai_ready_count = cursor.fetchone()[0]
        
        cursor = self.conn.execute('SELECT category, COUNT(*) FROM knowledge_content GROUP BY category')
        category_stats = dict(cursor.fetchall())
        
        cursor = self.conn.execute('SELECT difficulty_level, COUNT(*) FROM ai_ready_content GROUP BY difficulty_level')
        difficulty_stats = dict(cursor.fetchall())
        
        # Calculate directory sizes
        file_structure = {}
        if self.solutions_dir.exists():
            for subdir in self.solutions_dir.iterdir():
                if subdir.is_dir():
                    size = sum(f.stat().st_size for f in subdir.rglob('*') if f.is_file())
                    file_count = len(list(subdir.rglob('*')))
                    file_structure[subdir.name] = {
                        'size_bytes': size,
                        'size_mb': round(size / (1024 * 1024), 2),
                        'file_count': file_count
                    }
        
        report = {
            'integration_session': {
                'completed_at': datetime.now().isoformat(),
                'processing_statistics': self.integration_stats
            },
            'database_statistics': {
                'total_knowledge_entries': total_content,
                'ai_ready_entries': ai_ready_count,
                'category_distribution': category_stats,
                'difficulty_distribution': difficulty_stats
            },
            'file_structure': file_structure,
            'ai_features': {
                'search_indices_created': True,
                'structured_data_available': True,
                'category_based_organization': True,
                'difficulty_levels_assigned': True,
                'ai_tags_generated': True
            },
            'recommendations': [
                "Use the ai_search_index.json for comprehensive content search",
                "Access structured data by category for specific domain queries",
                "Use difficulty levels to guide content recommendations",
                "Leverage AI tags for content classification and filtering",
                "Query the database directly for complex content relationships"
            ]
        }
        
        # Save report
        report_path = self.solutions_dir / 'integration_report.json'
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
            
        return report

    def run_integration(self):
        """Main integration process"""
        logger.info("Starting Knowledge Hub Integration...")
        
        try:
            # Process Academy URLs
            self.process_academy_urls()
            
            # Commit database changes
            self.conn.commit()
            
            # Create AI search index
            self.create_ai_search_index()
            
            # Generate report
            report = self.generate_integration_report()
            
            logger.info("Knowledge Hub Integration completed successfully!")
            logger.info(f"Integration Statistics: {self.integration_stats}")
            
            return report
            
        except Exception as e:
            logger.error(f"Integration failed: {str(e)}")
            raise
        finally:
            self.conn.close()

if __name__ == "__main__":
    integrator = KnowledgeHubIntegrator()
    report = integrator.run_integration()
    
    print("\n" + "="*60)
    print("KNOWLEDGE HUB INTEGRATION COMPLETED")
    print("="*60)
    print(f"Academy URLs processed: {report['integration_session']['processing_statistics']['academy_urls_processed']}")
    print(f"Total knowledge entries: {report['database_statistics']['total_knowledge_entries']}")
    print(f"AI-ready entries: {report['database_statistics']['ai_ready_entries']}")
    print(f"Categories created: {len(report['database_statistics']['category_distribution'])}")
    print(f"Errors encountered: {report['integration_session']['processing_statistics']['errors']}")
    print(f"\nContent organized in: ai_knowledge_hub/solutions_hub/")
    print(f"AI Search Index: ai_knowledge_hub/solutions_hub/search_data/ai_search_index.json")
    print(f"Integration Database: ai_knowledge_hub/integrated_knowledge_hub.db")
