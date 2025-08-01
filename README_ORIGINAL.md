<<<<<<< HEAD
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
=======
# Creatio Academy Knowledge Database & MCP Server

A comprehensive knowledge management system for Creatio Academy content,
featuring AI-powered content processing, semantic search, and Model Context
Protocol (MCP) server integration for seamless AI agent access.

## 🌟 Complete System Overview

This system provides both **content processing capabilities** and a
**production-ready MCP server** for AI agents:

- 🌐 **Complete Content Processing**: Downloads and processes ALL content from
  academy.creatio.com
- 🎥 **Video Intelligence**: Full video transcription and AI-powered analysis
- 🚀 **MCP Server**: RESTful API with WebSocket support for real-time AI agent
  interaction
- 🔍 **Advanced Search**: Semantic search across all content types
- 📊 **Content Analytics**: AI-powered summaries, topic detection, and
  complexity assessment

## 🚀 Quick Start

### Run Complete Processing Pipeline

```bash
./run_complete_pipeline.sh run
```

This single command will:

1. Crawl all pages from academy.creatio.com
2. Extract all video URLs from every page
3. Download all videos with metadata
4. Transcribe all videos to text using AI
5. Convert all web pages to markdown
6. Download all resources (PDFs, docs, etc.)
7. Create comprehensive AI-readable index
8. Generate detailed processing report

### Check Status

```bash
./run_complete_pipeline.sh status
```

### Check Dependencies

```bash
./run_complete_pipeline.sh check
```

### Clean Cache

```bash
./run_complete_pipeline.sh clean
```

## 📁 Output Structure

After processing, all content will be organized in `processed_content/`:

```
processed_content/
├── 🎥 videos/                    # All downloaded videos
│   ├── video_id_title.mp4
│   ├── video_id_title.info.json
│   └── video_id_title.webp
├── 📝 transcripts/               # AI-generated transcriptions
│   ├── video_id_transcript.txt
│   └── video_id_detailed_transcript.json
├── 📄 pages/                     # Web pages as markdown
│   ├── page1.md
│   └── page2.md
├── 📋 resources/                 # Downloaded resources
│   ├── document1.pdf
│   └── image1.png
├── 🔍 ai_content_index.json      # Structured content index
├── 📖 searchable_content.txt     # Complete AI-readable content
└── 📊 processing_report.md       # Detailed processing report
```

## 🎯 Key Features

### Complete Content Coverage

- **Web Crawling**: Uses `wget` to recursively download all connected pages
- **Video Detection**: Finds videos from YouTube, Vimeo, direct MP4 links,
  iframes
- **Resource Extraction**: Downloads PDFs, documents, images, and other
  resources
- **Smart Organization**: Categorizes content by type and source

### AI-Powered Processing

- **Video Transcription**: Uses OpenAI Whisper for accurate speech-to-text
- **Content Conversion**: Converts HTML to clean markdown
- **Searchable Index**: Creates unified searchable content for AI analysis
- **Metadata Preservation**: Maintains source URLs, timestamps, and descriptions

### Robust Download System

- **Rate Limiting**: Prevents overwhelming servers
- **Retry Logic**: Handles temporary failures automatically
- **Progress Tracking**: Resumes interrupted downloads
- **Integrity Verification**: Validates downloaded content

## 🛠️ Technical Components

### Core Scripts

- `run_complete_pipeline.sh` - Master control script
- `content_processor.py` - Main Python processing engine
- `youtube_downloader.py` - Specialized YouTube video downloader
- `run_download.sh` - Video download management

### Dependencies

- **Python 3.8+** with virtual environment
- **wget** - Web crawling
- **yt-dlp** - Video downloading
- **ffmpeg** - Audio/video processing
- **OpenAI Whisper** - AI transcription
- **BeautifulSoup4** - HTML parsing
- **requests** - HTTP requests

## 📊 Processing Pipeline

### Phase 1: Discovery

1. Crawl academy.creatio.com recursively
2. Parse all HTML pages
3. Extract video URLs from all sources
4. Identify downloadable resources

### Phase 2: Content Download

1. Download all videos with metadata
2. Download all resources (PDFs, images, etc.)
3. Verify download integrity
4. Organize by category

### Phase 3: AI Processing

1. Extract audio from videos
2. Transcribe using Whisper AI
3. Convert HTML pages to markdown
4. Create structured metadata

### Phase 4: AI Optimization

1. Combine all content into searchable format
2. Create comprehensive index
3. Generate processing report
4. Optimize for AI queries

## 🔍 AI-Ready Output

The system produces several AI-optimized files:

### `searchable_content.txt`

- **Complete unified content** from all sources
- **Clean text format** optimized for AI processing
- **Structured sections** for pages and video transcripts
- **Source attribution** for all content

### `ai_content_index.json`

- **Structured metadata** for all processed content
- **File paths and relationships**
- **Processing timestamps and status**
- **Content summaries and statistics**

## 🎥 Video Processing Features

### Comprehensive Video Discovery

- YouTube embedded videos
- Direct video file links (.mp4, .webm, .mov)
- Vimeo embedded content
- iFrame video sources

### Rich Metadata Extraction

- Video titles and descriptions
- Upload dates and durations
- Thumbnail images
- Channel information
- View counts and ratings

### AI Transcription

- High-accuracy speech-to-text using Whisper
- Timestamped transcripts
- Multiple language support
- Automatic subtitle embedding

## 📈 Usage Statistics

After processing, you'll have access to:

- **Total pages processed**
- **Videos downloaded and transcribed**
- **Resources collected**
- **Total content volume**
- **Processing time and efficiency**

## 🔧 Advanced Usage

### Custom Processing

Edit `content_processor.py` to:

- Change crawling domains
- Modify video quality preferences
- Adjust transcription settings
- Customize output formats

### Manual Video Downloads

Use the standalone video downloader:

```bash
./run_download.sh start
```

### Selective Processing

Process specific content types by modifying the pipeline phases in the main
script.

## 🚨 Important Notes

### Processing Time

- **Complete processing can take several hours** depending on content volume
- **Video transcription is CPU-intensive** and takes time
- **Large files require significant disk space**

### Resource Requirements

- **Disk Space**: Several GB for complete content
- **CPU**: Multi-core recommended for faster transcription
- **Memory**: 8GB+ recommended for large video processing

### Network Considerations

- **Rate limiting is implemented** to be respectful of servers
- **Large downloads may take time** with rate limiting
- **Interrupted downloads can be resumed**

## 🎯 Perfect for AI Applications

The processed content is optimized for:

- **AI Training Data**: Clean, structured, and attributed
- **Knowledge Base Systems**: Searchable and cross-referenced
- **Content Analysis**: All formats unified and accessible
- **Research Applications**: Complete coverage with source tracking

---

**Ready to process all Creatio Academy content?**

Run: `./run_complete_pipeline.sh run`

The system will guide you through the complete processing pipeline and deliver
comprehensive, AI-ready content for analysis and learning.
>>>>>>> 91533ea95e557e33edc5f21bd8733baa51322354
