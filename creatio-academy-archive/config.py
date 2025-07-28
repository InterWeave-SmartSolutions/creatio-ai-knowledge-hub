"""
Configuration settings for Creatio Academy Archive project
"""

import os
from pathlib import Path

# Base directories
BASE_DIR = Path(__file__).parent
PAGES_DIR = BASE_DIR / "pages"
VIDEOS_DIR = BASE_DIR / "videos"
TRANSCRIPTS_DIR = BASE_DIR / "transcripts"
RESOURCES_DIR = BASE_DIR / "resources"
METADATA_DIR = BASE_DIR / "metadata"
LOGS_DIR = BASE_DIR / "logs"

# Database configuration
DATABASE_PATH = BASE_DIR / "metadata" / "archive.db"

# Scrapy settings
SCRAPY_SETTINGS = {
    'USER_AGENT': 'CreatioAcademyArchiver (+http://www.yourdomain.com)',
    'ROBOTSTXT_OBEY': True,
    'CONCURRENT_REQUESTS': 16,
    'CONCURRENT_REQUESTS_PER_DOMAIN': 8,
    'DOWNLOAD_DELAY': 1,  # 1 second delay between requests
    'RANDOMIZE_DOWNLOAD_DELAY': 0.5,
    'AUTOTHROTTLE_ENABLED': True,
    'AUTOTHROTTLE_START_DELAY': 1,
    'AUTOTHROTTLE_MAX_DELAY': 60,
    'AUTOTHROTTLE_TARGET_CONCURRENCY': 2.0,
    'AUTOTHROTTLE_DEBUG': False,
    'LOG_LEVEL': 'INFO',
}

# Crawling parameters
CRAWL_CONFIG = {
    'start_urls': [
        'https://academy.creatio.com/',
    ],
    'allowed_domains': [
        'academy.creatio.com',
    ],
    'max_depth': 5,
    'respect_robots_txt': True,
    'follow_redirects': True,
    'download_media': True,
    'extract_videos': True,
    'generate_transcripts': True,
}

# Video download settings
VIDEO_CONFIG = {
    'quality': 'best',
    'format': 'mp4',
    'audio_format': 'mp3',
    'max_file_size': '500M',  # Maximum file size for downloads
}

# Whisper transcription settings
WHISPER_CONFIG = {
    'model': 'base',  # Options: tiny, base, small, medium, large
    'language': 'en',
    'task': 'transcribe',
}

# Logging configuration
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'default': {
            'level': 'INFO',
            'formatter': 'standard',
            'class': 'logging.FileHandler',
            'filename': LOGS_DIR / 'archive.log',
            'mode': 'a',
        },
        'console': {
            'level': 'INFO',
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
        }
    },
    'loggers': {
        '': {
            'handlers': ['default', 'console'],
            'level': 'INFO',
            'propagate': False
        }
    }
}

# API Keys and credentials (to be set via environment variables)
API_KEYS = {
    'OPENAI_API_KEY': os.getenv('OPENAI_API_KEY'),
    'YOUTUBE_API_KEY': os.getenv('YOUTUBE_API_KEY'),
    # Add other API keys as needed
}

# File patterns to exclude from crawling
EXCLUDE_PATTERNS = [
    '*.pdf',
    '*.zip',
    '*.exe',
    '*.dmg',
    '*.pkg',
    '*.deb',
    '*.rpm',
]

# Maximum file sizes
MAX_FILE_SIZES = {
    'html': '10M',
    'video': '500M',
    'audio': '100M',
    'image': '50M',
    'document': '100M',
}
