import requests
from bs4 import BeautifulSoup
import json
import csv
import time
from urllib.parse import urljoin, urlparse
import os
from datetime import datetime

class CreatioAcademyScraper:
    def __init__(self):
        self.base_url = "https://academy.creatio.com"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.courses = []
        self.categories = {}
        self.sitemap = {}
        
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
    
    def extract_categories(self, soup):
        """Extract course categories and subcategories from the main page"""
        categories = {}
        
        # Try different possible selectors for categories
        category_selectors = [
            '.course-category',
            '.category-box',
            '.learning-path',
            'div[class*="category"]',
            'section[class*="course"]',
            '.catalog-section'
        ]
        
        for selector in category_selectors:
            elements = soup.select(selector)
            if elements:
                print(f"Found {len(elements)} elements with selector: {selector}")
                break
        
        # Also try to find links that might lead to course listings
        course_links = soup.find_all('a', href=True)
        for link in course_links:
            href = link.get('href', '')
            text = link.get_text(strip=True)
            
            # Look for links that might be course categories
            if any(keyword in href.lower() or keyword in text.lower() 
                   for keyword in ['course', 'training', 'learn', 'academy', 'catalog']):
                full_url = urljoin(self.base_url, href)
                if full_url not in categories and self.base_url in full_url:
                    categories[text] = full_url
        
        return categories
    
    def extract_courses_from_page(self, url, category_name):
        """Extract individual courses from a category page"""
        response = self.get_page(url)
        if not response:
            return []
        
        soup = BeautifulSoup(response.content, 'html.parser')
        courses = []
        
        # Try different selectors for course items
        course_selectors = [
            '.course-item',
            '.course-card',
            'article.course',
            'div[class*="course-list"] > div',
            '.training-item',
            'a[href*="/courses/"]'
        ]
        
        for selector in course_selectors:
            course_elements = soup.select(selector)
            if course_elements:
                print(f"Found {len(course_elements)} courses with selector: {selector}")
                
                for element in course_elements:
                    course_data = self.extract_course_info(element, category_name)
                    if course_data:
                        courses.append(course_data)
                break
        
        return courses
    
    def extract_course_info(self, element, category):
        """Extract course information from an HTML element"""
        course = {
            'category': category,
            'subcategory': '',
            'title': '',
            'url': '',
            'description': '',
            'duration': '',
            'level': '',
            'scraped_at': datetime.now().isoformat()
        }
        
        # Extract title
        title_elem = element.find(['h2', 'h3', 'h4', 'a'])
        if title_elem:
            course['title'] = title_elem.get_text(strip=True)
        
        # Extract URL
        link = element.find('a', href=True)
        if link:
            course['url'] = urljoin(self.base_url, link['href'])
        elif element.name == 'a' and element.get('href'):
            course['url'] = urljoin(self.base_url, element['href'])
        
        # Extract description
        desc_elem = element.find(['p', 'div'], class_=lambda x: x and 'desc' in x.lower() if x else False)
        if desc_elem:
            course['description'] = desc_elem.get_text(strip=True)
        
        # Extract duration
        duration_elem = element.find(text=lambda x: x and any(word in x.lower() for word in ['hour', 'minute', 'duration']))
        if duration_elem:
            course['duration'] = duration_elem.strip()
        
        # Extract level
        level_elem = element.find(text=lambda x: x and any(word in x.lower() for word in ['beginner', 'intermediate', 'advanced', 'level']))
        if level_elem:
            course['level'] = level_elem.strip()
        
        return course if course['title'] or course['url'] else None
    
    def build_sitemap(self):
        """Build a hierarchical sitemap of all courses"""
        sitemap = {
            'url': self.base_url,
            'title': 'Creatio Academy',
            'categories': {}
        }
        
        for course in self.courses:
            category = course['category']
            if category not in sitemap['categories']:
                sitemap['categories'][category] = {
                    'title': category,
                    'courses': []
                }
            sitemap['categories'][category]['courses'].append({
                'title': course['title'],
                'url': course['url'],
                'level': course['level'],
                'duration': course['duration']
            })
        
        return sitemap
    
    def save_to_csv(self, filename='creatio_courses.csv'):
        """Save courses to CSV file"""
        if not self.courses:
            print("No courses to save")
            return
        
        keys = self.courses[0].keys()
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=keys)
            writer.writeheader()
            writer.writerows(self.courses)
        print(f"Saved {len(self.courses)} courses to {filename}")
    
    def save_to_json(self, filename='creatio_courses.json'):
        """Save courses and sitemap to JSON file"""
        data = {
            'scraped_at': datetime.now().isoformat(),
            'total_courses': len(self.courses),
            'courses': self.courses,
            'sitemap': self.build_sitemap()
        }
        
        with open(filename, 'w', encoding='utf-8') as jsonfile:
            json.dump(data, jsonfile, indent=2, ensure_ascii=False)
        print(f"Saved courses and sitemap to {filename}")
    
    def scrape(self):
        """Main scraping function"""
        print(f"Starting scrape of {self.base_url}")
        
        # Get main page
        response = self.get_page(self.base_url)
        if not response:
            print("Failed to fetch main page")
            return
        
        soup = BeautifulSoup(response.content, 'html.parser')
        print(f"Successfully fetched main page")
        
        # Look for a specific courses or catalog page
        catalog_urls = [
            '/courses',
            '/catalog',
            '/training',
            '/learn',
            '/academy'
        ]
        
        catalog_found = False
        for catalog_path in catalog_urls:
            catalog_url = urljoin(self.base_url, catalog_path)
            print(f"Checking {catalog_url}...")
            response = self.get_page(catalog_url)
            if response and response.status_code == 200:
                print(f"Found catalog at {catalog_url}")
                soup = BeautifulSoup(response.content, 'html.parser')
                catalog_found = True
                break
        
        # Extract categories
        print("Extracting categories...")
        self.categories = self.extract_categories(soup)
        print(f"Found {len(self.categories)} potential categories")
        
        # If no categories found, try to extract courses directly
        if not self.categories:
            print("No categories found, attempting to extract courses directly...")
            courses = self.extract_courses_from_page(response.url, "General")
            self.courses.extend(courses)
        else:
            # Extract courses from each category
            for category_name, category_url in list(self.categories.items())[:10]:  # Limit to first 10 for initial scrape
                print(f"\nProcessing category: {category_name}")
                courses = self.extract_courses_from_page(category_url, category_name)
                self.courses.extend(courses)
                print(f"Found {len(courses)} courses in {category_name}")
        
        # Save results
        print(f"\nTotal courses found: {len(self.courses)}")
        self.save_to_csv()
        self.save_to_json()
        
        return self.courses

if __name__ == "__main__":
    scraper = CreatioAcademyScraper()
    courses = scraper.scrape()
    
    # Print summary
    print("\n=== Scraping Summary ===")
    print(f"Total courses scraped: {len(courses)}")
    if courses:
        print("\nSample courses:")
        for course in courses[:5]:
            print(f"- {course['title']} ({course['category']})")
            if course['url']:
                print(f"  URL: {course['url']}")
