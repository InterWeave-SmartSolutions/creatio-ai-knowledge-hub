#!/usr/bin/env python3
"""
Comprehensive processor for Creatio Developer Course materials integration.
Handles video processing, transcription, PDF extraction, and AI optimization.
"""

import os
import json
import shutil
import hashlib
import subprocess
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime
import logging
from dataclasses import dataclass, asdict

# Import our custom modules
from document_chunker import SemanticDocumentChunker, DocumentChunk
import PyPDF2
import whisper
import cv2
from PIL import Image
import numpy as np

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('developer_course_processing.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


@dataclass
class DeveloperCourseContent:
    """Represents processed developer course content."""
    content_id: str
    content_type: str  # 'video', 'pdf', 'transcript'
    title: str
    source_file: str
    processed_content: Dict[str, Any]
    metadata: Dict[str, Any]
    chunks: List[DocumentChunk]
    processing_timestamp: str


class DeveloperCourseProcessor:
    """
    Comprehensive processor for Developer Course materials.
    """
    
    def __init__(self, source_path: str, output_path: str):
        """
        Initialize the processor.
        
        Args:
            source_path: Path to source Developer Course materials
            output_path: Output path in the knowledge hub
        """
        self.source_path = Path(source_path)
        self.output_path = Path(output_path)
        self.processed_content = []
        
        # Initialize components
        self.chunker = SemanticDocumentChunker(
            max_chunk_size=1000,
            overlap_size=200
        )
        
        # Create output directories
        self.setup_output_directories()
        
        # Initialize Whisper for transcription
        try:
            self.whisper_model = whisper.load_model("base")
            logger.info("Whisper model loaded successfully")
        except Exception as e:
            logger.warning(f"Could not load Whisper model: {e}")
            self.whisper_model = None
    
    def setup_output_directories(self):
        """Create necessary output directories."""
        directories = [
            self.output_path / "developer_course",
            self.output_path / "developer_course" / "videos",
            self.output_path / "developer_course" / "transcripts", 
            self.output_path / "developer_course" / "pdfs",
            self.output_path / "developer_course" / "chunks",
            self.output_path / "developer_course" / "metadata",
            self.output_path / "developer_course" / "summaries",
            self.output_path / "developer_course" / "embeddings"
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            logger.info(f"Created directory: {directory}")
    
    def process_all_materials(self) -> List[DeveloperCourseContent]:
        """Process all Developer Course materials."""
        logger.info("Starting comprehensive processing of Developer Course materials")
        
        if not self.source_path.exists():
            logger.error(f"Source path does not exist: {self.source_path}")
            return []
        
        # Process video files
        self.process_videos()
        
        # Process PDF transcripts
        self.process_pdf_transcripts()
        
        # Process existing transcription files if any
        self.process_existing_transcripts()
        
        # Generate comprehensive metadata
        self.generate_course_metadata()
        
        # Create master index
        self.create_master_index()
        
        logger.info(f"Processing completed. {len(self.processed_content)} items processed.")
        return self.processed_content
    
    def process_videos(self):
        """Process all video files in the Developer Course."""
        video_extensions = ['.mp4', '.avi', '.mov', '.mkv']
        video_files = []
        
        for ext in video_extensions:
            video_files.extend(list(self.source_path.glob(f"*{ext}")))
        
        logger.info(f"Found {len(video_files)} video files to process")
        
        for video_file in sorted(video_files):
            try:
                self.process_single_video(video_file)
            except Exception as e:
                logger.error(f"Error processing video {video_file}: {e}")
    
    def process_single_video(self, video_path: Path):
        """Process a single video file."""
        logger.info(f"Processing video: {video_path.name}")
        
        # Generate content ID
        content_id = self.generate_content_id(video_path.name, "video")
        
        # Copy video to output directory
        output_video_path = self.output_path / "developer_course" / "videos" / video_path.name
        if not output_video_path.exists():
            shutil.copy2(video_path, output_video_path)
            logger.info(f"Copied video to: {output_video_path}")
        
        # Extract metadata
        video_metadata = self.extract_video_metadata(video_path)
        
        # Generate transcript if Whisper is available
        transcript_content = None
        if self.whisper_model:
            transcript_content = self.transcribe_video(video_path)
        
        # Extract key frames
        key_frames = self.extract_key_frames(video_path)
        
        # Create processed content structure
        processed_content = {
            'video_info': video_metadata,
            'transcript': transcript_content,
            'key_frames': key_frames,
            'file_path': str(output_video_path)
        }
        
        # Create chunks from transcript if available
        chunks = []
        if transcript_content:
            chunks = self.chunker.chunk_text_document(
                transcript_content.get('text', ''),
                content_id,
                metadata={
                    'source_type': 'video_transcript',
                    'video_file': video_path.name,
                    'duration': video_metadata.get('duration', 0)
                }
            )
        
        # Create course content object
        course_content = DeveloperCourseContent(
            content_id=content_id,
            content_type='video',
            title=self.extract_title_from_filename(video_path.name),
            source_file=str(video_path),
            processed_content=processed_content,
            metadata=video_metadata,
            chunks=chunks,
            processing_timestamp=datetime.now().isoformat()
        )
        
        self.processed_content.append(course_content)
        
        # Save individual components
        self.save_video_components(course_content)
        
        logger.info(f"Video processing completed: {video_path.name}")
    
    def transcribe_video(self, video_path: Path) -> Optional[Dict[str, Any]]:
        """Transcribe video using Whisper."""
        try:
            logger.info(f"Transcribing video: {video_path.name}")
            
            # Transcribe using Whisper
            result = self.whisper_model.transcribe(str(video_path))
            
            # Process segments for better structure
            segments = []
            if 'segments' in result:
                for segment in result['segments']:
                    segments.append({
                        'start': segment.get('start', 0),
                        'end': segment.get('end', 0),
                        'text': segment.get('text', '').strip()
                    })
            
            transcript_data = {
                'text': result.get('text', ''),
                'language': result.get('language', 'en'),
                'segments': segments,
                'duration': max(seg.get('end', 0) for seg in segments) if segments else 0
            }
            
            logger.info(f"Transcription completed for: {video_path.name}")
            return transcript_data
            
        except Exception as e:
            logger.error(f"Transcription failed for {video_path}: {e}")
            return None
    
    def extract_video_metadata(self, video_path: Path) -> Dict[str, Any]:
        """Extract metadata from video file."""
        metadata = {
            'filename': video_path.name,
            'file_size': video_path.stat().st_size,
            'created_date': datetime.fromtimestamp(video_path.stat().st_ctime).isoformat(),
            'modified_date': datetime.fromtimestamp(video_path.stat().st_mtime).isoformat()
        }
        
        try:
            # Use OpenCV to get basic video info
            cap = cv2.VideoCapture(str(video_path))
            if cap.isOpened():
                fps = cap.get(cv2.CAP_PROP_FPS)
                frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
                duration = frame_count / fps if fps > 0 else 0
                width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                
                metadata.update({
                    'duration': duration,
                    'fps': fps,
                    'frame_count': frame_count,
                    'resolution': {'width': width, 'height': height}
                })
                cap.release()
                
        except Exception as e:
            logger.warning(f"Could not extract video metadata for {video_path}: {e}")
        
        return metadata
    
    def extract_key_frames(self, video_path: Path, num_frames: int = 10) -> List[str]:
        """Extract key frames from video for visual context."""
        key_frames = []
        
        try:
            cap = cv2.VideoCapture(str(video_path))
            if not cap.isOpened():
                return key_frames
            
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            frame_interval = max(1, total_frames // num_frames)
            
            frames_dir = self.output_path / "developer_course" / "videos" / f"{video_path.stem}_frames"
            frames_dir.mkdir(exist_ok=True)
            
            for i in range(0, total_frames, frame_interval):
                cap.set(cv2.CAP_PROP_POS_FRAMES, i)
                ret, frame = cap.read()
                
                if ret:
                    frame_filename = f"frame_{i:06d}.jpg"
                    frame_path = frames_dir / frame_filename
                    cv2.imwrite(str(frame_path), frame)
                    key_frames.append(str(frame_path))
                    
                    if len(key_frames) >= num_frames:
                        break
            
            cap.release()
            logger.info(f"Extracted {len(key_frames)} key frames from {video_path.name}")
            
        except Exception as e:
            logger.warning(f"Could not extract key frames from {video_path}: {e}")
        
        return key_frames
    
    def process_pdf_transcripts(self):
        """Process PDF transcript files."""
        pdf_files = list(self.source_path.glob("transcripts/*.pdf"))
        logger.info(f"Found {len(pdf_files)} PDF transcript files to process")
        
        for pdf_file in sorted(pdf_files):
            try:
                self.process_single_pdf(pdf_file)
            except Exception as e:
                logger.error(f"Error processing PDF {pdf_file}: {e}")
    
    def process_single_pdf(self, pdf_path: Path):
        """Process a single PDF transcript file."""
        logger.info(f"Processing PDF: {pdf_path.name}")
        
        # Generate content ID
        content_id = self.generate_content_id(pdf_path.name, "pdf")
        
        # Copy PDF to output directory
        output_pdf_path = self.output_path / "developer_course" / "pdfs" / pdf_path.name
        if not output_pdf_path.exists():
            shutil.copy2(pdf_path, output_pdf_path)
        
        # Extract text from PDF
        pdf_text = self.extract_pdf_text(pdf_path)
        
        # Create chunks from PDF content
        chunks = self.chunker.chunk_text_document(
            pdf_text,
            content_id,
            metadata={
                'source_type': 'pdf_transcript',
                'pdf_file': pdf_path.name
            }
        )
        
        # Create processed content structure
        processed_content = {
            'text_content': pdf_text,
            'file_path': str(output_pdf_path),
            'page_count': self.get_pdf_page_count(pdf_path)
        }
        
        # Extract metadata
        pdf_metadata = {
            'filename': pdf_path.name,
            'file_size': pdf_path.stat().st_size,
            'created_date': datetime.fromtimestamp(pdf_path.stat().st_ctime).isoformat(),
            'page_count': processed_content['page_count']
        }
        
        # Create course content object
        course_content = DeveloperCourseContent(
            content_id=content_id,
            content_type='pdf',
            title=self.extract_title_from_filename(pdf_path.name),
            source_file=str(pdf_path),
            processed_content=processed_content,
            metadata=pdf_metadata,
            chunks=chunks,
            processing_timestamp=datetime.now().isoformat()
        )
        
        self.processed_content.append(course_content)
        
        # Save components
        self.save_pdf_components(course_content)
        
        logger.info(f"PDF processing completed: {pdf_path.name}")
    
    def extract_pdf_text(self, pdf_path: Path) -> str:
        """Extract text content from PDF file."""
        text_content = ""
        
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                
                for page_num, page in enumerate(pdf_reader.pages):
                    try:
                        page_text = page.extract_text()
                        if page_text.strip():
                            text_content += f"\n\n--- Page {page_num + 1} ---\n\n"
                            text_content += page_text
                    except Exception as e:
                        logger.warning(f"Could not extract text from page {page_num + 1} of {pdf_path}: {e}")
                        
        except Exception as e:
            logger.error(f"Could not extract text from PDF {pdf_path}: {e}")
        
        return text_content.strip()
    
    def get_pdf_page_count(self, pdf_path: Path) -> int:
        """Get the number of pages in a PDF file."""
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                return len(pdf_reader.pages)
        except Exception as e:
            logger.warning(f"Could not get page count for {pdf_path}: {e}")
            return 0
    
    def process_existing_transcripts(self):
        """Process any existing transcript files."""
        transcript_extensions = ['.txt', '.json', '.srt', '.vtt']
        transcript_files = []
        
        for ext in transcript_extensions:
            transcript_files.extend(list(self.source_path.glob(f"*{ext}")))
            transcript_files.extend(list(self.source_path.glob(f"transcripts/*{ext}")))
        
        logger.info(f"Found {len(transcript_files)} existing transcript files")
        
        for transcript_file in transcript_files:
            try:
                self.process_transcript_file(transcript_file)
            except Exception as e:
                logger.error(f"Error processing transcript {transcript_file}: {e}")
    
    def process_transcript_file(self, transcript_path: Path):
        """Process an existing transcript file."""
        logger.info(f"Processing transcript: {transcript_path.name}")
        
        content_id = self.generate_content_id(transcript_path.name, "transcript")
        
        # Read transcript content
        try:
            with open(transcript_path, 'r', encoding='utf-8') as f:
                if transcript_path.suffix == '.json':
                    transcript_data = json.load(f)
                    transcript_text = transcript_data.get('text', str(transcript_data))
                else:
                    transcript_text = f.read()
        except Exception as e:
            logger.error(f"Could not read transcript file {transcript_path}: {e}")
            return
        
        # Create chunks
        chunks = self.chunker.chunk_text_document(
            transcript_text,
            content_id,
            metadata={
                'source_type': 'existing_transcript',
                'transcript_file': transcript_path.name
            }
        )
        
        # Save processed transcript
        output_path = self.output_path / "developer_course" / "transcripts" / transcript_path.name
        if not output_path.exists():
            shutil.copy2(transcript_path, output_path)
        
        course_content = DeveloperCourseContent(
            content_id=content_id,
            content_type='transcript',
            title=self.extract_title_from_filename(transcript_path.name),
            source_file=str(transcript_path),
            processed_content={'text_content': transcript_text, 'file_path': str(output_path)},
            metadata={'filename': transcript_path.name, 'file_size': transcript_path.stat().st_size},
            chunks=chunks,
            processing_timestamp=datetime.now().isoformat()
        )
        
        self.processed_content.append(course_content)
        self.save_transcript_components(course_content)
    
    def save_video_components(self, course_content: DeveloperCourseContent):
        """Save video processing components."""
        content_id = course_content.content_id
        
        # Save transcript if available
        if course_content.processed_content.get('transcript'):
            transcript_file = self.output_path / "developer_course" / "transcripts" / f"{content_id}_transcript.json"
            with open(transcript_file, 'w', encoding='utf-8') as f:
                json.dump(course_content.processed_content['transcript'], f, indent=2)
        
        # Save chunks
        self.save_chunks(course_content.chunks, content_id)
        
        # Save metadata
        self.save_metadata(course_content, content_id)
    
    def save_pdf_components(self, course_content: DeveloperCourseContent):
        """Save PDF processing components."""
        content_id = course_content.content_id
        
        # Save extracted text
        text_file = self.output_path / "developer_course" / "transcripts" / f"{content_id}_text.txt"
        with open(text_file, 'w', encoding='utf-8') as f:
            f.write(course_content.processed_content['text_content'])
        
        # Save chunks
        self.save_chunks(course_content.chunks, content_id)
        
        # Save metadata
        self.save_metadata(course_content, content_id)
    
    def save_transcript_components(self, course_content: DeveloperCourseContent):
        """Save transcript processing components."""
        content_id = course_content.content_id
        
        # Save chunks
        self.save_chunks(course_content.chunks, content_id)
        
        # Save metadata
        self.save_metadata(course_content, content_id)
    
    def save_chunks(self, chunks: List[DocumentChunk], content_id: str):
        """Save document chunks."""
        if not chunks:
            return
        
        chunks_file = self.output_path / "developer_course" / "chunks" / f"{content_id}_chunks.json"
        chunks_data = [asdict(chunk) for chunk in chunks]
        
        with open(chunks_file, 'w', encoding='utf-8') as f:
            json.dump(chunks_data, f, indent=2, ensure_ascii=False)
    
    def save_metadata(self, course_content: DeveloperCourseContent, content_id: str):
        """Save content metadata."""
        metadata_file = self.output_path / "developer_course" / "metadata" / f"{content_id}_metadata.json"
        
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(asdict(course_content), f, indent=2, ensure_ascii=False, default=str)
    
    def generate_course_metadata(self):
        """Generate comprehensive course metadata."""
        logger.info("Generating comprehensive course metadata")
        
        course_metadata = {
            'course_title': 'Creatio Developer Course',
            'processing_date': datetime.now().isoformat(),
            'total_content_items': len(self.processed_content),
            'content_breakdown': {},
            'content_summary': [],
            'course_structure': self.analyze_course_structure()
        }
        
        # Analyze content breakdown
        content_types = {}
        total_chunks = 0
        
        for content in self.processed_content:
            content_type = content.content_type
            content_types[content_type] = content_types.get(content_type, 0) + 1
            total_chunks += len(content.chunks)
            
            course_metadata['content_summary'].append({
                'content_id': content.content_id,
                'title': content.title,
                'type': content.content_type,
                'chunk_count': len(content.chunks),
                'source_file': content.source_file
            })
        
        course_metadata['content_breakdown'] = content_types
        course_metadata['total_chunks'] = total_chunks
        
        # Save course metadata
        metadata_file = self.output_path / "developer_course" / "course_metadata.json"
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(course_metadata, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Course metadata saved: {total_chunks} total chunks from {len(self.processed_content)} content items")
    
    def analyze_course_structure(self) -> Dict[str, Any]:
        """Analyze the overall structure of the course."""
        structure = {
            'sessions': [],
            'topics_covered': set(),
            'learning_progression': []
        }
        
        # Sort content by filename to maintain order
        sorted_content = sorted(self.processed_content, key=lambda x: x.source_file)
        
        for i, content in enumerate(sorted_content):
            session_info = {
                'session_number': i + 1,
                'title': content.title,
                'content_type': content.content_type,
                'estimated_topics': self.extract_topics_from_content(content)
            }
            
            structure['sessions'].append(session_info)
            structure['topics_covered'].update(session_info['estimated_topics'])
        
        structure['topics_covered'] = list(structure['topics_covered'])
        return structure
    
    def extract_topics_from_content(self, content: DeveloperCourseContent) -> List[str]:
        """Extract likely topics from content."""
        topics = []
        
        # Extract from title
        title_keywords = self.extract_keywords_from_text(content.title)
        topics.extend(title_keywords)
        
        # Extract from chunks if available
        if content.chunks:
            for chunk in content.chunks[:3]:  # Check first few chunks
                chunk_keywords = self.extract_keywords_from_text(chunk.content[:500])
                topics.extend(chunk_keywords)
        
        # Remove duplicates and return
        return list(set(topics))
    
    def extract_keywords_from_text(self, text: str) -> List[str]:
        """Extract likely keywords/topics from text."""
        # Common Creatio/development keywords
        creatio_keywords = [
            'creatio', 'schema', 'business process', 'bpm', 'configuration',
            'development', 'customization', 'module', 'package', 'entity',
            'page', 'section', 'lookup', 'detail', 'workflow', 'integration',
            'api', 'web service', 'database', 'sql', 'javascript', 'c#'
        ]
        
        text_lower = text.lower()
        found_keywords = []
        
        for keyword in creatio_keywords:
            if keyword in text_lower:
                found_keywords.append(keyword.title())
        
        return found_keywords
    
    def create_master_index(self):
        """Create a master index for all processed content."""
        logger.info("Creating master index")
        
        master_index = {
            'index_version': '1.0',
            'created_date': datetime.now().isoformat(),
            'total_content_items': len(self.processed_content),
            'content_index': {},
            'chunk_index': {},
            'search_index': {}
        }
        
        all_chunks = []
        
        for content in self.processed_content:
            # Add to content index
            master_index['content_index'][content.content_id] = {
                'title': content.title,
                'type': content.content_type,
                'source_file': content.source_file,
                'chunk_count': len(content.chunks),
                'metadata_file': f"metadata/{content.content_id}_metadata.json",
                'chunks_file': f"chunks/{content.content_id}_chunks.json"
            }
            
            # Add chunks to master chunk index
            for chunk in content.chunks:
                master_index['chunk_index'][chunk.chunk_id] = {
                    'content_id': content.content_id,
                    'chunk_type': chunk.chunk_type,
                    'chunk_index': chunk.chunk_index,
                    'word_count': chunk.word_count,
                    'token_count': chunk.token_count
                }
                
                all_chunks.append(chunk)
        
        # Create search index (simplified)
        for chunk in all_chunks:
            words = chunk.content.lower().split()
            for word in words:
                if len(word) > 3:  # Only index meaningful words
                    if word not in master_index['search_index']:
                        master_index['search_index'][word] = []
                    master_index['search_index'][word].append(chunk.chunk_id)
        
        # Save master index
        index_file = self.output_path / "developer_course" / "master_index.json"
        with open(index_file, 'w', encoding='utf-8') as f:
            json.dump(master_index, f, indent=2, ensure_ascii=False)
        
        # Create RAG-compatible export
        self.create_rag_export(all_chunks)
        
        logger.info(f"Master index created with {len(all_chunks)} chunks")
    
    def create_rag_export(self, chunks: List[DocumentChunk]):
        """Create RAG-compatible export of all content."""
        rag_export_path = self.output_path / "developer_course" / "rag_export.json"
        
        self.chunker.export_chunks_for_rag(chunks, rag_export_path)
        logger.info(f"RAG export created: {rag_export_path}")
    
    def generate_content_id(self, filename: str, content_type: str) -> str:
        """Generate unique content ID."""
        content_string = f"{content_type}_{filename}_{datetime.now().isoformat()}"
        return hashlib.md5(content_string.encode()).hexdigest()[:12]
    
    def extract_title_from_filename(self, filename: str) -> str:
        """Extract a readable title from filename."""
        # Remove extension
        title = Path(filename).stem
        
        # Replace common separators with spaces
        title = title.replace('-', ' ').replace('_', ' ')
        
        # Capitalize words
        title = ' '.join(word.capitalize() for word in title.split())
        
        return title


def main():
    """Main execution function."""
    source_path = "/mnt/c/Users/amago/Desktop/InterWeave Documents/Creatio/Developer Course"
    output_path = "./creatio-academy-db"
    
    processor = DeveloperCourseProcessor(source_path, output_path)
    processed_content = processor.process_all_materials()
    
    print(f"\nProcessing Summary:")
    print(f"Total items processed: {len(processed_content)}")
    
    for content_type in ['video', 'pdf', 'transcript']:
        count = sum(1 for content in processed_content if content.content_type == content_type)
        print(f"{content_type.capitalize()} files: {count}")
    
    total_chunks = sum(len(content.chunks) for content in processed_content)
    print(f"Total chunks created: {total_chunks}")
    
    print(f"\nAll materials have been processed and integrated into the AI knowledge hub!")
    print(f"Output location: {output_path}/developer_course/")


if __name__ == "__main__":
    main()
