# Creatio Academy Scraping Summary

## Task Completed

Successfully scraped the Creatio Academy course catalog as requested in the
first 20-minute session.

## Execution Details

- **Start Time**: ~15:22 UTC
- **End Time**: ~15:24 UTC
- **Total Duration**: ~2 minutes (well within 20-minute limit)
- **Request Delays**: 2-second delays implemented between each request as
  specified

## Results

### Courses Discovered

- **Total Courses Found**: 33
- **Instructor-led Training**: 13 courses
- **E-Learning**: 20 courses

### Data Extracted

For each course, the following metadata was successfully extracted:

- Course title
- Category (Instructor-led Training or E-Learning)
- Course URL
- Duration (hours/days format)
- Level (where available: Beginner, Advanced, etc.)
- Format (where available: Online, Self-paced, etc.)
- Language (all courses are in English)
- Timestamp of when scraped

### Course Categories Found

#### Instructor-led Training Courses:

1. Development on Creatio platform (multiple versions with different durations)
2. Creatio administration and configuration (US/AUS versions)
3. Creatio.ai
4. Service Creatio functionality for end-users
5. Marketing Creatio functionality for end-users
6. Sales Creatio functionality for end-users
7. Full CRM bundle functionality for end-users

#### E-Learning Courses:

1. No-code Playbook series (Creator, Leader)
2. Platform fundamentals
3. Common Features
4. Marketing Tools
5. Sales Tools
6. Service Tools
7. Setup and Administration
8. Development on Creatio Platform
9. BPM Tools
10. Tech Hour series (various release highlights and feature deep-dives)

## Output Files Created

### 1. creatio_courses.csv

- CSV format with all course data
- Headers: title, category, subcategory, url, description, duration, level,
  format, price, language, scraped_at
- 33 rows of course data

### 2. creatio_courses.json

- Complete JSON file containing:
  - All course data with full metadata
  - Hierarchical sitemap structure
  - Scraping metadata (timestamps, total counts)
  - Organized by categories with course counts

### 3. Additional Files

- `creatio_main_page.html` - Sample of main page HTML structure
- `creatio_training_page.html` - Sample of training page HTML structure
- `analyze_creatio_structure.py` - Analysis script used to understand page
  structure
- `creatio_academy_scraper.py` - Initial scraper version
- `creatio_academy_scraper_v2.py` - Improved scraper that successfully extracted
  courses

## Technical Implementation

1. Used BeautifulSoup for HTML parsing
2. Implemented session management with proper headers
3. Added 2-second delays between requests to be respectful to the server
4. Created robust extraction logic that handles multiple page structures
5. Implemented deduplication based on URLs
6. Saved data in both CSV and JSON formats with proper encoding

## Next Steps Recommendations

For future scraping sessions, consider:

1. Extracting more detailed course descriptions from individual course pages
2. Capturing pricing information (currently not available on public pages)
3. Extracting prerequisites and learning objectives
4. Capturing instructor information where available
5. Monitoring for new courses added to the catalog
6. Creating a more detailed subcategory classification based on course content
