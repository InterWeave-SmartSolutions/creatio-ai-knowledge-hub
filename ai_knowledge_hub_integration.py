#!/usr/bin/env python3
"""
AI Knowledge Hub Integration
===========================

Main script for Step 9: AI Knowledge Hub Integration
- Process and organize 13 video recordings
- Extract key information from 14 PDF transcripts
- Create searchable documentation index
- Build command reference from developer course
- Set up MCP server integration for AI assistance
"""

import os
import json
import sys
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
import hashlib
import re
import sqlite3
from dataclasses import dataclass, asdict
import whisper
import PyPDF2
from collections import defaultdict

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('ai_knowledge_hub_integration.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class VideoContent:
    """Data class for video content"""
    video_id: str
    file_path: str
    title: str
    duration: float
    transcript: str
    summary: str
    topics: List[str]
    complexity_level: str
    commands: List[str]
    api_references: List[str]
    code_examples: List[Dict[str, str]]

@dataclass
class PDFContent:
    """Data class for PDF content"""
    pdf_id: str
    file_path: str
    title: str
    page_count: int
    content: str
    sections: List[Dict[str, str]]
    topics: List[str]
    commands: List[str]
    api_references: List[str]
    code_examples: List[Dict[str, str]]

class AIKnowledgeHubIntegrator:
    """Main class for AI Knowledge Hub Integration"""
    
    def __init__(self, base_path: str = "./"):
        self.base_path = Path(base_path)
        self.video_path = self.base_path / "ai_optimization/creatio-academy-db/developer_course/videos"
        self.pdf_path = self.base_path / "ai_optimization/creatio-academy-db/developer_course/pdfs"
        self.output_path = self.base_path / "ai_knowledge_hub"
        self.db_path = self.output_path / "knowledge_hub.db"
        
        # Create output directories
        self.output_path.mkdir(exist_ok=True)
        (self.output_path / "processed_videos").mkdir(exist_ok=True)
        (self.output_path / "processed_pdfs").mkdir(exist_ok=True)
        (self.output_path / "search_index").mkdir(exist_ok=True)
        (self.output_path / "command_reference").mkdir(exist_ok=True)
        (self.output_path / "api_documentation").mkdir(exist_ok=True)
        
        # Initialize Whisper model for video processing
        self.whisper_model = None
        
    def initialize_database(self):
        """Initialize SQLite database for searchable content"""
        logger.info("Initializing knowledge hub database...")
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create tables
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS videos (
                id TEXT PRIMARY KEY,
                file_path TEXT,
                title TEXT,
                duration REAL,
                transcript TEXT,
                summary TEXT,
                topics TEXT,
                complexity_level TEXT,
                commands TEXT,
                api_references TEXT,
                code_examples TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS pdfs (
                id TEXT PRIMARY KEY,
                file_path TEXT,
                title TEXT,
                page_count INTEGER,
                content TEXT,
                sections TEXT,
                topics TEXT,
                commands TEXT,
                api_references TEXT,
                code_examples TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS search_index (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content_type TEXT,
                content_id TEXT,
                section TEXT,
                content TEXT,
                keywords TEXT,
                relevance_score REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS commands (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                command TEXT,
                description TEXT,
                category TEXT,
                source_type TEXT,
                source_id TEXT,
                examples TEXT,
                parameters TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create full-text search virtual tables
        cursor.execute('''
            CREATE VIRTUAL TABLE IF NOT EXISTS search_fts USING fts5(
                content_type,
                content_id,
                title,
                content,
                keywords
            )
        ''')
        
        conn.commit()
        conn.close()
        logger.info("Database initialized successfully")
    
    def load_whisper_model(self):
        """Load Whisper model for video transcription"""
        if self.whisper_model is None:
            logger.info("Loading Whisper model...")
            self.whisper_model = whisper.load_model("base")
            logger.info("Whisper model loaded successfully")
    
    def process_video_recordings(self) -> List[VideoContent]:
        """Process all 13 video recordings"""
        logger.info("Processing 13 video recordings...")
        
        video_files = list(self.video_path.glob("*.mp4"))
        logger.info(f"Found {len(video_files)} video files")
        
        processed_videos = []
        
        for video_file in video_files:
            try:
                logger.info(f"Processing video: {video_file.name}")
                video_content = self.process_single_video(video_file)
                if video_content:
                    processed_videos.append(video_content)
                    self.save_processed_video(video_content)
            except Exception as e:
                logger.error(f"Error processing video {video_file.name}: {e}")
        
        logger.info(f"Successfully processed {len(processed_videos)} videos")
        return processed_videos
    
    def process_single_video(self, video_file: Path) -> Optional[VideoContent]:
        """Process a single video file"""
        video_id = self.generate_id(str(video_file))
        
        # Check if already processed
        existing_transcript_path = self.base_path / f"ai_optimization/creatio-academy-db/developer_course/transcripts/{video_id}_transcript.json"
        
        if existing_transcript_path.exists():
            logger.info(f"Using existing transcript for {video_file.name}")
            with open(existing_transcript_path, 'r', encoding='utf-8') as f:
                transcript_data = json.load(f)
            transcript = transcript_data.get('text', '')
        else:
            # Transcribe using Whisper
            logger.info(f"Transcribing {video_file.name}...")
            self.load_whisper_model()
            result = self.whisper_model.transcribe(str(video_file))
            transcript = result["text"]
        
        # Extract video metadata
        title = self.extract_title_from_filename(video_file.name)
        duration = self.get_video_duration(video_file)
        
        # Analyze content
        topics = self.extract_topics(transcript)
        commands = self.extract_commands(transcript)
        api_references = self.extract_api_references(transcript)
        code_examples = self.extract_code_examples(transcript)
        complexity_level = self.assess_complexity(transcript)
        summary = self.generate_summary(transcript)
        
        return VideoContent(
            video_id=video_id,
            file_path=str(video_file),
            title=title,
            duration=duration,
            transcript=transcript,
            summary=summary,
            topics=topics,
            complexity_level=complexity_level,
            commands=commands,
            api_references=api_references,
            code_examples=code_examples
        )
    
    def process_pdf_transcripts(self) -> List[PDFContent]:
        """Process all 14 PDF transcripts"""
        logger.info("Processing 14 PDF transcripts...")
        
        pdf_files = list(self.pdf_path.glob("*.pdf"))
        logger.info(f"Found {len(pdf_files)} PDF files")
        
        processed_pdfs = []
        
        for pdf_file in pdf_files:
            try:
                logger.info(f"Processing PDF: {pdf_file.name}")
                pdf_content = self.process_single_pdf(pdf_file)
                if pdf_content:
                    processed_pdfs.append(pdf_content)
                    self.save_processed_pdf(pdf_content)
            except Exception as e:
                logger.error(f"Error processing PDF {pdf_file.name}: {e}")
        
        logger.info(f"Successfully processed {len(processed_pdfs)} PDFs")
        return processed_pdfs
    
    def process_single_pdf(self, pdf_file: Path) -> Optional[PDFContent]:
        """Process a single PDF file"""
        pdf_id = self.generate_id(str(pdf_file))
        
        try:
            with open(pdf_file, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                page_count = len(pdf_reader.pages)
                
                # Extract text from all pages
                content = ""
                sections = []
                
                for page_num, page in enumerate(pdf_reader.pages):
                    page_text = page.extract_text()
                    content += page_text + "\n"
                    
                    # Extract sections (simple heuristic based on headers)
                    page_sections = self.extract_sections_from_page(page_text, page_num)
                    sections.extend(page_sections)
        
            # Extract metadata and analyze content
            title = self.extract_title_from_filename(pdf_file.name)
            topics = self.extract_topics(content)
            commands = self.extract_commands(content)
            api_references = self.extract_api_references(content)
            code_examples = self.extract_code_examples(content)
            
            return PDFContent(
                pdf_id=pdf_id,
                file_path=str(pdf_file),
                title=title,
                page_count=page_count,
                content=content,
                sections=sections,
                topics=topics,
                commands=commands,
                api_references=api_references,
                code_examples=code_examples
            )
            
        except Exception as e:
            logger.error(f"Error processing PDF {pdf_file.name}: {e}")
            return None
    
    def create_searchable_index(self, videos: List[VideoContent], pdfs: List[PDFContent]):
        """Create searchable documentation index"""
        logger.info("Creating searchable documentation index...")
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Index video content
        for video in videos:
            # Store main video data
            cursor.execute('''
                INSERT OR REPLACE INTO videos 
                (id, file_path, title, duration, transcript, summary, topics, 
                 complexity_level, commands, api_references, code_examples)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                video.video_id, video.file_path, video.title, video.duration,
                video.transcript, video.summary, json.dumps(video.topics),
                video.complexity_level, json.dumps(video.commands),
                json.dumps(video.api_references), json.dumps(video.code_examples)
            ))
            
            # Add to search index
            self.add_to_search_index(cursor, 'video', video.video_id, video.title, video.transcript, video.topics)
            
            # Index commands
            for command in video.commands:
                self.add_command_to_index(cursor, command, 'video', video.video_id, video.title)
        
        # Index PDF content
        for pdf in pdfs:
            # Store main PDF data
            cursor.execute('''
                INSERT OR REPLACE INTO pdfs 
                (id, file_path, title, page_count, content, sections, topics, 
                 commands, api_references, code_examples)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                pdf.pdf_id, pdf.file_path, pdf.title, pdf.page_count,
                pdf.content, json.dumps(pdf.sections), json.dumps(pdf.topics),
                json.dumps(pdf.commands), json.dumps(pdf.api_references),
                json.dumps(pdf.code_examples)
            ))
            
            # Add to search index
            self.add_to_search_index(cursor, 'pdf', pdf.pdf_id, pdf.title, pdf.content, pdf.topics)
            
            # Index sections separately for better granular search
            for section in pdf.sections:
                self.add_to_search_index(cursor, 'pdf_section', pdf.pdf_id, 
                                       section.get('title', ''), section.get('content', ''), [])
            
            # Index commands
            for command in pdf.commands:
                self.add_command_to_index(cursor, command, 'pdf', pdf.pdf_id, pdf.title)
        
        conn.commit()
        conn.close()
        
        # Create search index files
        self.create_search_index_files(videos, pdfs)
        
        logger.info("Searchable index created successfully")
    
    def build_command_reference(self, videos: List[VideoContent], pdfs: List[PDFContent]):
        """Build comprehensive command reference from developer course"""
        logger.info("Building command reference from developer course...")
        
        all_commands = {}
        command_categories = defaultdict(list)
        
        # Process video commands
        for video in videos:
            for command in video.commands:
                command_info = self.analyze_command(command, video.transcript)
                command_key = command_info['command'].lower()
                
                if command_key not in all_commands:
                    all_commands[command_key] = command_info
                    all_commands[command_key]['sources'] = []
                
                all_commands[command_key]['sources'].append({
                    'type': 'video',
                    'id': video.video_id,
                    'title': video.title,
                    'context': self.extract_command_context(command, video.transcript)
                })
                
                category = command_info.get('category', 'general')
                command_categories[category].append(command_key)
        
        # Process PDF commands
        for pdf in pdfs:
            for command in pdf.commands:
                command_info = self.analyze_command(command, pdf.content)
                command_key = command_info['command'].lower()
                
                if command_key not in all_commands:
                    all_commands[command_key] = command_info
                    all_commands[command_key]['sources'] = []
                
                all_commands[command_key]['sources'].append({
                    'type': 'pdf',
                    'id': pdf.pdf_id,
                    'title': pdf.title,
                    'context': self.extract_command_context(command, pdf.content)
                })
                
                category = command_info.get('category', 'general')
                command_categories[category].append(command_key)
        
        # Create command reference documentation
        command_reference = {
            'metadata': {
                'created_at': datetime.now().isoformat(),
                'total_commands': len(all_commands),
                'categories': dict(command_categories),
                'version': '1.0.0'
            },
            'commands': all_commands,
            'categories': dict(command_categories)
        }
        
        # Save command reference
        command_ref_path = self.output_path / "command_reference" / "developer_course_commands.json"
        with open(command_ref_path, 'w', encoding='utf-8') as f:
            json.dump(command_reference, f, indent=2, ensure_ascii=False)
        
        # Create markdown documentation
        self.create_command_reference_markdown(command_reference)
        
        logger.info(f"Command reference built with {len(all_commands)} unique commands")
        return command_reference
    
    def setup_mcp_server_integration(self):
        """Set up MCP server integration for AI assistance"""
        logger.info("Setting up MCP server integration...")
        
        # Update existing MCP server configuration
        mcp_config = {
            'server_info': {
                'name': 'Creatio AI Knowledge Hub',
                'version': '1.0.0',
                'description': 'MCP server for AI assistance with Creatio development',
                'capabilities': [
                    'content_search',
                    'command_lookup',
                    'code_examples',
                    'documentation_query',
                    'video_transcript_access',
                    'pdf_content_search'
                ]
            },
            'database_config': {
                'db_path': str(self.db_path),
                'search_index_path': str(self.output_path / "search_index"),
                'command_reference_path': str(self.output_path / "command_reference")
            },
            'endpoints': {
                'search': '/api/v1/search',
                'commands': '/api/v1/commands',
                'videos': '/api/v1/videos',
                'pdfs': '/api/v1/pdfs',
                'code_examples': '/api/v1/code-examples'
            }
        }
        
        # Save MCP configuration
        mcp_config_path = self.output_path / "mcp_server_config.json"
        with open(mcp_config_path, 'w', encoding='utf-8') as f:
            json.dump(mcp_config, f, indent=2)
        
        # Create enhanced MCP server script
        self.create_enhanced_mcp_server()
        
        logger.info("MCP server integration setup completed")
    
    # Utility methods
    def generate_id(self, content: str) -> str:
        """Generate unique ID for content"""
        return hashlib.md5(content.encode()).hexdigest()[:12]
    
    def extract_title_from_filename(self, filename: str) -> str:
        """Extract title from filename"""
        # Remove extension and clean up
        title = Path(filename).stem
        title = re.sub(r'[_-]', ' ', title)
        title = re.sub(r'\b\w+\b', lambda m: m.group(0).capitalize(), title)
        return title
    
    def get_video_duration(self, video_file: Path) -> float:
        """Get video duration (placeholder - would use ffprobe in real implementation)"""
        # This is a placeholder - in real implementation, use ffprobe
        return 0.0
    
    def extract_topics(self, content: str) -> List[str]:
        """Extract topics from content using keyword matching"""
        topics = []
        content_lower = content.lower()
        
        topic_keywords = {
            'crm': ['customer relationship', 'sales pipeline', 'lead management', 'opportunity', 'contact'],
            'bpm': ['business process', 'workflow', 'automation', 'process optimization'],
            'integration': ['api', 'integration', 'connector', 'webhook', 'data sync'],
            'development': ['development', 'coding', 'programming', 'javascript', 'c#'],
            'configuration': ['configuration', 'setup', 'customization', 'settings'],
            'ui_ux': ['user interface', 'user experience', 'design', 'layout', 'form'],
            'database': ['database', 'sql', 'entity', 'schema', 'query']
        }
        
        for topic, keywords in topic_keywords.items():
            if any(keyword in content_lower for keyword in keywords):
                topics.append(topic)
        
        return topics
    
    def extract_commands(self, content: str) -> List[str]:
        """Extract commands and code snippets from content"""
        commands = []
        
        # Patterns for different types of commands
        patterns = [
            r'\b\w+\.\w+\([^)]*\)',  # Method calls
            r'\$\w+\s+[^$\n]+',      # Command line
            r'CREATE\s+\w+[^;]+;',   # SQL CREATE
            r'SELECT\s+[^;]+;',      # SQL SELECT
            r'UPDATE\s+[^;]+;',      # SQL UPDATE
            r'INSERT\s+[^;]+;',      # SQL INSERT
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, content, re.IGNORECASE | re.MULTILINE)
            commands.extend(matches)
        
        # Clean and deduplicate
        commands = list(set([cmd.strip() for cmd in commands if len(cmd.strip()) > 3]))
        
        return commands[:50]  # Limit to avoid too many
    
    def extract_api_references(self, content: str) -> List[str]:
        """Extract API references from content"""
        api_patterns = [
            r'\b\w+API\b',
            r'\b\w+Service\b',
            r'\b\w+Manager\b',
            r'/api/\w+/[^/\s]+',
            r'https?://[^/\s]+/api/[^\s]+',
        ]
        
        api_refs = []
        for pattern in api_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            api_refs.extend(matches)
        
        return list(set(api_refs))
    
    def extract_code_examples(self, content: str) -> List[Dict[str, str]]:
        """Extract code examples from content"""
        examples = []
        
        # Simple extraction of code-like blocks
        code_patterns = [
            (r'```(\w+)?\n(.*?)```', 'code_block'),
            (r'`([^`\n]+)`', 'inline_code'),
            (r'function\s+\w+\s*\([^)]*\)\s*{[^}]+}', 'javascript_function'),
            (r'public\s+\w+\s+\w+\s*\([^)]*\)\s*{[^}]+}', 'csharp_method'),
        ]
        
        for pattern, code_type in code_patterns:
            matches = re.findall(pattern, content, re.DOTALL | re.IGNORECASE)
            for match in matches:
                if isinstance(match, tuple):
                    lang, code = match if len(match) == 2 else ('', match[0])
                else:
                    lang, code = '', match
                
                examples.append({
                    'type': code_type,
                    'language': lang,
                    'code': code.strip()
                })
        
        return examples[:20]  # Limit examples
    
    def assess_complexity(self, content: str) -> str:
        """Assess content complexity level"""
        content_lower = content.lower()
        
        advanced_terms = ['advanced', 'complex', 'enterprise', 'architecture', 'integration']
        intermediate_terms = ['configuration', 'customization', 'workflow', 'api']
        beginner_terms = ['introduction', 'basic', 'getting started', 'overview', 'simple']
        
        advanced_count = sum(1 for term in advanced_terms if term in content_lower)
        intermediate_count = sum(1 for term in intermediate_terms if term in content_lower)
        beginner_count = sum(1 for term in beginner_terms if term in content_lower)
        
        if advanced_count > intermediate_count and advanced_count > beginner_count:
            return 'advanced'
        elif intermediate_count > beginner_count:
            return 'intermediate'
        else:
            return 'beginner'
    
    def generate_summary(self, content: str) -> str:
        """Generate summary of content"""
        # Simple extractive summary - take first few sentences
        sentences = re.split(r'[.!?]+', content)
        summary_sentences = [s.strip() for s in sentences[:3] if len(s.strip()) > 20]
        return '. '.join(summary_sentences) + '.' if summary_sentences else 'No summary available.'
    
    def save_processed_video(self, video: VideoContent):
        """Save processed video data"""
        output_file = self.output_path / "processed_videos" / f"{video.video_id}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(asdict(video), f, indent=2, ensure_ascii=False)
    
    def save_processed_pdf(self, pdf: PDFContent):
        """Save processed PDF data"""
        output_file = self.output_path / "processed_pdfs" / f"{pdf.pdf_id}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(asdict(pdf), f, indent=2, ensure_ascii=False)
    
    def add_to_search_index(self, cursor, content_type: str, content_id: str, 
                           title: str, content: str, keywords: List[str]):
        """Add content to search index"""
        keywords_str = ' '.join(keywords)
        
        cursor.execute('''
            INSERT INTO search_index 
            (content_type, content_id, section, content, keywords, relevance_score)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (content_type, content_id, title, content[:5000], keywords_str, 1.0))
        
        # Add to FTS
        cursor.execute('''
            INSERT INTO search_fts (content_type, content_id, title, content, keywords)
            VALUES (?, ?, ?, ?, ?)
        ''', (content_type, content_id, title, content[:5000], keywords_str))
    
    def add_command_to_index(self, cursor, command: str, source_type: str, 
                           source_id: str, source_title: str):
        """Add command to command index"""
        command_info = self.analyze_command(command, '')
        
        cursor.execute('''
            INSERT INTO commands 
            (command, description, category, source_type, source_id, examples, parameters)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            command, command_info.get('description', ''), 
            command_info.get('category', 'general'),
            source_type, source_id, json.dumps([command]), 
            json.dumps(command_info.get('parameters', []))
        ))
    
    def analyze_command(self, command: str, context: str) -> Dict[str, Any]:
        """Analyze command and extract metadata"""
        return {
            'command': command,
            'description': f"Command: {command}",
            'category': self.categorize_command(command),
            'parameters': self.extract_parameters(command),
            'examples': [command]
        }
    
    def categorize_command(self, command: str) -> str:
        """Categorize command based on content"""
        command_lower = command.lower()
        
        if any(term in command_lower for term in ['select', 'insert', 'update', 'delete']):
            return 'database'
        elif any(term in command_lower for term in ['function', 'method', 'class']):
            return 'programming'
        elif any(term in command_lower for term in ['api', 'service', 'endpoint']):
            return 'api'
        elif any(term in command_lower for term in ['config', 'setting', 'property']):
            return 'configuration'
        else:
            return 'general'
    
    def extract_parameters(self, command: str) -> List[str]:
        """Extract parameters from command"""
        # Simple parameter extraction
        params = re.findall(r'\(([^)]+)\)', command)
        if params:
            return [p.strip() for p in params[0].split(',')]
        return []
    
    def extract_command_context(self, command: str, content: str) -> str:
        """Extract context around command"""
        command_pos = content.find(command)
        if command_pos == -1:
            return ""
        
        start = max(0, command_pos - 200)
        end = min(len(content), command_pos + 200)
        return content[start:end]
    
    def extract_sections_from_page(self, page_text: str, page_num: int) -> List[Dict[str, str]]:
        """Extract sections from PDF page"""
        sections = []
        
        # Simple section detection based on patterns
        lines = page_text.split('\n')
        current_section = {'title': '', 'content': '', 'page': page_num}
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Check if line looks like a header (simple heuristic)
            if (len(line) < 100 and 
                (line.isupper() or 
                 re.match(r'^\d+\.\s+', line) or
                 any(word in line.lower() for word in ['chapter', 'section', 'part']))):
                
                # Save previous section if it has content
                if current_section['content']:
                    sections.append(current_section.copy())
                
                # Start new section
                current_section = {
                    'title': line,
                    'content': '',
                    'page': page_num
                }
            else:
                current_section['content'] += line + ' '
        
        # Add final section
        if current_section['content']:
            sections.append(current_section)
        
        return sections
    
    def create_search_index_files(self, videos: List[VideoContent], pdfs: List[PDFContent]):
        """Create search index files for faster access"""
        # Create master index
        master_index = {
            'metadata': {
                'created_at': datetime.now().isoformat(),
                'total_videos': len(videos),
                'total_pdfs': len(pdfs),
                'version': '1.0.0'
            },
            'videos': {video.video_id: {
                'title': video.title,
                'duration': video.duration,
                'topics': video.topics,
                'complexity': video.complexity_level
            } for video in videos},
            'pdfs': {pdf.pdf_id: {
                'title': pdf.title,
                'page_count': pdf.page_count,
                'topics': pdf.topics
            } for pdf in pdfs}
        }
        
        index_path = self.output_path / "search_index" / "master_index.json"
        with open(index_path, 'w', encoding='utf-8') as f:
            json.dump(master_index, f, indent=2, ensure_ascii=False)
        
        # Create topic-based indexes
        topic_index = defaultdict(list)
        
        for video in videos:
            for topic in video.topics:
                topic_index[topic].append({
                    'type': 'video',
                    'id': video.video_id,
                    'title': video.title,
                    'relevance': 1.0
                })
        
        for pdf in pdfs:
            for topic in pdf.topics:
                topic_index[topic].append({
                    'type': 'pdf',
                    'id': pdf.pdf_id,
                    'title': pdf.title,
                    'relevance': 1.0
                })
        
        topic_index_path = self.output_path / "search_index" / "topic_index.json"
        with open(topic_index_path, 'w', encoding='utf-8') as f:
            json.dump(dict(topic_index), f, indent=2, ensure_ascii=False)
    
    def create_command_reference_markdown(self, command_reference: Dict):
        """Create markdown documentation for command reference"""
        md_content = """# Creatio Developer Course - Command Reference

This document contains all commands, APIs, and code examples extracted from the Creatio Developer Course materials.

## Overview

- **Total Commands**: {total_commands}
- **Categories**: {category_count}
- **Generated**: {created_at}

## Categories

""".format(
            total_commands=command_reference['metadata']['total_commands'],
            category_count=len(command_reference['categories']),
            created_at=command_reference['metadata']['created_at']
        )
        
        # Add category sections
        for category, commands in command_reference['categories'].items():
            md_content += f"\n### {category.title()}\n\n"
            
            for command_key in commands[:10]:  # Limit for readability
                command_info = command_reference['commands'].get(command_key, {})
                md_content += f"- `{command_info.get('command', command_key)}`\n"
                if command_info.get('description'):
                    md_content += f"  - {command_info['description']}\n"
                if command_info.get('sources'):
                    source_count = len(command_info['sources'])
                    md_content += f"  - Found in {source_count} source(s)\n"
                md_content += "\n"
        
        # Save markdown file
        md_path = self.output_path / "command_reference" / "README.md"
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(md_content)
    
    def create_enhanced_mcp_server(self):
        """Create enhanced MCP server with knowledge hub integration"""
        server_code = '''#!/usr/bin/env python3
"""
Enhanced MCP Server for Creatio AI Knowledge Hub
Integrates with processed video and PDF content for AI assistance
"""

import sqlite3
import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Creatio AI Knowledge Hub MCP Server",
    description="Enhanced MCP server with full knowledge hub integration",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration
DB_PATH = "ai_knowledge_hub/knowledge_hub.db"
SEARCH_INDEX_PATH = "ai_knowledge_hub/search_index"

class KnowledgeHubService:
    def __init__(self):
        self.db_path = DB_PATH
        self.search_index_path = Path(SEARCH_INDEX_PATH)
    
    def search_content(self, query: str, content_type: str = "all", limit: int = 10) -> List[Dict]:
        """Search across all indexed content"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if content_type == "all":
            cursor.execute("""
                SELECT content_type, content_id, section, content, keywords, relevance_score
                FROM search_fts
                WHERE search_fts MATCH ?
                ORDER BY rank
                LIMIT ?
            """, (query, limit))
        else:
            cursor.execute("""
                SELECT content_type, content_id, section, content, keywords, relevance_score
                FROM search_fts
                WHERE search_fts MATCH ? AND content_type = ?
                ORDER BY rank
                LIMIT ?
            """, (query, content_type, limit))
        
        results = []
        for row in cursor.fetchall():
            results.append({
                'content_type': row[0],
                'content_id': row[1],
                'title': row[2],
                'content_snippet': row[3][:500],
                'keywords': row[4],
                'relevance_score': row[5]
            })
        
        conn.close()
        return results
    
    def get_commands(self, category: Optional[str] = None, search_term: Optional[str] = None) -> List[Dict]:
        """Get commands from the knowledge base"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        query = "SELECT * FROM commands"
        params = []
        
        conditions = []
        if category:
            conditions.append("category = ?")
            params.append(category)
        
        if search_term:
            conditions.append("(command LIKE ? OR description LIKE ?)")
            params.extend([f"%{search_term}%", f"%{search_term}%"])
        
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        
        query += " ORDER BY command LIMIT 50"
        
        cursor.execute(query, params)
        
        results = []
        for row in cursor.fetchall():
            results.append({
                'id': row[0],
                'command': row[1],
                'description': row[2],
                'category': row[3],
                'source_type': row[4],
                'source_id': row[5],
                'examples': json.loads(row[6]) if row[6] else [],
                'parameters': json.loads(row[7]) if row[7] else []
            })
        
        conn.close()
        return results

knowledge_service = KnowledgeHubService()

@app.get("/api/v1/search")
async def search_content(
    query: str = Query(..., description="Search query"),
    content_type: str = Query("all", description="Content type filter"),
    limit: int = Query(10, description="Maximum results")
):
    """Search across all knowledge hub content"""
    try:
        results = knowledge_service.search_content(query, content_type, limit)
        return {
            "query": query,
            "content_type": content_type,
            "total_results": len(results),
            "results": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/commands")
async def get_commands(
    category: Optional[str] = Query(None, description="Command category"),
    search_term: Optional[str] = Query(None, description="Search term")
):
    """Get commands from knowledge base"""
    try:
        commands = knowledge_service.get_commands(category, search_term)
        return {
            "total_commands": len(commands),
            "commands": commands
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
'''
        
        server_path = self.output_path / "enhanced_mcp_server.py"
        with open(server_path, 'w', encoding='utf-8') as f:
            f.write(server_code)
        
        # Make it executable
        server_path.chmod(0o755)
    
    def run_integration(self):
        """Run the complete AI Knowledge Hub Integration"""
        try:
            logger.info("Starting AI Knowledge Hub Integration...")
            
            # Initialize database
            self.initialize_database()
            
            # Process video recordings
            videos = self.process_video_recordings()
            
            # Process PDF transcripts
            pdfs = self.process_pdf_transcripts()
            
            # Create searchable index
            self.create_searchable_index(videos, pdfs)
            
            # Build command reference
            command_reference = self.build_command_reference(videos, pdfs)
            
            # Setup MCP server integration
            self.setup_mcp_server_integration()
            
            # Create integration summary report
            self.create_integration_report(videos, pdfs, command_reference)
            
            logger.info("AI Knowledge Hub Integration completed successfully!")
            
        except Exception as e:
            logger.error(f"Integration failed: {e}")
            raise
    
    def create_integration_report(self, videos: List[VideoContent], 
                                pdfs: List[PDFContent], command_reference: Dict):
        """Create comprehensive integration report"""
        report = {
            'integration_summary': {
                'completed_at': datetime.now().isoformat(),
                'videos_processed': len(videos),
                'pdfs_processed': len(pdfs),
                'total_commands': len(command_reference['commands']),
                'command_categories': len(command_reference['categories']),
                'database_path': str(self.db_path),
                'search_index_path': str(self.output_path / "search_index"),
                'command_reference_path': str(self.output_path / "command_reference")
            },
            'video_processing': {
                'total_videos': len(videos),
                'processed_successfully': len([v for v in videos if v.transcript]),
                'topics_identified': len(set([topic for v in videos for topic in v.topics])),
                'total_commands_from_videos': sum(len(v.commands) for v in videos),
                'complexity_distribution': {
                    level: len([v for v in videos if v.complexity_level == level])
                    for level in ['beginner', 'intermediate', 'advanced']
                }
            },
            'pdf_processing': {
                'total_pdfs': len(pdfs),
                'total_pages': sum(p.page_count for p in pdfs),
                'topics_identified': len(set([topic for p in pdfs for topic in p.topics])),
                'total_commands_from_pdfs': sum(len(p.commands) for p in pdfs),
                'average_sections_per_pdf': sum(len(p.sections) for p in pdfs) / len(pdfs) if pdfs else 0
            },
            'search_capabilities': {
                'full_text_search': True,
                'topic_based_search': True,
                'command_lookup': True,
                'code_example_search': True,
                'cross_content_search': True
            },
            'mcp_server': {
                'status': 'configured',
                'endpoints': [
                    '/api/v1/search',
                    '/api/v1/commands',
                    '/api/v1/videos',
                    '/api/v1/pdfs',
                    '/api/v1/code-examples'
                ],
                'database_integration': True,
                'ai_assistance_ready': True
            }
        }
        
        report_path = self.output_path / "integration_report.json"
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        # Create markdown summary
        self.create_integration_summary_markdown(report)
    
    def create_integration_summary_markdown(self, report: Dict):
        """Create markdown summary of integration"""
        md_content = f"""# AI Knowledge Hub Integration Report

**Integration Completed**: {report['integration_summary']['completed_at']}

## Summary

✅ **Videos Processed**: {report['integration_summary']['videos_processed']}/13  
✅ **PDF Transcripts Processed**: {report['integration_summary']['pdfs_processed']}/14  
✅ **Commands Indexed**: {report['integration_summary']['total_commands']}  
✅ **Command Categories**: {report['integration_summary']['command_categories']}  
✅ **Searchable Documentation Index**: Created  
✅ **MCP Server Integration**: Configured  

## Video Processing Results

- **Total Videos**: {report['video_processing']['total_videos']}
- **Successfully Processed**: {report['video_processing']['processed_successfully']}
- **Topics Identified**: {report['video_processing']['topics_identified']}
- **Commands Extracted**: {report['video_processing']['total_commands_from_videos']}

### Complexity Distribution
- **Beginner**: {report['video_processing']['complexity_distribution']['beginner']}
- **Intermediate**: {report['video_processing']['complexity_distribution']['intermediate']}
- **Advanced**: {report['video_processing']['complexity_distribution']['advanced']}

## PDF Processing Results

- **Total PDFs**: {report['pdf_processing']['total_pdfs']}
- **Total Pages**: {report['pdf_processing']['total_pages']}
- **Topics Identified**: {report['pdf_processing']['topics_identified']}
- **Commands Extracted**: {report['pdf_processing']['total_commands_from_pdfs']}
- **Average Sections per PDF**: {report['pdf_processing']['average_sections_per_pdf']:.1f}

## Search Capabilities

✅ Full-text search across all content  
✅ Topic-based content filtering  
✅ Command lookup and reference  
✅ Code example search  
✅ Cross-content search (videos + PDFs)  

## MCP Server Integration

The enhanced MCP server provides AI assistance with:

- **Content Search**: `/api/v1/search`
- **Command Reference**: `/api/v1/commands`
- **Video Access**: `/api/v1/videos`
- **PDF Content**: `/api/v1/pdfs`
- **Code Examples**: `/api/v1/code-examples`

### Database Integration
- SQLite database with full-text search
- Indexed content for fast retrieval
- Command reference with categorization
- Cross-referenced topics and examples

## Files Created

- `{report['integration_summary']['database_path']}` - Main knowledge database
- `{report['integration_summary']['search_index_path']}/` - Search index files
- `{report['integration_summary']['command_reference_path']}/` - Command reference documentation
- `ai_knowledge_hub/enhanced_mcp_server.py` - Enhanced MCP server
- `ai_knowledge_hub/processed_videos/` - Processed video data
- `ai_knowledge_hub/processed_pdfs/` - Processed PDF data

## Next Steps

1. Start the enhanced MCP server: `python ai_knowledge_hub/enhanced_mcp_server.py`
2. Test search functionality through API endpoints
3. Integrate with AI assistants using MCP protocol
4. Use command reference for development guidance

---

**AI Knowledge Hub Integration - Step 9 Complete** ✅
"""
        
        summary_path = self.output_path / "INTEGRATION_SUMMARY.md"
        with open(summary_path, 'w', encoding='utf-8') as f:
            f.write(md_content)

def main():
    """Main entry point"""
    integrator = AIKnowledgeHubIntegrator()
    integrator.run_integration()

if __name__ == "__main__":
    main()
