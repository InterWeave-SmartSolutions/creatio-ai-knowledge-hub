#!/usr/bin/env python3
"""
Data processing script for scraped Creatio training courses.
This script cleans, deduplicates, and organizes the scraped data.
"""

import json
import csv
import pandas as pd
from pathlib import Path
from datetime import datetime
import hashlib
from collections import defaultdict

# Create necessary directories
Path("processed_data").mkdir(exist_ok=True)
Path("processed_data/markdown").mkdir(exist_ok=True)
Path("processed_data/summaries").mkdir(exist_ok=True)
Path("processed_data/indexes").mkdir(exist_ok=True)

def load_data():
    """Load scraped data from JSON file."""
    with open('creatio_courses.json', 'r') as f:
        data = json.load(f)
    return data

def clean_and_deduplicate(data):
    """Clean and deduplicate course data."""
    courses = data['courses']
    
    # Create a set to track unique courses by URL
    seen_urls = set()
    unique_courses = []
    duplicates = []
    
    for course in courses:
        # Clean empty strings and convert to None
        for key, value in course.items():
            if value == "":
                course[key] = None
        
        # Check for duplicates based on URL
        if course['url'] not in seen_urls:
            seen_urls.add(course['url'])
            unique_courses.append(course)
        else:
            duplicates.append(course)
    
    print(f"Total courses: {len(courses)}")
    print(f"Unique courses: {len(unique_courses)}")
    print(f"Duplicates removed: {len(duplicates)}")
    
    # Update data with cleaned courses
    data['courses'] = unique_courses
    data['total_courses'] = len(unique_courses)
    data['processing_date'] = datetime.now().isoformat()
    data['duplicates_removed'] = len(duplicates)
    
    return data, duplicates

def generate_markdown(course):
    """Convert course data to Markdown format."""
    md_content = f"# {course['title']}\n\n"
    
    if course.get('category'):
        md_content += f"**Category:** {course['category']}\n\n"
    
    if course.get('subcategory'):
        md_content += f"**Subcategory:** {course['subcategory']}\n\n"
    
    if course.get('description'):
        md_content += f"## Description\n\n{course['description']}\n\n"
    
    md_content += "## Course Details\n\n"
    
    details = []
    if course.get('duration'):
        details.append(f"- **Duration:** {course['duration']}")
    if course.get('level'):
        details.append(f"- **Level:** {course['level']}")
    if course.get('format'):
        details.append(f"- **Format:** {course['format']}")
    if course.get('price'):
        details.append(f"- **Price:** {course['price']}")
    if course.get('language'):
        details.append(f"- **Language:** {course['language']}")
    
    md_content += "\n".join(details) + "\n\n"
    
    if course.get('url'):
        md_content += f"**Course URL:** [{course['url']}]({course['url']})\n\n"
    
    md_content += f"*Last updated: {course.get('scraped_at', 'Unknown')}*\n"
    
    return md_content

def save_markdown_files(data):
    """Save each course as a Markdown file."""
    for i, course in enumerate(data['courses']):
        # Create a safe filename from the title
        safe_title = "".join(c for c in course['title'] if c.isalnum() or c in (' ', '-', '_')).rstrip()
        safe_title = safe_title.replace(' ', '_')[:100]  # Limit length
        
        filename = f"processed_data/markdown/{i+1:03d}_{safe_title}.md"
        
        md_content = generate_markdown(course)
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(md_content)
    
    print(f"Created {len(data['courses'])} Markdown files")

def create_category_index(data):
    """Create an index organized by categories."""
    categories = defaultdict(list)
    
    for course in data['courses']:
        category = course.get('category', 'Uncategorized')
        categories[category].append(course)
    
    # Create main index
    index_content = "# Creatio Training Courses Index\n\n"
    index_content += f"Total Courses: {data['total_courses']}\n"
    index_content += f"Last Updated: {data.get('processing_date', 'Unknown')}\n\n"
    
    index_content += "## Categories\n\n"
    
    for category, courses in sorted(categories.items()):
        index_content += f"- [{category}](#{category.lower().replace(' ', '-').replace('-', '')}): {len(courses)} courses\n"
    
    index_content += "\n---\n\n"
    
    # Add courses by category
    for category, courses in sorted(categories.items()):
        index_content += f"## {category}\n\n"
        
        for course in sorted(courses, key=lambda x: x['title']):
            index_content += f"### {course['title']}\n"
            if course.get('duration'):
                index_content += f"- Duration: {course['duration']}\n"
            if course.get('level'):
                index_content += f"- Level: {course['level']}\n"
            if course.get('format'):
                index_content += f"- Format: {course['format']}\n"
            if course.get('url'):
                index_content += f"- [View Course]({course['url']})\n"
            index_content += "\n"
    
    with open('processed_data/indexes/category_index.md', 'w', encoding='utf-8') as f:
        f.write(index_content)
    
    return categories

