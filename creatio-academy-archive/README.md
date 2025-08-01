# Creatio Academy Archive

A comprehensive web scraping and archival tool for the Creatio Academy website,
designed to download, organize, and transcribe educational content.

## Project Structure

```
creatio-academy-archive/
├── pages/          # Downloaded HTML pages
├── videos/         # Downloaded video files
├── transcripts/    # Generated transcriptions
├── resources/      # Other resources (PDFs, images, etc.)
├── metadata/       # Database and metadata files
├── logs/           # Application logs
├── venv/           # Python virtual environment
├── config.py       # Configuration settings
├── database_setup.py # Database initialization script
├── requirements.txt # Python dependencies
├── .env.template   # Environment variables template
└── README.md       # This file
```

## Setup and Installation

### 1. Prerequisites

- Python 3.8 or higher
- FFmpeg (required for audio processing with Whisper)

### 2. Install Dependencies

```bash
# Navigate to project directory
cd creatio-academy-archive

# Activate virtual environment
source venv/bin/activate

# Install dependencies (already done)
pip install -r requirements.txt
```

### 3. Configuration

1. **Environment Variables**: Copy `.env.template` to `.env` and fill in your
   API keys:

   ```bash
   cp .env.template .env
   # Edit .env with your API keys
   ```

2. **Configuration**: Edit `config.py` to customize crawling parameters, file
   paths, and other settings.

### 4. Database Setup

The SQLite database has been automatically created with the following tables:

- **pages**: Web pages metadata and content
- **videos**: Video files metadata and download info
- **transcripts**: Video transcriptions and metadata
- **resources**: Other downloadable resources
- **crawl_sessions**: Crawling session tracking

## Features

### Web Scraping

- **Scrapy-based**: Professional web scraping framework
- **Rate limiting**: Respects robots.txt and implements delays
- **Content extraction**: HTML content processing with html2text
- **Resource download**: Automated download of linked resources

### Video Processing

- **yt-dlp integration**: Advanced video downloading capabilities
- **Multiple formats**: Support for various video formats
- **Quality selection**: Configurable quality preferences
- **Metadata extraction**: Title, description, duration tracking

### Audio Transcription

- **Whisper integration**: OpenAI's speech recognition model
- **Multiple languages**: Configurable language detection
- **Quality control**: Confidence scoring for transcriptions
- **Batch processing**: Automated transcription pipeline

### Data Management

- **SQLite database**: Structured metadata storage
- **Progress tracking**: Resume interrupted downloads
- **Error handling**: Comprehensive error logging
- **Session management**: Track multiple crawling sessions

## Configuration Options

### Crawling Parameters (`config.py`)

- **start_urls**: Initial URLs to crawl
- **allowed_domains**: Domains to restrict crawling to
- **max_depth**: Maximum crawling depth
- **download_delay**: Delay between requests
- **concurrent_requests**: Number of simultaneous requests

### Video Settings

- **quality**: Video quality preference (best, worst, specific)
- **format**: Preferred video format (mp4, mkv, etc.)
- **max_file_size**: Maximum file size for downloads

### Whisper Settings

- **model**: Model size (tiny, base, small, medium, large)
- **language**: Target language for transcription
- **task**: transcribe or translate

## Usage

### Basic Usage

1. **Initialize Database**: Already done during setup
2. **Configure Settings**: Edit `config.py` for your needs
3. **Set Environment Variables**: Configure API keys in `.env`
4. **Run Crawler**: Execute your crawler scripts (to be implemented)

### Database Operations

```python
from database_setup import get_database_stats
get_database_stats()  # View current database status
```

## File Organization

- **Pages**: Saved as HTML files with metadata in database
- **Videos**: Downloaded with original names, metadata tracked
- **Transcripts**: Text files linked to corresponding videos
- **Resources**: Organized by file type and source page
- **Logs**: Timestamped logs for debugging and monitoring

## Dependencies

- **scrapy**: Web scraping framework
- **beautifulsoup4**: HTML parsing
- **requests**: HTTP library
- **yt-dlp**: Video downloading
- **whisper**: Speech recognition
- **html2text**: HTML to text conversion
- **python-dotenv**: Environment variable management

## Next Steps

The infrastructure is now ready. Next phases will include:

1. Implementing the web crawler
2. Video download automation
3. Transcription pipeline
4. Content analysis and indexing
5. Search and retrieval interface

## Notes

- Virtual environment is set up and activated
- All required tools are installed
- Database schema is created and ready
- Configuration files are in place
- Logging is configured for monitoring

For questions or issues, refer to the logs in the `logs/` directory or check the
database for crawling progress.
