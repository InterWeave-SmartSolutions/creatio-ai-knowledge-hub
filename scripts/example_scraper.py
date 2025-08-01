"""
Example Web Scraper
This script demonstrates how to use the installed tools and templates for web scraping.
"""

import sys
import os
import json
import pandas as pd
from datetime import datetime

# Add parent directory to path to import templates
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Import our custom templates
from templates.rate_limiter import RateLimiter, rate_limit_decorator, random_delay
from templates.error_handler import ErrorHandler, retry_on_exception, validate_scraped_data


class WebScraper:
    """
    A comprehensive web scraper that can handle both static and dynamic content.
    """
    
    def __init__(self, use_selenium=False, headless=True):
        """
        Initialize the web scraper.
        
        Args:
            use_selenium: Whether to use Selenium for dynamic content
            headless: Whether to run browser in headless mode
        """
        self.use_selenium = use_selenium
        self.driver = None
        self.error_handler = ErrorHandler()
        self.rate_limiter = RateLimiter(max_requests=10, time_window=60)
        
        if use_selenium:
            self._setup_selenium(headless)
    
    def _setup_selenium(self, headless):
        """Set up Selenium WebDriver with Chrome."""
        chrome_options = Options()
        if headless:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Use webdriver-manager to automatically handle ChromeDriver
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
    
    @retry_on_exception(max_retries=3, delay=2, exceptions=(requests.RequestException,))
    @rate_limit_decorator(calls_per_minute=30)
    def scrape_static_page(self, url):
        """
        Scrape a static web page using requests and BeautifulSoup.
        
        Args:
            url: The URL to scrape
        
        Returns:
            BeautifulSoup object or None if failed
        """
        try:
            self.rate_limiter.wait_if_needed()
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            return BeautifulSoup(response.content, 'html.parser')
            
        except requests.RequestException as e:
            action = self.error_handler.handle_request_error(e, url)
            if action == 'abort':
                raise
            return None
    
    def scrape_dynamic_page(self, url, wait_for_element=None):
        """
        Scrape a dynamic web page using Selenium.
        
        Args:
            url: The URL to scrape
            wait_for_element: Tuple of (By.TYPE, 'selector') to wait for
        
        Returns:
            BeautifulSoup object or None if failed
        """
        if not self.driver:
            raise RuntimeError("Selenium not initialized. Set use_selenium=True")
        
        try:
            self.rate_limiter.wait_if_needed()
            self.driver.get(url)
            
            if wait_for_element:
                wait = WebDriverWait(self.driver, 10)
                wait.until(EC.presence_of_element_located(wait_for_element))
            
            # Add random delay to appear more human-like
            random_delay(1, 3)
            
            return BeautifulSoup(self.driver.page_source, 'html.parser')
            
        except Exception as e:
            print(f"Error scraping dynamic page {url}: {str(e)}")
            return None
    
    def extract_product_data(self, soup, selectors):
        """
        Extract product data from a BeautifulSoup object.
        
        Args:
            soup: BeautifulSoup object
            selectors: Dictionary of field names to CSS selectors
        
        Returns:
            Dictionary of extracted data
        """
        data = {}
        
        for field, selector in selectors.items():
            try:
                element = soup.select_one(selector)
                if element:
                    data[field] = element.get_text(strip=True)
                else:
                    data[field] = None
            except Exception as e:
                print(f"Error extracting {field}: {str(e)}")
                data[field] = None
        
        return data
    
    def save_to_csv(self, data_list, filename):
        """
        Save scraped data to CSV file.
        
        Args:
            data_list: List of dictionaries containing scraped data
            filename: Output filename
        """
        df = pd.DataFrame(data_list)
        filepath = os.path.join('..', 'data', 'processed', filename)
        df.to_csv(filepath, index=False)
        print(f"Data saved to {filepath}")
    
    def save_to_json(self, data_list, filename):
        """
        Save scraped data to JSON file.
        
        Args:
            data_list: List of dictionaries containing scraped data
            filename: Output filename
        """
        filepath = os.path.join('..', 'data', 'raw', filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data_list, f, indent=2, ensure_ascii=False)
        print(f"Data saved to {filepath}")
    
    def close(self):
        """Clean up resources."""
        if self.driver:
            self.driver.quit()
        self.error_handler.log_summary()


# Example usage
def main():
    """
    Example of how to use the WebScraper class.
    """
    # Example 1: Scrape static content
    print("Example 1: Scraping static content")
    scraper = WebScraper(use_selenium=False)
    
    # Example URL (you would replace this with actual URLs)
    url = "https://example.com"
    soup = scraper.scrape_static_page(url)
    
    if soup:
        # Extract title
        title = soup.find('title')
        if title:
            print(f"Page title: {title.get_text()}")
    
    # Example 2: Scrape dynamic content
    print("\nExample 2: Scraping dynamic content")
    dynamic_scraper = WebScraper(use_selenium=True, headless=True)
    
    try:
        # Example: Wait for a specific element to load
        soup = dynamic_scraper.scrape_dynamic_page(
            url,
            wait_for_element=(By.CLASS_NAME, 'content')
        )
        
        if soup:
            # Extract data using CSS selectors
            selectors = {
                'title': 'h1',
                'description': '.description',
                'price': '.price'
            }
            
            data = dynamic_scraper.extract_product_data(soup, selectors)
            
            # Validate the data
            try:
                validate_scraped_data(data, ['title'])
                print("Data validation passed!")
            except Exception as e:
                print(f"Data validation failed: {e}")
            
            # Save data
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            dynamic_scraper.save_to_json([data], f'scraped_data_{timestamp}.json')
            dynamic_scraper.save_to_csv([data], f'scraped_data_{timestamp}.csv')
    
    finally:
        dynamic_scraper.close()
    
    print("\nScraping completed!")


if __name__ == "__main__":
    main()
