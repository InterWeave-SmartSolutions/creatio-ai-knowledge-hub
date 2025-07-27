#!/usr/bin/env python3
"""
Transcription Status Checker
View processing results, statistics, and quality metrics
"""

import json
import yaml
from pathlib import Path
from datetime import datetime
import argparse

def load_yaml_safe(file_path):
    """Safely load YAML file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except Exception as e:
        return {"error": str(e)}

def load_json_safe(file_path):
    """Safely load JSON file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        return {"error": str(e)}

def format_duration(seconds):
    """Format duration in human readable format"""
    if seconds < 60:
        return f"{seconds:.1f} seconds"
    elif seconds < 3600:
        return f"{seconds/60:.1f} minutes"
    else:
        return f"{seconds/3600:.1f} hours"

def format_size(bytes):
    """Format file size in human readable format"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes < 1024:
            return f"{bytes:.1f} {unit}"
        bytes /= 1024
    return f"{bytes:.1f} TB"

def print_separator(char="=", length=80):
    """Print a separator line"""
    print(char * length)

def check_transcriptions_status(transcriptions_dir):
    """Check status of all transcriptions"""
    trans_path = Path(transcriptions_dir)
    
    if not trans_path.exists():
        print(f"❌ Transcriptions directory not found: {trans_path}")
        return
    
    print(f"📁 Checking transcriptions in: {trans_path.absolute()}")
    print_separator()
    
    # Check directory structure
    subdirs = ['transcripts', 'metadata', 'summaries']
    for subdir in subdirs:
        subdir_path = trans_path / subdir
        if subdir_path.exists():
            count = len(list(subdir_path.glob('*')))
            print(f"✅ {subdir}: {count} files")
        else:
            print(f"❌ {subdir}: directory missing")
    
    print_separator()
    
    # Get file counts by type
    stats = {
        'transcripts': len(list((trans_path / 'transcripts').glob('*.txt'))) if (trans_path / 'transcripts').exists() else 0,
        'full_transcriptions': len(list((trans_path / 'transcripts').glob('*.json'))) if (trans_path / 'transcripts').exists() else 0,
        'subtitles': len(list((trans_path / 'transcripts').glob('*.srt'))) if (trans_path / 'transcripts').exists() else 0,
        'metadata_yaml': len(list((trans_path / 'metadata').glob('*.yaml'))) if (trans_path / 'metadata').exists() else 0,
        'metadata_json': len(list((trans_path / 'metadata').glob('*.json'))) if (trans_path / 'metadata').exists() else 0,
        'basic_summaries': len(list((trans_path / 'summaries').glob('*_summary.json'))) if (trans_path / 'summaries').exists() else 0,
        'enhanced_summaries': len(list((trans_path / 'summaries').glob('*_enhanced_summary.json'))) if (trans_path / 'summaries').exists() else 0,
    }
    
    print("📊 FILE STATISTICS")
    print_separator("-")
    for file_type, count in stats.items():
        icon = "✅" if count > 0 else "❌"
        print(f"{icon} {file_type.replace('_', ' ').title()}: {count}")
    
    # Check processing report
    report_path = trans_path / 'processing_report.json'
    if report_path.exists():
        print_separator()
        print("📋 PROCESSING REPORT")
        print_separator("-")
        
        report = load_json_safe(report_path)
        if 'error' not in report and 'processing_summary' in report:
            summary = report['processing_summary']
            print(f"Total files processed: {summary.get('total_files', 0)}")
            print(f"Successful: {summary.get('successful', 0)}")
            print(f"Failed: {summary.get('failed', 0)}")
            print(f"Success rate: {summary.get('success_rate', '0%')}")
            print(f"Model used: {summary.get('whisper_model', 'unknown')}")
            print(f"Processed at: {summary.get('processed_at', 'unknown')}")
    
    # Check individual video details
    metadata_dir = trans_path / 'metadata'
    if metadata_dir.exists():
        metadata_files = list(metadata_dir.glob('*.yaml'))
        if metadata_files:
            print_separator()
            print("🎥 VIDEO DETAILS")
            print_separator("-")
            
            total_duration = 0
            total_size = 0
            total_words = 0
            quality_stats = {'good': 0, 'poor': 0, 'unknown': 0}
            
            for metadata_file in metadata_files:
                metadata = load_yaml_safe(metadata_file)
                if 'error' not in metadata:
                    video_name = metadata_file.stem.replace('_metadata', '')
                    video_info = metadata.get('video_info', {})
                    processing_info = metadata.get('processing_info', {})
                    content_info = metadata.get('content_metadata', {})
                    
                    duration = video_info.get('duration_seconds', 0)
                    size_mb = video_info.get('file_size_mb', 0)
                    word_count = processing_info.get('word_count', 0)
                    quality = processing_info.get('transcription_quality', 'unknown')
                    language = content_info.get('language', 'unknown')
                    title = content_info.get('title', video_name)
                    
                    total_duration += duration
                    total_size += size_mb
                    total_words += word_count
                    quality_stats[quality] = quality_stats.get(quality, 0) + 1
                    
                    quality_icon = "✅" if quality == 'good' else "⚠️" if quality == 'poor' else "❓"
                    
                    print(f"{quality_icon} {title[:50]:<50} | {format_duration(duration):>12} | {word_count:>6} words | {language}")
            
            print_separator("-")
            print(f"📈 TOTALS:")
            print(f"   Total videos: {len(metadata_files)}")
            print(f"   Total duration: {format_duration(total_duration)}")
            print(f"   Total content size: {total_size:.1f} MB")
            print(f"   Total words transcribed: {total_words:,}")
            print(f"   Quality distribution:")
            for quality, count in quality_stats.items():
                if count > 0:
                    icon = "✅" if quality == 'good' else "⚠️" if quality == 'poor' else "❓"
                    print(f"     {icon} {quality.title()}: {count}")
    
    # Check for common issues
    print_separator()
    print("🔍 HEALTH CHECK")
    print_separator("-")
    
    issues = []
    
    # Check for empty transcripts
    if stats['transcripts'] > 0:
        transcript_dir = trans_path / 'transcripts'
        empty_transcripts = 0
        for transcript_file in transcript_dir.glob('*.txt'):
            if transcript_file.stat().st_size < 10:  # Less than 10 bytes
                empty_transcripts += 1
        
        if empty_transcripts > 0:
            issues.append(f"⚠️  {empty_transcripts} empty or very short transcripts found")
    
    # Check for mismatched file counts
    if stats['transcripts'] != stats['metadata_yaml']:
        issues.append(f"⚠️  Mismatch: {stats['transcripts']} transcripts but {stats['metadata_yaml']} metadata files")
    
    # Check for missing enhanced summaries
    if stats['enhanced_summaries'] < stats['basic_summaries']:
        missing = stats['basic_summaries'] - stats['enhanced_summaries']
        issues.append(f"ℹ️  {missing} videos missing enhanced summaries")
    
    if not issues:
        print("✅ No issues detected - all files appear to be properly generated")
    else:
        for issue in issues:
            print(issue)

def main():
    parser = argparse.ArgumentParser(description="Check transcription processing status")
    parser.add_argument("--dir", default="transcriptions", help="Transcriptions directory (default: transcriptions)")
    parser.add_argument("--detailed", action="store_true", help="Show detailed information for each video")
    
    args = parser.parse_args()
    
    print("🎬 CREATIO ACADEMY TRANSCRIPTION STATUS")
    print(f"Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print_separator("=")
    
    check_transcriptions_status(args.dir)
    
    print_separator("=")
    print("✨ Status check complete!")
    
    if Path(args.dir).exists():
        print(f"\n💡 Tips:")
        print(f"   • Review videos with poor transcription quality")
        print(f"   • Consider reprocessing short videos with larger Whisper models")
        print(f"   • Check log files for processing errors")
        print(f"   • Use metadata files for search and organization")

if __name__ == "__main__":
    main()