def generate_category_summaries(categories, data):
    """Generate summary documents for each course category."""
    for category, courses in categories.items():
        summary_content = f"# {category} - Summary\n\n"
        summary_content += f"**Total Courses:** {len(courses)}\n"
        summary_content += f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        # Analyze levels
        levels = defaultdict(int)
        for course in courses:
            level = course.get('level', 'Not specified')
            levels[level] += 1
        
        if levels:
            summary_content += "## Course Levels\n\n"
            for level, count in sorted(levels.items(), key=lambda x: (x[0] is None, x[0])):
                summary_content += f"- {level}: {count} courses\n"
            summary_content += "\n"
        
        # Analyze formats
        formats = defaultdict(int)
        for course in courses:
            format_type = course.get('format', 'Not specified')
            formats[format_type] += 1
        
        if formats:
            summary_content += "## Course Formats\n\n"
            for format_type, count in sorted(formats.items(), key=lambda x: (x[0] is None, x[0])):
                summary_content += f"- {format_type}: {count} courses\n"
            summary_content += "\n"
        
        # Analyze durations
        summary_content += "## Duration Analysis\n\n"
        durations = []
        for course in courses:
            if course.get('duration'):
                durations.append(course['duration'])
        
        if durations:
            summary_content += "Durations found:\n"
            duration_counts = defaultdict(int)
            for d in durations:
                duration_counts[d] += 1
            
            for duration, count in sorted(duration_counts.items(), key=lambda x: (x[0] is None, x[0])):
                summary_content += f"- {duration}: {count} courses\n"
        else:
            summary_content += "No duration information available.\n"
        
        summary_content += "\n## Course List\n\n"
        
        for course in sorted(courses, key=lambda x: x['title']):
            summary_content += f"1. **{course['title']}**\n"
            if course.get('duration'):
                summary_content += f"   - Duration: {course['duration']}\n"
            if course.get('level'):
                summary_content += f"   - Level: {course['level']}\n"
            summary_content += "\n"
        
        # Save summary
        safe_category = "".join(c for c in category if c.isalnum() or c in (' ', '-', '_')).rstrip()
        safe_category = safe_category.replace(' ', '_')
        
        with open(f'processed_data/summaries/{safe_category}_summary.md', 'w', encoding='utf-8') as f:
            f.write(summary_content)
    
    print(f"Created {len(categories)} category summaries")

def create_master_index():
    """Create a master index file for navigation."""
    index_content = """# Creatio Training Courses - Master Index

This index provides navigation to all processed course data.

## Directory Structure

```
processed_data/
├── indexes/
│   ├── master_index.md (this file)
│   └── category_index.md
├── markdown/
│   └── [Individual course files in Markdown]
├── summaries/
│   └── [Category summary files]
└── cleaned_data.json
```

## Quick Links

- [Course Categories Index](./category_index.md)
- [Cleaned Data (JSON)](../cleaned_data.json)
- [Original Data Backup](../original_data_backup.json)

## Category Summaries

"""
    
    # List all summary files
    summary_files = list(Path('processed_data/summaries').glob('*.md'))
    
    for summary_file in sorted(summary_files):
        category_name = summary_file.stem.replace('_summary', '').replace('_', ' ')
        index_content += f"- [{category_name}](../summaries/{summary_file.name})\n"
    
    index_content += "\n## Statistics\n\n"
    
    # Add statistics from cleaned data
    with open('processed_data/cleaned_data.json', 'r') as f:
        clean_data = json.load(f)
    
    index_content += f"- Total Courses: {clean_data['total_courses']}\n"
    index_content += f"- Duplicates Removed: {clean_data.get('duplicates_removed', 0)}\n"
    index_content += f"- Processing Date: {clean_data.get('processing_date', 'Unknown')}\n"
    index_content += f"- Original Scrape Date: {clean_data.get('scraped_at', 'Unknown')}\n"
    
    with open('processed_data/indexes/master_index.md', 'w', encoding='utf-8') as f:
        f.write(index_content)

def save_cleaned_data(data):
    """Save cleaned data to JSON file."""
    with open('processed_data/cleaned_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    # Also save as CSV for compatibility
    df = pd.DataFrame(data['courses'])
    df.to_csv('processed_data/cleaned_data.csv', index=False)
    
    print("Saved cleaned data to JSON and CSV formats")

def create_backup():
    """Create a backup of original data before processing."""
    import shutil
    
    # Backup original files
    files_to_backup = [
        'creatio_courses.json',
        'creatio_courses.csv'
    ]
    
    backup_dir = Path('backups')
    backup_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    for file in files_to_backup:
        if Path(file).exists():
            backup_name = f"{backup_dir}/{timestamp}_{file}"
            shutil.copy2(file, backup_name)
            print(f"Backed up {file} to {backup_name}")
    
    # Also copy to processed_data for easy access
    if Path('creatio_courses.json').exists():
        shutil.copy2('creatio_courses.json', 'processed_data/original_data_backup.json')

def main():
    """Main processing function."""
    print("Starting data processing...")
    
    # Create backup first
    create_backup()
    
    # Load data
    data = load_data()
    
    # Clean and deduplicate
    cleaned_data, duplicates = clean_and_deduplicate(data)
    
    # Save cleaned data
    save_cleaned_data(cleaned_data)
    
    # Convert to Markdown
    save_markdown_files(cleaned_data)
    
    # Create indexes
    categories = create_category_index(cleaned_data)
    
    # Generate summaries
    generate_category_summaries(categories, cleaned_data)
    
    # Create master index
    create_master_index()
    
    print("\nProcessing complete!")
    print(f"Check the 'processed_data' directory for all outputs.")
    
    # Summary report
    if duplicates:
        print(f"\nDuplicates found and removed:")
        for dup in duplicates:
            print(f"  - {dup['title']} ({dup['url']})")

if __name__ == "__main__":
    main()
