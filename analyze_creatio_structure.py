import requests
from bs4 import BeautifulSoup
import time
from urllib.parse import urljoin
import json
from utils.cli import base_parser
import argparse, sys

def analyze_page_structure(url):
    """Analyze the structure of a page to understand how to extract data"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    print(f"Analyzing {url}...")
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Failed to fetch page: {response.status_code}")
        return

    soup = BeautifulSoup(response.content, 'html.parser')

    # Analyze page title
    title = soup.find('title')
    print(f"\nPage Title: {title.get_text() if title else 'No title found'}")

    # Look for navigation links
    print("\nNavigation Links:")
    nav_links = soup.find_all('a', href=True)[:20]  # First 20 links
    for link in nav_links:
        href = link.get('href', '')
        text = link.get_text(strip=True)
        if text and len(text) > 2:  # Skip empty or very short links
            print(f"  - {text}: {href}")

    # Look for course-related elements
    print("\nSearching for course-related elements...")

    # Common course-related class names and IDs
    course_indicators = [
        'course', 'training', 'program', 'curriculum', 'module',
        'lesson', 'tutorial', 'workshop', 'certification', 'learning'
    ]

    found_elements = {}

    # Search by class names
    for indicator in course_indicators:
        elements = soup.find_all(class_=lambda x: x and indicator in str(x).lower())
        if elements:
            found_elements[f"class containing '{indicator}'"] = len(elements)

    # Search by IDs
    for indicator in course_indicators:
        elements = soup.find_all(id=lambda x: x and indicator in str(x).lower())
        if elements:
            found_elements[f"id containing '{indicator}'"] = len(elements)

    # Search in divs and sections
    for tag in ['div', 'section', 'article']:
        elements = soup.find_all(tag)
        for elem in elements:
            elem_text = elem.get_text(strip=True).lower()
            for indicator in course_indicators:
                if indicator in elem_text and len(elem_text) < 200:  # Short text likely to be titles
                    class_name = elem.get('class', ['no-class'])[0]
                    found_elements[f"{tag}.{class_name}"] = found_elements.get(f"{tag}.{class_name}", 0) + 1

    print("\nFound elements:")
    for key, count in found_elements.items():
        print(f"  - {key}: {count} elements")

    # Look for specific patterns
    print("\nLooking for specific patterns...")

    # Pattern 1: Links with 'course' or 'training' in href
    course_links = [link for link in soup.find_all('a', href=True)
                   if any(word in link.get('href', '').lower()
                         for word in ['course', 'training', 'learn', 'module'])]

    if course_links:
        print(f"\nFound {len(course_links)} course-related links:")
        for link in course_links[:10]:  # Show first 10
            print(f"  - {link.get_text(strip=True)}: {link.get('href')}")

    # Pattern 2: Look for card-like structures
    cards = soup.find_all(['div', 'article'], class_=lambda x: x and 'card' in str(x).lower())
    if cards:
        print(f"\nFound {len(cards)} card elements")
        if cards:
            print("Sample card content:")
            print(cards[0].prettify()[:500])

    return soup

# Analyze the main academy page
base_url = "https://academy.creatio.com"
soup = analyze_page_structure(base_url)

print("\n" + "="*50)
time.sleep(2)

# Try the training page
training_url = "https://academy.creatio.com/training"
soup_training = analyze_page_structure(training_url)

# Save the raw HTML for inspection
if soup:
    with open('creatio_main_page.html', 'w', encoding='utf-8') as f:
        f.write(str(soup.prettify()[:5000]))  # Save first 5000 chars
    print("\nSaved main page HTML sample to creatio_main_page.html")

if soup_training:
    with open('creatio_training_page.html', 'w', encoding='utf-8') as f:
        f.write(str(soup_training.prettify()[:5000]))  # Save first 5000 chars
    print("Saved training page HTML sample to creatio_training_page.html")

# Minimal CLI entry to align with pipeline usage (non-invasive)
if __name__ == "__main__":
    try:
        parser = base_parser("Analyze Creatio site structure (discovery helper)")
    except Exception:
        parser = argparse.ArgumentParser(description="Analyze Creatio site structure (discovery helper)")
        parser.add_argument("-c","--config", type=str, default="config.yaml")
        parser.add_argument("--in", dest="input_dir", default=None)
        parser.add_argument("--out", dest="output_dir", default="out")
        parser.add_argument("--limit", type=int, default=0)
        parser.add_argument("--format", choices=["json","ndjson"], default="json")
    args = parser.parse_args()
    # Emit JSON line with parsed args so pipeline logs are machine-readable
    print(json.dumps({
        "tool": "analyze_creatio_structure",
        "config": getattr(args, "config", "config.yaml"),
        "input_dir": getattr(args, "input_dir", None),
        "output_dir": getattr(args, "output_dir", "out"),
        "limit": getattr(args, "limit", 0),
        "format": getattr(args, "format", "json")
    }), flush=True)
