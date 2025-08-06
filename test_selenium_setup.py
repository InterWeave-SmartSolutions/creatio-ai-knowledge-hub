#!/usr/bin/env python3
"""
Test script to verify Selenium and Chrome driver setup
"""

import sys
from selenium_knowledge_hub_scraper import CreatioKnowledgeHubScraper, logger

def test_driver_setup():
    """Test if the Chrome driver can be set up successfully"""
    try:
        print("Testing Selenium Chrome driver setup...")
        
        scraper = CreatioKnowledgeHubScraper(headless=True)
        
        if scraper.setup_driver():
            print("✓ Chrome driver setup successful!")
            
            # Test navigation to a simple page
            try:
                scraper.driver.get("https://www.example.com")
                title = scraper.driver.title
                print(f"✓ Successfully navigated to example.com (title: {title})")
                
                # Test Knowledge Hub accessibility (without login)
                scraper.driver.get("https://knowledge-hub.creatio.com")
                title = scraper.driver.title
                print(f"✓ Successfully accessed knowledge-hub.creatio.com (title: {title})")
                
            except Exception as e:
                print(f"✗ Navigation test failed: {e}")
                return False
            
            scraper.close()
            return True
        else:
            print("✗ Chrome driver setup failed!")
            return False
            
    except Exception as e:
        print(f"✗ Test failed with exception: {e}")
        return False

def main():
    """Run the test"""
    if test_driver_setup():
        print("\n✓ All tests passed! The scraper should work correctly.")
        return 0
    else:
        print("\n✗ Some tests failed. Please check the setup.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
