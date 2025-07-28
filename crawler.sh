#!/bin/bash

# Creatio Academy Web Crawler and Downloader
# Crawl all connected web pages, download videos, transcribe content, and organize

set -e

# Base URL for crawling
BASE_URL="https://academy.creatio.com"
OUTPUT_DIR="crawler_output"

# Function to crawl and download all connected pages
crawl_pages() {
    echo "Starting web crawl for $BASE_URL..."
    wget \
        --recursive \
        --no-clobber \
        --page-requisites \
        --html-extension \
        --convert-links \
        --domains academy.creatio.com \
        --restrict-file-names=windows \
        --no-parent \
        -e robots=off \
        --wait=1 \
        --random-wait \
        --directory-prefix="$OUTPUT_DIR" \
        "$BASE_URL"
    echo "Web crawl completed."
}

# Ensure the output directory exists
mkdir -p "$OUTPUT_DIR"

# Start the crawling process
crawl_pages
