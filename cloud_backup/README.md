# Creatio Training Courses - Scraped Data Backup

## Backup Information
- **Date**: 2025-08-01 16:09:35
- **Source**: Creatio Academy (https://academy.creatio.com)
- **Total Courses**: 33

## Directory Structure
```
cloud_backup/
├── data/
│   ├── json/          # Cleaned JSON data
│   ├── csv/           # CSV exports
│   └── html/          # Original HTML files
├── processed/
│   ├── markdown/      # Individual course Markdown files
│   ├── summaries/     # Category summaries
│   └── indexes/       # Navigation indexes
└── archives/
    ├── *.tar.gz       # Compressed backups
    └── *.zip          # Alternative format
```

## File Descriptions

### Data Files
- `creatio_courses.json` - Main scraped data in JSON format
- `creatio_courses.csv` - Same data in CSV format
- `cleaned_data.json` - Processed and deduplicated data

### Processed Files
- `markdown/` - Individual course files in Markdown format
- `summaries/` - Category-wise summaries
- `indexes/` - Navigation and category indexes

### Scripts
- `process_data.py` - Data processing script
- `html_to_markdown.py` - HTML to Markdown converter

## Usage
1. Download the entire backup or specific directories
2. Use the indexes for navigation
3. Markdown files are human-readable
4. JSON/CSV files can be imported into other tools

## Statistics
- Total unique courses: 33
- Categories: E-Learning, Instructor-led Training
- Data processed on: 2025-08-01
