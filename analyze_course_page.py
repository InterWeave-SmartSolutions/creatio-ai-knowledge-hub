import requests
from bs4 import BeautifulSoup
import json

# Test URL - trying an e-learning course instead
url = "https://academy.creatio.com/e-learning/platform"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

print(f"Analyzing course page: {url}")
print("=" * 60)

try:
    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Save raw HTML for inspection
    with open('course_page_raw.html', 'w', encoding='utf-8') as f:
        f.write(response.text)
    
    print("Page title:", soup.title.string if soup.title else "No title")
    
    # Look for common content sections
    print("\nSearching for content sections...")
    
    # Check for different types of content containers
    content_selectors = [
        ('Main content', ['main', '.main-content', '#main-content', '.content', '#content']),
        ('Course info', ['.course-info', '.course-details', '.course-content']),
        ('Description', ['.description', '.course-description', '.overview']),
        ('Curriculum', ['.curriculum', '.course-curriculum', '.syllabus']),
        ('Materials', ['.materials', '.course-materials', '.resources'])
    ]
    
    for section_name, selectors in content_selectors:
        for selector in selectors:
            elements = soup.select(selector)
            if elements:
                print(f"\n{section_name} found with selector '{selector}':")
                for i, elem in enumerate(elements[:2]):  # Show first 2
                    text = elem.get_text(strip=True)[:200]
                    print(f"  Element {i+1}: {text}...")
                break
    
    # Look for all links
    print("\n\nAll links on page:")
    links = soup.find_all('a', href=True)
    link_types = {'pdf': 0, 'video': 0, 'doc': 0, 'ppt': 0, 'other': 0}
    
    for link in links[:20]:  # Show first 20 links
        href = link['href']
        text = link.get_text(strip=True)
        print(f"  - {text[:50]}: {href[:80]}")
        
        # Categorize links
        if '.pdf' in href.lower():
            link_types['pdf'] += 1
        elif any(vid in href.lower() for vid in ['youtube', 'vimeo', 'video']):
            link_types['video'] += 1
        elif '.doc' in href.lower() or '.docx' in href.lower():
            link_types['doc'] += 1
        elif '.ppt' in href.lower() or '.pptx' in href.lower():
            link_types['ppt'] += 1
        else:
            link_types['other'] += 1
    
    print(f"\nTotal links found: {len(links)}")
    print("Link types:", link_types)
    
    # Look for iframes (videos)
    print("\n\nIframes found:")
    iframes = soup.find_all('iframe')
    for i, iframe in enumerate(iframes):
        src = iframe.get('src', 'No src')
        print(f"  Iframe {i+1}: {src}")
    
    # Check for text patterns
    print("\n\nSearching for key text patterns...")
    patterns = ['Prerequisites', 'Objectives', 'Learning', 'Download', 'Materials', 'Resources']
    
    for pattern in patterns:
        elements = soup.find_all(text=lambda text: text and pattern.lower() in text.lower())
        if elements:
            print(f"\n'{pattern}' found in {len(elements)} places:")
            for elem in elements[:3]:
                parent = elem.parent
                context = parent.get_text(strip=True)[:150]
                print(f"  - {context}...")
    
    # Look for structured data
    print("\n\nStructured data:")
    scripts = soup.find_all('script', type='application/ld+json')
    for i, script in enumerate(scripts):
        try:
            data = json.loads(script.string)
            print(f"  Script {i+1}: {json.dumps(data, indent=2)[:200]}...")
        except:
            pass
    
    # Check page structure
    print("\n\nPage structure analysis:")
    print(f"  H1 tags: {len(soup.find_all('h1'))}")
    print(f"  H2 tags: {len(soup.find_all('h2'))}")
    print(f"  H3 tags: {len(soup.find_all('h3'))}")
    print(f"  Divs: {len(soup.find_all('div'))}")
    print(f"  Sections: {len(soup.find_all('section'))}")
    
    # Show some H2/H3 headers
    print("\nHeaders found:")
    for tag in ['h1', 'h2', 'h3']:
        headers = soup.find_all(tag)
        if headers:
            print(f"\n{tag.upper()} headers:")
            for header in headers[:5]:
                print(f"  - {header.get_text(strip=True)}")

except Exception as e:
    print(f"Error: {e}")
