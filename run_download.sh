#!/bin/bash

# Creatio Academy YouTube Downloader - Shell Wrapper Script
# Provides easy access to download functionality with additional utilities

set -e

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_SCRIPT="$SCRIPT_DIR/youtube_downloader.py"
DEFAULT_OUTPUT_DIR="$SCRIPT_DIR/downloads"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_color() {
    local color=$1
    shift
    echo -e "${color}$*${NC}"
}

# Function to check dependencies
check_dependencies() {
    print_color $BLUE "Checking dependencies..."
    
    # Check if yt-dlp is available
    if ! command -v yt-dlp &> /dev/null; then
        print_color $RED "Error: yt-dlp is not installed or not in PATH"
        print_color $YELLOW "Please install yt-dlp using: pipx install yt-dlp"
        exit 1
    fi
    
    # Check if Python 3 is available
    if ! command -v python3 &> /dev/null; then
        print_color $RED "Error: Python 3 is not installed or not in PATH"
        exit 1
    fi
    
    # Check if the main Python script exists
    if [ ! -f "$PYTHON_SCRIPT" ]; then
        print_color $RED "Error: Main script not found at $PYTHON_SCRIPT"
        exit 1
    fi
    
    print_color $GREEN "✓ All dependencies are satisfied"
}

# Function to show current progress
show_progress() {
    local progress_file="$DEFAULT_OUTPUT_DIR/download_progress.json"
    
    if [ -f "$progress_file" ]; then
        print_color $BLUE "Current Download Progress:"
        print_color $BLUE "========================="
        
        # Extract key metrics from JSON (using Python for reliable JSON parsing)
        python3 -c "
import json
try:
    with open('$progress_file', 'r') as f:
        data = json.load(f)
    
    total = data.get('total_videos', 0)
    downloaded = data.get('downloaded_count', 0)
    failed = data.get('failed_count', 0)
    
    print(f'Total videos: {total}')
    print(f'Downloaded: {downloaded}')
    print(f'Failed: {failed}')
    print(f'Remaining: {total - downloaded - failed}')
    
    if total > 0:
        completion_rate = (downloaded / total) * 100
        print(f'Completion rate: {completion_rate:.1f}%')
        
    print(f'Last updated: {data.get(\"last_updated\", \"Unknown\")}')
        
except Exception as e:
    print(f'Error reading progress file: {e}')
"
    else
        print_color $YELLOW "No progress file found. Downloads haven't started yet."
    fi
}

# Function to start downloads
start_downloads() {
    local output_dir=${1:-$DEFAULT_OUTPUT_DIR}
    local rate_limit=${2:-"1M"}
    local max_retries=${3:-3}
    
    print_color $GREEN "Starting Creatio Academy YouTube downloads..."
    print_color $BLUE "Output directory: $output_dir"
    print_color $BLUE "Rate limit: $rate_limit"
    print_color $BLUE "Max retries: $max_retries"
    
    # Create output directory if it doesn't exist
    mkdir -p "$output_dir"
    
    # Run the Python downloader
    python3 "$PYTHON_SCRIPT" \
        --output-dir "$output_dir" \
        --rate-limit "$rate_limit" \
        --max-retries "$max_retries"
}

# Function to resume downloads
resume_downloads() {
    local output_dir=${1:-$DEFAULT_OUTPUT_DIR}
    
    if [ -f "$output_dir/download_progress.json" ]; then
        print_color $GREEN "Resuming downloads from previous session..."
        start_downloads "$output_dir" "1M" 3
    else
        print_color $YELLOW "No previous session found. Starting fresh downloads..."
        start_downloads "$output_dir" "1M" 3
    fi
}

# Function to clean up partial downloads
cleanup_partials() {
    local output_dir=${1:-$DEFAULT_OUTPUT_DIR}
    
    print_color $YELLOW "Cleaning up partial downloads..."
    
    # Find and remove .part files
    find "$output_dir" -name "*.part" -type f -delete 2>/dev/null || true
    find "$output_dir" -name "*.ytdl" -type f -delete 2>/dev/null || true
    find "$output_dir" -name "*.temp" -type f -delete 2>/dev/null || true
    
    # Find and remove empty directories
    find "$output_dir" -type d -empty -delete 2>/dev/null || true
    
    print_color $GREEN "Cleanup completed"
}

# Function to verify existing downloads
verify_downloads() {
    local output_dir=${1:-$DEFAULT_OUTPUT_DIR}
    
    print_color $BLUE "Verifying existing downloads..."
    
    # Count video files
    local video_count=$(find "$output_dir" -name "*.mp4" -o -name "*.webm" -o -name "*.mkv" -o -name "*.avi" 2>/dev/null | wc -l)
    local info_count=$(find "$output_dir" -name "*.info.json" 2>/dev/null | wc -l)
    local thumb_count=$(find "$output_dir" -name "*.jpg" -o -name "*.png" -o -name "*.webp" 2>/dev/null | wc -l)
    
    print_color $GREEN "Found $video_count video files"
    print_color $GREEN "Found $info_count info.json files"
    print_color $GREEN "Found $thumb_count thumbnail files"
    
    # Show directory structure
    print_color $BLUE "\nDirectory structure:"
    if [ -d "$output_dir" ]; then
        ls -la "$output_dir"
    else
        print_color $YELLOW "Output directory doesn't exist yet"
    fi
}

# Function to show disk usage
show_disk_usage() {
    local output_dir=${1:-$DEFAULT_OUTPUT_DIR}
    
    if [ -d "$output_dir" ]; then
        print_color $BLUE "Disk usage for downloads:"
        du -sh "$output_dir"
        echo
        print_color $BLUE "Breakdown by category:"
        find "$output_dir" -mindepth 1 -maxdepth 1 -type d -exec du -sh {} \; 2>/dev/null | sort -hr || true
    else
        print_color $YELLOW "Output directory doesn't exist yet"
    fi
}

# Function to show help
show_help() {
    echo "Creatio Academy YouTube Downloader"
    echo "=================================="
    echo
    echo "Usage: $0 [COMMAND] [OPTIONS]"
    echo
    echo "Commands:"
    echo "  start [output_dir] [rate_limit] [max_retries]  Start fresh downloads"
    echo "  resume [output_dir]                            Resume previous downloads"
    echo "  progress                                       Show current progress"
    echo "  verify [output_dir]                           Verify existing downloads"
    echo "  cleanup [output_dir]                          Clean up partial files"
    echo "  disk [output_dir]                             Show disk usage"
    echo "  help                                          Show this help"
    echo
    echo "Examples:"
    echo "  $0 start                                       Start with defaults"
    echo "  $0 start ./videos 500K 5                      Custom output, rate limit, retries"
    echo "  $0 resume                                      Resume previous session"
    echo "  $0 progress                                    Check current progress"
    echo
    echo "Default output directory: $DEFAULT_OUTPUT_DIR"
    echo "Default rate limit: 1M (1 MB/s)"
    echo "Default max retries: 3"
}

# Main script logic
main() {
    local command=${1:-help}
    
    case $command in
        "check")
            check_dependencies
            ;;
        "start")
            check_dependencies
            start_downloads "$2" "$3" "$4"
            ;;
        "resume")
            check_dependencies
            resume_downloads "$2"
            ;;
        "progress")
            show_progress
            ;;
        "verify")
            verify_downloads "$2"
            ;;
        "cleanup")
            cleanup_partials "$2"
            ;;
        "disk")
            show_disk_usage "$2"
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

# Run main function with all arguments
main "$@"
