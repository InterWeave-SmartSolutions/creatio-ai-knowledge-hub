#!/usr/bin/env python3
"""
Enhanced Creatio Documentation Scraper
Targets the actual Creatio documentation structure
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

class CreatioDocsScraper:
    def __init__(self):
        self.docs_url = "https://academy.creatio.com/docs"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.resources = {
            'user_docs': [],
            'developer_docs': [],
            'api_references': [],
            'release_notes': [],
            'best_practices': []
        }
        self.visited_urls = set()
        
    def get_page(self, url, delay=2):
        """Fetch a page with delay"""
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
    
    def extract_metadata(self, text, url):
        """Extract metadata from text and URL"""
        text_lower = text.lower()
        
        # Difficulty level
        if any(word in text_lower for word in ['getting started', 'introduction', 'basics', 'beginner']):
            difficulty = 'Beginner'
        elif any(word in text_lower for word in ['advanced', 'expert', 'complex']):
            difficulty = 'Advanced'
        else:
            difficulty = 'Intermediate'
        
        # Topic category
        topic_mappings = {
            'Development': ['developer', 'development', 'coding', 'api', 'script'],
            'Administration': ['admin', 'configuration', 'setup', 'install'],
            'User Guide': ['user', 'guide', 'how to', 'tutorial'],
            'Integration': ['integration', 'connector', 'api'],
            'Release Notes': ['release', 'update', 'version', 'changelog']
        }
        
        topic = 'General'
        for t, keywords in topic_mappings.items():
            if any(k in text_lower or k in url.lower() for k in keywords):
                topic = t
                break
        
        return difficulty, topic
    
    def scrape_docs_section(self, section_url, section_name):
        """Scrape a specific documentation section"""
        print(f"\nScraping {section_name} section...")
        response = self.get_page(section_url)
        
        if not response:
            return []
        
        soup = BeautifulSoup(response.content, 'html.parser')
        resources = []
        
        # Find documentation links
        doc_links = soup.find_all('a', href=True)
        
        for link in doc_links:
            href = link.get('href')
            text = link.get_text(strip=True)
            
            if not text or len(text) < 5:
                continue
            
            # Skip navigation and external links
            if any(skip in href for skip in ['#', 'javascript:', 'mailto:', 'http']):
                if 'academy.creatio.com' not in href:
                    continue
            
            doc_url = urljoin(section_url, href)
            difficulty, topic = self.extract_metadata(text, doc_url)
            
            resource = {
                'title': text,
                'url': doc_url,
                'section': section_name,
                'topic': topic,
                'difficulty': difficulty,
                'scraped_at': datetime.now().isoformat()
            }
            
            resources.append(resource)
            print(f"  Found: {text[:50]}...")
        
        return resources
    
    def scrape_main_docs(self):
        """Scrape main documentation sections"""
        print("\n" + "="*60)
        print("Scraping Creatio Documentation")
        print("="*60)
        
        # Main documentation sections
        sections = {
            'user_docs': [
                ('/docs/user', 'User Documentation'),
                ('/docs/8.x/user', 'User Guide 8.x'),
                ('/docs/user/platform_basics', 'Platform Basics')
            ],
            'developer_docs': [
                ('/docs/developer', 'Developer Documentation'),
                ('/docs/8.x/dev', 'Developer Guide 8.x'),
                ('/docs/developer/getting_started', 'Getting Started')
            ],
            'api_references': [
                ('/docs/developer/api', 'API Reference'),
                ('/docs/api-reference', 'API Documentation')
            ],
            'release_notes': [
                ('/docs/release-notes', 'Release Notes'),
                ('/docs/release', 'Release Information')
            ]
        }
        
        for resource_type, section_list in sections.items():
            for path, name in section_list:
                url = urljoin(self.docs_url, path)
                resources = self.scrape_docs_section(url, name)
                self.resources[resource_type].extend(resources)
    
    def scrape_specific_topics(self):
        """Scrape specific topic pages"""
        print("\n" + "="*60)
        print("Scraping Specific Topics")
        print("="*60)
        
        # Specific topics to look for
        topics = [
            'business-process-management',
            'no-code-development',
            'integrations',
            'marketplace',
            'mobile-application',
            'analytics',
            'ai-tools'
        ]
        
        for topic in topics:
            url = f"{self.docs_url}/8.x/user/{topic}"
            print(f"\nChecking topic: {topic}")
            response = self.get_page(url)
            
            if response:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Extract main content
                content = soup.find(['main', 'article', 'div'], class_=re.compile('content|main'))
                if content:
                    title = content.find(['h1', 'h2'])
                    if title:
                        resource = {
                            'title': title.get_text(strip=True),
                            'url': url,
                            'topic': topic.replace('-', ' ').title(),
                            'difficulty': 'Intermediate',
                            'scraped_at': datetime.now().isoformat()
                        }
                        self.resources['best_practices'].append(resource)
                        print(f"  Found topic page: {resource['title']}")
    
    def organize_resources(self):
        """Organize all resources by topic and difficulty"""
        organized = defaultdict(lambda: defaultdict(list))
        
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
        """Save all results"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_dir = f'creatio_docs_{timestamp}'
        os.makedirs(output_dir, exist_ok=True)
        
        # Save raw resources
        with open(os.path.join(output_dir, 'all_resources.json'), 'w', encoding='utf-8') as f:
            json.dump(self.resources, f, indent=2, ensure_ascii=False)
        
        # Save organized resources
        organized = self.organize_resources()
        with open(os.path.join(output_dir, 'organized_resources.json'), 'w', encoding='utf-8') as f:
            json.dump(organized, f, indent=2, ensure_ascii=False)
        
        # Create summary
        total_resources = sum(len(r) for r in self.resources.values())
        summary = {
            'scraped_at': datetime.now().isoformat(),
            'total_resources': total_resources,
            'breakdown': {k: len(v) for k, v in self.resources.items()},
            'topics': list(organized.keys())
        }
        
        with open(os.path.join(output_dir, 'summary.json'), 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        
        # Create report
        self.create_report(output_dir, summary, organized)
        
        return output_dir
    
    def create_report(self, output_dir, summary, organized):
        """Create markdown report"""
        with open(os.path.join(output_dir, 'REPORT.md'), 'w', encoding='utf-8') as f:
            f.write("# Creatio Documentation Scraping Report\n\n")
            f.write(f"**Generated**: {summary['scraped_at']}\n\n")
            f.write("## Summary\n\n")
            f.write(f"- **Total Resources**: {summary['total_resources']}\n")
            
            for resource_type, count in summary['breakdown'].items():
                f.write(f"- **{resource_type.replace('_', ' ').title()}**: {count}\n")
            
            f.write("\n## Resources by Topic\n\n")
            
            for topic in sorted(organized.keys()):
                f.write(f"### {topic}\n\n")
                
                for difficulty in ['Beginner', 'Intermediate', 'Advanced']:
                    if difficulty in organized[topic]:
                        resources = organized[topic][difficulty]
                        f.write(f"#### {difficulty} ({len(resources)} resources)\n\n")
                        
                        for item in resources[:5]:
                            resource = item['resource']
                            f.write(f"- {resource.get('title', 'Untitled')}\n")
                            f.write(f"  - URL: {resource.get('url', 'N/A')}\n\n")
    
    def scrape(self):
        """Main scraping function"""
        print("Starting Creatio Documentation Scraping")
        print("="*60)
        start_time = datetime.now()
        
        # Scrape documentation
        self.scrape_main_docs()
        self.scrape_specific_topics()
        
        # Save results
        output_dir = self.save_results()
        
        # Print summary
        total = sum(len(r) for r in self.resources.values())
        print(f"\n{'='*60}")
        print("SCRAPING COMPLETE")
        print(f"{'='*60}")
        print(f"Total resources found: {total}")
        print(f"Time taken: {datetime.now() - start_time}")
        print(f"Results saved to: {output_dir}")
        
        return self.resources

if __name__ == "__main__":
    scraper = CreatioDocsScraper()
    scraper.scrape()
