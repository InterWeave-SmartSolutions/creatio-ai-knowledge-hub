#!/usr/bin/env python3
"""
Creatio Academy Documentation Scraper
Downloads all missing content from academy.creatio.com/docs/
"""
from utils.cli import base_parser
import argparse, json, sys

import os
import json
import subprocess
import logging
from pathlib import Path
from datetime import datetime
from urllib.parse import urlparse
import time

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('academy_docs_scraper.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class CreatioAcademyDocsScraper:
    def __init__(self):
        # Base directory for downloads
        self.base_dir = Path("/mnt/c/Creatio/knowledge-hub/academy-docs")
        self.base_dir.mkdir(parents=True, exist_ok=True)

        # Load URLs to scrape
        self.urls_file = Path("discovered_8x_urls.json")
        self.scraped_urls_file = self.base_dir / "scraped_urls.json"

        # Track scraped URLs
        self.scraped_urls = self.load_scraped_urls()

        # Statistics
        self.stats = {
            'total_urls': 0,
            'scraped': 0,
            'errors': 0,
            'skipped': 0,
            'start_time': datetime.now()
        }

    def load_scraped_urls(self):
        """Load previously scraped URLs"""
        if self.scraped_urls_file.exists():
            with open(self.scraped_urls_file, 'r') as f:
                return set(json.load(f))
        return set()

    def save_scraped_urls(self):
        """Save scraped URLs to avoid re-downloading"""
        with open(self.scraped_urls_file, 'w') as f:
            json.dump(list(self.scraped_urls), f, indent=2)

    def load_urls(self):
        """Load URLs to scrape"""
        if not self.urls_file.exists():
            logger.error(f"URLs file not found: {self.urls_file}")
            return []

        with open(self.urls_file, 'r') as f:
            data = json.load(f)
            urls = data.get('urls', [])
            logger.info(f"Loaded {len(urls)} URLs to scrape")
            return urls

    def create_dir_for_url(self, url):
        """Create directory structure based on URL"""
        parsed = urlparse(url)
        path_parts = parsed.path.strip('/').split('/')

        # Create subdirectory structure
        dir_path = self.base_dir
        for part in path_parts[:-1]:  # Exclude the last part (filename)
            dir_path = dir_path / part

        dir_path.mkdir(parents=True, exist_ok=True)
        return dir_path

    def download_with_wget(self, url):
        """Download a single URL with wget, preserving directory structure"""
        if url in self.scraped_urls:
            logger.info(f"Skipping already scraped: {url}")
            self.stats['skipped'] += 1
            return True

        logger.info(f"Downloading: {url}")

        try:
            # Create directory for this URL
            url_dir = self.create_dir_for_url(url)

            # Wget command with options
            cmd = [
                'wget',
                '--recursive',                    # Download recursively
                '--level=2',                     # Go 2 levels deep
                '--no-parent',                   # Don't ascend to parent directory
                '--page-requisites',             # Download all page assets
                '--html-extension',              # Save HTML files with .html extension
                '--convert-links',               # Convert links for offline viewing
                '--adjust-extension',            # Adjust extensions based on content-type
                '--restrict-file-names=windows', # Make filenames Windows-compatible
                '--no-clobber',                  # Don't overwrite existing files
                '--timeout=30',                  # Set timeout
                '--tries=3',                     # Number of retries
                '--wait=1',                      # Wait between requests
                '--random-wait',                 # Random wait to avoid detection
                '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                '--accept=html,htm,css,js,json,jpg,jpeg,png,gif,svg,ico,woff,woff2,ttf,eot',
                '--reject=exe,zip,tar,gz',       # Reject binary downloads
                '--directory-prefix=' + str(self.base_dir),
                url
            ]

            # Run wget
            result = subprocess.run(cmd, capture_output=True, text=True)

            if result.returncode == 0:
                logger.info(f"✅ Successfully downloaded: {url}")
                self.scraped_urls.add(url)
                self.stats['scraped'] += 1
                return True
            else:
                logger.error(f"❌ Failed to download {url}: {result.stderr}")
                self.stats['errors'] += 1
                return False

        except Exception as e:
            logger.error(f"❌ Error downloading {url}: {str(e)}")
            self.stats['errors'] += 1
            return False

    def download_with_httrack(self, urls):
        """Alternative: Use HTTrack for bulk downloading"""
        logger.info("Using HTTrack for bulk download...")

        # Create URLs file for HTTrack
        urls_file = self.base_dir / "urls_to_download.txt"
        with open(urls_file, 'w') as f:
            for url in urls:
                if url not in self.scraped_urls:
                    f.write(url + '\n')

        # HTTrack command
        cmd = [
            'httrack',
            '-O', str(self.base_dir),           # Output directory
            '-%v',                               # Verbose
            '-s0',                               # Follow robots.txt
            '-%e0',                              # No external links
            '-A25000000',                        # Max transfer size 25MB
            '-c10',                              # Max connections
            '-F', 'Mozilla/5.0',                 # User agent
            '-%P',                               # No proxy
            '-I0',                               # No index
            '-%L', str(urls_file),               # URLs list file
            '+*.css', '+*.js', '+*.jpg', '+*.jpeg', '+*.png', '+*.gif', '+*.svg',
            '+*.json', '+*.html', '+*.htm'
        ]

        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                logger.info("✅ HTTrack download completed successfully")
                # Mark all URLs as scraped
                for url in urls:
                    self.scraped_urls.add(url)
                return True
            else:
                logger.error(f"❌ HTTrack failed: {result.stderr}")
                return False
        except FileNotFoundError:
            logger.warning("HTTrack not found, falling back to wget")
            return False

    def download_missing_assets(self, url):
        """Download missing CSS, JS, images for a specific page"""
        # This would parse the HTML and download any missing assets
        # For now, wget with --page-requisites should handle this
        pass

    def generate_report(self):
        """Generate download report"""
        end_time = datetime.now()
        duration = end_time - self.stats['start_time']

        report = {
            'download_session': {
                'start_time': self.stats['start_time'].isoformat(),
                'end_time': end_time.isoformat(),
                'duration': str(duration)
            },
            'statistics': {
                'total_urls': self.stats['total_urls'],
                'successfully_scraped': self.stats['scraped'],
                'errors': self.stats['errors'],
                'skipped': self.stats['skipped']
            },
            'output_directory': str(self.base_dir),
            'scraped_urls_file': str(self.scraped_urls_file)
        }

        report_file = self.base_dir / 'download_report.json'
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)

        logger.info(f"📊 Report saved to: {report_file}")
        return report

    def run(self):
        """Main execution method"""
        logger.info("🚀 Starting Creatio Academy Documentation Download...")

        # Load URLs
        urls = self.load_urls()
        if not urls:
            logger.error("No URLs to download")
            return False

        self.stats['total_urls'] = len(urls)

        # Try HTTrack first for bulk download
        if not self.download_with_httrack(urls):
            # Fall back to wget for individual URLs
            logger.info("Using wget for individual URL downloads...")

            for i, url in enumerate(urls, 1):
                logger.info(f"Progress: {i}/{len(urls)}")

                if url in self.scraped_urls:
                    self.stats['skipped'] += 1
                    continue

                self.download_with_wget(url)

                # Save progress periodically
                if i % 10 == 0:
                    self.save_scraped_urls()

                # Be respectful
                time.sleep(1)

        # Save final scraped URLs
        self.save_scraped_urls()

        # Generate report
        report = self.generate_report()

        logger.info("🎉 Download completed!")
        logger.info(f"📊 Stats: {self.stats}")

        return True

