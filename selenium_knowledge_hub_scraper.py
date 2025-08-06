#!/usr/bin/env python3
"""
Selenium-based Creatio Knowledge Hub Scraper
Handles authentication, cross-domain login, and security measures
"""

import os
import sys
import time
import json
import sqlite3
import hashlib
import logging
from datetime import datetime
from pathlib import Path
from urllib.parse import urljoin, urlparse
from typing import Dict, List, Optional, Set

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager

import requests
from bs4 import BeautifulSoup
import html2text

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('knowledge_hub_scraper.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class CreatioKnowledgeHubScraper:
    def __init__(self, headless: bool = False, wait_timeout: int = 30):
        """Initialize the scraper with Selenium WebDriver"""
        self.base_url = "https://knowledge-hub.creatio.com"
        self.solutions_url = f"{self.base_url}/solutions"
        self.login_url = f"{self.base_url}/solutions/user/login"
        self.headless = headless
        self.wait_timeout = wait_timeout
        
        # Setup directories
        self.base_dir = Path("ai_knowledge_hub/solutions_hub")
        self.base_dir.mkdir(parents=True, exist_ok=True)
        
        # Database setup
        self.db_path = self.base_dir / "knowledge_hub.db"
        self.init_database()
        
        # HTML to markdown converter
        self.html_converter = html2text.HTML2Text()
        self.html_converter.ignore_links = False
        self.html_converter.ignore_images = False
        
        # Initialize webdriver
        self.driver = None
        self.session = requests.Session()
        
        # Scraped URLs tracker
        self.scraped_urls: Set[str] = set()
        
    def init_database(self):
        """Initialize SQLite database for storing scraped content"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS pages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    url TEXT UNIQUE NOT NULL,
                    title TEXT,
                    content_text TEXT,
                    content_markdown TEXT,
                    content_html TEXT,
                    scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    metadata TEXT
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS media (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    page_id INTEGER,
                    url TEXT NOT NULL,
                    local_path TEXT,
                    media_type TEXT,
                    file_size INTEGER,
                    scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (page_id) REFERENCES pages (id)
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS links (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    source_page_id INTEGER,
                    target_url TEXT NOT NULL,
                    link_text TEXT,
                    discovered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    processed BOOLEAN DEFAULT FALSE,
                    FOREIGN KEY (source_page_id) REFERENCES pages (id)
                )
            """)
    
    def setup_driver(self):
        """Setup Chrome WebDriver with appropriate options"""
        try:
            chrome_options = Options()
            
            if self.headless:
                chrome_options.add_argument("--headless")
            
            # Security and performance options
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1920,1080")
            
            # User agent to appear more like a real browser
            chrome_options.add_argument("--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
            
            # Additional options to bypass detection
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            # Setup webdriver
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            
            # Execute script to remove webdriver property
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            logger.info("Chrome WebDriver initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to setup WebDriver: {e}")
            return False
    
    def login(self, username: str, password: str) -> bool:
        """Login to the Knowledge Hub using Selenium"""
        try:
            logger.info("Attempting to login to Knowledge Hub...")
            
            # Navigate to login page
            self.driver.get(self.login_url)
            time.sleep(3)
            
            # Wait for page to load and check if we're redirected
            current_url = self.driver.current_url
            logger.info(f"Current URL after login page load: {current_url}")
            
            # Handle potential redirects to profile.creatio.com
            if "profile.creatio.com" in current_url:
                logger.info("Redirected to profile.creatio.com for authentication")
            
            # Wait for login form elements
            wait = WebDriverWait(self.driver, self.wait_timeout)
            
            # Try different possible selectors for username field
            username_selectors = [
                "input[name='mail']",
                "input[name='email']", 
                "input[name='username']",
                "input[type='email']",
                "#edit-mail",
                "#edit-name"
            ]
            
            username_field = None
            for selector in username_selectors:
                try:
                    username_field = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
                    logger.info(f"Found username field with selector: {selector}")
                    break
                except TimeoutException:
                    continue
            
            if not username_field:
                logger.error("Could not find username field")
                return False
            
            # Try different possible selectors for password field
            password_selectors = [
                "input[name='pass']",
                "input[name='password']",
                "input[type='password']",
                "#edit-pass"
            ]
            
            password_field = None
            for selector in password_selectors:
                try:
                    password_field = self.driver.find_element(By.CSS_SELECTOR, selector)
                    logger.info(f"Found password field with selector: {selector}")
                    break
                except NoSuchElementException:
                    continue
            
            if not password_field:
                logger.error("Could not find password field")
                return False
            
            # Fill in credentials
            username_field.clear()
            username_field.send_keys(username)
            time.sleep(1)
            
            password_field.clear()
            password_field.send_keys(password)
            time.sleep(1)
            
            # Find and click submit button
            submit_selectors = [
                "input[type='submit']",
                "button[type='submit']",
                "input[value='Log in']",
                "button:contains('Log in')",
                "#edit-submit"
            ]
            
            submit_button = None
            for selector in submit_selectors:
                try:
                    submit_button = self.driver.find_element(By.CSS_SELECTOR, selector)
                    logger.info(f"Found submit button with selector: {selector}")
                    break
                except NoSuchElementException:
                    continue
            
            if not submit_button:
                logger.error("Could not find submit button")
                return False
            
            # Submit the form
            logger.info("Submitting login form...")
            submit_button.click()
            
            # Wait for login to complete
            time.sleep(5)
            
            # Check if login was successful
            current_url = self.driver.current_url
            logger.info(f"URL after login attempt: {current_url}")
            
            # Check for error messages
            error_selectors = [
                ".messages.error",
                ".alert-danger",
                ".error-message",
                "#messages"
            ]
            
            for selector in error_selectors:
                try:
                    error_element = self.driver.find_element(By.CSS_SELECTOR, selector)
                    if error_element.is_displayed():
                        logger.error(f"Login error: {error_element.text}")
                        return False
                except NoSuchElementException:
                    continue
            
            # Try to navigate to solutions page to verify login
            self.driver.get(self.solutions_url)
            time.sleep(3)
            
            # Check if we can access protected content
            page_source = self.driver.page_source
            if "403 Forbidden" in page_source or "Access denied" in page_source:
                logger.error("Login failed - still getting access denied")
                return False
            
            # Check for login indicators
            if "login" not in self.driver.current_url.lower() and "user" in page_source.lower():
                logger.info("Login appears successful!")
                return True
            
            logger.warning("Login status unclear, proceeding with caution")
            return True
            
        except Exception as e:
            logger.error(f"Login failed with exception: {e}")
            return False
    
    def extract_cookies_for_requests(self):
        """Extract cookies from Selenium session for use with requests"""
        try:
            selenium_cookies = self.driver.get_cookies()
            for cookie in selenium_cookies:
                self.session.cookies.set(
                    cookie['name'], 
                    cookie['value'],
                    domain=cookie.get('domain', ''),
                    path=cookie.get('path', '/')
                )
            logger.info(f"Extracted {len(selenium_cookies)} cookies from Selenium session")
        except Exception as e:
            logger.error(f"Failed to extract cookies: {e}")
    
    def scrape_page(self, url: str) -> Optional[Dict]:
        """Scrape a single page using Selenium"""
        if url in self.scraped_urls:
            logger.info(f"Already scraped: {url}")
            return None
        
        try:
            logger.info(f"Scraping page: {url}")
            
            # Navigate to page
            self.driver.get(url)
            time.sleep(3)
            
            # Check for access denied
            page_source = self.driver.page_source
            if "403 Forbidden" in page_source or "Access denied" in page_source:
                logger.error(f"Access denied for: {url}")
                return None
            
            # Extract page information
            try:
                title = self.driver.title
            except:
                title = "No title"
            
            # Get page content
            soup = BeautifulSoup(page_source, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Extract main content
            content_selectors = [
                ".main-content",
                "#main-content", 
                ".content",
                "#content",
                "main",
                "article",
                ".page-content"
            ]
            
            main_content = None
            for selector in content_selectors:
                main_content = soup.select_one(selector)
                if main_content:
                    break
            
            if not main_content:
                main_content = soup.find('body')
            
            if not main_content:
                logger.warning(f"Could not find main content for: {url}")
                return None
            
            # Convert to text and markdown
            html_content = str(main_content)
            text_content = main_content.get_text(strip=True, separator='\n')
            markdown_content = self.html_converter.handle(html_content)
            
            # Extract links
            links = []
            for link in main_content.find_all('a', href=True):
                href = link['href']
                if href.startswith('/'):
                    href = urljoin(self.base_url, href)
                elif not href.startswith('http'):
                    href = urljoin(url, href)
                
                links.append({
                    'url': href,
                    'text': link.get_text(strip=True)
                })
            
            # Extract images and media
            media = []
            for img in main_content.find_all('img', src=True):
                src = img['src']
                if src.startswith('/'):
                    src = urljoin(self.base_url, src)
                elif not src.startswith('http'):
                    src = urljoin(url, src)
                
                media.append({
                    'url': src,
                    'type': 'image',
                    'alt': img.get('alt', '')
                })
            
            # Save to database
            page_data = {
                'url': url,
                'title': title,
                'content_text': text_content,
                'content_markdown': markdown_content,
                'content_html': html_content,
                'links': links,
                'media': media,
                'scraped_at': datetime.now().isoformat()
            }
            
            self.save_page_data(page_data)
            self.scraped_urls.add(url)
            
            logger.info(f"Successfully scraped: {url}")
            return page_data
            
        except Exception as e:
            logger.error(f"Failed to scrape page {url}: {e}")
            return None
    
    def save_page_data(self, page_data: Dict):
        """Save page data to database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Insert page data
                cursor.execute("""
                    INSERT OR REPLACE INTO pages 
                    (url, title, content_text, content_markdown, content_html, metadata)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    page_data['url'],
                    page_data['title'],
                    page_data['content_text'],
                    page_data['content_markdown'],
                    page_data['content_html'],
                    json.dumps({
                        'scraped_at': page_data['scraped_at'],
                        'links_count': len(page_data['links']),
                        'media_count': len(page_data['media'])
                    })
                ))
                
                page_id = cursor.lastrowid
                
                # Insert links
                for link in page_data['links']:
                    cursor.execute("""
                        INSERT OR IGNORE INTO links 
                        (source_page_id, target_url, link_text)
                        VALUES (?, ?, ?)
                    """, (page_id, link['url'], link['text']))
                
                # Insert media
                for media_item in page_data['media']:
                    cursor.execute("""
                        INSERT OR IGNORE INTO media
                        (page_id, url, media_type)
                        VALUES (?, ?, ?)
                    """, (page_id, media_item['url'], media_item['type']))
                
                conn.commit()
                logger.info(f"Saved page data for: {page_data['url']}")
                
        except Exception as e:
            logger.error(f"Failed to save page data: {e}")
    
    def discover_solution_links(self) -> List[str]:
        """Discover solution links from the main solutions page"""
        try:
            logger.info("Discovering solution links...")
            
            self.driver.get(self.solutions_url)
            time.sleep(5)
            
            page_source = self.driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')
            
            solution_links = set()
            
            # Look for various link patterns
            link_selectors = [
                'a[href*="/solutions/"]',
                'a[href*="/knowledge/"]', 
                'a[href*="/article/"]',
                '.solution-link a',
                '.knowledge-item a',
                '.article-link a'
            ]
            
            for selector in link_selectors:
                links = soup.select(selector)
                for link in links:
                    href = link.get('href')
                    if href:
                        if href.startswith('/'):
                            href = urljoin(self.base_url, href)
                        elif not href.startswith('http'):
                            href = urljoin(self.solutions_url, href)
                        
                        if self.base_url in href and href not in solution_links:
                            solution_links.add(href)
            
            logger.info(f"Discovered {len(solution_links)} solution links")
            return list(solution_links)
            
        except Exception as e:
            logger.error(f"Failed to discover solution links: {e}")
            return []
    
    def scrape_all_solutions(self, max_pages: int = 100):
        """Scrape all discovered solution pages"""
        try:
            # First scrape the main solutions page
            self.scrape_page(self.solutions_url)
            
            # Discover solution links
            solution_links = self.discover_solution_links()
            
            if not solution_links:
                logger.warning("No solution links discovered")
                return
            
            # Scrape each solution page
            scraped_count = 0
            for url in solution_links:
                if scraped_count >= max_pages:
                    logger.info(f"Reached maximum page limit: {max_pages}")
                    break
                
                result = self.scrape_page(url)
                if result:
                    scraped_count += 1
                
                # Respectful delay
                time.sleep(2)
            
            logger.info(f"Scraping completed. Scraped {scraped_count} pages.")
            
        except Exception as e:
            logger.error(f"Failed to scrape all solutions: {e}")
    
    def close(self):
        """Clean up resources"""
        if self.driver:
            self.driver.quit()
        logger.info("Scraper closed")

def main():
    """Main function to run the scraper"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Scrape Creatio Knowledge Hub")
    parser.add_argument("--username", required=True, help="Login username")
    parser.add_argument("--password", required=True, help="Login password")
    parser.add_argument("--headless", action="store_true", help="Run in headless mode")
    parser.add_argument("--max-pages", type=int, default=100, help="Maximum pages to scrape")
    
    args = parser.parse_args()
    
    scraper = CreatioKnowledgeHubScraper(headless=args.headless)
    
    try:
        # Setup driver
        if not scraper.setup_driver():
            logger.error("Failed to setup WebDriver")
            return
        
        # Login
        if not scraper.login(args.username, args.password):
            logger.error("Login failed")
            return
        
        # Extract cookies for requests session
        scraper.extract_cookies_for_requests()
        
        # Scrape all solutions
        scraper.scrape_all_solutions(max_pages=args.max_pages)
        
    except KeyboardInterrupt:
        logger.info("Scraping interrupted by user")
    except Exception as e:
        logger.error(f"Scraping failed: {e}")
    finally:
        scraper.close()

if __name__ == "__main__":
    main()
