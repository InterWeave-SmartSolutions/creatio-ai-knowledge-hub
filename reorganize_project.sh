#!/bin/bash

# Directories
BASE_DIR="/home/andrewwork/academy.creatio.com"
ARCHIVE_DIR="$BASE_DIR/creatio-academy-archive"
DB_DIR="$BASE_DIR/creatio-academy-db"
VIDEO_DIR="$DB_DIR/videos"
TRANSCRIPTION_DIR="$DB_DIR/videos/transcripts"
SUMMARY_DIR="$DB_DIR/videos/summaries"
SCRIPT_DIR="$BASE_DIR/scripts"
DOCUMENTATION_DIR="$DB_DIR/documentation"
DOWNLOADS_DIR="$BASE_DIR/downloads"

# Create target directories
mkdir -p "$VIDEO_DIR/live_sessions"
mkdir -p "$TRANSCRIPTION_DIR"
mkdir -p "$SUMMARY_DIR"
mkdir -p "$SCRIPT_DIR"
mkdir -p "$DOCUMENTATION_DIR"

# Move video files
echo "Moving video files..."
mv "$ARCHIVE_DIR/videos/general"/* "$VIDEO_DIR/live_sessions/"
mv "$DOWNLOADS_DIR/creatio"* "$VIDEO_DIR/live_sessions/"

# Move transcriptions and summaries
echo "Moving transcriptions and summaries..."
mv "$BASE_DIR/transcriptions/transcripts"/* "$TRANSCRIPTION_DIR/"
mv "$BASE_DIR/transcriptions/summaries"/* "$SUMMARY_DIR/"

# Move scripts
echo "Moving scripts..."
mv "$BASE_DIR"/*.py "$SCRIPT_DIR/"

# Consolidate documentation
echo "Consolidating documentation..."
mv "$ARCHIVE_DIR/pages/raw" "$DOCUMENTATION_DIR/raw"
mv "$ARCHIVE_DIR/pages/metadata" "$DOCUMENTATION_DIR/metadata"

# Clean up
rm -rf "$DOWNLOADS_DIR/creatio - Live"

# Report completion
echo "Reorganization complete."
