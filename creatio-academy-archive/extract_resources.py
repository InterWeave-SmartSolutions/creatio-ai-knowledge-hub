#!/usr/bin/env python3
"""
Resource extraction and download script for Creatio Academy Archive
Extracts and downloads PDFs, images, and documents from crawled HTML files.
"""

import os
import re
import json
import hashlib
import urllib.request
import urllib.parse
from pathlib import Path
from bs4 import BeautifulSoup
from collections import defaultdict
import time
import mimetypes

# Configuration
PAGES_DIR = "pages/raw"
RESOURCES_DIR = "resources"
RESOURCE_INDEX_FILE = "resource_index.json"
DOWNLOAD_DELAY = 0.5  # Seconds between downloads to be respectful

# Resource type mappings
RESOURCE_EXTENSIONS = {
    'pdfs': ['.pdf'],
    'images': ['.jpg', '.jpeg', '.png', '.gif', '.svg', '.webp', '.bmp', '.ico'],
    'documents': ['.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.txt', '.rtf', '.odt', '.ods', '.odp']
}

def get_resource_type(url):
    """Determine resource type based on URL extension."""
    parsed_url = urllib.parse.urlparse(url.lower())
    path = parsed_url.path
    ext = Path(path).suffix.lower()
    
    for resource_type, extensions in RESOURCE_EXTENSIONS.items():
        if ext in extensions:
            return resource_type
    return None

def extract_resources_from_html(html_file, source_url=None):
    """Extract all resource URLs from an HTML file."""
    resources = []
    
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        soup = BeautifulSoup(content, 'html.parser')
        
        # Extract from img tags
        for img in soup.find_all('img'):
            src = img.get('src')
            if src:
                resources.append({
                    'url': src,
                    'tag': 'img',
                    'attributes': dict(img.attrs)
                })
        
        # Extract from links (href)
        for link in soup.find_all('a'):
            href = link.get('href')
            if href and get_resource_type(href):
                resources.append({
                    'url': href,
                    'tag': 'a',
                    'attributes': dict(link.attrs)
                })
        
        # Extract from link tags (stylesheets, etc.)
        for link in soup.find_all('link'):
            href = link.get('href')
            if href and get_resource_type(href):
                resources.append({
                    'url': href,
                    'tag': 'link',
                    'attributes': dict(link.attrs)
                })
        
        # Extract from script tags
        for script in soup.find_all('script'):
            src = script.get('src')
            if src and get_resource_type(src):
                resources.append({
                    'url': src,
                    'tag': 'script',
                    'attributes': dict(script.attrs)
                })
        
        # Extract from preload links
        for link in soup.find_all('link', rel='preload'):
            href = link.get('href')
            if href and get_resource_type(href):
                resources.append({
                    'url': href,
                    'tag': 'link',
                    'attributes': dict(link.attrs)
                })
                
        # Use regex to find any remaining resource URLs in the content
        url_pattern = r'https://academy\.creatio\.com/[^\s"\'<>]*\.(?:pdf|jpg|jpeg|png|gif|svg|doc|docx|xls|xlsx|ppt|pptx)'
        regex_matches = re.findall(url_pattern, content, re.IGNORECASE)
        
        for url in regex_matches:
            resources.append({
                'url': url,
                'tag': 'regex',
                'attributes': {}
            })
            
    except Exception as e:
        print(f"Error processing {html_file}: {e}")
        
    return resources

def normalize_url(url, base_url="https://academy.creatio.com"):
    """Normalize URLs to absolute format."""
    if url.startswith('//'):
        url = 'https:' + url
    elif url.startswith('/'):
        url = base_url + url
    elif not url.startswith('http'):
        url = base_url + '/' + url
    return url

def generate_unique_filename(original_url, existing_files):
    """Generate unique filename with hash to prevent conflicts."""
    parsed_url = urllib.parse.urlparse(original_url)
    path = parsed_url.path
    filename = Path(path).name
    
    if not filename or '.' not in filename:
        # Extract filename from URL hash or use default
        url_hash = hashlib.md5(original_url.encode()).hexdigest()[:8]
        ext = '.bin'  # Default extension
        filename = f"resource_{url_hash}{ext}"
    
    # Add unique identifier if file already exists
    base_name = Path(filename).stem
    extension = Path(filename).suffix
    counter = 1
    
    while filename in existing_files:
        filename = f"{base_name}_{counter}{extension}"
        counter += 1
    
    existing_files.add(filename)
    return filename

