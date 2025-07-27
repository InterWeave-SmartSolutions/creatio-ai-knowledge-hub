#!/usr/bin/env python3
"""
Cleanup Duplicates Script
Removes duplicate files and redundant directories after reorganization
"""

import os
import shutil
import json
from pathlib import Path
from datetime import datetime

class DuplicateCleanup:
    def __init__(self, base_dir):
        self.base_dir = Path(base_dir)
        self.duplicate_report = self.base_dir / "duplicate_files_report.json"
        self.cleanup_log = self.base_dir / "cleanup.log"
        
    def log(self, message):
        """Log messages to file and console"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] {message}"
        print(log_message)
        
        with open(self.cleanup_log, 'a') as f:
            f.write(log_message + '\n')
    
    def remove_old_directories(self):
        """Remove old redundant directories"""
        directories_to_remove = [
            'creatio-academy-db/videos',  # Now moved to videos/
            'transcriptions',  # Now consolidated in videos/
            'downloads/creatio - Live',  # Files moved
            'search_engine',  # Keep this for now
            'src'  # Scripts moved to scripts/
        ]
        
        for dir_path in directories_to_remove:
            full_path = self.base_dir / dir_path
            if full_path.exists():
                try:
                    if dir_path == 'search_engine':
                        # Move search_engine to proper location
                        target = self.base_dir / 'search-index' / 'engines'
                        target.mkdir(parents=True, exist_ok=True)
                        for item in full_path.iterdir():
                            if item.is_file():
                                shutil.move(str(item), str(target / item.name))
                                self.log(f"Moved search engine file: {item} -> {target / item.name}")
                        shutil.rmtree(str(full_path))
                    else:
                        shutil.rmtree(str(full_path))
                    self.log(f"Removed directory: {full_path}")
                except Exception as e:
                    self.log(f"Error removing {full_path}: {e}")
    
    def clean_duplicates_from_report(self):
        """Remove duplicates based on the duplicate report"""
        if not self.duplicate_report.exists():
            self.log("No duplicate report found")
            return
        
        with open(self.duplicate_report, 'r') as f:
            duplicates = json.load(f)
        
        removed_count = 0
        for file_hash, file_list in duplicates.items():
            if len(file_list) <= 1:
                continue
            
            # Keep the first file (usually in the new organized structure)
            # Remove the others
            files_to_keep = []
            files_to_remove = []
            
            for file_path in file_list:
                path = Path(file_path)
                if not path.exists():
                    continue
                
                # Prioritize files in the new organized structure
                if any(x in str(path) for x in ['videos/', 'documentation/', 'scripts/']):
                    files_to_keep.append(path)
                else:
                    files_to_remove.append(path)
            
            # If no files in new structure, keep the first one
            if not files_to_keep and files_to_remove:
                files_to_keep.append(files_to_remove.pop(0))
            
            # Remove duplicates
            for file_path in files_to_remove:
                try:
                    file_path.unlink()
                    self.log(f"Removed duplicate: {file_path}")
                    removed_count += 1
                except Exception as e:
                    self.log(f"Error removing {file_path}: {e}")
        
        self.log(f"Removed {removed_count} duplicate files")
    
    def remove_empty_directories(self):
        """Remove empty directories recursively"""
        def is_empty_dir(path):
            try:
                return path.is_dir() and not any(path.iterdir())
            except:
                return False
        
        # Traverse directories multiple times to catch nested empty dirs
        for _ in range(5):  # Max 5 iterations
            empty_dirs = []
            for root, dirs, files in os.walk(self.base_dir):
                root_path = Path(root)
                if is_empty_dir(root_path) and root_path != self.base_dir:
                    empty_dirs.append(root_path)
            
            for empty_dir in empty_dirs:
                try:
                    empty_dir.rmdir()
                    self.log(f"Removed empty directory: {empty_dir}")
                except Exception as e:
                    self.log(f"Could not remove {empty_dir}: {e}")
            
            if not empty_dirs:
                break
    
    def clean_venv_duplicates(self):
        """Clean up virtual environment duplicates"""
        venv_dirs = [
            self.base_dir / 'venv',
            self.base_dir / 'creatio-academy-archive/venv'
        ]
        
        # Keep only the main venv, remove the archive one
        archive_venv = self.base_dir / 'creatio-academy-archive/venv'
        if archive_venv.exists():
            try:
                shutil.rmtree(str(archive_venv))
                self.log(f"Removed duplicate venv: {archive_venv}")
            except Exception as e:
                self.log(f"Error removing archive venv: {e}")
    
    def move_remaining_assets(self):
        """Move remaining assets to proper locations"""
        assets_mappings = [
            # Move CSS files
            ('themes/custom/creatio/css', 'assets/css/creatio'),
            ('docs/8.x/assets/css', 'assets/css/docs'),
            # Move JS files  
            ('libraries/slick', 'assets/js/slick'),
            # Move module CSS
            ('modules/contrib/*/css', 'assets/css/modules')
        ]
        
        assets_dir = self.base_dir / 'assets'
        assets_dir.mkdir(exist_ok=True)
        
        # Move theme CSS
        theme_css = self.base_dir / 'themes/custom/creatio/css'
        if theme_css.exists():
            target = assets_dir / 'css/creatio'
            target.mkdir(parents=True, exist_ok=True)
            for css_file in theme_css.rglob('*.css'):
                target_file = target / css_file.name
                try:
                    shutil.move(str(css_file), str(target_file))
                    self.log(f"Moved CSS: {css_file} -> {target_file}")
                except Exception as e:
                    self.log(f"Error moving {css_file}: {e}")
        
        # Move docs CSS
        docs_css = self.base_dir / 'docs/8.x/assets/css'
        if docs_css.exists():
            target = assets_dir / 'css/docs'
            target.mkdir(parents=True, exist_ok=True)
            for css_file in docs_css.rglob('*.css'):
                target_file = target / css_file.name
                try:
                    shutil.move(str(css_file), str(target_file))
                    self.log(f"Moved docs CSS: {css_file} -> {target_file}")
                except Exception as e:
                    self.log(f"Error moving {css_file}: {e}")
        
        # Move JS libraries
        slick_lib = self.base_dir / 'libraries/slick'
        if slick_lib.exists():
            target = assets_dir / 'js/slick'
            try:
                shutil.move(str(slick_lib), str(target))
                self.log(f"Moved JS library: {slick_lib} -> {target}")
            except Exception as e:
                self.log(f"Error moving {slick_lib}: {e}")
    
    def create_final_structure_report(self):
        """Create a report of the final structure"""
        report = {
            'cleanup_completed': datetime.now().isoformat(),
            'final_structure': {}
        }
        
        for root, dirs, files in os.walk(self.base_dir):
            rel_path = os.path.relpath(root, self.base_dir)
            if rel_path == '.':
                rel_path = 'root'
            
            # Skip venv directory for report
            if 'venv' in rel_path:
                continue
                
            report['final_structure'][rel_path] = {
                'directories': [d for d in dirs if d != 'venv'],
                'files': files,
                'file_count': len(files),
                'directory_count': len([d for d in dirs if d != 'venv'])
            }
        
        report_file = self.base_dir / 'final_structure_report.json'
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        self.log(f"Final structure report saved: {report_file}")
    
    def cleanup(self):
        """Main cleanup method"""
        self.log("Starting duplicate cleanup and final organization...")
        
        # Remove duplicate files
        self.log("Removing duplicate files...")
        self.clean_duplicates_from_report()
        
        # Clean up venv duplicates
        self.log("Cleaning up virtual environment duplicates...")
        self.clean_venv_duplicates()
        
        # Move remaining assets
        self.log("Moving remaining assets...")
        self.move_remaining_assets()
        
        # Remove old directories
        self.log("Removing old redundant directories...")
        self.remove_old_directories()
        
        # Remove empty directories
        self.log("Removing empty directories...")
        self.remove_empty_directories()
        
        # Create final report
        self.log("Creating final structure report...")
        self.create_final_structure_report()
        
        self.log("Cleanup completed successfully!")
        
        # Print final summary
        print("\n" + "="*60)
        print("CLEANUP SUMMARY")
        print("="*60)
        print(f"Cleanup log: {self.cleanup_log}")
        print(f"Final structure report: {self.base_dir}/final_structure_report.json")
        print("\nFinal organized structure:")
        
        # Show top-level directories
        for item in sorted(self.base_dir.iterdir()):
            if item.is_dir() and item.name not in ['__pycache__', 'venv']:
                print(f"- {item.name}/")
        
        print("="*60)

if __name__ == "__main__":
    base_directory = "/home/andrewwork/creatio-ai-knowledge-hub"
    cleanup = DuplicateCleanup(base_directory)
    cleanup.cleanup()
