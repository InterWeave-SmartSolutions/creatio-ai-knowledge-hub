import os
import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time
from datetime import datetime

# Configuration
BASE_DIR = './scraped_courses'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def create_directory(path):
    """Create directory if it doesn't exist"""
    os.makedirs(path, exist_ok=True)

def sanitize_filename(filename):
    """Remove invalid characters from filename"""
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    return filename[:200]  # Limit length

def download_file(url, save_path):
    """Download a file from URL"""
    try:
        response = requests.get(url, headers=HEADERS, timeout=30)
        response.raise_for_status()
        
        with open(save_path, 'wb') as f:
            f.write(response.content)
        return True
    except Exception as e:
        print(f"Error downloading {url}: {e}")
        return False

def extract_course_details(soup, course_url):
    """Extract course details from the page"""
    details = {
        'url': course_url,
        'scraped_at': datetime.now().isoformat(),
        'description': '',
        'prerequisites': [],
        'objectives': [],
        'materials': [],
        'videos': [],
        'slides': [],
        'additional_info': {}
    }
    
    # Try to find description
    # Method 1: Meta description
    meta_desc = soup.find('meta', attrs={'name': 'description'})
    if meta_desc and meta_desc.get('content'):
        details['description'] = meta_desc['content']
    
    # Method 2: Look for description in various containers
    if not details['description']:
        for selector in ['.course-description', '.description', '.overview', '#course-overview']:
            desc_elem = soup.select_one(selector)
            if desc_elem:
                details['description'] = desc_elem.get_text(strip=True)
                break
    
    # Extract course title
    title_elem = soup.find('h1') or soup.find('h2', class_='course-title')
    if title_elem:
        details['additional_info']['title'] = title_elem.get_text(strip=True)
    
    # Look for prerequisites
    prereq_keywords = ['Prerequisites', 'Pre-requisites', 'Required Knowledge']
    for keyword in prereq_keywords:
        elem = soup.find(text=lambda text: text and keyword in text)
        if elem:
            parent = elem.parent
            # Look for list items
            ul = parent.find_next('ul')
            if ul:
                details['prerequisites'] = [li.get_text(strip=True) for li in ul.find_all('li')]
            else:
                # Try next sibling
                next_elem = parent.find_next_sibling()
                if next_elem and next_elem.name == 'ul':
                    details['prerequisites'] = [li.get_text(strip=True) for li in next_elem.find_all('li')]
    
    # Look for learning objectives
    objective_keywords = ['Learning Objectives', 'Course Objectives', 'What you will learn']
    for keyword in objective_keywords:
        elem = soup.find(text=lambda text: text and keyword in text)
        if elem:
            parent = elem.parent
            ul = parent.find_next('ul')
            if ul:
                details['objectives'] = [li.get_text(strip=True) for li in ul.find_all('li')]
            else:
                next_elem = parent.find_next_sibling()
                if next_elem and next_elem.name == 'ul':
                    details['objectives'] = [li.get_text(strip=True) for li in next_elem.find_all('li')]
    
    # Extract PDF links
    pdf_links = []
    for link in soup.find_all('a', href=True):
        href = link['href']
        if href.lower().endswith('.pdf'):
            full_url = urljoin(course_url, href)
            pdf_links.append({
                'url': full_url,
                'text': link.get_text(strip=True) or 'PDF Document',
                'filename': os.path.basename(urlparse(full_url).path) or 'document.pdf'
            })
    details['materials'] = pdf_links
    
    # Extract video URLs (YouTube, Vimeo, etc.)
    video_urls = []
    
    # Look for iframe embeds
    for iframe in soup.find_all('iframe'):
        src = iframe.get('src', '')
        if any(domain in src for domain in ['youtube.com', 'vimeo.com', 'wistia.com']):
            video_urls.append({
                'url': src,
                'type': 'embedded',
                'title': iframe.get('title', 'Video')
            })
    
    # Look for video links
    for link in soup.find_all('a', href=True):
        href = link['href']
        if any(domain in href for domain in ['youtube.com', 'youtu.be', 'vimeo.com']):
            video_urls.append({
                'url': href,
                'type': 'link',
                'title': link.get_text(strip=True) or 'Video Link'
            })
    
    details['videos'] = video_urls
    
    # Look for slide presentations
    slide_keywords = ['.ppt', '.pptx', 'slides', 'presentation']
    for link in soup.find_all('a', href=True):
        href = link['href'].lower()
        text = link.get_text(strip=True).lower()
        if any(keyword in href or keyword in text for keyword in slide_keywords):
            full_url = urljoin(course_url, link['href'])
            details['slides'].append({
                'url': full_url,
                'text': link.get_text(strip=True),
                'filename': os.path.basename(urlparse(full_url).path)
            })
    
    # Extract additional course information
    info_selectors = {
        'duration': ['.duration', '.course-duration', 'span:contains("Duration")'],
        'level': ['.level', '.difficulty', 'span:contains("Level")'],
        'instructor': ['.instructor', '.teacher', 'span:contains("Instructor")'],
        'language': ['.language', 'span:contains("Language")']
    }
    
    for info_type, selectors in info_selectors.items():
        for selector in selectors:
            try:
                elem = soup.select_one(selector)
                if elem:
                    details['additional_info'][info_type] = elem.get_text(strip=True)
                    break
            except:
                continue
    
    return details

