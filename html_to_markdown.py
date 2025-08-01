#!/usr/bin/env python3
"""
Convert HTML files to Markdown for better readability.
"""

import html2text
from pathlib import Path
from bs4 import BeautifulSoup
import re

def install_html2text():
    """Install html2text if not available."""
    try:
        import html2text
    except ImportError:
        import subprocess
        print("Installing html2text...")
        subprocess.check_call(["pip", "install", "html2text"])
        import html2text

def convert_html_to_markdown(html_file):
    """Convert HTML file to Markdown."""
    # Read HTML content
    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Parse with BeautifulSoup first to clean up
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Remove script and style elements
    for script in soup(["script", "style"]):
        script.decompose()
    
    # Configure html2text
    h = html2text.HTML2Text()
    h.ignore_links = False
    h.ignore_images = False
    h.body_width = 0  # Don't wrap lines
    h.skip_internal_links = False
    
    # Convert to markdown
    markdown_content = h.handle(str(soup))
    
    # Clean up excessive newlines
    markdown_content = re.sub(r'\n{3,}', '\n\n', markdown_content)
    
    return markdown_content

def process_html_files():
    """Process all HTML files in the project."""
    html_files = [
        'course_page_raw.html',
        'creatio_main_page.html',
        'creatio_training_page.html'
    ]
    
    # Create markdown directory for HTML conversions
    Path("processed_data/html_markdown").mkdir(exist_ok=True)
    
    for html_file in html_files:
        if Path(html_file).exists():
            print(f"Converting {html_file}...")
            
            try:
                markdown_content = convert_html_to_markdown(html_file)
                
                # Save markdown file
                output_file = f"processed_data/html_markdown/{Path(html_file).stem}.md"
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(f"# {Path(html_file).stem.replace('_', ' ').title()}\n\n")
                    f.write(f"*Converted from: {html_file}*\n\n")
                    f.write("---\n\n")
                    f.write(markdown_content)
                
                print(f"  → Saved to {output_file}")
                
            except Exception as e:
                print(f"  → Error converting {html_file}: {e}")
        else:
            print(f"  → {html_file} not found")

if __name__ == "__main__":
    # First, ensure html2text is installed
    try:
        import html2text
    except ImportError:
        import subprocess
        print("Installing html2text...")
        subprocess.check_call(["pip", "install", "html2text"])
    
    print("Converting HTML files to Markdown...")
    process_html_files()
    print("\nHTML to Markdown conversion complete!")
