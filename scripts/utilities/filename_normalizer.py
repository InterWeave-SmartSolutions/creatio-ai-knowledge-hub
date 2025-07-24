#!/usr/bin/env python3
"""
Website Mirror Filename Normalizer

This script recursively scans directories for URL-encoded and problematic filenames,
normalizes them according to safe conventions, updates internal links, and creates
a mapping file for reference.

Features:
- Decodes URL-encoded filenames (%20, %2F, etc.)
- Normalizes spaces and special characters
- Updates internal HTML links and references
- Creates comprehensive mapping file
- Preserves website functionality
- Safe filename conventions
"""

import os
import re
import json
import urllib.parse
import shutil
from pathlib import Path
from typing import Dict, List, Tuple, Set
import logging
from datetime import datetime
import argparse
from dataclasses import dataclass
import mimetypes

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('filename_normalization.log'),
        logging.StreamHandler()
    ]
)

@dataclass
class FileMapping:
    """Data class to store file mapping information"""
    original_path: str
    normalized_path: str
    original_name: str
    normalized_name: str
    file_type: str
    references_updated: int = 0
    reason: str = ""

class FilenameNormalizer:
    def __init__(self, root_directory: str, dry_run: bool = False):
        self.root_directory = Path(root_directory).resolve()
        self.dry_run = dry_run
        self.mappings: List[FileMapping] = []
        self.processed_files: Set[str] = set()
        
        # Characters that should be replaced or removed
        self.unsafe_chars = {
            ' ': '_',           # Spaces to underscores
            '%20': '_',         # URL-encoded space
            '%2F': '_',         # URL-encoded forward slash
            '%3A': '_',         # URL-encoded colon
            '%3D': '=',         # URL-encoded equals (keep as is)
            '%3F': '_',         # URL-encoded question mark
            '%26': '_',         # URL-encoded ampersand
            '%23': '_',         # URL-encoded hash
            '%2B': '_',         # URL-encoded plus
            '%5B': '(',         # URL-encoded left bracket
            '%5D': ')',         # URL-encoded right bracket
            '[': '(',           # Square brackets to parentheses
            ']': ')',
            '?': '_',           # Question marks
            '&': '_',           # Ampersands
            '#': '_',           # Hash symbols
            '<': '_',           # Less than
            '>': '_',           # Greater than
            '|': '_',           # Pipe
            '"': '_',           # Double quotes
            "'": '_',           # Single quotes (in filenames)
            ':': '_',           # Colons (problematic on Windows)
            '*': '_',           # Asterisks
        }
        
        # File extensions to process for link updates
        self.processable_extensions = {'.html', '.htm', '.css', '.js', '.xml', '.json', '.txt', '.md'}
        
        # Statistics
        self.stats = {
            'files_processed': 0,
            'files_renamed': 0,
            'links_updated': 0,
            'errors': 0
        }

    def is_filename_problematic(self, filename: str) -> bool:
        """Check if a filename has problematic characters"""
        # Check for URL encoding
        if '%' in filename and re.search(r'%[0-9A-Fa-f]{2}', filename):
            return True
        
        # Check for unsafe characters
        for unsafe_char in self.unsafe_chars:
            if unsafe_char in filename:
                return True
                
        # Check for multiple consecutive underscores or dots
        if '__' in filename or '..' in filename:
            return True
            
        # Check for trailing/leading spaces or dots
        if filename != filename.strip(' .'):
            return True
            
        return False

    def normalize_filename(self, filename: str) -> Tuple[str, str]:
        """
        Normalize a filename by removing/replacing problematic characters
        Returns (normalized_filename, reason)
        """
        original = filename
        reasons = []
        
        # First decode URL encoding
        if '%' in filename:
            try:
                decoded = urllib.parse.unquote(filename)
                if decoded != filename:
                    filename = decoded
                    reasons.append("URL-decoded")
            except Exception as e:
                logging.warning(f"Failed to URL decode {filename}: {e}")
        
        # Replace unsafe characters
        for unsafe, replacement in self.unsafe_chars.items():
            if unsafe in filename:
                filename = filename.replace(unsafe, replacement)
                reasons.append(f"Replaced '{unsafe}' with '{replacement}'")
        
        # Remove multiple consecutive underscores
        while '__' in filename:
            filename = filename.replace('__', '_')
            reasons.append("Removed duplicate underscores")
        
        # Remove multiple consecutive dots (but preserve file extensions)
        parts = filename.rsplit('.', 1)
        if len(parts) == 2:
            name_part, ext_part = parts
            while '..' in name_part:
                name_part = name_part.replace('..', '.')
                reasons.append("Removed duplicate dots")
            filename = f"{name_part}.{ext_part}"
        
        # Clean leading/trailing characters
        filename = filename.strip(' ._-')
        if filename != original:
            reasons.append("Cleaned leading/trailing characters")
        
        # Ensure filename is not empty
        if not filename or filename == '.':
            filename = 'unnamed_file'
            reasons.append("Generated name for empty filename")
        
        # Limit filename length (keeping extension)
        max_length = 200
        if len(filename) > max_length:
            parts = filename.rsplit('.', 1)
            if len(parts) == 2:
                name_part, ext_part = parts
                name_part = name_part[:max_length - len(ext_part) - 1]
                filename = f"{name_part}.{ext_part}"
            else:
                filename = filename[:max_length]
            reasons.append(f"Truncated to {max_length} characters")
        
        return filename, "; ".join(reasons)

    def scan_files(self) -> List[Path]:
        """Scan the directory tree for files that need normalization"""
        problematic_files = []
        
        logging.info(f"Scanning directory: {self.root_directory}")
        
        for file_path in self.root_directory.rglob('*'):
            if file_path.is_file() and not self.should_skip_file(file_path):
                if self.is_filename_problematic(file_path.name):
                    problematic_files.append(file_path)
        
        logging.info(f"Found {len(problematic_files)} files that need normalization")
        return problematic_files

    def should_skip_file(self, file_path: Path) -> bool:
        """Check if a file should be skipped during processing"""
        # Skip hidden files and directories
        if any(part.startswith('.') for part in file_path.parts):
            return True
        
        # Skip system directories
        skip_dirs = {'__pycache__', '.git', '.svn', 'node_modules', 'venv', '.venv'}
        if any(skip_dir in file_path.parts for skip_dir in skip_dirs):
            return True
        
        # Skip binary files that don't need link updates
        skip_extensions = {'.pyc', '.pyo', '.so', '.dll', '.exe'}
        if file_path.suffix.lower() in skip_extensions:
            return True
            
        return False

    def create_safe_target_path(self, original_path: Path) -> Path:
        """Create a safe target path, handling potential conflicts"""
        normalized_name, reason = self.normalize_filename(original_path.name)
        target_path = original_path.parent / normalized_name
        
        # Handle naming conflicts
        counter = 1
        base_target = target_path
        while target_path.exists() and target_path != original_path:
            if target_path.suffix:
                stem = target_path.stem
                suffix = target_path.suffix
                target_path = target_path.parent / f"{stem}_{counter}{suffix}"
            else:
                target_path = target_path.parent / f"{normalized_name}_{counter}"
            counter += 1
        
        return target_path

    def rename_file(self, original_path: Path) -> FileMapping:
        """Rename a single file and create mapping entry"""
        target_path = self.create_safe_target_path(original_path)
        normalized_name, reason = self.normalize_filename(original_path.name)
        
        file_mapping = FileMapping(
            original_path=str(original_path),
            normalized_path=str(target_path),
            original_name=original_path.name,
            normalized_name=target_path.name,
            file_type=mimetypes.guess_type(str(original_path))[0] or 'unknown',
            reason=reason
        )
        
        if not self.dry_run:
            try:
                if original_path != target_path:
                    shutil.move(str(original_path), str(target_path))
                    logging.info(f"Renamed: {original_path.name} -> {target_path.name}")
                    self.stats['files_renamed'] += 1
            except Exception as e:
                logging.error(f"Failed to rename {original_path}: {e}")
                self.stats['errors'] += 1
                return None
        
        return file_mapping

    def update_file_references(self, file_path: Path, mappings_dict: Dict[str, str]):
        """Update references in a text-based file"""
        if not file_path.suffix.lower() in self.processable_extensions:
            return
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                
            original_content = content
            updates_count = 0
            
            # Update references based on mappings
            for old_name, new_name in mappings_dict.items():
                if old_name != new_name:
                    # Update direct filename references
                    if old_name in content:
                        content = content.replace(old_name, new_name)
                        updates_count += 1
                    
                    # Update URL-encoded references
                    encoded_old = urllib.parse.quote(old_name)
                    if encoded_old in content and encoded_old != old_name:
                        content = content.replace(encoded_old, urllib.parse.quote(new_name))
                        updates_count += 1
            
            # Only write if changes were made
            if content != original_content and not self.dry_run:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                    
            if updates_count > 0:
                logging.info(f"Updated {updates_count} references in {file_path}")
                self.stats['links_updated'] += updates_count
                
        except Exception as e:
            logging.error(f"Failed to update references in {file_path}: {e}")
            self.stats['errors'] += 1

    def process_all_files(self):
        """Main processing function"""
        logging.info("Starting filename normalization process")
        
        # Step 1: Scan for problematic files
        problematic_files = self.scan_files()
        
        if not problematic_files:
            logging.info("No problematic filenames found!")
            return
        
        # Step 2: Create rename mappings
        logging.info("Creating filename mappings...")
        mappings_dict = {}
        
        for file_path in problematic_files:
            mapping = self.rename_file(file_path)
            if mapping:
                self.mappings.append(mapping)
                mappings_dict[mapping.original_name] = mapping.normalized_name
        
        # Step 3: Update internal references
        logging.info("Updating internal references...")
        all_files = [f for f in self.root_directory.rglob('*') 
                    if f.is_file() and not self.should_skip_file(f)]
        
        for file_path in all_files:
            self.update_file_references(file_path, mappings_dict)
            self.stats['files_processed'] += 1

    def create_mapping_file(self):
        """Create a comprehensive mapping file documenting all changes"""
        mapping_data = {
            'metadata': {
                'timestamp': datetime.now().isoformat(),
                'root_directory': str(self.root_directory),
                'dry_run': self.dry_run,
                'statistics': self.stats
            },
            'mappings': [
                {
                    'original_path': mapping.original_path,
                    'normalized_path': mapping.normalized_path,
                    'original_name': mapping.original_name,
                    'normalized_name': mapping.normalized_name,
                    'file_type': mapping.file_type,
                    'references_updated': mapping.references_updated,
                    'reason': mapping.reason
                }
                for mapping in self.mappings
            ]
        }
        
        mapping_file = self.root_directory / 'filename_mapping.json'
        
        if not self.dry_run:
            with open(mapping_file, 'w', encoding='utf-8') as f:
                json.dump(mapping_data, f, indent=2, ensure_ascii=False)
        
        logging.info(f"Mapping file {'would be' if self.dry_run else ''} created: {mapping_file}")
        return mapping_file

    def print_summary(self):
        """Print processing summary"""
        print("\n" + "="*60)
        print("FILENAME NORMALIZATION SUMMARY")
        print("="*60)
        print(f"Root directory: {self.root_directory}")
        print(f"Mode: {'DRY RUN' if self.dry_run else 'LIVE RUN'}")
        print(f"Files processed: {self.stats['files_processed']}")
        print(f"Files renamed: {self.stats['files_renamed']}")
        print(f"Links updated: {self.stats['links_updated']}")
        print(f"Errors: {self.stats['errors']}")
        print(f"Total mappings created: {len(self.mappings)}")
        print("="*60)
        
        if self.mappings:
            print("\nSample mappings:")
            for mapping in self.mappings[:5]:  # Show first 5 mappings
                print(f"  {mapping.original_name} -> {mapping.normalized_name}")
                if mapping.reason:
                    print(f"    Reason: {mapping.reason}")
            
            if len(self.mappings) > 5:
                print(f"  ... and {len(self.mappings) - 5} more")

def main():
    parser = argparse.ArgumentParser(description='Normalize filenames in website mirror')
    parser.add_argument('directory', help='Root directory to process')
    parser.add_argument('--dry-run', action='store_true', 
                       help='Show what would be done without making changes')
    parser.add_argument('--exclude-venv', action='store_true', default=True,
                       help='Exclude virtual environment directories')
    
    args = parser.parse_args()
    
    # Validate directory
    if not os.path.isdir(args.directory):
        print(f"Error: {args.directory} is not a valid directory")
        return 1
    
    # Create normalizer and process
    normalizer = FilenameNormalizer(args.directory, dry_run=args.dry_run)
    
    try:
        normalizer.process_all_files()
        normalizer.create_mapping_file()
        normalizer.print_summary()
        
        if args.dry_run:
            print("\nThis was a dry run. Use --no-dry-run to apply changes.")
        else:
            print("\nFilename normalization completed successfully!")
            
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        return 1
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return 1
    
    return 0

if __name__ == '__main__':
    exit(main())
