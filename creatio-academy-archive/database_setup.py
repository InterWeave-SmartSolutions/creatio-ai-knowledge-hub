"""
Database setup script for Creatio Academy Archive project
Creates SQLite database with tables for tracking progress and metadata
"""

import sqlite3
import os
from pathlib import Path
from config import DATABASE_PATH, METADATA_DIR

def create_database():
    """Create the SQLite database and tables"""
    
    # Ensure metadata directory exists
    METADATA_DIR.mkdir(exist_ok=True)
    
    # Connect to database (creates it if it doesn't exist)
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    # Create pages table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT UNIQUE NOT NULL,
            title TEXT,
            content_hash TEXT,
            scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            file_path TEXT,
            status TEXT DEFAULT 'pending',
            error_message TEXT,
            page_size INTEGER,
            content_type TEXT
        )
    ''')
    
    # Create videos table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS videos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT UNIQUE NOT NULL,
            title TEXT,
            description TEXT,
            duration INTEGER,
            file_path TEXT,
            thumbnail_path TEXT,
            downloaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            status TEXT DEFAULT 'pending',
            error_message TEXT,
            file_size INTEGER,
            format TEXT,
            quality TEXT
        )
    ''')
    
    # Create transcripts table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transcripts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            video_id INTEGER,
            video_url TEXT,
            transcript_text TEXT,
            language TEXT DEFAULT 'en',
            confidence_score REAL,
            generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            file_path TEXT,
            status TEXT DEFAULT 'pending',
            error_message TEXT,
            model_used TEXT,
            FOREIGN KEY (video_id) REFERENCES videos (id)
        )
    ''')
    
    # Create resources table (for other files like PDFs, images, etc.)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS resources (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT UNIQUE NOT NULL,
            filename TEXT,
            file_type TEXT,
            file_path TEXT,
            file_size INTEGER,
            downloaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            status TEXT DEFAULT 'pending',
            error_message TEXT,
            mime_type TEXT,
            parent_page_url TEXT
        )
    ''')
    
    # Create crawl_sessions table to track crawling sessions
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS crawl_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_name TEXT,
            start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            end_time TIMESTAMP,
            status TEXT DEFAULT 'running',
            pages_crawled INTEGER DEFAULT 0,
            videos_downloaded INTEGER DEFAULT 0,
            transcripts_generated INTEGER DEFAULT 0,
            resources_downloaded INTEGER DEFAULT 0,
            errors_count INTEGER DEFAULT 0,
            notes TEXT
        )
    ''')
    
    # Create indexes for better performance
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_pages_url ON pages(url)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_pages_status ON pages(status)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_videos_url ON videos(url)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_videos_status ON videos(status)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_transcripts_video_id ON transcripts(video_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_resources_url ON resources(url)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_crawl_sessions_status ON crawl_sessions(status)')
    
    # Commit changes and close connection
    conn.commit()
    conn.close()
    
    print(f"Database created successfully at: {DATABASE_PATH}")
    print("Tables created:")
    print("- pages: Web pages metadata and content")
    print("- videos: Video files metadata and download info")
    print("- transcripts: Video transcriptions and metadata")
    print("- resources: Other downloadable resources")
    print("- crawl_sessions: Crawling session tracking")

def get_database_stats():
    """Get statistics about the database contents"""
    
    if not DATABASE_PATH.exists():
        print("Database does not exist. Run create_database() first.")
        return
    
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    # Get table statistics
    tables = ['pages', 'videos', 'transcripts', 'resources', 'crawl_sessions']
    
    print("\nDatabase Statistics:")
    print("=" * 40)
    
    for table in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        print(f"{table.capitalize()}: {count} records")
    
    conn.close()

if __name__ == "__main__":
    create_database()
    get_database_stats()
