#!/usr/bin/env python3
"""
Enhanced launcher for the Creatio Knowledge Hub Scraper
Supports .env files and command line arguments
"""

import os
import sys
import argparse
from pathlib import Path

# Add current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("Warning: python-dotenv not installed. Using environment variables only.")

from selenium_knowledge_hub_scraper import CreatioKnowledgeHubScraper, logger

def get_credentials():
    """Get credentials from environment variables or command line"""
    parser = argparse.ArgumentParser(description="Scrape Creatio Knowledge Hub")
    parser.add_argument("--username", help="Login username (overrides env var)")
    parser.add_argument("--password", help="Login password (overrides env var)")
    parser.add_argument("--headless", action="store_true", help="Run in headless mode")
    parser.add_argument("--max-pages", type=int, help="Maximum pages to scrape")
    parser.add_argument("--interactive", action="store_true", help="Run in interactive mode (non-headless)")
    
    args = parser.parse_args()
    
    # Get credentials from args or environment
    username = args.username or os.getenv('CREATIO_USERNAME')
    password = args.password or os.getenv('CREATIO_PASSWORD')
    
    # Interactive mode overrides headless
    if args.interactive:
        headless = False
    else:
        headless = args.headless or os.getenv('HEADLESS', 'false').lower() == 'true'
    
    max_pages = args.max_pages or int(os.getenv('MAX_PAGES', 100))
    
    # Prompt for missing credentials
    if not username:
        username = input("Enter Creatio username: ")
    
    if not password:
        import getpass
        password = getpass.getpass("Enter Creatio password: ")
    
    return username, password, headless, max_pages

def main():
    """Main function to run the scraper with enhanced options"""
    try:
        username, password, headless, max_pages = get_credentials()
        
        if not username or not password:
            print("Error: Username and password are required")
            return 1
        
        print(f"Starting scraper with the following settings:")
        print(f"  Username: {username}")
        print(f"  Headless mode: {headless}")
        print(f"  Max pages: {max_pages}")
        print()
        
        scraper = CreatioKnowledgeHubScraper(headless=headless)
        
        # Setup driver
        if not scraper.setup_driver():
            logger.error("Failed to setup WebDriver")
            return 1
        
        # Login
        print("Attempting to login...")
        if not scraper.login(username, password):
            logger.error("Login failed")
            return 1
        
        print("Login successful! Starting to scrape...")
        
        # Extract cookies for requests session
        scraper.extract_cookies_for_requests()
        
        # Scrape all solutions
        scraper.scrape_all_solutions(max_pages=max_pages)
        
        print("\nScraping completed successfully!")
        return 0
        
    except KeyboardInterrupt:
        logger.info("Scraping interrupted by user")
        return 1
    except Exception as e:
        logger.error(f"Scraping failed: {e}")
        return 1
    finally:
        if 'scraper' in locals():
            scraper.close()

if __name__ == "__main__":
    sys.exit(main())