def scrape_course(course_url, course_title, save_dir):
    """Scrape a single course"""
    print(f"\nScraping: {course_title}")
    print(f"URL: {course_url}")
    
    try:
        response = requests.get(course_url, headers=HEADERS, timeout=30)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract course details
        details = extract_course_details(soup, course_url)
        details['course_title'] = course_title
        
        # Save course details as JSON
        json_path = os.path.join(save_dir, 'course_details.json')
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(details, f, indent=2, ensure_ascii=False)
        
        # Create subdirectories for materials
        materials_dir = os.path.join(save_dir, 'materials')
        slides_dir = os.path.join(save_dir, 'slides')
        create_directory(materials_dir)
        create_directory(slides_dir)
        
        # Download PDFs
        print(f"Found {len(details['materials'])} PDF files")
        for i, pdf in enumerate(details['materials']):
            filename = sanitize_filename(pdf['filename'])
            save_path = os.path.join(materials_dir, filename)
            print(f"  Downloading PDF {i+1}/{len(details['materials'])}: {filename}")
            if download_file(pdf['url'], save_path):
                pdf['downloaded'] = True
                pdf['local_path'] = save_path
        
        # Download slides
        print(f"Found {len(details['slides'])} slide presentations")
        for i, slide in enumerate(details['slides']):
            filename = sanitize_filename(slide['filename'])
            save_path = os.path.join(slides_dir, filename)
            print(f"  Downloading slides {i+1}/{len(details['slides'])}: {filename}")
            if download_file(slide['url'], save_path):
                slide['downloaded'] = True
                slide['local_path'] = save_path
        
        # Save video URLs separately
        if details['videos']:
            video_path = os.path.join(save_dir, 'video_urls.txt')
            with open(video_path, 'w', encoding='utf-8') as f:
                f.write(f"Video URLs for {course_title}\n")
                f.write("=" * 50 + "\n\n")
                for i, video in enumerate(details['videos'], 1):
                    f.write(f"{i}. {video['title']}\n")
                    f.write(f"   URL: {video['url']}\n")
                    f.write(f"   Type: {video['type']}\n\n")
        
        # Update JSON with download status
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(details, f, indent=2, ensure_ascii=False)
        
        return True
        
    except Exception as e:
        print(f"Error scraping course: {e}")
        error_log = os.path.join(save_dir, 'error.log')
        with open(error_log, 'w') as f:
            f.write(f"Error scraping {course_url}: {str(e)}\n")
        return False

def main():
    """Main function to process courses"""
    # Load course data from JSON
    with open('creatio_courses.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    courses = data['courses'][:50]  # Limit to first 50 courses
    
    # Create base directory
    create_directory(BASE_DIR)
    
    # Create summary log
    summary_path = os.path.join(BASE_DIR, 'scraping_summary.json')
    summary = {
        'start_time': datetime.now().isoformat(),
        'total_courses': len(courses),
        'successful': 0,
        'failed': 0,
        'courses_processed': []
    }
    
    # Process each course
    for i, course in enumerate(courses, 1):
        print(f"\n{'='*60}")
        print(f"Processing course {i}/{len(courses)}")
        
        course_title = course['title']
        course_url = course['url']
        
        # Create directory for this course
        course_dir_name = sanitize_filename(f"{i:03d}_{course_title}")
        course_dir = os.path.join(BASE_DIR, course_dir_name)
        create_directory(course_dir)
        
        # Scrape the course
        success = scrape_course(course_url, course_title, course_dir)
        
        # Update summary
        if success:
            summary['successful'] += 1
        else:
            summary['failed'] += 1
        
        summary['courses_processed'].append({
            'index': i,
            'title': course_title,
            'url': course_url,
            'directory': course_dir_name,
            'success': success,
            'timestamp': datetime.now().isoformat()
        })
        
        # Save summary after each course
        summary['last_updated'] = datetime.now().isoformat()
        with open(summary_path, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        
        # Small delay to be respectful
        time.sleep(2)
    
    # Final summary
    summary['end_time'] = datetime.now().isoformat()
    with open(summary_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    
    print(f"\n{'='*60}")
    print(f"Scraping completed!")
    print(f"Total courses: {summary['total_courses']}")
    print(f"Successful: {summary['successful']}")
    print(f"Failed: {summary['failed']}")
    print(f"Results saved in: {BASE_DIR}")

if __name__ == "__main__":
    main()
