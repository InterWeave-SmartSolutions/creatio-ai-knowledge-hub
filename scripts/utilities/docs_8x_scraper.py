#!/usr/bin/env python3
"""
Script to discover and download all pages under https://academy.creatio.com/docs/8.x/
following the original criteria.
"""

import requests
import os
import sys
import time
import hashlib
import json
from pathlib import Path
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Configuration
BASE_URL = "https://academy.creatio.com/docs/8.x/"
OUTPUT_DIR = "creatio-academy-archive/pages/raw"
METADATA_DIR = "creatio-academy-archive/pages/metadata"
DISCOVERED_URLS_FILE = "discovered_8x_urls.json"
DELAY_BETWEEN_REQUESTS = 1  # seconds
MAX_RETRIES = 3

# Ensure directories exist
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(METADATA_DIR, exist_ok=True)

# User Agent to appear as a regular browser
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1'
}

def get_file_hash(url):
    """Generate a hash for the URL to use as filename"""
    return hashlib.md5(url.encode()).hexdigest()

def is_valid_docs_8x_url(url):
    """Check if URL is within the docs/8.x section"""
    return url.startswith("https://academy.creatio.com/docs/8.x/")

def get_existing_files():
    """Get list of already downloaded files"""
    existing_files = {}
    if os.path.exists(OUTPUT_DIR):
        for file in os.listdir(OUTPUT_DIR):
            if file.endswith('.html'):
                file_path = os.path.join(OUTPUT_DIR, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        # Try to extract original URL from content
                        soup = BeautifulSoup(content, 'html.parser')
                        canonical = soup.find('link', rel='canonical')
                        if canonical and canonical.get('href'):
                            existing_files[canonical['href']] = file
                        else:
                            # Check for base URL in content
                            if 'academy.creatio.com/docs/8.x' in content:
                                existing_files[file.replace('.html', '')] = file
                except Exception as e:
                    logger.warning(f"Could not read existing file {file}: {e}")
    return existing_files

def discover_urls_from_page(url, visited_urls=set()):
    """Discover URLs from a single page"""
    if url in visited_urls:
        return set()
    
    visited_urls.add(url)
    discovered = set()
    
    try:
        logger.info(f"Discovering URLs from: {url}")
        response = requests.get(url, headers=HEADERS, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find all links on the page
        links = soup.find_all('a', href=True)
        
        for link in links:
            href = link['href']
            
            # Convert relative URLs to absolute
            absolute_url = urljoin(url, href)
            
            # Check if it's a valid docs/8.x URL
            if is_valid_docs_8x_url(absolute_url):
                # Remove anchor fragments
                clean_url = absolute_url.split('#')[0]
                discovered.add(clean_url)
                logger.debug(f"Discovered: {clean_url}")
        
        # Also look for navigation menus, sitemaps, etc.
        nav_elements = soup.find_all(['nav', 'ul', 'ol'], class_=lambda x: x and any(
            term in x.lower() for term in ['menu', 'nav', 'toc', 'sidebar', 'index']
        ))
        
        for nav in nav_elements:
            nav_links = nav.find_all('a', href=True)
            for link in nav_links:
                href = link['href']
                absolute_url = urljoin(url, href)
                if is_valid_docs_8x_url(absolute_url):
                    clean_url = absolute_url.split('#')[0]
                    discovered.add(clean_url)
        
        time.sleep(DELAY_BETWEEN_REQUESTS)
        
    except Exception as e:
        logger.error(f"Error discovering URLs from {url}: {e}")
    
    return discovered

def discover_all_urls():
    """Discover all URLs under docs/8.x/"""
    logger.info("Starting URL discovery process...")
    
    all_urls = set()
    visited_urls = set()
    urls_to_visit = {BASE_URL}
    
    # Also check common starting points
    common_starting_points = [
        "https://academy.creatio.com/docs/8.x/",
        "https://academy.creatio.com/docs/8.x/no-code/",
        "https://academy.creatio.com/docs/8.x/dev/",
        "https://academy.creatio.com/docs/8.x/setup/",
        "https://academy.creatio.com/docs/8.x/setup-and-administration/",
        "https://academy.creatio.com/docs/8.x/mobile/",
        "https://academy.creatio.com/docs/8.x/release-notes/",
    ]
    
    urls_to_visit.update(common_starting_points)
    
    while urls_to_visit:
        current_url = urls_to_visit.pop()
        
        if current_url in visited_urls:
            continue
            
        new_urls = discover_urls_from_page(current_url, visited_urls)
        all_urls.update(new_urls)
        
        # Add newly discovered URLs to visit queue
        for new_url in new_urls:
            if new_url not in visited_urls:
                urls_to_visit.add(new_url)
        
        logger.info(f"Discovered {len(new_urls)} new URLs from {current_url}")
        logger.info(f"Total URLs discovered: {len(all_urls)}")
        logger.info(f"URLs remaining to visit: {len(urls_to_visit)}")
        
        # Limit discovery to prevent infinite loops
        if len(all_urls) > 1000:
            logger.warning("Discovered over 1000 URLs, stopping discovery")
            break
    
    return all_urls

def download_page(url, existing_files):
    """Download a single page"""
    if url in existing_files:
        logger.info(f"Already downloaded: {url}")
        return True
    
    file_hash = get_file_hash(url)
    output_file = os.path.join(OUTPUT_DIR, f"{file_hash}.html")
    metadata_file = os.path.join(METADATA_DIR, f"{file_hash}.json")
    
    if os.path.exists(output_file):
        logger.info(f"File already exists: {output_file}")
        return True
    
    for attempt in range(MAX_RETRIES):
        try:
            logger.info(f"Downloading: {url} (attempt {attempt + 1})")
            
            response = requests.get(url, headers=HEADERS, timeout=30)
            response.raise_for_status()
            
            # Save HTML content
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(response.text)
            
            # Save metadata
            metadata = {
                'url': url,
                'timestamp': time.time(),
                'status_code': response.status_code,
                'content_type': response.headers.get('content-type', ''),
                'file_hash': file_hash,
                'file_path': output_file
            }
            
            with open(metadata_file, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2)
            
            logger.info(f"Successfully downloaded: {url}")
            time.sleep(DELAY_BETWEEN_REQUESTS)
            return True
            
        except Exception as e:
            logger.error(f"Error downloading {url} (attempt {attempt + 1}): {e}")
            if attempt < MAX_RETRIES - 1:
                time.sleep(2 ** attempt)  # Exponential backoff
            
    return False

def save_discovered_urls(urls):
    """Save discovered URLs to file"""
    with open(DISCOVERED_URLS_FILE, 'w', encoding='utf-8') as f:
        json.dump({
            'urls': list(urls),
            'count': len(urls),
            'timestamp': time.time()
        }, f, indent=2)
    
    logger.info(f"Saved {len(urls)} URLs to {DISCOVERED_URLS_FILE}")

def load_discovered_urls():
    """Load previously discovered URLs"""
    if os.path.exists(DISCOVERED_URLS_FILE):
        try:
            with open(DISCOVERED_URLS_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return set(data.get('urls', []))
        except Exception as e:
            logger.warning(f"Could not load discovered URLs: {e}")
    return set()

def main():
    """Main execution function"""
    logger.info("Starting Creatio Academy docs/8.x scraper...")
    
    # Check if we should rediscover URLs or use existing list
    if len(sys.argv) > 1 and sys.argv[1] == '--rediscover':
        logger.info("Rediscovering URLs...")
        all_urls = discover_all_urls()
        save_discovered_urls(all_urls)
    else:
        logger.info("Loading previously discovered URLs...")
        all_urls = load_discovered_urls()
        if not all_urls:
            logger.info("No previously discovered URLs found, starting discovery...")
            all_urls = discover_all_urls()
            save_discovered_urls(all_urls)
    
    logger.info(f"Total URLs to process: {len(all_urls)}")
    
    # Get existing files
    existing_files = get_existing_files()
    logger.info(f"Found {len(existing_files)} existing files")
    
    # Download missing pages
    successful_downloads = 0
    failed_downloads = 0
    
    for url in sorted(all_urls):
        if download_page(url, existing_files):
            successful_downloads += 1
        else:
            failed_downloads += 1
    
    logger.info(f"Download complete!")
    logger.info(f"Successful: {successful_downloads}")
    logger.info(f"Failed: {failed_downloads}")
    logger.info(f"Total processed: {len(all_urls)}")

if __name__ == "__main__":
    main()
