# Creatio Knowledge Hub Selenium Scraper

This directory contains a comprehensive Selenium-based scraper for the Creatio
Knowledge Hub that can handle authentication, cross-domain logins, and security
measures that prevented the previous requests-based scrapers from working.

## Features

- **Selenium WebDriver Integration**: Uses Chrome browser automation to handle
  JavaScript, cookies, and security measures
- **Robust Authentication**: Handles cross-domain login flows and session
  management
- **Anti-Bot Bypass**: Configured to appear as a real browser rather than
  automated traffic
- **Comprehensive Data Storage**: Stores scraped content in SQLite database with
  full text, markdown, and HTML versions
- **Link Discovery**: Automatically discovers and follows solution links
- **Media Extraction**: Identifies and catalogs images and other media files
- **Resumable Scraping**: Tracks already scraped URLs to avoid duplication
- **Flexible Configuration**: Supports both command-line arguments and
  environment variables

## Installation

### Prerequisites

1. **Python 3.8+** with pip
2. **Google Chrome browser** (installed automatically via package manager if not
   present)
3. **Virtual environment** (recommended)

### Setup

1. **Install Python dependencies:**

   ```bash
   pip install selenium webdriver-manager beautifulsoup4 requests lxml python-dotenv
   ```

2. **Configure credentials:**

   Create a `.env` file from the example:

   ```bash
   cp .env.example .env
   ```

   Edit `.env` and add your Creatio credentials:

   ```
   CREATIO_USERNAME=your_email@example.com
   CREATIO_PASSWORD=your_password_here
   HEADLESS=false
   MAX_PAGES=100
   ```

## Usage

### Quick Start

**Interactive mode (recommended for first run):**

```bash
python run_scraper.py --interactive
```

**Headless mode (for automated runs):**

```bash
python run_scraper.py --headless --max-pages 50
```

**Using environment variables:**

```bash
# With .env file configured
python run_scraper.py
```

**Command line with credentials:**

```bash
python run_scraper.py --username "your@email.com" --password "yourpass" --headless
```

### Command Line Options

- `--username`: Login username (overrides env var)
- `--password`: Login password (overrides env var)
- `--headless`: Run browser in headless mode (no GUI)
- `--interactive`: Force interactive mode (shows browser window)
- `--max-pages`: Maximum number of pages to scrape (default: 100)

### Testing the Setup

Verify that Selenium and Chrome are properly configured:

```bash
python test_selenium_setup.py
```

This will test:

- Chrome WebDriver initialization
- Basic navigation capabilities
- Access to the Knowledge Hub website

## How It Works

### Authentication Process

1. **Navigate to Login Page**: Opens the Creatio Knowledge Hub login page
2. **Handle Redirects**: Automatically follows redirects to profile.creatio.com
   if needed
3. **Form Detection**: Dynamically finds username, password, and submit elements
4. **Credential Entry**: Fills in login credentials securely
5. **Session Validation**: Verifies successful authentication by checking access
   to protected content

### Data Extraction

1. **Page Discovery**: Starts from the main solutions page and discovers linked
   content
2. **Content Extraction**: Extracts main content while removing scripts and
   styling
3. **Format Conversion**: Converts HTML to both plain text and markdown formats
4. **Link Following**: Discovers and queues additional pages for scraping
5. **Media Cataloging**: Identifies and records images and media files

### Data Storage

The scraper uses SQLite database
(`ai_knowledge_hub/solutions_hub/knowledge_hub.db`) with the following
structure:

- **`pages`**: Main content storage (URL, title, text, markdown, HTML, metadata)
- **`links`**: Discovered links and their relationships
- **`media`**: Media files and their locations

## Output Structure

```
ai_knowledge_hub/
└── solutions_hub/
    ├── knowledge_hub.db       # SQLite database with all scraped content
    └── knowledge_hub_scraper.log  # Detailed scraping logs
```

## Security and Ethics

### Responsible Scraping

- **Rate Limiting**: Includes respectful delays between requests (2 seconds)
- **User-Agent**: Uses realistic browser user-agent strings
- **Session Management**: Properly handles cookies and authentication
- **Error Handling**: Gracefully handles failures and access denials

### Security Features

- **Credential Protection**: Passwords are handled securely and not logged
- **Session Isolation**: Each run uses fresh session data
- **Access Validation**: Verifies authentication before proceeding
- **Error Recovery**: Handles various failure scenarios gracefully

## Troubleshooting

### Common Issues

**Chrome Binary Not Found:**

```bash
# Install Google Chrome
sudo apt update
sudo apt install -y google-chrome-stable
```

**WebDriver Issues:**

```bash
# Clear WebDriver cache
rm -rf ~/.wdm/
```

**Authentication Failures:**

- Verify credentials are correct
- Check if 2FA is enabled on your account
- Try interactive mode to see detailed error messages
- Ensure account has access to the Knowledge Hub

**403 Forbidden Errors:**

- Run in interactive mode to see if manual intervention is needed
- Check if your IP is blocked
- Try again later as it might be rate limiting

### Debug Mode

Run with interactive mode to see browser actions:

```bash
python run_scraper.py --interactive --max-pages 5
```

### Logs

Check the log file for detailed information:

```bash
tail -f knowledge_hub_scraper.log
```

## Advanced Usage

### Custom Scripts

The `CreatioKnowledgeHubScraper` class can be imported and used in custom
scripts:

```python
from selenium_knowledge_hub_scraper import CreatioKnowledgeHubScraper

scraper = CreatioKnowledgeHubScraper(headless=True)
scraper.setup_driver()
scraper.login("username", "password")
scraper.scrape_page("https://knowledge-hub.creatio.com/solutions/specific-page")
scraper.close()
```

### Database Queries

Access scraped data directly:

```python
import sqlite3

conn = sqlite3.connect('ai_knowledge_hub/solutions_hub/knowledge_hub.db')
cursor = conn.cursor()

# Get all page titles
cursor.execute("SELECT title, url FROM pages")
pages = cursor.fetchall()

# Search content
cursor.execute("SELECT title, content_text FROM pages WHERE content_text LIKE ?", ('%search_term%',))
results = cursor.fetchall()
```

## Limitations

- **Rate Limiting**: Respects server resources with built-in delays
- **JavaScript Dependency**: Requires full browser environment (Chrome)
- **Resource Usage**: More memory and CPU intensive than simple HTTP requests
- **Site Changes**: May need updates if Knowledge Hub structure changes
- **Access Requirements**: Requires valid Creatio account with Knowledge Hub
  access

## Support

For issues or questions:

1. Check the troubleshooting section above
2. Review the log files for detailed error information
3. Test with interactive mode to see browser behavior
4. Verify credentials and account access independently

The scraper is designed to be robust and handle most common scenarios, but the
Creatio Knowledge Hub may implement changes that require script updates.
