# Web Scraping Project

A comprehensive web scraping environment with rate limiting, error handling, and support for both static and dynamic content.

## Setup Completed

### 1. Python Environment
- **Python Version**: 3.12.3
- **Virtual Environment**: Created in `venv/` directory
- **Activation**: Run `source venv/bin/activate` before using

### 2. Installed Libraries
- **requests**: HTTP library for fetching web pages
- **beautifulsoup4**: HTML/XML parsing library
- **selenium**: Web browser automation for dynamic content
- **pandas**: Data manipulation and analysis
- **webdriver-manager**: Automatic management of browser drivers

### 3. Browser Setup
- **Chrome**: Installed (version 138.0.7204.168)
- **ChromeDriver**: Managed automatically by webdriver-manager

### 4. Project Structure
```
web-scraping-project/
├── data/
│   ├── raw/          # Raw scraped data (JSON format)
│   └── processed/    # Processed data (CSV format)
├── scripts/
│   └── example_scraper.py  # Example scraper implementation
├── logs/             # Log files for error tracking
├── templates/
│   ├── rate_limiter.py    # Rate limiting utilities
│   └── error_handler.py   # Error handling utilities
├── venv/             # Virtual environment
└── README.md         # This file
```

## Usage

### 1. Activate Virtual Environment
```bash
cd ~/web-scraping-project
source venv/bin/activate
```

### 2. Basic Static Web Scraping
```python
from scripts.example_scraper import WebScraper

scraper = WebScraper(use_selenium=False)
soup = scraper.scrape_static_page("https://example.com")
```

### 3. Dynamic Web Scraping (JavaScript-rendered content)
```python
from scripts.example_scraper import WebScraper
from selenium.webdriver.common.by import By

scraper = WebScraper(use_selenium=True, headless=True)
soup = scraper.scrape_dynamic_page(
    "https://example.com",
    wait_for_element=(By.CLASS_NAME, 'content')
)
scraper.close()
```

### 4. Rate Limiting

The project includes multiple rate limiting strategies:

- **RateLimiter Class**: Controls request frequency with a sliding window
- **Random Delays**: Human-like browsing patterns
- **Exponential Backoff**: For retry logic
- **Decorator Pattern**: Easy application to any function

Example:
```python
from templates.rate_limiter import RateLimiter, rate_limit_decorator

# Class-based rate limiting
limiter = RateLimiter(max_requests=10, time_window=60)
limiter.wait_if_needed()

# Decorator-based rate limiting
@rate_limit_decorator(calls_per_minute=30)
def scrape_page(url):
    # Your code here
    pass
```

### 5. Error Handling

Comprehensive error handling for robust scraping:

- **Retry Logic**: Automatic retries with exponential backoff
- **HTTP Error Handling**: Specific handling for 429, 404, 500, etc.
- **Selenium Error Handling**: For dynamic content issues
- **Data Validation**: Ensure scraped data meets requirements

Example:
```python
from templates.error_handler import retry_on_exception, validate_scraped_data

@retry_on_exception(max_retries=3, delay=2)
def fetch_page(url):
    # Your code here
    pass

# Validate scraped data
data = {'title': 'Product', 'price': '$29.99'}
validate_scraped_data(data, required_fields=['title', 'price'])
```

## Best Practices

1. **Respect robots.txt**: Always check and follow website policies
2. **Use appropriate delays**: Avoid overwhelming servers
3. **Set proper User-Agent**: Identify your scraper appropriately
4. **Handle errors gracefully**: Use the provided error handling templates
5. **Store data efficiently**: Use JSON for raw data, CSV for processed data
6. **Monitor your scraping**: Check logs regularly for issues

## Running the Example

To test the setup:

```bash
cd ~/web-scraping-project
source venv/bin/activate
python scripts/example_scraper.py
```

## Troubleshooting

### Chrome/ChromeDriver Issues
- The webdriver-manager package automatically downloads and manages ChromeDriver
- If you encounter issues, ensure Chrome is up to date

### Import Errors
- Make sure the virtual environment is activated
- Run from the project root directory

### Permission Errors
- Ensure you have write permissions in the data/ and logs/ directories

## Next Steps

1. Customize the example_scraper.py for your specific needs
2. Add more sophisticated data extraction logic
3. Implement data cleaning and processing pipelines
4. Set up scheduled scraping jobs (using cron or similar)
5. Consider using a database for larger datasets

## Security Considerations

- Never commit credentials or API keys to version control
- Use environment variables for sensitive information
- Be cautious when scraping sites that require authentication
- Consider using proxies for large-scale scraping

---

Happy scraping! Remember to always respect website terms of service and rate limits.
