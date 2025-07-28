#!/usr/bin/env python3
"""
Enhanced resource extraction script to download supporting resources and video content
from crawled HTML files, specifically targeting e-learning content.
"""

import os
import re
import json
import requests
import hashlib
from urllib.parse import urljoin, urlparse
from pathlib import Path
from bs4 import BeautifulSoup
import time

def extract_video_urls_from_html(html_content, base_url):
    """Extract video URLs from HTML content"""
    video_urls = set()
    
    # Parse with BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Look for YouTube embeds
    youtube_patterns = [
        r'youtube\.com/embed/([a-zA-Z0-9_-]+)',
        r'youtube\.com/watch\?v=([a-zA-Z0-9_-]+)',
        r'youtu\.be/([a-zA-Z0-9_-]+)',
    ]
    
    # Look for Vimeo embeds
    vimeo_patterns = [
        r'vimeo\.com/(\d+)',
        r'player\.vimeo\.com/video/(\d+)',
    ]
    
    # Search in iframe src attributes
    for iframe in soup.find_all('iframe'):
        src = iframe.get('src', '')
        if src:
            full_url = urljoin(base_url, src)
            for pattern in youtube_patterns + vimeo_patterns:
                if re.search(pattern, full_url):
                    video_urls.add(full_url)
    
    # Search in video tag sources
    for video in soup.find_all('video'):
        src = video.get('src', '')
        if src:
            video_urls.add(urljoin(base_url, src))
        
        # Check source tags within video
        for source in video.find_all('source'):
            src = source.get('src', '')
            if src:
                video_urls.add(urljoin(base_url, src))
    
    # Search for video links in href attributes
    for link in soup.find_all('a'):
        href = link.get('href', '')
        if href:
            for pattern in youtube_patterns + vimeo_patterns:
                if re.search(pattern, href):
                    video_urls.add(href)
    
    # Search in text content for video URLs
    text_content = soup.get_text()
    for pattern in youtube_patterns + vimeo_patterns:
        matches = re.findall(pattern, text_content)
        for match in matches:
            if 'youtube' in pattern:
                video_urls.add(f'https://www.youtube.com/watch?v={match}')
            elif 'vimeo' in pattern:
                video_urls.add(f'https://vimeo.com/{match}')
    
    return list(video_urls)

def extract_course_metadata(html_content):
    """Extract course metadata from HTML"""
    soup = BeautifulSoup(html_content, 'html.parser')
    metadata = {}
    
    # Look for course titles
    title_selectors = [
        'h1', 'h2.course-title', '.course-name', '.learning-path-title', 
        'title', '[class*="course"]', '[class*="learning"]'
    ]
    
    for selector in title_selectors:
        element = soup.select_one(selector)
        if element and element.get_text(strip=True):
            metadata['title'] = element.get_text(strip=True)
            break
    
    # Look for course descriptions
    desc_selectors = [
        '.course-description', '.description', 'meta[name="description"]',
        '.course-content', '.learning-objectives'
    ]
    
    for selector in desc_selectors:
        element = soup.select_one(selector)
        if element:
            if element.name == 'meta':
                metadata['description'] = element.get('content', '')
            else:
                metadata['description'] = element.get_text(strip=True)
            break
    
    # Look for duration
    duration_patterns = [
        r'(\d+)\s*hours?', r'(\d+)\s*minutes?', r'(\d+)\s*hrs?', r'(\d+)\s*min'
    ]
    
    text_content = soup.get_text()
    for pattern in duration_patterns:
        match = re.search(pattern, text_content, re.IGNORECASE)
        if match:
            metadata['duration'] = match.group(0)
            break
    
    # Look for learning path or tech hour indicators
    if 'learning path' in text_content.lower():
        metadata['type'] = 'Learning Path'
    elif 'tech hour' in text_content.lower():
        metadata['type'] = 'Tech Hour'
    elif 'course' in text_content.lower():
        metadata['type'] = 'Course'
    
    return metadata

