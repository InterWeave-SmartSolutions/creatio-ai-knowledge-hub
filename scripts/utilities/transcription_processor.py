#!/usr/bin/env python3
"""
Video Transcription and Metadata Processor
Comprehensive tool for generating transcriptions and structured metadata for video files
"""

import os
import json
import subprocess
import argparse
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
import whisper
import yaml
from tqdm import tqdm
import re

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('transcription_processor.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class TranscriptionProcessor:
    def __init__(self, whisper_model: str = "base", output_dir: str = "transcriptions"):
        """
        Initialize the transcription processor
        
        Args:
            whisper_model: Whisper model size (tiny, base, small, medium, large)
            output_dir: Directory to store transcriptions and metadata
        """
        self.whisper_model = whisper_model
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Initialize Whisper model
        logger.info(f"Loading Whisper model: {whisper_model}")
        self.model = whisper.load_model(whisper_model)
        
        # Create subdirectories
        (self.output_dir / "transcripts").mkdir(exist_ok=True)
        (self.output_dir / "metadata").mkdir(exist_ok=True)
        (self.output_dir / "summaries").mkdir(exist_ok=True)
        
    def find_video_files(self, directory: str) -> List[Path]:
        """Find all video files in directory and subdirectories"""
        video_extensions = ['.mp4', '.mkv', '.avi', '.mov', '.webm', '.flv', '.m4v']
        video_files = []
        
        for ext in video_extensions:
            video_files.extend(Path(directory).rglob(f'*{ext}'))
            
        logger.info(f"Found {len(video_files)} video files")
        return video_files
    
    def get_video_duration(self, video_path: Path) -> float:
        """Get video duration using ffprobe"""
        try:
            cmd = [
                'ffprobe', '-v', 'error', '-select_streams', 'v:0',
                '-count_packets', '-show_entries', 'stream=duration',
                '-of', 'csv=p=0', str(video_path)
            ]
            result = subprocess.run(cmd, capture_output=True, text=True)
            return float(result.stdout.strip())
        except Exception as e:
            logger.warning(f"Could not get duration for {video_path}: {e}")
            return 0.0
    
    def extract_metadata_from_filename(self, video_path: Path) -> Dict[str, Any]:
        """Extract metadata from filename and directory structure"""
        metadata = {
            "filename": video_path.name,
            "file_path": str(video_path.absolute()),
            "file_size": video_path.stat().st_size,
            "created_date": datetime.fromtimestamp(video_path.stat().st_ctime).isoformat(),
            "modified_date": datetime.fromtimestamp(video_path.stat().st_mtime).isoformat(),
        }
        
        # Try to find corresponding info.json file
        info_json_path = video_path.with_suffix('.info.json')
        if info_json_path.exists():
            try:
                with open(info_json_path, 'r', encoding='utf-8') as f:
                    youtube_data = json.load(f)
                    metadata.update(self.extract_youtube_metadata(youtube_data))
            except Exception as e:
                logger.warning(f"Could not read info.json for {video_path}: {e}")
        
        # Extract information from filename
        filename_info = self.parse_filename(video_path.stem)
        metadata.update(filename_info)
        
        return metadata
    
    def extract_youtube_metadata(self, youtube_data: Dict) -> Dict[str, Any]:
        """Extract relevant metadata from YouTube info.json"""
        metadata = {}
        
        # Map YouTube fields to our metadata structure
        field_mapping = {
            'id': 'video_id',
            'title': 'title',
            'description': 'description',
            'duration': 'duration_seconds',
            'upload_date': 'upload_date',
            'channel': 'channel_name',
            'channel_id': 'channel_id',
            'uploader': 'uploader',
            'view_count': 'view_count',
            'like_count': 'like_count',
            'categories': 'categories',
            'tags': 'tags',
            'webpage_url': 'original_url',
            'thumbnail': 'thumbnail_url',
        }
        
        for youtube_field, our_field in field_mapping.items():
            if youtube_field in youtube_data:
                metadata[our_field] = youtube_data[youtube_field]
        
        # Convert upload_date to ISO format if present
        if 'upload_date' in youtube_data:
            try:
                upload_date = datetime.strptime(youtube_data['upload_date'], '%Y%m%d')
                metadata['upload_date_iso'] = upload_date.isoformat()
            except:
                pass
        
        return metadata
    
    def parse_filename(self, filename: str) -> Dict[str, Any]:
        """Parse filename to extract potential metadata"""
        metadata = {}
        
        # Common patterns in video filenames
        patterns = {
            'youtube_id': r'([a-zA-Z0-9_-]{11})',  # YouTube video IDs
            'date': r'(\d{4}-\d{2}-\d{2})',
            'time': r'(\d{2}:\d{2}:\d{2})',
        }
        
        for key, pattern in patterns.items():
            match = re.search(pattern, filename)
            if match:
                metadata[f'filename_{key}'] = match.group(1)
        
        return metadata
    
    def transcribe_video(self, video_path: Path) -> Dict[str, Any]:
        """Transcribe video using Whisper"""
        logger.info(f"Transcribing {video_path.name}")
        
        try:
            # Transcribe with Whisper
            result = self.model.transcribe(
                str(video_path),
                word_timestamps=True,
                verbose=True
            )
            
            # Process the result
            transcription_data = {
                "text": result["text"],
                "language": result["language"],
                "segments": [],
                "word_count": len(result["text"].split()),
                "processing_time": datetime.now().isoformat(),
            }
            
            # Process segments with timestamps
            for segment in result["segments"]:
                segment_data = {
                    "id": segment["id"],
                    "start": segment["start"],
                    "end": segment["end"],
                    "text": segment["text"].strip(),
                    "words": []
                }
                
                # Add word-level timestamps if available
                if "words" in segment:
                    for word in segment["words"]:
                        word_data = {
                            "word": word["word"],
                            "start": word["start"],
                            "end": word["end"],
                            "probability": word.get("probability", 1.0)
                        }
                        segment_data["words"].append(word_data)
                
                transcription_data["segments"].append(segment_data)
            
            return transcription_data
            
        except Exception as e:
            logger.error(f"Error transcribing {video_path}: {e}")
            return {
                "text": "",
                "language": "unknown",
                "segments": [],
                "error": str(e),
                "processing_time": datetime.now().isoformat(),
            }
    
    def generate_summary(self, transcription_text: str, metadata: Dict) -> Dict[str, Any]:
        """Generate AI-friendly summary and extract key concepts"""
        # For now, we'll create a basic summary
        # In a full implementation, you'd use an LLM like GPT or Claude
        
        words = transcription_text.split()
        word_count = len(words)
        
        # Extract potential key concepts (simplified approach)
        # Remove common stop words and extract frequent terms
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with',
            'by', 'from', 'up', 'about', 'into', 'through', 'during', 'before', 'after',
            'above', 'below', 'between', 'among', 'is', 'are', 'was', 'were', 'be', 'been',
            'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'should',
            'could', 'may', 'might', 'must', 'can', 'this', 'that', 'these', 'those', 'i',
            'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them'
        }
        
        # Clean and count words
        clean_words = []
        for word in words:
            clean_word = re.sub(r'[^\w\s]', '', word.lower())
            if clean_word and clean_word not in stop_words and len(clean_word) > 2:
                clean_words.append(clean_word)
        
        # Get word frequency
        word_freq = {}
        for word in clean_words:
            word_freq[word] = word_freq.get(word, 0) + 1
        
        # Get top keywords
        top_keywords = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:20]
        
        # Generate basic summary
        sentences = re.split(r'[.!?]+', transcription_text)
        summary_sentences = [s.strip() for s in sentences[:3] if s.strip()]
        
        summary_data = {
            "brief_summary": ' '.join(summary_sentences),
            "word_count": word_count,
            "estimated_reading_time": max(1, word_count // 200),  # ~200 WPM reading speed
            "key_concepts": [word for word, freq in top_keywords[:10]],
            "top_keywords": dict(top_keywords[:10]),
            "language_detected": metadata.get('language', 'unknown'),
            "topics": self.extract_topics(clean_words),
            "generated_at": datetime.now().isoformat(),
        }
        
        return summary_data
    
    def extract_topics(self, words: List[str]) -> List[str]:
        """Extract potential topics from the word list"""
        # Common business/CRM/BPM related terms
        topic_keywords = {
            'crm': ['crm', 'customer', 'relationship', 'management', 'sales', 'lead', 'opportunity'],
            'bpm': ['bpm', 'business', 'process', 'workflow', 'automation', 'management'],
            'creatio': ['creatio', 'platform', 'application', 'system', 'software'],
            'tutorial': ['tutorial', 'guide', 'how', 'demo', 'demonstration', 'training'],
            'configuration': ['configuration', 'setup', 'configure', 'settings', 'customization'],
            'integration': ['integration', 'api', 'connector', 'sync', 'synchronization'],
            'reporting': ['report', 'dashboard', 'analytics', 'data', 'visualization'],
            'development': ['development', 'code', 'programming', 'developer', 'custom'],
        }
        
        detected_topics = []
        for topic, keywords in topic_keywords.items():
            if any(keyword in words for keyword in keywords):
                detected_topics.append(topic)
        
        return detected_topics
    
    def create_structured_metadata(self, video_path: Path, transcription: Dict, metadata: Dict, summary: Dict) -> Dict[str, Any]:
        """Create comprehensive structured metadata"""
        
        structured_metadata = {
            "video_info": {
                "file_path": str(video_path.absolute()),
                "filename": video_path.name,
                "file_size_bytes": video_path.stat().st_size,
                "file_size_mb": round(video_path.stat().st_size / (1024 * 1024), 2),
                "duration_seconds": metadata.get('duration_seconds', self.get_video_duration(video_path)),
                "created_date": metadata.get('created_date'),
                "modified_date": metadata.get('modified_date'),
            },
            "content_metadata": {
                "title": metadata.get('title', video_path.stem),
                "description": metadata.get('description', ''),
                "language": transcription.get('language', 'unknown'),
                "categories": metadata.get('categories', []),
                "tags": metadata.get('tags', []),
                "topics": summary.get('topics', []),
                "key_concepts": summary.get('key_concepts', []),
            },
            "source_info": {
                "channel_name": metadata.get('channel_name', ''),
                "uploader": metadata.get('uploader', ''),
                "upload_date": metadata.get('upload_date_iso', ''),
                "original_url": metadata.get('original_url', ''),
                "video_id": metadata.get('video_id', ''),
            },
            "processing_info": {
                "transcription_model": self.whisper_model,
                "processed_at": datetime.now().isoformat(),
                "word_count": summary.get('word_count', 0),
                "estimated_duration_minutes": round((metadata.get('duration_seconds', 0) / 60), 2),
                "transcription_quality": "good" if len(transcription.get('text', '')) > 100 else "poor",
            },
            "ai_analysis": {
                "summary": summary.get('brief_summary', ''),
                "key_topics": summary.get('topics', []),
                "top_keywords": summary.get('top_keywords', {}),
                "estimated_reading_time_minutes": summary.get('estimated_reading_time', 0),
            }
        }
        
        return structured_metadata
    
    def save_transcription_files(self, video_path: Path, transcription: Dict, metadata: Dict, summary: Dict):
        """Save all transcription and metadata files"""
        base_name = video_path.stem
        
        # Save full transcription as JSON
        transcription_file = self.output_dir / "transcripts" / f"{base_name}_transcription.json"
        with open(transcription_file, 'w', encoding='utf-8') as f:
            json.dump(transcription, f, indent=2, ensure_ascii=False)
        
        # Save plain text transcription
        text_file = self.output_dir / "transcripts" / f"{base_name}_transcript.txt"
        with open(text_file, 'w', encoding='utf-8') as f:
            f.write(transcription.get('text', ''))
        
        # Save SRT subtitle file
        srt_file = self.output_dir / "transcripts" / f"{base_name}_subtitles.srt"
        self.create_srt_file(transcription, srt_file)
        
        # Save comprehensive metadata
        structured_metadata = self.create_structured_metadata(video_path, transcription, metadata, summary)
        
        metadata_file = self.output_dir / "metadata" / f"{base_name}_metadata.yaml"
        with open(metadata_file, 'w', encoding='utf-8') as f:
            yaml.dump(structured_metadata, f, default_flow_style=False, allow_unicode=True)
        
        metadata_json = self.output_dir / "metadata" / f"{base_name}_metadata.json"
        with open(metadata_json, 'w', encoding='utf-8') as f:
            json.dump(structured_metadata, f, indent=2, ensure_ascii=False)
        
        # Save summary
        summary_file = self.output_dir / "summaries" / f"{base_name}_summary.json"
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Saved all files for {base_name}")
    
    def create_srt_file(self, transcription: Dict, srt_path: Path):
        """Create SRT subtitle file from transcription"""
        with open(srt_path, 'w', encoding='utf-8') as f:
            for i, segment in enumerate(transcription.get('segments', []), 1):
                start_time = self.seconds_to_srt_time(segment['start'])
                end_time = self.seconds_to_srt_time(segment['end'])
                
                f.write(f"{i}\n")
                f.write(f"{start_time} --> {end_time}\n")
                f.write(f"{segment['text'].strip()}\n\n")
    
    def seconds_to_srt_time(self, seconds: float) -> str:
        """Convert seconds to SRT time format"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millisecs = int((seconds % 1) * 1000)
        return f"{hours:02d}:{minutes:02d}:{secs:02d},{millisecs:03d}"
    
    def process_video(self, video_path: Path) -> bool:
        """Process a single video file"""
        try:
            logger.info(f"Processing {video_path}")
            
            # Check if already processed
            base_name = video_path.stem
            metadata_file = self.output_dir / "metadata" / f"{base_name}_metadata.yaml"
            if metadata_file.exists():
                logger.info(f"Already processed {video_path}, skipping...")
                return True
            
            # Extract metadata
            metadata = self.extract_metadata_from_filename(video_path)
            
            # Transcribe video
            transcription = self.transcribe_video(video_path)
            
            # Generate summary
            summary = self.generate_summary(transcription.get('text', ''), transcription)
            
            # Save all files
            self.save_transcription_files(video_path, transcription, metadata, summary)
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to process {video_path}: {e}")
            return False
    
    def process_directory(self, directory: str, max_files: Optional[int] = None):
        """Process all video files in a directory"""
        video_files = self.find_video_files(directory)
        
        if max_files:
            video_files = video_files[:max_files]
        
        successful = 0
        failed = 0
        
        for video_path in tqdm(video_files, desc="Processing videos"):
            if self.process_video(video_path):
                successful += 1
            else:
                failed += 1
        
        logger.info(f"Processing complete: {successful} successful, {failed} failed")
        
        # Generate summary report
        self.generate_processing_report(successful, failed, len(video_files))
    
    def generate_processing_report(self, successful: int, failed: int, total: int):
        """Generate a processing summary report"""
        report = {
            "processing_summary": {
                "total_files": total,
                "successful": successful,
                "failed": failed,
                "success_rate": f"{(successful/total*100):.1f}%" if total > 0 else "0%",
                "processed_at": datetime.now().isoformat(),
                "whisper_model": self.whisper_model,
            }
        }
        
        report_file = self.output_dir / "processing_report.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        logger.info(f"Processing report saved to {report_file}")

def main():
    parser = argparse.ArgumentParser(description="Process videos for transcription and metadata extraction")
    parser.add_argument("directory", help="Directory containing video files")
    parser.add_argument("--model", default="base", choices=["tiny", "base", "small", "medium", "large"], 
                       help="Whisper model size")
    parser.add_argument("--output", default="transcriptions", help="Output directory")
    parser.add_argument("--max-files", type=int, help="Maximum number of files to process")
    
    args = parser.parse_args()
    
    processor = TranscriptionProcessor(whisper_model=args.model, output_dir=args.output)
    processor.process_directory(args.directory, max_files=args.max_files)

if __name__ == "__main__":
    main()
