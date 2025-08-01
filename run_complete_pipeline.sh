#!/bin/bash

# Master Script for Complete Creatio Academy Content Processing
# This script handles the entire pipeline from web crawling to AI-ready content

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_color() {
    local color=$1
    shift
    echo -e "${color}$*${NC}"
}

print_header() {
    echo
    print_color $BLUE "=============================================="
    print_color $BLUE "$1"
    print_color $BLUE "=============================================="
    echo
}

check_dependencies() {
    print_header "CHECKING DEPENDENCIES"
    
    # Check if virtual environment exists
    if [ ! -d "venv" ]; then
        print_color $YELLOW "Creating Python virtual environment..."
        python3 -m venv venv
    fi
    
    # Check if dependencies are installed
    if ! source venv/bin/activate && python -c "import beautifulsoup4, requests, whisper" 2>/dev/null; then
        print_color $YELLOW "Installing required Python packages..."
        source venv/bin/activate && pip install beautifulsoup4 requests openai-whisper
    fi
    
    # Check for wget
    if ! command -v wget &> /dev/null; then
        print_color $RED "Error: wget is required but not installed"
        exit 1
    fi
    
    # Check for yt-dlp
    if ! command -v yt-dlp &> /dev/null; then
        print_color $YELLOW "Installing yt-dlp..."
        pipx install yt-dlp
    fi
    
    # Check for ffmpeg (required for audio extraction)
    if ! command -v ffmpeg &> /dev/null; then
        print_color $YELLOW "ffmpeg not found, installing..."
        sudo apt update && sudo apt install -y ffmpeg
    fi
    
    print_color $GREEN "✓ All dependencies are ready"
}

run_pipeline() {
    print_header "STARTING COMPLETE CONTENT PIPELINE"
    
    print_color $GREEN "Pipeline will:"
    echo "  1. Crawl all pages from academy.creatio.com"
    echo "  2. Extract all video URLs from pages"
    echo "  3. Download all videos with metadata"
    echo "  4. Transcribe all videos using Whisper AI"
    echo "  5. Convert all pages to markdown"
    echo "  6. Download all resources (PDFs, documents, etc.)"
    echo "  7. Create comprehensive AI-readable index"
    echo "  8. Generate detailed processing report"
    
    print_color $YELLOW "This process may take several hours depending on content volume."
    read -p "Continue? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_color $YELLOW "Pipeline cancelled."
        exit 0
    fi
    
    # Run the content processor
    print_color $BLUE "Starting content processor..."
    source venv/bin/activate && python content_processor.py
    
    print_header "PIPELINE COMPLETED SUCCESSFULLY"
    
    # Show results
    if [ -d "processed_content" ]; then
        print_color $GREEN "Results are available in:"
        echo "  📁 processed_content/"
        echo "    ├── 🎥 videos/              # Downloaded videos"
        echo "    ├── 📝 transcripts/         # Video transcriptions"
        echo "    ├── 📄 pages/               # Web pages as markdown"
        echo "    ├── 📋 resources/           # Downloaded resources"
        echo "    ├── 🔍 ai_content_index.json      # Structured index"
        echo "    ├── 📖 searchable_content.txt     # AI-readable content"
        echo "    └── 📊 processing_report.md       # Detailed report"
        
        # Show summary statistics
        if [ -f "processed_content/processing_report.md" ]; then
            echo
            print_color $BLUE "Quick Summary:"
            grep -E "^\- \*\*" "processed_content/processing_report.md" | head -4
        fi
        
        echo
        print_color $GREEN "Content is now fully processed and AI-ready!"
        print_color $BLUE "Use 'searchable_content.txt' for AI queries and analysis."
    fi
}

show_status() {
    print_header "PROCESSING STATUS"
    
    if [ -f "processed_content/processing_progress.json" ]; then
        print_color $BLUE "Current progress:"
        source venv/bin/activate && python -c "
import json
try:
    with open('processed_content/processing_progress.json', 'r') as f:
        data = json.load(f)
    
    pages = len(data.get('pages', {}))
    videos = len(data.get('videos', {}))
    resources = len(data.get('resources', {}))
    
    print(f'📄 Pages processed: {pages}')
    print(f'🎥 Videos downloaded: {videos}')
    print(f'📋 Resources downloaded: {resources}')
    print(f'⏰ Last updated: {data.get(\"last_updated\", \"Unknown\")}')
except Exception as e:
    print(f'Error reading progress: {e}')
"
    else
        print_color $YELLOW "No processing has started yet."
    fi
    
    if [ -d "crawler_output" ]; then
        html_count=$(find crawler_output -name "*.html" -o -name "*.htm" 2>/dev/null | wc -l)
        print_color $BLUE "Crawled HTML files: $html_count"
    fi
    
    if [ -d "processed_content" ]; then
        echo
        print_color $BLUE "Directory sizes:"
        du -sh processed_content/* 2>/dev/null | sort -hr || true
    fi
}

clean_cache() {
    print_header "CLEANING CACHE"
    
    print_color $YELLOW "This will remove temporary files and cached content."
    read -p "Continue? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_color $YELLOW "Cleanup cancelled."
        exit 0
    fi
    
    # Remove crawler cache
    if [ -d "crawler_output" ]; then
        rm -rf crawler_output
        print_color $GREEN "✓ Removed crawler cache"
    fi
    
    # Remove partial downloads
    find . -name "*.part" -delete 2>/dev/null || true
    find . -name "*.temp" -delete 2>/dev/null || true
    find . -name "*.ytdl" -delete 2>/dev/null || true
    
    print_color $GREEN "✓ Cache cleaned"
}

show_help() {
    echo "Creatio Academy Complete Content Processor"
    echo "=========================================="
    echo
    echo "This tool downloads and processes ALL content from academy.creatio.com:"
    echo "- Crawls every connected web page"
    echo "- Downloads all videos from all pages"
    echo "- Transcribes videos to text using AI"
    echo "- Downloads all resources (PDFs, docs, etc.)"
    echo "- Makes everything AI-readable and searchable"
    echo
    echo "Usage: $0 [COMMAND]"
    echo
    echo "Commands:"
    echo "  run       Start the complete processing pipeline"
    echo "  status    Show current processing status"
    echo "  clean     Clean cache and temporary files"
    echo "  check     Check dependencies and setup"
    echo "  help      Show this help message"
    echo
    echo "Examples:"
    echo "  $0 run      # Process everything"
    echo "  $0 status   # Check progress"
    echo "  $0 clean    # Clean up cache"
    echo
    echo "Output will be organized in 'processed_content/' directory."
}

main() {
    local command=${1:-help}
    
    case $command in
        "run")
            check_dependencies
            run_pipeline
            ;;
        "status")
            show_status
            ;;
        "check")
            check_dependencies
            ;;
        "clean")
            clean_cache
            ;;
        "help"|"--help"|"-h")
            show_help
            ;;
        *)
            print_color $RED "Unknown command: $command"
            echo
            show_help
            exit 1
            ;;
    esac
}

main "$@"