if __name__ == "__main__":
    # Preserve existing behavior but add CLI summary for pipeline integration
    try:
        parser = base_parser("Creatio Academy documentation scraper")
    except Exception:
        # Fallback if utils.cli is unavailable in some envs
        parser = argparse.ArgumentParser(description="Creatio Academy documentation scraper")
        parser.add_argument("-c","--config", type=str, default="config.yaml")
        parser.add_argument("--in", dest="input_dir", default=None)
        parser.add_argument("--out", dest="output_dir", default="out")
        parser.add_argument("--limit", type=int, default=0)
        parser.add_argument("--format", choices=["json","ndjson"], default="json")
    args = parser.parse_args()

    # Emit a machine-readable summary on stdout first
    summary = {
        "tool": "academy_docs_scraper",
        "config": str(getattr(args, "config", "config.yaml")),
        "input_dir": str(getattr(args, "input_dir", "") or ""),
        "output_dir": str(getattr(args, "output_dir", "out")),
        "limit": int(getattr(args, "limit", 0)),
        "format": str(getattr(args, "format", "json")),
        "ts": __import__("datetime").datetime.utcnow().isoformat() + "Z"
    }
    print(json.dumps(summary), flush=True)

    # Then execute the original behavior
    scraper = CreatioAcademyDocsScraper()
    scraper.run()
