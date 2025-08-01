#!/usr/bin/env python3
"""
Website Functionality Tester

Tests the website mirror after filename normalization to ensure:
- No broken links remain
- All referenced files exist
- Website structure is intact
- CSS, JS, and other assets are accessible
"""

import os
import re
import json
import urllib.parse
from pathlib import Path
from typing import Dict, List, Set, Tuple
import logging
from datetime import datetime
import argparse
from dataclasses import dataclass
from urllib.parse import urljoin, urlparse
import mimetypes

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

@dataclass
class LinkIssue:
    """Data class for tracking link issues"""
    source_file: str
    link: str
    issue_type: str
    line_number: int = 0
    context: str = ""

@dataclass
class TestResults:
    """Data class for test results"""
    total_files_tested: int = 0
    total_links_found: int = 0
    broken_links: List[LinkIssue] = None
    missing_files: Set[str] = None
    
    def __post_init__(self):
        if self.broken_links is None:
            self.broken_links = []
        if self.missing_files is None:
            self.missing_files = set()

class WebsiteTester:
    def __init__(self, root_directory: str, mapping_file: str = None):
        self.root_directory = Path(root_directory).resolve()
        self.mapping_file = mapping_file
        self.results = TestResults()
        
        # File extensions to test for link references
        self.testable_extensions = {'.html', '.htm', '.css', '.js', '.xml', '.json', '.txt', '.md'}
        
        # Common link patterns to search for
        self.link_patterns = [
            # HTML links
            re.compile(r'href=["\']([^"\']+)["\']', re.IGNORECASE),
            re.compile(r'src=["\']([^"\']+)["\']', re.IGNORECASE),
            # CSS links
            re.compile(r'url\(["\']?([^"\'()]+)["\']?\)', re.IGNORECASE),
            re.compile(r'@import\s+["\']([^"\']+)["\']', re.IGNORECASE),
            # JavaScript links
            re.compile(r'["\']([^"\']+\.(js|css|png|jpg|jpeg|gif|svg|ico|woff|woff2|ttf|eot))["\']', re.IGNORECASE),
            # General file references
            re.compile(r'["\']([^"\']*\.[a-zA-Z0-9]{1,6})["\']')
        ]
        
        # Skip these types of links
        self.skip_protocols = {'http://', 'https://', 'ftp://', 'mailto:', 'tel:', 'javascript:', 'data:'}
        self.skip_fragments = {'#', 'javascript:', 'mailto:'}
        
    def load_mapping_file(self) -> Dict[str, str]:
        """Load the filename mapping file if it exists"""
        if not self.mapping_file:
            return {}
            
        try:
            with open(self.mapping_file, 'r', encoding='utf-8') as f:
                mapping_data = json.load(f)
                return {
                    mapping['original_name']: mapping['normalized_name']
                    for mapping in mapping_data.get('mappings', [])
                }
        except Exception as e:
            logging.warning(f"Could not load mapping file {self.mapping_file}: {e}")
            return {}

    def extract_links_from_file(self, file_path: Path) -> List[Tuple[str, int, str]]:
        """Extract all links from a file"""
        if file_path.suffix.lower() not in self.testable_extensions:
            return []
            
        links = []
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                
            lines = content.split('\n')
            
            for pattern in self.link_patterns:
                for match in pattern.finditer(content):
                    link = match.group(1)
                    
                    # Skip certain types of links
                    if any(link.startswith(skip) for skip in self.skip_protocols):
                        continue
                    if any(fragment in link for fragment in self.skip_fragments):
                        continue
                    if link.startswith('#'):
                        continue
                        
                    # Find line number
                    line_num = content[:match.start()].count('\n') + 1
                    context = lines[line_num - 1].strip() if line_num <= len(lines) else ""
                    
                    links.append((link, line_num, context))
                    
        except Exception as e:
            logging.error(f"Error reading file {file_path}: {e}")
            
        return links

    def resolve_link_path(self, source_file: Path, link: str) -> Path:
        """Resolve a link relative to the source file"""
        try:
            # Handle URL-encoded links
            if '%' in link:
                link = urllib.parse.unquote(link)
                
            # Remove query strings and fragments
            if '?' in link:
                link = link.split('?')[0]
            if '#' in link:
                link = link.split('#')[0]
                
            # Skip empty links
            if not link.strip():
                return None
                
            # Resolve relative to source file directory
            if link.startswith('/'):
                # Absolute path from root
                return self.root_directory / link.lstrip('/')
            else:
                # Relative path
                return source_file.parent / link
                
        except Exception as e:
            logging.debug(f"Error resolving link {link}: {e}")
            return None

    def check_file_exists(self, file_path: Path) -> bool:
        """Check if a file exists, handling various cases"""
        if not file_path:
            return False
            
        # Try exact path
        if file_path.exists():
            return True
            
        # Try with index.html if it's a directory
        if file_path.is_dir():
            index_files = ['index.html', 'index.htm', 'default.html', 'default.htm']
            for index_file in index_files:
                if (file_path / index_file).exists():
                    return True
                    
        # Try case-insensitive search (for case-sensitive filesystems)
        try:
            parent_dir = file_path.parent
            filename = file_path.name
            
            if parent_dir.exists():
                for existing_file in parent_dir.iterdir():
                    if existing_file.name.lower() == filename.lower():
                        return True
        except Exception:
            pass
            
        return False

    def test_single_file(self, file_path: Path) -> List[LinkIssue]:
        """Test all links in a single file"""
        issues = []
        links = self.extract_links_from_file(file_path)
        
        for link, line_num, context in links:
            self.results.total_links_found += 1
            
            resolved_path = self.resolve_link_path(file_path, link)
            
            if resolved_path and not self.check_file_exists(resolved_path):
                issue = LinkIssue(
                    source_file=str(file_path),
                    link=link,
                    issue_type="broken_link",
                    line_number=line_num,
                    context=context
                )
                issues.append(issue)
                self.results.missing_files.add(str(resolved_path))
                
        return issues

    def scan_all_files(self) -> List[Path]:
        """Get all testable files in the directory"""
        files = []
        
        for file_path in self.root_directory.rglob('*'):
            if file_path.is_file() and not self.should_skip_file(file_path):
                if file_path.suffix.lower() in self.testable_extensions:
                    files.append(file_path)
                    
        return files

    def should_skip_file(self, file_path: Path) -> bool:
        """Check if a file should be skipped during testing"""
        # Skip hidden files and directories
        if any(part.startswith('.') for part in file_path.parts):
            return True
            
        # Skip system directories
        skip_dirs = {'__pycache__', '.git', '.svn', 'node_modules', 'venv', '.venv'}
        if any(skip_dir in file_path.parts for skip_dir in skip_dirs):
            return True
            
        return False

    def run_tests(self):
        """Run all website functionality tests"""
        logging.info("Starting website functionality tests")
        
        # Load mapping file for reference
        mappings = self.load_mapping_file()
        if mappings:
            logging.info(f"Loaded {len(mappings)} filename mappings")
            
        # Get all testable files
        files_to_test = self.scan_all_files()
        logging.info(f"Testing {len(files_to_test)} files")
        
        # Test each file
        all_issues = []
        for file_path in files_to_test:
            issues = self.test_single_file(file_path)
            all_issues.extend(issues)
            self.results.total_files_tested += 1
            
            if issues:
                logging.info(f"Found {len(issues)} issues in {file_path}")
                
        self.results.broken_links = all_issues
        logging.info(f"Testing completed. Found {len(all_issues)} broken links")

    def generate_report(self) -> str:
        """Generate a comprehensive test report"""
        report_lines = [
            "="*80,
            "WEBSITE FUNCTIONALITY TEST REPORT",
            "="*80,
            f"Test Date: {datetime.now().isoformat()}",
            f"Root Directory: {self.root_directory}",
            "",
            "SUMMARY:",
            f"  Files tested: {self.results.total_files_tested}",
            f"  Links found: {self.results.total_links_found}",
            f"  Broken links: {len(self.results.broken_links)}",
            f"  Missing files: {len(self.results.missing_files)}",
            ""
        ]
        
        if self.results.broken_links:
            report_lines.extend([
                "BROKEN LINKS DETAIL:",
                "-" * 40
            ])
            
            # Group by source file
            by_file = {}
            for issue in self.results.broken_links:
                if issue.source_file not in by_file:
                    by_file[issue.source_file] = []
                by_file[issue.source_file].append(issue)
                
            for source_file, issues in by_file.items():
                report_lines.append(f"\nFile: {source_file}")
                for issue in issues:
                    report_lines.append(f"  Line {issue.line_number}: {issue.link}")
                    if issue.context:
                        report_lines.append(f"    Context: {issue.context[:100]}...")
                        
        if self.results.missing_files:
            report_lines.extend([
                "",
                "MISSING FILES:",
                "-" * 40
            ])
            
            for missing_file in sorted(self.results.missing_files):
                report_lines.append(f"  {missing_file}")
                
        if not self.results.broken_links and not self.results.missing_files:
            report_lines.extend([
                "",
                "✓ ALL TESTS PASSED!",
                "  No broken links found.",
                "  All referenced files exist.",
                "  Website functionality appears intact."
            ])
            
        report_lines.append("\n" + "="*80)
        return "\n".join(report_lines)

    def save_report(self, report_content: str):
        """Save the test report to a file"""
        report_file = self.root_directory / 'website_test_report.txt'
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report_content)
            
        logging.info(f"Report saved to: {report_file}")
        return report_file

    def fix_common_issues(self):
        """Attempt to fix common link issues automatically"""
        if not self.results.broken_links:
            return
            
        logging.info("Attempting to fix common link issues...")
        fixes_applied = 0
        
        # Group issues by file for efficient processing
        by_file = {}
        for issue in self.results.broken_links:
            if issue.source_file not in by_file:
                by_file[issue.source_file] = []
            by_file[issue.source_file].append(issue)
            
        for source_file, issues in by_file.items():
            try:
                file_path = Path(source_file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                original_content = content
                
                for issue in issues:
                    # Try to find alternative files with similar names
                    resolved_path = self.resolve_link_path(file_path, issue.link)
                    if resolved_path:
                        alternatives = self.find_similar_files(resolved_path)
                        if alternatives:
                            # Use the first alternative
                            alt_path = alternatives[0]
                            relative_alt = os.path.relpath(alt_path, file_path.parent)
                            content = content.replace(issue.link, relative_alt)
                            fixes_applied += 1
                            
                # Save changes if any were made
                if content != original_content:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                        
            except Exception as e:
                logging.error(f"Error fixing issues in {source_file}: {e}")
                
        if fixes_applied > 0:
            logging.info(f"Applied {fixes_applied} automatic fixes")
        else:
            logging.info("No automatic fixes could be applied")

    def find_similar_files(self, missing_path: Path) -> List[Path]:
        """Find files with similar names to a missing file"""
        if not missing_path.parent.exists():
            return []
            
        similar_files = []
        missing_name = missing_path.name.lower()
        missing_stem = missing_path.stem.lower()
        missing_suffix = missing_path.suffix.lower()
        
        try:
            for existing_file in missing_path.parent.iterdir():
                if existing_file.is_file():
                    existing_name = existing_file.name.lower()
                    
                    # Exact match (case-insensitive)
                    if existing_name == missing_name:
                        similar_files.append(existing_file)
                        continue
                        
                    # Same extension, similar name
                    if (existing_file.suffix.lower() == missing_suffix and
                        existing_file.stem.lower().replace('_', ' ') == missing_stem.replace('_', ' ')):
                        similar_files.append(existing_file)
                        
        except Exception:
            pass
            
        return similar_files

def main():
    parser = argparse.ArgumentParser(description='Test website functionality after filename normalization')
    parser.add_argument('directory', help='Root directory of website mirror')
    parser.add_argument('--mapping-file', help='JSON file with filename mappings')
    parser.add_argument('--fix-issues', action='store_true',
                       help='Attempt to automatically fix common issues')
    
    args = parser.parse_args()
    
    # Validate directory
    if not os.path.isdir(args.directory):
        print(f"Error: {args.directory} is not a valid directory")
        return 1
        
    # Auto-detect mapping file if not provided
    mapping_file = args.mapping_file
    if not mapping_file:
        auto_mapping = os.path.join(args.directory, 'filename_mapping.json')
        if os.path.exists(auto_mapping):
            mapping_file = auto_mapping
            
    # Create tester and run tests
    tester = WebsiteTester(args.directory, mapping_file)
    
    try:
        tester.run_tests()
        
        if args.fix_issues:
            tester.fix_common_issues()
            
        # Generate and save report
        report_content = tester.generate_report()
        tester.save_report(report_content)
        
        # Print summary to console
        print(report_content)
        
        # Return appropriate exit code
        return 0 if not tester.results.broken_links else 1
        
    except KeyboardInterrupt:
        print("\nTesting cancelled by user")
        return 1
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return 1

if __name__ == '__main__':
    exit(main())
