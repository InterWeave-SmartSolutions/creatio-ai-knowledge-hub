#!/usr/bin/env python3
"""
Test Document Processor functionality
"""

import sys
import tempfile
import os
from pathlib import Path

# Add the scripts utilities directory to path
sys.path.append(str(Path(__file__).parent / "scripts" / "utilities"))

from document_processor import DocumentProcessor

def create_test_files(test_dir):
    """Create sample test files for processing."""
    test_files = []
    
    # Create a test text file
    txt_file = test_dir / "sample.txt"
    with open(txt_file, 'w') as f:
        f.write("This is a sample text file for testing.\nIt contains multiple lines.\nAnd some basic content.")
    test_files.append(txt_file)
    
    # Create a test HTML file
    html_file = test_dir / "sample.html"
    with open(html_file, 'w') as f:
        f.write("""
        <html>
        <head><title>Sample HTML Document</title></head>
        <body>
            <h1>Test Document</h1>
            <p>This is a test HTML document.</p>
            <p>It contains <strong>formatted</strong> text.</p>
        </body>
        </html>
        """)
    test_files.append(html_file)
    
    # Create a test JSON file
    json_file = test_dir / "sample.json"
    with open(json_file, 'w') as f:
        f.write('{"name": "test", "type": "document", "content": "sample data"}')
    test_files.append(json_file)
    
    return test_files

def main():
    """Test the document processor."""
    print("Testing Document Processor...")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        test_dir = Path(temp_dir) / "test_files"
        test_dir.mkdir()
        
        output_dir = Path(temp_dir) / "output"
        
        # Create test files
        test_files = create_test_files(test_dir)
        print(f"Created {len(test_files)} test files")
        
        # Initialize document processor
        processor = DocumentProcessor(output_dir=str(output_dir))
        
        # Test individual file processing
        print("\nTesting individual file processing:")
        for test_file in test_files:
            print(f"Processing: {test_file.name}")
            result = processor.process_file(test_file)
            if result.get('success'):
                print(f"  ✓ Success: {result.get('method', 'Unknown method')}")
            else:
                print(f"  ✗ Failed: {result.get('error', 'Unknown error')}")
        
        # Test directory processing
        print(f"\nTesting directory processing:")
        result = processor.process_directory(test_dir)
        if result.get('success'):
            print(f"  ✓ Processed {result.get('files_processed', 0)} files")
            print(f"  Statistics: {result.get('statistics', {})}")
        else:
            print(f"  ✗ Failed: {result.get('error', 'Unknown error')}")
        
        # Generate and display report
        print(f"\nGenerating report...")
        report = processor.generate_report()
        print("Report preview:")
        print("=" * 50)
        print(report[:500] + "..." if len(report) > 500 else report)
        print("=" * 50)
        
        # List output files
        if output_dir.exists():
            output_files = list(output_dir.glob("*.md"))
            print(f"\nGenerated {len(output_files)} markdown files:")
            for output_file in output_files:
                print(f"  - {output_file.name}")
        
        print("\nDocument processor test completed!")

if __name__ == "__main__":
    main()
