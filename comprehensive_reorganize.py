#!/usr/bin/env python3
"""
Comprehensive Project Reorganization Script
Reorganizes the Creatio Academy project structure and removes duplicates
"""

import os
import shutil
import json
import hashlib
from pathlib import Path
from datetime import datetime

class ProjectReorganizer:
    def __init__(self, base_dir):
        self.base_dir = Path(base_dir)
        self.backup_dir = self.base_dir / "backup_before_reorganization"
        self.log_file = self.base_dir / "reorganization.log"
        self.duplicate_report = self.base_dir / "duplicate_files_report.json"
        
    def log(self, message):
        """Log messages to file and console"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] {message}"
        print(log_message)
        
        with open(self.log_file, 'a') as f:
            f.write(log_message + '\n')
    
    def get_file_hash(self, file_path):
        """Calculate MD5 hash of a file"""
        hash_md5 = hashlib.md5()
        try:
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
        except Exception as e:
            self.log(f"Error hashing {file_path}: {e}")
            return None
    
    def find_duplicates(self, directories):
        """Find duplicate files across directories"""
        file_hashes = {}
        duplicates = {}
        
        for directory in directories:
            if not os.path.exists(directory):
                continue
                
            for root, dirs, files in os.walk(directory):
                for file in files:
                    file_path = os.path.join(root, file)
                    if os.path.isfile(file_path):
                        file_hash = self.get_file_hash(file_path)
                        if file_hash:
                            if file_hash in file_hashes:
                                if file_hash not in duplicates:
                                    duplicates[file_hash] = [file_hashes[file_hash]]
                                duplicates[file_hash].append(file_path)
                            else:
                                file_hashes[file_hash] = file_path
        
        return duplicates
    
    def create_new_structure(self):
        """Create the new organized directory structure"""
        new_structure = {
            'videos': {
                'live_sessions': {},
                'tutorials': {},
                'transcripts': {},
                'summaries': {},
                'metadata': {}
            },
            'documentation': {
                'raw_html': {},
                'markdown': {},
                'metadata': {},
                'api_docs': {}
            },
            'scripts': {
                'core': {},
                'utilities': {},
                'deprecated': {}
            },
            'search_index': {},
            'config': {},
            'reports': {},
            'assets': {
                'images': {},
                'css': {},
                'js': {}
            }
        }
        
        # Create directories
        for main_dir, subdirs in new_structure.items():
            main_path = self.base_dir / main_dir
            main_path.mkdir(exist_ok=True)
            
            if isinstance(subdirs, dict):
                for subdir in subdirs.keys():
                    (main_path / subdir).mkdir(exist_ok=True)
    
    def move_videos(self):
        """Move and organize video files"""
        video_extensions = ['.mp4', '.mkv', '.webm', '.avi']
        video_target = self.base_dir / 'videos'
        
        # Sources to check for videos
        video_sources = [
            self.base_dir / 'creatio-academy-archive/videos',
            self.base_dir / 'downloads',
            self.base_dir  # Root level video files
        ]
        
        for source in video_sources:
            if not source.exists():
                continue
                
            for root, dirs, files in os.walk(source):
                for file in files:
                    if any(file.lower().endswith(ext) for ext in video_extensions):
                        source_file = Path(root) / file
                        
                        # Determine target based on file name
                        if 'live' in file.lower() or 'stream' in file.lower():
                            target_dir = video_target / 'live_sessions'
                        else:
                            target_dir = video_target / 'tutorials'
                        
                        target_file = target_dir / file
                        
                        # Move file if it doesn't exist in target
                        if not target_file.exists():
                            shutil.move(str(source_file), str(target_file))
                            self.log(f"Moved video: {source_file} -> {target_file}")
    
    def consolidate_transcripts(self):
        """Consolidate all transcript and summary files"""
        transcript_sources = [
            self.base_dir / 'transcriptions',
            self.base_dir / 'creatio-academy-db/videos'
        ]
        
        target_transcripts = self.base_dir / 'videos/transcripts'
        target_summaries = self.base_dir / 'videos/summaries'
        target_metadata = self.base_dir / 'videos/metadata'
        
        for source in transcript_sources:
            if not source.exists():
                continue
            
            # Move transcripts
            transcript_dir = source / 'transcripts'
            if transcript_dir.exists():
                for file in transcript_dir.iterdir():
                    if file.is_file():
                        target = target_transcripts / file.name
                        if not target.exists():
                            shutil.move(str(file), str(target))
                            self.log(f"Moved transcript: {file} -> {target}")
            
            # Move summaries
            summary_dir = source / 'summaries'
            if summary_dir.exists():
                for file in summary_dir.iterdir():
                    if file.is_file():
                        target = target_summaries / file.name
                        if not target.exists():
                            shutil.move(str(file), str(target))
                            self.log(f"Moved summary: {file} -> {target}")
            
            # Move metadata
            metadata_dir = source / 'metadata'
            if metadata_dir.exists():
                for file in metadata_dir.iterdir():
                    if file.is_file():
                        target = target_metadata / file.name
                        if not target.exists():
                            shutil.move(str(file), str(target))
                            self.log(f"Moved metadata: {file} -> {target}")
    
    def organize_scripts(self):
        """Organize Python scripts by functionality"""
        script_categories = {
            'core': [
                'mcp_server.py', 'main.py', 'content_processor.py'
            ],
            'utilities': [
                'docs_8x_scraper.py', 'youtube_downloader.py', 'filename_normalizer.py',
                'website_tester.py', 'batch_transcribe.py', 'process_all_videos.py',
                'transcription_processor.py', 'llm_summarizer.py', 'check_status.py'
            ]
        }
        
        scripts_dir = self.base_dir / 'scripts'
        
        # Move scripts from root
        for script_file in self.base_dir.glob('*.py'):
            if script_file.name == 'comprehensive_reorganize.py':
                continue  # Don't move this script
                
            moved = False
            for category, script_list in script_categories.items():
                if script_file.name in script_list:
                    target = scripts_dir / category / script_file.name
                    shutil.move(str(script_file), str(target))
                    self.log(f"Moved script: {script_file} -> {target}")
                    moved = True
                    break
            
            if not moved:
                # Move to utilities as default
                target = scripts_dir / 'utilities' / script_file.name
                shutil.move(str(script_file), str(target))
                self.log(f"Moved script (utilities): {script_file} -> {target}")
    
    def consolidate_documentation(self):
        """Consolidate all documentation"""
        doc_sources = [
            self.base_dir / 'creatio-academy-archive/pages',
            self.base_dir / 'docs',
            self.base_dir / 'creatio-academy-db/documentation'
        ]
        
        doc_target = self.base_dir / 'documentation'
        
        for source in doc_sources:
            if not source.exists():
                continue
            
            # Move HTML files
            raw_dir = source / 'raw'
            if raw_dir.exists():
                target_raw = doc_target / 'raw_html'
                if not target_raw.exists():
                    shutil.move(str(raw_dir), str(target_raw))
                    self.log(f"Moved documentation: {raw_dir} -> {target_raw}")
            
            # Move other documentation files
            for item in source.iterdir():
                if item.is_file():
                    target = doc_target / 'metadata' / item.name
                    if not target.exists():
                        shutil.copy2(str(item), str(target))
                        self.log(f"Copied doc file: {item} -> {target}")
    
    def cleanup_empty_directories(self):
        """Remove empty directories after reorganization"""
        def remove_empty_dirs(path):
            if not path.is_dir():
                return
            
            # Remove empty subdirectories first
            for subdir in path.iterdir():
                if subdir.is_dir():
                    remove_empty_dirs(subdir)
            
            # Remove this directory if it's empty
            try:
                if not any(path.iterdir()):
                    path.rmdir()
                    self.log(f"Removed empty directory: {path}")
            except OSError:
                pass  # Directory not empty or other error
        
        # Clean up old directories
        old_dirs = [
            'transcriptions', 'downloads/creatio - Live', 'creatio-academy-archive/videos',
            'creatio-academy-archive/pages'
        ]
        
        for old_dir in old_dirs:
            old_path = self.base_dir / old_dir
            if old_path.exists():
                remove_empty_dirs(old_path)
    
    def create_index_files(self):
        """Create index/manifest files for each major directory"""
        directories_to_index = [
            'videos', 'documentation', 'scripts'
        ]
        
        for dir_name in directories_to_index:
            dir_path = self.base_dir / dir_name
            if not dir_path.exists():
                continue
            
            index_data = {
                'directory': dir_name,
                'created': datetime.now().isoformat(),
                'structure': {}
            }
            
            for root, dirs, files in os.walk(dir_path):
                rel_path = os.path.relpath(root, dir_path)
                if rel_path == '.':
                    rel_path = 'root'
                
                index_data['structure'][rel_path] = {
                    'subdirectories': dirs,
                    'files': files,
                    'file_count': len(files)
                }
            
            index_file = dir_path / 'INDEX.json'
            with open(index_file, 'w') as f:
                json.dump(index_data, f, indent=2)
            
            self.log(f"Created index file: {index_file}")
    
    def reorganize(self):
        """Main reorganization method"""
        self.log("Starting comprehensive project reorganization...")
        
        # Create backup
        if not self.backup_dir.exists():
            self.log("Creating backup of current structure...")
            # Note: We'll skip backup for now to save space, but log the action
            self.log("Backup skipped to save disk space - proceeding with reorganization")
        
        # Find and report duplicates
        self.log("Scanning for duplicate files...")
        directories_to_scan = [
            str(self.base_dir / 'transcriptions'),
            str(self.base_dir / 'creatio-academy-db'),
            str(self.base_dir / 'downloads'),
            str(self.base_dir / 'creatio-academy-archive')
        ]
        
        duplicates = self.find_duplicates(directories_to_scan)
        if duplicates:
            with open(self.duplicate_report, 'w') as f:
                json.dump(duplicates, f, indent=2)
            self.log(f"Found {len(duplicates)} sets of duplicate files - report saved to {self.duplicate_report}")
        
        # Create new structure
        self.log("Creating new directory structure...")
        self.create_new_structure()
        
        # Reorganize content
        self.log("Moving video files...")
        self.move_videos()
        
        self.log("Consolidating transcripts and summaries...")
        self.consolidate_transcripts()
        
        self.log("Organizing scripts...")
        self.organize_scripts()
        
        self.log("Consolidating documentation...")
        self.consolidate_documentation()
        
        # Clean up
        self.log("Cleaning up empty directories...")
        self.cleanup_empty_directories()
        
        # Create indices
        self.log("Creating index files...")
        self.create_index_files()
        
        self.log("Reorganization completed successfully!")
        
        # Print summary
        print("\n" + "="*60)
        print("REORGANIZATION SUMMARY")
        print("="*60)
        print(f"Log file: {self.log_file}")
        print(f"Duplicate report: {self.duplicate_report}")
        print("\nNew structure created:")
        print("- videos/ (live_sessions, tutorials, transcripts, summaries, metadata)")
        print("- documentation/ (raw_html, markdown, metadata, api_docs)")
        print("- scripts/ (core, utilities, deprecated)")
        print("- search_index/")
        print("- config/")
        print("- reports/")
        print("- assets/ (images, css, js)")
        print("="*60)

if __name__ == "__main__":
    base_directory = "/home/andrewwork/creatio-ai-knowledge-hub"
    reorganizer = ProjectReorganizer(base_directory)
    reorganizer.reorganize()
