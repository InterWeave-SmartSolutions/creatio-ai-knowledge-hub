#!/usr/bin/env python3
"""
Prepare and package all processed data for cloud storage backup.
"""

import tarfile
import zipfile
from pathlib import Path
from datetime import datetime
import json
import hashlib

def calculate_file_hash(filepath):
    """Calculate SHA256 hash of a file."""
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def create_backup_manifest():
    """Create a manifest of all files to be backed up."""
    manifest = {
        "backup_date": datetime.now().isoformat(),
        "project": "Creatio Training Courses Scraper",
        "files": []
    }
    
    # List all directories to backup
    backup_dirs = [
        "processed_data",
        "backups"
    ]
    
    # Add original data files
    backup_files = [
        "creatio_courses.json",
        "creatio_courses.csv",
        "course_page_raw.html",
        "creatio_main_page.html",
        "creatio_training_page.html",
        "process_data.py",
        "html_to_markdown.py"
    ]
    
    # Collect all files
    all_files = []
    
    # Add individual files
    for file in backup_files:
        if Path(file).exists():
            all_files.append(Path(file))
    
    # Add files from directories
    for dir_path in backup_dirs:
        if Path(dir_path).exists():
            all_files.extend(Path(dir_path).rglob("*"))
    
    # Process each file
    for file_path in all_files:
        if file_path.is_file():
            file_info = {
                "path": str(file_path),
                "size": file_path.stat().st_size,
                "modified": datetime.fromtimestamp(file_path.stat().st_mtime).isoformat(),
                "hash": calculate_file_hash(file_path)
            }
            manifest["files"].append(file_info)
    
    manifest["total_files"] = len(manifest["files"])
    manifest["total_size"] = sum(f["size"] for f in manifest["files"])
    
    # Save manifest
    with open("backup_manifest.json", "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
    
    print(f"Created backup manifest with {manifest['total_files']} files")
    print(f"Total size: {manifest['total_size'] / (1024*1024):.2f} MB")
    
    return manifest

def create_tar_backup():
    """Create a tar.gz backup of all data."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"creatio_courses_backup_{timestamp}.tar.gz"
    
    print(f"Creating tar backup: {backup_name}")
    
    with tarfile.open(backup_name, "w:gz") as tar:
        # Add directories
        tar.add("processed_data", arcname="processed_data")
        tar.add("backups", arcname="backups")
        
        # Add individual files
        files_to_add = [
            "creatio_courses.json",
            "creatio_courses.csv",
            "course_page_raw.html",
            "creatio_main_page.html",
            "creatio_training_page.html",
            "process_data.py",
            "html_to_markdown.py",
            "backup_manifest.json"
        ]
        
        for file in files_to_add:
            if Path(file).exists():
                tar.add(file, arcname=file)
    
    print(f"Created: {backup_name}")
    return backup_name

def create_zip_backup():
    """Create a zip backup of all data."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"creatio_courses_backup_{timestamp}.zip"
    
    print(f"Creating zip backup: {backup_name}")
    
    with zipfile.ZipFile(backup_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Add directories
        for dir_path in ["processed_data", "backups"]:
            if Path(dir_path).exists():
                for file_path in Path(dir_path).rglob("*"):
                    if file_path.is_file():
                        zipf.write(file_path, arcname=file_path)
        
        # Add individual files
        files_to_add = [
            "creatio_courses.json",
            "creatio_courses.csv",
            "course_page_raw.html",
            "creatio_main_page.html",
            "creatio_training_page.html",
            "process_data.py",
            "html_to_markdown.py",
            "backup_manifest.json"
        ]
        
        for file in files_to_add:
            if Path(file).exists():
                zipf.write(file, arcname=file)
    
    print(f"Created: {backup_name}")
    return backup_name

def create_cloud_ready_structure():
    """Create a cloud-ready directory structure."""
    cloud_dir = Path("cloud_backup")
    cloud_dir.mkdir(exist_ok=True)
    
    # Create README for cloud storage
    readme_content = f"""# Creatio Training Courses - Scraped Data Backup

## Backup Information
- **Date**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
- **Source**: Creatio Academy (https://academy.creatio.com)
- **Total Courses**: 33

## Directory Structure
```
cloud_backup/
├── data/
│   ├── json/          # Cleaned JSON data
│   ├── csv/           # CSV exports
│   └── html/          # Original HTML files
├── processed/
│   ├── markdown/      # Individual course Markdown files
│   ├── summaries/     # Category summaries
│   └── indexes/       # Navigation indexes
└── archives/
    ├── *.tar.gz       # Compressed backups
    └── *.zip          # Alternative format
```

## File Descriptions

### Data Files
- `creatio_courses.json` - Main scraped data in JSON format
- `creatio_courses.csv` - Same data in CSV format
- `cleaned_data.json` - Processed and deduplicated data

### Processed Files
- `markdown/` - Individual course files in Markdown format
- `summaries/` - Category-wise summaries
- `indexes/` - Navigation and category indexes

### Scripts
- `process_data.py` - Data processing script
- `html_to_markdown.py` - HTML to Markdown converter

## Usage
1. Download the entire backup or specific directories
2. Use the indexes for navigation
3. Markdown files are human-readable
4. JSON/CSV files can be imported into other tools

## Statistics
- Total unique courses: 33
- Categories: E-Learning, Instructor-led Training
- Data processed on: {datetime.now().strftime("%Y-%m-%d")}
"""
    
    with open(cloud_dir / "README.md", "w", encoding="utf-8") as f:
        f.write(readme_content)
    
    # Create subdirectories
    (cloud_dir / "data" / "json").mkdir(parents=True, exist_ok=True)
    (cloud_dir / "data" / "csv").mkdir(parents=True, exist_ok=True)
    (cloud_dir / "data" / "html").mkdir(parents=True, exist_ok=True)
    (cloud_dir / "processed").mkdir(exist_ok=True)
    (cloud_dir / "archives").mkdir(exist_ok=True)
    
    # Copy files to appropriate locations
    import shutil
    
    # Copy data files
    files_to_copy = {
        "creatio_courses.json": cloud_dir / "data" / "json" / "creatio_courses.json",
        "processed_data/cleaned_data.json": cloud_dir / "data" / "json" / "cleaned_data.json",
        "creatio_courses.csv": cloud_dir / "data" / "csv" / "creatio_courses.csv",
        "processed_data/cleaned_data.csv": cloud_dir / "data" / "csv" / "cleaned_data.csv",
        "course_page_raw.html": cloud_dir / "data" / "html" / "course_page_raw.html",
        "creatio_main_page.html": cloud_dir / "data" / "html" / "creatio_main_page.html",
        "creatio_training_page.html": cloud_dir / "data" / "html" / "creatio_training_page.html"
    }
    
    for src, dst in files_to_copy.items():
        if Path(src).exists():
            shutil.copy2(src, dst)
    
    # Copy processed data
    if Path("processed_data").exists():
        shutil.copytree("processed_data", cloud_dir / "processed", dirs_exist_ok=True)
    
    print(f"Created cloud-ready structure in: {cloud_dir}")
    return cloud_dir

def main():
    """Main backup preparation function."""
    print("Preparing backup for cloud storage...")
    print("=" * 50)
    
    # Create manifest
    manifest = create_backup_manifest()
    
    # Create compressed backups
    tar_backup = create_tar_backup()
    zip_backup = create_zip_backup()
    
    # Create cloud-ready structure
    cloud_dir = create_cloud_ready_structure()
    
    # Move archives to cloud directory
    import shutil
    if Path(tar_backup).exists():
        shutil.move(tar_backup, cloud_dir / "archives" / tar_backup)
    if Path(zip_backup).exists():
        shutil.move(zip_backup, cloud_dir / "archives" / zip_backup)
    if Path("backup_manifest.json").exists():
        shutil.copy2("backup_manifest.json", cloud_dir / "backup_manifest.json")
    
    print("\n" + "=" * 50)
    print("Backup preparation complete!")
    print(f"\nCloud backup directory: {cloud_dir}")
    print("\nNext steps:")
    print("1. Upload the 'cloud_backup' directory to your cloud storage")
    print("2. You can upload the entire directory or specific subdirectories")
    print("3. The archives in 'cloud_backup/archives' contain complete backups")
    print("\nRecommended cloud storage options:")
    print("- Google Drive")
    print("- Dropbox")
    print("- OneDrive")
    print("- AWS S3")
    print("- GitHub (for code and markdown files)")

if __name__ == "__main__":
    main()
