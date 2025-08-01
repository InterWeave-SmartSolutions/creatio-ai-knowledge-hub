import requests
from bs4 import BeautifulSoup
import json
import csv
import time
from urllib.parse import urljoin, urlparse
from datetime import datetime
import re

class CreatioAcademyScraper:
    def __init__(self):
        self.base_url = "https://academy.creatio.com"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.courses = []
        self.categories = {}
        self.visited_urls = set()
        
    def get_page(self, url):
        """Fetch a page with 2-second delay between requests"""
        time.sleep(2)  # Implement 2-second delay
        try:
            response = self.session.get(url)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return None
    
    def extract_course_from_page(self, url, category="General"):
        """Extract detailed course information from a specific course page"""
        if url in self.visited_urls:
            return None
        self.visited_urls.add(url)
        
        response = self.get_page(url)
        if not response:
            return None
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        course = {
            'category': category,
            'subcategory': '',
            'title': '',
            'url': url,
            'description': '',
            'duration': '',
            'level': '',
            'format': '',
            'price': '',
            'language': '',
            'scraped_at': datetime.now().isoformat()
        }
        
        # Extract title
        title = soup.find('h1')
        if title:
            course['title'] = title.get_text(strip=True)
        else:
            # Try meta title
            meta_title = soup.find('meta', property='og:title')
            if meta_title:
                course['title'] = meta_title.get('content', '').replace(' | Creatio Academy', '')
        
        # Extract description
        meta_desc = soup.find('meta', {'name': 'description'})
        if meta_desc:
            course['description'] = meta_desc.get('content', '')
        
        # Look for course details in various formats
        # Search for duration
        duration_patterns = [
            r'(\d+\s*(?:hours?|days?|weeks?))',
            r'Duration:\s*([^\n]+)',
            r'Length:\s*([^\n]+)'
        ]
        
        page_text = soup.get_text()
        for pattern in duration_patterns:
            match = re.search(pattern, page_text, re.IGNORECASE)
            if match:
                course['duration'] = match.group(1).strip()
                break
        
        # Search for level
        level_keywords = ['beginner', 'intermediate', 'advanced', 'expert']
        for keyword in level_keywords:
            if keyword in page_text.lower():
                course['level'] = keyword.capitalize()
                break
        
        # Search for format (online, in-person, etc.)
        format_keywords = ['online', 'virtual', 'in-person', 'classroom', 'self-paced', 'instructor-led']
        for keyword in format_keywords:
            if keyword in page_text.lower():
                course['format'] = keyword.replace('-', ' ').title()
                break
        
        # Extract language if available
        lang_elem = soup.find('html')
        if lang_elem and lang_elem.get('lang'):
            course['language'] = lang_elem['lang']
        
        return course
    
    def scrape_training_catalog(self):
        """Scrape the training catalog page"""
        training_url = urljoin(self.base_url, '/training')
        response = self.get_page(training_url)
        if not response:
            return []
        
        soup = BeautifulSoup(response.content, 'html.parser')
        courses = []
        
        # Find all "Learn more" links which lead to individual training pages
        learn_more_links = soup.find_all('a', text=re.compile('Learn more', re.IGNORECASE))
        
        for link in learn_more_links:
            href = link.get('href')
            if href and '/training/' in href:
                course_url = urljoin(self.base_url, href)
                
                # Try to get the course title from parent elements
                parent = link.parent
                title = ""
                for _ in range(5):  # Look up to 5 levels up
                    if parent:
                        title_elem = parent.find(['h2', 'h3', 'h4'])
                        if title_elem:
                            title = title_elem.get_text(strip=True)
                            break
                        parent = parent.parent
                
                print(f"Found training: {title if title else 'Unknown'} - {course_url}")
                
                # Extract detailed course info
                course_data = self.extract_course_from_page(course_url, "Instructor-led Training")
                if course_data:
                    if not course_data['title'] and title:
                        course_data['title'] = title
                    courses.append(course_data)
        
        # Also look for any direct training links
        training_links = soup.find_all('a', href=re.compile(r'/training/[^/]+$'))
        for link in training_links:
            href = link.get('href')
            if href and href not in ['/training', '/training/']:
                course_url = urljoin(self.base_url, href)
                if course_url not in self.visited_urls:
                    title = link.get_text(strip=True)
                    if title and len(title) > 3:  # Skip very short texts
                        print(f"Found additional training: {title} - {course_url}")
                        course_data = self.extract_course_from_page(course_url, "Instructor-led Training")
                        if course_data:
                            courses.append(course_data)
        
        return courses
    
    def scrape_elearning_catalog(self):
        """Scrape the e-learning catalog"""
        elearning_url = urljoin(self.base_url, '/e-learning')
        response = self.get_page(elearning_url)
        if not response:
            return []
        
        soup = BeautifulSoup(response.content, 'html.parser')
        courses = []
        
        # Look for e-learning course links
        course_links = soup.find_all('a', href=True)
        for link in course_links:
            href = link.get('href')
            text = link.get_text(strip=True)
            
            # Check if this looks like an e-learning course
            if href and ('/e-learning/' in href or '/course/' in href) and len(text) > 5:
                course_url = urljoin(self.base_url, href)
                if course_url not in self.visited_urls and self.base_url in course_url:
                    print(f"Found e-learning course: {text} - {course_url}")
                    course_data = self.extract_course_from_page(course_url, "E-Learning")
                    if course_data:
                        courses.append(course_data)
        
        return courses
    
    def build_sitemap(self):
        """Build a hierarchical sitemap of all courses"""
        sitemap = {
            'url': self.base_url,
            'title': 'Creatio Academy',
            'total_courses': len(self.courses),
            'last_updated': datetime.now().isoformat(),
            'categories': {}
        }
        
        for course in self.courses:
            category = course['category']
            if category not in sitemap['categories']:
                sitemap['categories'][category] = {
                    'title': category,
                    'course_count': 0,
                    'courses': []
                }
            
            sitemap['categories'][category]['courses'].append({
                'title': course['title'],
                'url': course['url'],
                'level': course['level'],
                'duration': course['duration'],
                'format': course['format']
            })
            sitemap['categories'][category]['course_count'] += 1
        
        return sitemap
    
    def save_to_csv(self, filename='creatio_courses.csv'):
        """Save courses to CSV file"""
        if not self.courses:
            print("No courses to save to CSV")
            return
        
        keys = ['title', 'category', 'subcategory', 'url', 'description', 
                'duration', 'level', 'format', 'price', 'language', 'scraped_at']
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=keys)
            writer.writeheader()
            writer.writerows(self.courses)
        print(f"Saved {len(self.courses)} courses to {filename}")
    
    def save_to_json(self, filename='creatio_courses.json'):
        """Save courses and sitemap to JSON file"""
        sitemap = self.build_sitemap()
        
        data = {
            'scraped_at': datetime.now().isoformat(),
            'total_courses': len(self.courses),
            'academy_url': self.base_url,
            'courses': self.courses,
            'sitemap': sitemap
        }
        
        with open(filename, 'w', encoding='utf-8') as jsonfile:
            json.dump(data, jsonfile, indent=2, ensure_ascii=False)
        print(f"Saved courses and sitemap to {filename}")
    
    def extract_tutorials_and_guides(self, public_page_url):
        """Scrape public tutorials and guides pages"""
        response = self.get_page(public_page_url)
        if not response:
            return []
        
        soup = BeautifulSoup(response.content, 'html.parser')
        resources = []
        
        # Example of finding links to guides/tutorials (this would need adjustment for actual page structure):
        links = soup.find_all('a', href=True)
        for link in links:
            href = link.get('href')
            text = link.get_text(strip=True)
            if 'guide' in text.lower() or 'tutorial' in text.lower():
                resource_url = urljoin(self.base_url, href)
                resources.append({'title': text, 'url': resource_url})
        
        return resources

    def organize_resources(self, resources):
        """Organize resources by topic and difficulty"""
        organized = {}
        # Example of organizing by a fictitious difficulty structure
        for resource in resources:
            topic = "General"
            difficulty = "Beginner"
            organized.setdefault(topic, {}).setdefault(difficulty, []).append(resource)

        return organized
    
    def scrape(self):
        """Main scraping function"""
        print(f"Starting scrape of Creatio Academy")
        print("=" * 50)
        
        # Scrape training courses
        print("\nScraping Instructor-led Training courses...")
        training_courses = self.scrape_training_catalog()
        self.courses.extend(training_courses)
        print(f"Found {len(training_courses)} instructor-led training courses")
        
        # Scrape e-learning courses
        print("\nScraping E-Learning courses...")
        elearning_courses = self.scrape_elearning_catalog()
        self.courses.extend(elearning_courses)
        print(f"Found {len(elearning_courses)} e-learning courses")
        
        # Remove duplicates based on URL
        unique_courses = []
        seen_urls = set()
        for course in self.courses:
            if course['url'] not in seen_urls:
                seen_urls.add(course['url'])
                unique_courses.append(course)
        self.courses = unique_courses
        
        # Save results
        print(f"\nTotal unique courses found: {len(self.courses)}")
        self.save_to_csv()
        self.save_to_json()
        
        # Print summary
        self.print_summary()
        
        return self.courses
    
    def print_summary(self):
        """Print a summary of scraped courses"""
        print("\n" + "=" * 50)
        print("SCRAPING SUMMARY")
        print("=" * 50)
        print(f"Total courses scraped: {len(self.courses)}")
        
        # Count by category
        categories = {}
        for course in self.courses:
            cat = course['category']
            categories[cat] = categories.get(cat, 0) + 1
        
        print("\nCourses by category:")
        for cat, count in categories.items():
            print(f"  - {cat}: {count}")
        
        # Show sample courses
        if self.courses:
            print("\nSample courses:")
            for course in self.courses[:5]:
                print(f"\n  Title: {course['title']}")
                print(f"  Category: {course['category']}")
                print(f"  URL: {course['url']}")
                if course['duration']:
                    print(f"  Duration: {course['duration']}")
                if course['level']:
                    print(f"  Level: {course['level']}")

if __name__ == "__main__":
    scraper = CreatioAcademyScraper()
    courses = scraper.scrape()
