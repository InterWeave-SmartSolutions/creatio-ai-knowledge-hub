#!/usr/bin/env python3
"""
Comprehensive Metadata Generator for Creatio AI Knowledge Hub

This script generates comprehensive metadata for each file in the knowledge hub:
- JSON metadata with title, type, size, creation date, topics
- Key concept extraction and topic tags
- Full-text search index
- Cross-references between related documents
"""

import os
import json
import re
import hashlib
import mimetypes
from datetime import datetime, timezone
import argparse
from pathlib import Path
from collections import defaultdict, Counter
from typing import Dict, List, Set, Any, Optional, Tuple
import logging

# Try to import optional dependencies
try:
    import textract
    HAS_TEXTRACT = True
except ImportError:
    HAS_TEXTRACT = False
    logging.warning("textract not available - text extraction from binary files will be limited")

try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    import numpy as np
    HAS_SKLEARN = True
except ImportError:
    HAS_SKLEARN = False
    logging.warning("scikit-learn not available - advanced similarity analysis will be disabled")

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class MetadataGenerator:
    """Comprehensive metadata generator for knowledge hub files."""
    
    def __init__(self, root_dir: str, output_dir: str = "./metadata_output"):
        """Initialize the metadata generator.
        
        Args:
            root_dir: Root directory to scan for files
            output_dir: Directory to store generated metadata
        """
        self.root_dir = Path(root_dir).resolve()
        self.output_dir = Path(output_dir).resolve()
        self.output_dir.mkdir(exist_ok=True)
        
        # Initialize storage
        self.file_metadata = {}
        self.topic_index = defaultdict(set)
        self.search_index = {}
        self.concept_graph = defaultdict(set)
        self.similarity_matrix = {}
        
        # File type categories
        self.file_categories = {
            'documents': {'.md', '.txt', '.docx', '.pdf', '.rtf', '.odt'},
            'code': {'.py', '.js', '.ts', '.html', '.css', '.json', '.xml', '.yaml', '.yml', '.sh', '.sql'},
            'images': {'.png', '.jpg', '.jpeg', '.gif', '.svg', '.bmp', '.ico', '.webp'},
            'videos': {'.mp4', '.avi', '.mov', '.wmv', '.flv', '.webm', '.mkv'},
            'audio': {'.mp3', '.wav', '.flac', '.aac', '.ogg', '.wma'},
            'archives': {'.zip', '.tar', '.gz', '.rar', '.7z', '.bz2'},
            'data': {'.csv', '.xlsx', '.xls', '.db', '.sqlite', '.json'},
            'configuration': {'.conf', '.cfg', '.ini', '.env', '.properties'}
        }
        
        # Common stop words for better topic extraction
        self.stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with',
            'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had',
            'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'must',
            'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they',
            'me', 'him', 'her', 'us', 'them', 'my', 'your', 'his', 'her', 'its', 'our', 'their'
        }
        
        # Creatio-specific terms for enhanced topic detection
        self.creatio_terms = {
            'creatio', 'bpm', 'crm', 'business process', 'workflow', 'entity', 'schema',
            'section', 'detail', 'lookup', 'process', 'campaign', 'lead', 'opportunity',
            'contact', 'account', 'case', 'activity', 'dashboard', 'report', 'chart',
            'configuration', 'customization', 'development', 'integration', 'api',
            'mobile', 'portal', 'user', 'role', 'permission', 'security', 'authentication',
            'database', 'query', 'filter', 'search', 'notification', 'email', 'template'
        }

    def get_file_category(self, file_path: Path) -> str:
        """Determine the category of a file based on its extension."""
        ext = file_path.suffix.lower()
        for category, extensions in self.file_categories.items():
            if ext in extensions:
                return category
        return 'other'

    def calculate_file_hash(self, file_path: Path) -> str:
        """Calculate SHA-256 hash of a file."""
        try:
            with open(file_path, 'rb') as f:
                return hashlib.sha256(f.read()).hexdigest()
        except Exception as e:
            logger.warning(f"Could not calculate hash for {file_path}: {e}")
            return ""

    def extract_text_content(self, file_path: Path) -> str:
        """Extract text content from various file types."""
        content = ""
        ext = file_path.suffix.lower()
        
        try:
            if ext in {'.txt', '.md', '.py', '.js', '.ts', '.html', '.css', '.json', '.xml', 
                      '.yaml', '.yml', '.sh', '.sql', '.conf', '.cfg', '.ini', '.env'}:
                # Plain text files
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
            
            elif ext == '.json':
                # JSON files - extract string values
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    content = self.extract_json_strings(data)
                except json.JSONDecodeError:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
            
            elif HAS_TEXTRACT and ext in {'.pdf', '.docx', '.pptx', '.xlsx'}:
                # Binary documents using textract
                content = textract.process(str(file_path)).decode('utf-8', errors='ignore')
            
            else:
                logger.debug(f"Skipping text extraction for {file_path} (unsupported type)")
                
        except Exception as e:
            logger.warning(f"Could not extract text from {file_path}: {e}")
            
        return content[:10000]  # Limit content length for performance

    def extract_json_strings(self, obj: Any) -> str:
        """Recursively extract string values from JSON objects."""
        if isinstance(obj, str):
            return obj + " "
        elif isinstance(obj, dict):
            return " ".join(self.extract_json_strings(v) for v in obj.values())
        elif isinstance(obj, list):
            return " ".join(self.extract_json_strings(item) for item in obj)
        else:
            return str(obj) + " "

    def extract_concepts_and_topics(self, text: str, file_path: Path) -> Tuple[List[str], List[str]]:
        """Extract key concepts and topics from text content."""
        if not text:
            return [], []
        
        # Clean and normalize text
        text = text.lower()
        text = re.sub(r'[^\w\s]', ' ', text)
        words = text.split()
        
        # Extract concepts (longer phrases and technical terms)
        concepts = set()
        topics = set()
        
        # Look for multi-word Creatio terms
        text_lower = text.lower()
        for term in self.creatio_terms:
            if term in text_lower:
                topics.add(term)
                if len(term.split()) > 1:
                    concepts.add(term)
        
        # Extract meaningful words (not stop words, length > 2)
        meaningful_words = [w for w in words if w not in self.stop_words and len(w) > 2]
        
        # Use word frequency to identify important terms
        word_freq = Counter(meaningful_words)
        
        # Add most frequent words as topics
        for word, freq in word_freq.most_common(20):
            if freq > 1:  # Only words that appear multiple times
                topics.add(word)
        
        # Look for patterns that might be concepts
        # CamelCase words
        camel_case_pattern = re.compile(r'[A-Z][a-z]+(?:[A-Z][a-z]+)+')
        camel_cases = camel_case_pattern.findall(text)
        concepts.update(case.lower() for case in camel_cases)
        
        # Extract file path components as potential topics
        path_parts = file_path.parts
        for part in path_parts:
            clean_part = re.sub(r'[^\w]', ' ', part.lower()).strip()
            if clean_part and clean_part not in self.stop_words:
                topics.add(clean_part)
        
        return list(concepts)[:20], list(topics)[:30]  # Limit for performance

    def find_related_files(self, file_path: Path, content: str) -> List[str]:
        """Find files related to the current file based on content similarity."""
        related = []
        
        if not HAS_SKLEARN or not content:
            return related
        
        # Simple keyword-based similarity for now
        current_words = set(re.findall(r'\w+', content.lower()))
        
        for other_path, other_metadata in self.file_metadata.items():
            if other_path == str(file_path):
                continue
                
            other_content = other_metadata.get('content_preview', '')
            if not other_content:
                continue
                
            other_words = set(re.findall(r'\w+', other_content.lower()))
            
            # Calculate Jaccard similarity
            intersection = current_words.intersection(other_words)
            union = current_words.union(other_words)
            
            if union:
                similarity = len(intersection) / len(union)
                if similarity > 0.1:  # Threshold for relatedness
                    related.append(other_path)
        
        return related[:10]  # Limit number of related files

    def generate_file_metadata(self, file_path: Path) -> Dict[str, Any]:
        """Generate comprehensive metadata for a single file."""
        try:
            stat = file_path.stat()
            content = self.extract_text_content(file_path)
            concepts, topics = self.extract_concepts_and_topics(content, file_path)
            
            # Basic file information
            metadata = {
                'file_path': str(file_path.relative_to(self.root_dir)),
                'absolute_path': str(file_path),
                'filename': file_path.name,
                'extension': file_path.suffix.lower(),
                'size_bytes': stat.st_size,
                'size_human': self.format_file_size(stat.st_size),
                'created_date': datetime.fromtimestamp(stat.st_ctime, tz=timezone.utc).isoformat(),
                'modified_date': datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc).isoformat(),
                'accessed_date': datetime.fromtimestamp(stat.st_atime, tz=timezone.utc).isoformat(),
                'file_hash': self.calculate_file_hash(file_path),
                'mime_type': mimetypes.guess_type(str(file_path))[0] or 'application/octet-stream',
                'category': self.get_file_category(file_path),
                
                # Content analysis
                'has_content': bool(content),
                'content_length': len(content),
                'content_preview': content[:500] if content else "",
                'word_count': len(content.split()) if content else 0,
                'line_count': content.count('\n') + 1 if content else 0,
                
                # Topics and concepts
                'concepts': concepts,
                'topics': topics,
                'topic_count': len(topics),
                
                # Auto-generated title
                'title': self.generate_title(file_path, content),
                
                # Metadata generation info
                'metadata_generated': datetime.now(timezone.utc).isoformat(),
                'metadata_version': '1.0'
            }
            
            # Add related files (will be updated in a second pass)
            metadata['related_files'] = []
            
            return metadata
            
        except Exception as e:
            logger.error(f"Error generating metadata for {file_path}: {e}")
            return {
                'file_path': str(file_path.relative_to(self.root_dir)),
                'error': str(e),
                'metadata_generated': datetime.now(timezone.utc).isoformat()
            }

    def generate_title(self, file_path: Path, content: str) -> str:
        """Generate a descriptive title for the file."""
        # Try to extract title from content
        if content:
            lines = content.split('\n')
            for line in lines[:10]:  # Check first 10 lines
                line = line.strip()
                if line:
                    # Look for markdown headers
                    if line.startswith('#'):
                        return line.lstrip('# ').strip()
                    # Look for title-like patterns
                    if len(line) < 100 and not line.startswith(('//', '/*', '--', '*')):
                        # Check if it looks like a title (not code)
                        if not re.search(r'[{}()\[\];]', line):
                            return line
        
        # Fallback to filename-based title
        name = file_path.stem
        # Convert snake_case and kebab-case to Title Case
        title = re.sub(r'[_-]', ' ', name)
        title = ' '.join(word.capitalize() for word in title.split())
        
        # Add context from parent directory
        parent = file_path.parent.name
        if parent and parent != '.' and parent.lower() not in title.lower():
            title = f"{parent.replace('_', ' ').replace('-', ' ').title()} - {title}"
        
        return title

    def format_file_size(self, size_bytes: int) -> str:
        """Format file size in human-readable format."""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f} PB"

    def build_search_index(self) -> Dict[str, Any]:
        """Build a full-text search index from all file metadata."""
        search_index = {
            'files': {},
            'topics': defaultdict(list),
            'concepts': defaultdict(list),
            'categories': defaultdict(list),
            'extensions': defaultdict(list),
            'index_generated': datetime.now(timezone.utc).isoformat()
        }
        
        for file_path, metadata in self.file_metadata.items():
            relative_path = metadata.get('file_path', file_path)
            
            # Add to file index
            searchable_text = ' '.join([
                metadata.get('title', ''),
                metadata.get('filename', ''),
                metadata.get('content_preview', ''),
                ' '.join(metadata.get('topics', [])),
                ' '.join(metadata.get('concepts', []))
            ]).lower()
            
            search_index['files'][relative_path] = {
                'title': metadata.get('title', ''),
                'searchable_text': searchable_text,
                'size': metadata.get('size_bytes', 0),
                'modified': metadata.get('modified_date', ''),
                'category': metadata.get('category', 'other'),
                'topics': metadata.get('topics', []),
                'concepts': metadata.get('concepts', [])
            }
            
            # Add to topic index
            for topic in metadata.get('topics', []):
                search_index['topics'][topic].append(relative_path)
            
            # Add to concept index
            for concept in metadata.get('concepts', []):
                search_index['concepts'][concept].append(relative_path)
            
            # Add to category index
            category = metadata.get('category', 'other')
            search_index['categories'][category].append(relative_path)
            
            # Add to extension index
            ext = metadata.get('extension', '')
            if ext:
                search_index['extensions'][ext].append(relative_path)
        
        return dict(search_index)

    def find_cross_references(self):
        """Find cross-references between documents based on content similarity."""
        logger.info("Finding cross-references between documents...")
        
        # Update related files for each file
        for file_path, metadata in self.file_metadata.items():
            content = metadata.get('content_preview', '')
            related = self.find_related_files(Path(file_path), content)
            metadata['related_files'] = related
            
            # Update concept graph
            concepts = metadata.get('concepts', [])
            for concept in concepts:
                self.concept_graph[concept].add(metadata.get('file_path', file_path))

    def generate_statistics(self) -> Dict[str, Any]:
        """Generate statistics about the knowledge hub."""
        stats = {
            'total_files': len(self.file_metadata),
            'total_size_bytes': sum(m.get('size_bytes', 0) for m in self.file_metadata.values()),
            'categories': defaultdict(int),
            'extensions': defaultdict(int),
            'topics': defaultdict(int),
            'concepts': defaultdict(int),
            'files_with_content': 0,
            'total_word_count': 0,
            'generated_at': datetime.now(timezone.utc).isoformat()
        }
        
        for metadata in self.file_metadata.values():
            # Category stats
            category = metadata.get('category', 'other')
            stats['categories'][category] += 1
            
            # Extension stats
            ext = metadata.get('extension', '')
            if ext:
                stats['extensions'][ext] += 1
            
            # Content stats
            if metadata.get('has_content'):
                stats['files_with_content'] += 1
                stats['total_word_count'] += metadata.get('word_count', 0)
            
            # Topic stats
            for topic in metadata.get('topics', []):
                stats['topics'][topic] += 1
            
            # Concept stats
            for concept in metadata.get('concepts', []):
                stats['concepts'][concept] += 1
        
        # Convert defaultdicts to regular dicts and sort
        stats['categories'] = dict(sorted(stats['categories'].items(), key=lambda x: x[1], reverse=True))
        stats['extensions'] = dict(sorted(stats['extensions'].items(), key=lambda x: x[1], reverse=True))
        stats['topics'] = dict(sorted(stats['topics'].items(), key=lambda x: x[1], reverse=True)[:50])  # Top 50
        stats['concepts'] = dict(sorted(stats['concepts'].items(), key=lambda x: x[1], reverse=True)[:30])  # Top 30
        
        stats['total_size_human'] = self.format_file_size(stats['total_size_bytes'])
        
        return stats

    def scan_files(self, exclude_patterns: List[str] = None) -> List[Path]:
        """Scan the root directory for files to process."""
        if exclude_patterns is None:
            exclude_patterns = [
                '*/venv/*', '*/__pycache__/*', '*/node_modules/*', '*/.git/*',
                '*/.*', '*.pyc', '*.pyo', '*.pyd', '*.so', '*.dll', '*.exe'
            ]
        
        files = []
        for file_path in self.root_dir.rglob('*'):
            if file_path.is_file():
                # Check exclude patterns
                relative_path = file_path.relative_to(self.root_dir)
                exclude = False
                
                for pattern in exclude_patterns:
                    if file_path.match(pattern) or str(relative_path).startswith('.'):
                        exclude = True
                        break
                
                if not exclude:
                    files.append(file_path)
        
        return sorted(files)

    def generate_all_metadata(self) -> Dict[str, Any]:
        """Generate metadata for all files in the knowledge hub."""
        logger.info(f"Starting metadata generation for {self.root_dir}")
        
        # Scan for files
        files = self.scan_files()
        logger.info(f"Found {len(files)} files to process")
        
        # Generate metadata for each file
        for i, file_path in enumerate(files, 1):
            if i % 100 == 0:
                logger.info(f"Processed {i}/{len(files)} files...")
            
            metadata = self.generate_file_metadata(file_path)
            self.file_metadata[str(file_path)] = metadata
        
        logger.info("Finding cross-references...")
        # Find cross-references (second pass)
        self.find_cross_references()
        
        logger.info("Building search index...")
        # Build search index
        self.search_index = self.build_search_index()
        
        logger.info("Generating statistics...")
        # Generate statistics
        statistics = self.generate_statistics()
        
        # Compile final output
        output = {
            'metadata': dict(self.file_metadata),
            'search_index': self.search_index,
            'statistics': statistics,
            'concept_graph': {k: list(v) for k, v in self.concept_graph.items()},
            'generation_info': {
                'root_directory': str(self.root_dir),
                'total_files_processed': len(files),
                'generation_time': datetime.now(timezone.utc).isoformat(),
                'generator_version': '1.0'
            }
        }
        
        return output

    def save_metadata(self, metadata: Dict[str, Any]):
        """Save generated metadata to files."""
        logger.info(f"Saving metadata to {self.output_dir}")
        
        # Save complete metadata
        with open(self.output_dir / 'complete_metadata.json', 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        
        # Save individual components
        with open(self.output_dir / 'file_metadata.json', 'w', encoding='utf-8') as f:
            json.dump(metadata['metadata'], f, indent=2, ensure_ascii=False)
        
        with open(self.output_dir / 'search_index.json', 'w', encoding='utf-8') as f:
            json.dump(metadata['search_index'], f, indent=2, ensure_ascii=False)
        
        with open(self.output_dir / 'statistics.json', 'w', encoding='utf-8') as f:
            json.dump(metadata['statistics'], f, indent=2, ensure_ascii=False)
        
        with open(self.output_dir / 'concept_graph.json', 'w', encoding='utf-8') as f:
            json.dump(metadata['concept_graph'], f, indent=2, ensure_ascii=False)
        
        # Create a human-readable summary
        self.create_summary_report(metadata)
        
        logger.info("Metadata generation completed successfully!")

    def create_summary_report(self, metadata: Dict[str, Any]):
        """Create a human-readable summary report."""
        stats = metadata['statistics']
        
        report = f"""# Creatio AI Knowledge Hub - Metadata Summary Report

Generated: {metadata['generation_info']['generation_time']}
Root Directory: {metadata['generation_info']['root_directory']}

## Overview
- **Total Files**: {stats['total_files']:,}
- **Total Size**: {stats['total_size_human']}
- **Files with Content**: {stats['files_with_content']:,}
- **Total Words**: {stats['total_word_count']:,}

## File Categories
"""
        
        for category, count in stats['categories'].items():
            percentage = (count / stats['total_files']) * 100
            report += f"- **{category.title()}**: {count:,} files ({percentage:.1f}%)\n"
        
        report += "\n## Most Common File Types\n"
        for ext, count in list(stats['extensions'].items())[:10]:
            percentage = (count / stats['total_files']) * 100
            report += f"- **{ext}**: {count:,} files ({percentage:.1f}%)\n"
        
        report += "\n## Top Topics\n"
        for topic, count in list(stats['topics'].items())[:20]:
            report += f"- **{topic}**: {count:,} files\n"
        
        report += "\n## Top Concepts\n"
        for concept, count in list(stats['concepts'].items())[:15]:
            report += f"- **{concept}**: {count:,} files\n"
        
        report += f"""
## Metadata Files Generated
- `complete_metadata.json` - Complete metadata for all files
- `file_metadata.json` - Individual file metadata
- `search_index.json` - Full-text search index
- `statistics.json` - Statistical analysis
- `concept_graph.json` - Concept relationship graph
- `summary_report.md` - This summary report

## Usage Examples

### Search for files by topic:
```python
import json
with open('search_index.json') as f:
    index = json.load(f)
    creatio_files = index['topics'].get('creatio', [])
```

### Find related files:
```python
with open('file_metadata.json') as f:
    metadata = json.load(f)
    for file_path, data in metadata.items():
        related = data.get('related_files', [])
        if related:
            print(f"{file_path} is related to: {related}")
```

### Get statistics:
```python
with open('statistics.json') as f:
    stats = json.load(f)
    print(f"Total files: {stats['total_files']}")
    print(f"Most common topic: {list(stats['topics'].items())[0]}")
```
"""
        
        with open(self.output_dir / 'summary_report.md', 'w', encoding='utf-8') as f:
            f.write(report)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description='Generate comprehensive metadata for Creatio AI Knowledge Hub')
    parser.add_argument('--root-dir', '-r', default='.', help='Root directory to scan (default: current directory)')
    parser.add_argument('--output-dir', '-o', default='./metadata_output', help='Output directory for metadata files')
    parser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose logging')
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Initialize generator
    generator = MetadataGenerator(args.root_dir, args.output_dir)
    
    try:
        # Generate metadata
        metadata = generator.generate_all_metadata()
        
        # Save results
        generator.save_metadata(metadata)
        
        print(f"\n✅ Metadata generation completed successfully!")
        print(f"📊 Processed {metadata['generation_info']['total_files_processed']} files")
        print(f"📁 Results saved to: {generator.output_dir}")
        print(f"📋 Check summary_report.md for detailed overview")
        
    except Exception as e:
        logger.error(f"Error during metadata generation: {e}")
        raise


if __name__ == '__main__':
    main()
