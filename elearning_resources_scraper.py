#!/usr/bin/env python3
"""
E-Learning Resources Scraper for Creatio Academy
Focuses on extracting:
- Tutorials and guides
- Best practices documentation
- Code examples and templates
- Community forum valuable threads
- Organization by topic and difficulty level
"""

import requests
from bs4 import BeautifulSoup
import json
import os
import time
from urllib.parse import urljoin, urlparse
from datetime import datetime
import re
from collections import defaultdict

class ELearningResourcesScraper:
    def __init__(self):
        self.base_url = "https://academy.creatio.com"
        self.community_url = "https://community.creatio.com"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.resources = {
            'tutorials': [],
            'guides': [],
            'best_practices': [],
            'code_examples': [],
            'forum_threads': []
        }
        self.visited_urls = set()
        
    def get_page(self, url, delay=2):
        """Fetch a page with configurable delay between requests"""
        if url in self.visited_urls:
            return None
        
        time.sleep(delay)
        self.visited_urls.add(url)
        
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return None
    
    def extract_difficulty_level(self, text):
        """Extract difficulty level from text content"""
        text_lower = text.lower()
        if any(word in text_lower for word in ['beginner', 'basic', 'introduction', 'getting started']):
            return 'Beginner'
        elif any(word in text_lower for word in ['intermediate', 'moderate']):
            return 'Intermediate'
        elif any(word in text_lower for word in ['advanced', 'expert', 'complex']):
            return 'Advanced'
        return 'General'
    
    def extract_topic_category(self, text, url):
        """Extract topic category from text and URL"""
        text_lower = text.lower()
        url_lower = url.lower()
        
        # Define topic mappings
        topic_mappings = {
            'Development': ['development', 'coding', 'programming', 'api', 'script', 'code'],
            'Administration': ['admin', 'configuration', 'setup', 'install', 'deploy'],
            'Business Process': ['bpm', 'business process', 'workflow', 'automation'],
            'Marketing': ['marketing', 'campaign', 'email', 'lead'],
            'Sales': ['sales', 'opportunity', 'quote', 'forecast'],
            'Service': ['service', 'case', 'support', 'ticket'],
            'Integration': ['integration', 'connector', 'sync', 'import', 'export'],
            'UI/UX': ['ui', 'ux', 'design', 'interface', 'page', 'form'],
            'Security': ['security', 'permission', 'access', 'authentication'],
            'Performance': ['performance', 'optimization', 'speed', 'cache']
        }
        
        for topic, keywords in topic_mappings.items():
            if any(keyword in text_lower or keyword in url_lower for keyword in keywords):
                return topic
        
        return 'General'
    
    def scrape_documentation_pages(self):
        """Scrape documentation pages for tutorials and guides"""
        print("\n" + "="*50)
        print("Scraping Documentation Pages")
        print("="*50)
        
        # Common documentation URLs to check
        doc_urls = [
            '/docs',
            '/documentation',
            '/guides',
            '/tutorials',
            '/resources',
            '/learning',
            '/knowledge-base'
        ]
        
        for doc_path in doc_urls:
            url = urljoin(self.base_url, doc_path)
            response = self.get_page(url)
            
            if not response:
                continue
                
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Look for tutorial and guide links
            links = soup.find_all('a', href=True)
            for link in links:
                href = link.get('href')
                text = link.get_text(strip=True)
                
                if not text or len(text) < 5:
                    continue
                
                # Check if this looks like a tutorial or guide
                if any(keyword in text.lower() for keyword in ['tutorial', 'guide', 'how to', 'getting started', 'walkthrough']):
                    resource_url = urljoin(self.base_url, href)
                    
                    resource = {
                        'title': text,
                        'url': resource_url,
                        'type': 'tutorial' if 'tutorial' in text.lower() else 'guide',
                        'topic': self.extract_topic_category(text, resource_url),
                        'difficulty': self.extract_difficulty_level(text),
                        'scraped_at': datetime.now().isoformat()
                    }
                    
                    if 'tutorial' in text.lower():
                        self.resources['tutorials'].append(resource)
                        print(f"Found tutorial: {text}")
                    else:
                        self.resources['guides'].append(resource)
                        print(f"Found guide: {text}")
    
    def scrape_best_practices(self):
        """Scrape best practices documentation"""
        print("\n" + "="*50)
        print("Scraping Best Practices")
        print("="*50)
        
        # URLs likely to contain best practices
        bp_urls = [
            '/best-practices',
            '/docs/best-practices',
            '/resources/best-practices'
        ]
        
        for bp_path in bp_urls:
            url = urljoin(self.base_url, bp_path)
            response = self.get_page(url)
            
            if not response:
                continue
                
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Look for best practice content
            articles = soup.find_all(['article', 'div'], class_=re.compile('content|article|post'))
            
            for article in articles:
                title_elem = article.find(['h1', 'h2', 'h3'])
                if title_elem:
                    title = title_elem.get_text(strip=True)
                    
                    # Extract description
                    desc_elem = article.find(['p', 'div'], class_=re.compile('desc|summary|excerpt'))
                    description = desc_elem.get_text(strip=True) if desc_elem else ""
                    
                    resource = {
                        'title': title,
                        'description': description,
                        'url': url,
                        'topic': self.extract_topic_category(title + ' ' + description, url),
                        'difficulty': self.extract_difficulty_level(title + ' ' + description),
                        'scraped_at': datetime.now().isoformat()
                    }
                    
                    self.resources['best_practices'].append(resource)
                    print(f"Found best practice: {title}")
    
    def scrape_code_examples(self):
        """Scrape code examples and templates"""
        print("\n" + "="*50)
        print("Scraping Code Examples and Templates")
        print("="*50)
        
        # URLs likely to contain code examples
        code_urls = [
            '/examples',
            '/code-examples',
            '/templates',
            '/snippets',
            '/downloads'
        ]
        
        for code_path in code_urls:
            url = urljoin(self.base_url, code_path)
            response = self.get_page(url)
            
            if not response:
                continue
                
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Look for code blocks and download links
            code_blocks = soup.find_all(['pre', 'code'])
            for block in code_blocks:
                # Get parent context for title
                parent = block.parent
                title = "Code Example"
                
                for _ in range(3):
                    if parent:
                        title_elem = parent.find(['h1', 'h2', 'h3', 'h4'])
                        if title_elem:
                            title = title_elem.get_text(strip=True)
                            break
                        parent = parent.parent
                
                code_content = block.get_text(strip=True)
                if len(code_content) > 50:  # Skip very short snippets
                    resource = {
                        'title': title,
                        'code_snippet': code_content[:500] + '...' if len(code_content) > 500 else code_content,
                        'url': url,
                        'language': block.get('class', [''])[0] if block.get('class') else 'unknown',
                        'topic': self.extract_topic_category(title + ' ' + code_content, url),
                        'difficulty': self.extract_difficulty_level(title),
                        'scraped_at': datetime.now().isoformat()
                    }
                    
                    self.resources['code_examples'].append(resource)
                    print(f"Found code example: {title}")
            
            # Look for downloadable templates
            download_links = soup.find_all('a', href=re.compile(r'\.(zip|rar|gz|template)$', re.I))
            for link in download_links:
                href = link.get('href')
                text = link.get_text(strip=True)
                
                resource = {
                    'title': text or os.path.basename(href),
                    'download_url': urljoin(url, href),
                    'type': 'template',
                    'topic': self.extract_topic_category(text, href),
                    'scraped_at': datetime.now().isoformat()
                }
                
                self.resources['code_examples'].append(resource)
                print(f"Found template: {resource['title']}")
    
    def scrape_community_forum(self):
        """Scrape valuable community forum threads"""
        print("\n" + "="*50)
        print("Scraping Community Forum")
        print("="*50)
        
        # Try to access community forum
        forum_response = self.get_page(self.community_url)
        
        if not forum_response:
            print("Could not access community forum")
            return
            
        soup = BeautifulSoup(forum_response.content, 'html.parser')
        
        # Look for popular or featured threads
        thread_containers = soup.find_all(['div', 'article'], class_=re.compile('topic|thread|post|discussion'))
        
        for container in thread_containers[:20]:  # Limit to top 20 threads
            title_elem = container.find(['h2', 'h3', 'a'], class_=re.compile('title|subject'))
            if not title_elem:
                continue
                
            title = title_elem.get_text(strip=True)
            thread_url = title_elem.get('href') if title_elem.name == 'a' else None
            
            if not thread_url:
                link = container.find('a', href=True)
                if link:
                    thread_url = link.get('href')
            
            if thread_url:
                thread_url = urljoin(self.community_url, thread_url)
            
            # Extract metadata
            views = 0
            replies = 0
            
            # Look for view count
            view_elem = container.find(text=re.compile(r'\d+\s*views?', re.I))
            if view_elem:
                views_match = re.search(r'(\d+)', view_elem)
                if views_match:
                    views = int(views_match.group(1))
            
            # Look for reply count
            reply_elem = container.find(text=re.compile(r'\d+\s*(?:replies|comments|responses)', re.I))
            if reply_elem:
                replies_match = re.search(r'(\d+)', reply_elem)
                if replies_match:
                    replies = int(replies_match.group(1))
            
            # Consider thread valuable if it has many views or replies
            if views > 100 or replies > 5:
                resource = {
                    'title': title,
                    'url': thread_url or self.community_url,
                    'views': views,
                    'replies': replies,
                    'topic': self.extract_topic_category(title, thread_url or ''),
                    'difficulty': self.extract_difficulty_level(title),
                    'scraped_at': datetime.now().isoformat()
                }
                
                self.resources['forum_threads'].append(resource)
                print(f"Found valuable thread: {title} ({views} views, {replies} replies)")
    
    def organize_by_topic_and_difficulty(self):
        """Organize all resources by topic and difficulty level"""
        organized = defaultdict(lambda: defaultdict(list))
        
        # Organize each resource type
        for resource_type, resources in self.resources.items():
            for resource in resources:
                topic = resource.get('topic', 'General')
                difficulty = resource.get('difficulty', 'General')
                
                organized[topic][difficulty].append({
                    'type': resource_type,
                    'resource': resource
                })
        
        return dict(organized)
    
    def save_results(self):
        """Save all scraped resources to files"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Create output directory
        output_dir = f'elearning_resources_{timestamp}'
        os.makedirs(output_dir, exist_ok=True)
        
        # Save raw resources
        with open(os.path.join(output_dir, 'all_resources.json'), 'w', encoding='utf-8') as f:
            json.dump(self.resources, f, indent=2, ensure_ascii=False)
        
        # Save organized resources
        organized = self.organize_by_topic_and_difficulty()
        with open(os.path.join(output_dir, 'organized_resources.json'), 'w', encoding='utf-8') as f:
            json.dump(organized, f, indent=2, ensure_ascii=False)
        
        # Create summary report
        summary = {
            'scraped_at': datetime.now().isoformat(),
            'total_resources': sum(len(resources) for resources in self.resources.values()),
            'breakdown': {
                'tutorials': len(self.resources['tutorials']),
                'guides': len(self.resources['guides']),
                'best_practices': len(self.resources['best_practices']),
                'code_examples': len(self.resources['code_examples']),
                'forum_threads': len(self.resources['forum_threads'])
            },
            'topics': list(organized.keys()),
            'output_directory': output_dir
        }
        
        with open(os.path.join(output_dir, 'summary.json'), 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        
        # Create markdown report
        self.create_markdown_report(output_dir, summary, organized)
        
        print(f"\n\nResults saved to: {output_dir}")
        return output_dir
    
    def create_markdown_report(self, output_dir, summary, organized):
        """Create a comprehensive markdown report"""
        report_path = os.path.join(output_dir, 'REPORT.md')
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("# E-Learning Resources Scraping Report\n\n")
            f.write(f"**Generated**: {summary['scraped_at']}\n\n")
            f.write("## Summary\n\n")
            f.write(f"- **Total Resources Found**: {summary['total_resources']}\n")
            f.write(f"- **Tutorials**: {summary['breakdown']['tutorials']}\n")
            f.write(f"- **Guides**: {summary['breakdown']['guides']}\n")
            f.write(f"- **Best Practices**: {summary['breakdown']['best_practices']}\n")
            f.write(f"- **Code Examples**: {summary['breakdown']['code_examples']}\n")
            f.write(f"- **Forum Threads**: {summary['breakdown']['forum_threads']}\n\n")
            
            f.write("## Resources by Topic and Difficulty\n\n")
            
            for topic in sorted(organized.keys()):
                f.write(f"### {topic}\n\n")
                
                for difficulty in ['Beginner', 'Intermediate', 'Advanced', 'General']:
                    if difficulty in organized[topic]:
                        resources = organized[topic][difficulty]
                        if resources:
                            f.write(f"#### {difficulty} Level ({len(resources)} resources)\n\n")
                            
                            for item in resources[:5]:  # Show first 5 of each
                                resource = item['resource']
                                resource_type = item['type'].replace('_', ' ').title()
                                f.write(f"- **[{resource_type}]** {resource.get('title', 'Untitled')}\n")
                                if resource.get('url'):
                                    f.write(f"  - URL: {resource['url']}\n")
                                if resource.get('description'):
                                    f.write(f"  - Description: {resource['description'][:100]}...\n")
                                f.write("\n")
                            
                            if len(resources) > 5:
                                f.write(f"  *...and {len(resources) - 5} more*\n\n")
    
    def scrape(self):
        """Main scraping function"""
        print("Starting E-Learning Resources Scraping")
        print("=" * 60)
        print(f"Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Run all scraping functions
        self.scrape_documentation_pages()
        self.scrape_best_practices()
        self.scrape_code_examples()
        self.scrape_community_forum()
        
        # Save results
        output_dir = self.save_results()
        
        # Print summary
        print("\n" + "=" * 60)
        print("SCRAPING COMPLETE")
        print("=" * 60)
        print(f"Total resources scraped: {sum(len(resources) for resources in self.resources.values())}")
        print(f"- Tutorials: {len(self.resources['tutorials'])}")
        print(f"- Guides: {len(self.resources['guides'])}")
        print(f"- Best Practices: {len(self.resources['best_practices'])}")
        print(f"- Code Examples: {len(self.resources['code_examples'])}")
        print(f"- Forum Threads: {len(self.resources['forum_threads'])}")
        print(f"\nEnd time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        return self.resources

if __name__ == "__main__":
    scraper = ELearningResourcesScraper()
    resources = scraper.scrape()