def download_resource(url, output_path, max_retries=3):
    """Download a resource with retry logic"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=headers, stream=True, timeout=30)
            response.raise_for_status()
            
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            # Calculate checksum
            sha256_hash = hashlib.sha256()
            with open(output_path, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(chunk)
            
            return {
                'success': True,
                'size': os.path.getsize(output_path),
                'checksum': sha256_hash.hexdigest(),
                'content_type': response.headers.get('content-type', 'unknown')
            }
            
        except Exception as e:
            print(f"Attempt {attempt + 1} failed for {url}: {e}")
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)  # Exponential backoff
            else:
                return {'success': False, 'error': str(e)}

def process_html_files():
    """Process all HTML files and extract video and resource information"""
    pages_dir = Path('pages/raw')
    resources_dir = Path('resources')
    videos_dir = resources_dir / 'videos'
    
    # Create directories
    for dir_path in [resources_dir / 'videos', resources_dir / 'images', 
                     resources_dir / 'pdfs', resources_dir / 'documents']:
        dir_path.mkdir(parents=True, exist_ok=True)
    
    video_index = {}
    resource_index = {}
    course_metadata = {}
    
    html_files = list(pages_dir.glob('*.html'))
    print(f"Processing {len(html_files)} HTML files...")
    
    for i, html_file in enumerate(html_files):
        if i % 100 == 0:
            print(f"Processing file {i+1}/{len(html_files)}: {html_file.name}")
        
        try:
            with open(html_file, 'r', encoding='utf-8', errors='ignore') as f:
                html_content = f.read()
            
            base_url = 'https://academy.creatio.com'
            
            # Extract video URLs
            video_urls = extract_video_urls_from_html(html_content, base_url)
            
            # Extract course metadata
            metadata = extract_course_metadata(html_content)
            
            if video_urls or metadata:
                file_key = html_file.stem
                
                if video_urls:
                    video_index[file_key] = {
                        'source_file': html_file.name,
                        'videos': video_urls,
                        'metadata': metadata,
                        'extracted_at': time.time()
                    }
                
                if metadata:
                    course_metadata[file_key] = metadata
            
            # Extract regular resources (existing functionality)
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Extract images, PDFs, documents
            resource_urls = set()
            
            # Images
            for img in soup.find_all('img'):
                src = img.get('src', '')
                if src:
                    resource_urls.add(('image', urljoin(base_url, src)))
            
            # PDFs and documents
            for link in soup.find_all('a'):
                href = link.get('href', '')
                if href:
                    if href.lower().endswith(('.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx')):
                        if href.lower().endswith('.pdf'):
                            resource_urls.add(('pdf', urljoin(base_url, href)))
                        else:
                            resource_urls.add(('document', urljoin(base_url, href)))
            
            # Process resources
            for resource_type, url in resource_urls:
                if url not in resource_index:
                    resource_index[url] = {
                        'type': resource_type,
                        'source_files': [html_file.name],
                        'url': url
                    }
                else:
                    resource_index[url]['source_files'].append(html_file.name)
        
        except Exception as e:
            print(f"Error processing {html_file}: {e}")
    
    # Save video index
    print(f"\nFound {len(video_index)} files with video content")
    with open('video_index.json', 'w', encoding='utf-8') as f:
        json.dump(video_index, f, indent=2, ensure_ascii=False)
    
    # Save course metadata
    print(f"Found {len(course_metadata)} files with course metadata")
    with open('course_metadata.json', 'w', encoding='utf-8') as f:
        json.dump(course_metadata, f, indent=2, ensure_ascii=False)
    
    # Download additional resources if not already downloaded
    existing_resource_index = {}
    if os.path.exists('resource_index.json'):
        with open('resource_index.json', 'r', encoding='utf-8') as f:
            existing_data = json.load(f)
            existing_resource_index = {item['url']: item for item in existing_data.get('resources', [])}
    
    new_resources = []
    for url, info in resource_index.items():
        if url not in existing_resource_index:
            new_resources.append((url, info))
    
    if new_resources:
        print(f"\nFound {len(new_resources)} new resources to download...")
        
        for url, info in new_resources:
            resource_type = info['type']
            filename = os.path.basename(urlparse(url).path)
            
            if not filename or filename == '/':
                filename = f"resource_{hashlib.md5(url.encode()).hexdigest()[:8]}"
            
            if resource_type == 'image':
                output_path = resources_dir / 'images' / filename
            elif resource_type == 'pdf':
                output_path = resources_dir / 'pdfs' / filename
            else:
                output_path = resources_dir / 'documents' / filename
            
            # Add unique suffix if file exists
            counter = 1
            original_output_path = output_path
            while output_path.exists():
                stem = original_output_path.stem
                suffix = original_output_path.suffix
                output_path = original_output_path.parent / f"{stem}_{counter}{suffix}"
                counter += 1
            
            print(f"Downloading: {filename}")
            result = download_resource(url, output_path)
            
            info.update(result)
            info['local_path'] = str(output_path)
            info['filename'] = output_path.name
    
    print(f"\nVideo extraction and enhanced resource discovery complete!")
    print(f"Video index saved to: video_index.json")
    print(f"Course metadata saved to: course_metadata.json")
    return video_index, course_metadata

if __name__ == "__main__":
    video_index, course_metadata = process_html_files()