def download_resource(url, filepath, timeout=30, retries=3):
    """Download a resource with error handling and retries."""
    for attempt in range(retries):
        try:
            # Create request with headers
            req = urllib.request.Request(url)
            req.add_header('User-Agent', 'Mozilla/5.0 (compatible; CreatioArchiveBot/1.0)')
            
            with urllib.request.urlopen(req, timeout=timeout) as response:
                content = response.read()
                
                # Write to file
                with open(filepath, 'wb') as f:
                    f.write(content)
                
                # Calculate checksum
                checksum = hashlib.sha256(content).hexdigest()
                
                return {
                    'success': True,
                    'size': len(content),
                    'checksum': checksum,
                    'content_type': response.headers.get('Content-Type', 'unknown')
                }
                
        except Exception as e:
            print(f"Attempt {attempt + 1} failed for {url}: {e}")
            if attempt == retries - 1:
                return {
                    'success': False,
                    'error': str(e)
                }
            time.sleep(1)  # Wait before retry

def main():
    """Main execution function."""
    print("Starting resource extraction and download...")
    
    # Initialize data structures
    resource_index = {
        'extraction_timestamp': time.time(),
        'total_resources': 0,
        'successful_downloads': 0,
        'failed_downloads': 0,
        'resources_by_type': defaultdict(list),
        'resources_by_page': defaultdict(list),
        'failed_resources': []
    }
    
    existing_files = {
        'pdfs': set(),
        'images': set(),
        'documents': set()
    }
    
    # Create resource directories
    for resource_type in RESOURCE_EXTENSIONS.keys():
        os.makedirs(os.path.join(RESOURCES_DIR, resource_type), exist_ok=True)
    
    # Process all HTML files
    html_files = list(Path(PAGES_DIR).glob('*.html'))
    print(f"Found {len(html_files)} HTML files to process")
    
    all_resources = {}  # URL -> resource info
    
    # Extract resources from all HTML files
    print("Extracting resources from HTML files...")
    for html_file in html_files:
        print(f"Processing: {html_file.name}")
        resources = extract_resources_from_html(html_file)
        
        for resource in resources:
            url = normalize_url(resource['url'])
            resource_type = get_resource_type(url)
            
            if resource_type:
                if url not in all_resources:
                    all_resources[url] = {
                        'url': url,
                        'type': resource_type,
                        'source_pages': [],
                        'extraction_info': []
                    }
                
                all_resources[url]['source_pages'].append(str(html_file))
                all_resources[url]['extraction_info'].append(resource)
    
    print(f"Found {len(all_resources)} unique resources")
    
    # Download resources
    print("Starting downloads...")
    for i, (url, resource_info) in enumerate(all_resources.items(), 1):
        resource_type = resource_info['type']
        print(f"[{i}/{len(all_resources)}] Downloading {resource_type}: {url}")
        
        # Generate unique filename
        filename = generate_unique_filename(url, existing_files[resource_type])
        filepath = os.path.join(RESOURCES_DIR, resource_type, filename)
        
        # Download resource
        download_result = download_resource(url, filepath)
        
        # Update resource info
        resource_info['filename'] = filename
        resource_info['filepath'] = filepath
        resource_info['download_result'] = download_result
        
        # Update index
        resource_index['total_resources'] += 1
        if download_result['success']:
            resource_index['successful_downloads'] += 1
        else:
            resource_index['failed_downloads'] += 1
            resource_index['failed_resources'].append({
                'url': url,
                'error': download_result.get('error', 'Unknown error'),
                'type': resource_type
            })
        
        resource_index['resources_by_type'][resource_type].append(resource_info)
        for page in resource_info['source_pages']:
            resource_index['resources_by_page'][page].append({
                'url': url,
                'filename': filename,
                'type': resource_type
            })
        
        # Be respectful with delays
        time.sleep(DOWNLOAD_DELAY)
    
    # Save resource index
    print(f"Saving resource index to {RESOURCE_INDEX_FILE}")
    with open(RESOURCE_INDEX_FILE, 'w', encoding='utf-8') as f:
        json.dump(resource_index, f, indent=2, default=str)
    
    # Print summary
    print("\n" + "="*60)
    print("DOWNLOAD SUMMARY")
    print("="*60)
    print(f"Total resources found: {resource_index['total_resources']}")
    print(f"Successful downloads: {resource_index['successful_downloads']}")
    print(f"Failed downloads: {resource_index['failed_downloads']}")
    print(f"Success rate: {resource_index['successful_downloads']/resource_index['total_resources']*100:.1f}%")
    
    print("\nResources by type:")
    for resource_type, resources in resource_index['resources_by_type'].items():
        successful = sum(1 for r in resources if r['download_result']['success'])
        print(f"  {resource_type}: {successful}/{len(resources)}")
    
    if resource_index['failed_resources']:
        print(f"\nFirst 10 failed downloads:")
        for failed in resource_index['failed_resources'][:10]:
            print(f"  {failed['type']}: {failed['url']} ({failed['error']})")
    
    print(f"\nResource index saved to: {RESOURCE_INDEX_FILE}")
    print("Download complete!")

if __name__ == "__main__":
    main()
