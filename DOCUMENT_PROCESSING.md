# Document Processing System

## Overview

The Document Processing System is a comprehensive solution for extracting and
converting content from various file types to markdown format for AI
readability. This system supports multiple document formats and uses different
processing methods to ensure maximum text extraction accuracy.

## Supported File Types

### 1. PDF Documents

- **Extensions**: `.pdf`
- **Processing Methods**:
  1. **pdftotext** (Primary): Command-line tool for direct text extraction
  2. **PyPDF2** (Fallback): Python library for PDF text extraction
  3. **OCR with Tesseract** (Last resort): For scanned PDFs or when text
     extraction fails

### 2. Microsoft Office Documents

- **DOCX Files** (`.docx`, `.doc`):
  - Uses `python-docx` library
  - Extracts text content, tables, and formatting
- **PowerPoint Files** (`.pptx`, `.ppt`):
  - Uses `python-pptx` library
  - Extracts text from slides and tables
  - Preserves slide structure

### 3. Images

- **Extensions**: `.png`, `.jpg`, `.jpeg`, `.gif`, `.bmp`, `.tiff`, `.webp`
- **Processing Method**: Tesseract OCR
- **Features**:
  - Automatic image format conversion
  - English language text recognition
  - Metadata extraction

### 4. Videos

- **Extensions**: `.mp4`, `.avi`, `.mkv`, `.webm`, `.mov`, `.flv`, `.m4v`
- **Processing Method**: Whisper AI transcription
- **Features**:
  - Audio extraction using FFmpeg
  - Speech-to-text conversion
  - Timestamp-aware transcription
  - Multiple language support

### 5. Text Files

- **Extensions**: `.txt`, `.md`, `.rtf`, `.csv`
- **Processing Method**: Direct conversion
- **Features**: Preserves original formatting

### 6. Other Formats

- **HTML Files** (`.html`, `.htm`): BeautifulSoup parsing
- **XML Files** (`.xml`): Structure preservation
- **JSON Files** (`.json`): Pretty printing and formatting

## System Requirements

### System Dependencies

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install -y poppler-utils tesseract-ocr tesseract-ocr-eng ffmpeg

# For PDF to image conversion (if needed)
sudo apt install -y pdftoppm
```

### Python Dependencies

```bash
pip install python-docx python-pptx pytesseract pillow pypdf2 beautifulsoup4 whisper
```

## Installation

1. **Install system dependencies**:

   ```bash
   sudo apt update
   sudo apt install -y poppler-utils tesseract-ocr tesseract-ocr-eng ffmpeg
   ```

2. **Install Python packages**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Verify installation**:
   ```bash
   python test_document_processor.py
   ```

## Usage

### Command Line Interface

```bash
# Process a single file
python scripts/utilities/document_processor.py /path/to/document.pdf

# Process a directory
python scripts/utilities/document_processor.py /path/to/documents/ -r

# Specify output directory
python scripts/utilities/document_processor.py /path/to/documents/ -o /path/to/output/

# Generate processing report
python scripts/utilities/document_processor.py /path/to/documents/ --report
```

### Python API

```python
from document_processor import DocumentProcessor

# Initialize processor
processor = DocumentProcessor(output_dir="processed_documents")

# Process a single file
result = processor.process_file("/path/to/document.pdf")
if result['success']:
    print(f"Processed successfully: {result['output_file']}")
else:
    print(f"Processing failed: {result['error']}")

# Process entire directory
result = processor.process_directory("/path/to/documents", recursive=True)
print(f"Processed {result['files_processed']} files")

# Generate processing report
report = processor.generate_report()
print(report)
```

## Output Format

All processed documents are converted to standardized markdown format with:

### Document Header

```markdown
# filename.ext

**Document Type:** PDF Document **Source File:** /path/to/original/file
**Processing Method:** pdftotext **Processed Date:** 2025-07-23T15:12:02.393023
**File Size:** 1024 bytes

**Metadata:**

- **Pages:** 5
- **Size:** (1024, 768)

---
```

### Content Body

The extracted text content, cleaned and formatted for readability.

### Special Features

- **Video Transcripts**: Include timestamps for easy navigation
- **Tables**: Preserved in markdown table format
- **Code Blocks**: JSON and XML preserved with syntax highlighting

## Integration with Content Processor

The document processing system is fully integrated into the main content
processing pipeline:

1. **Website Crawling**: Discovers downloadable documents
2. **Resource Download**: Downloads PDFs, Office documents, images, etc.
3. **Document Processing**: Converts all documents to markdown
4. **AI Index Creation**: Includes processed documents in searchable content

### Pipeline Integration

```python
class CreatioContentProcessor:
    def process_documents(self):
        """Process all downloaded documents using the document processor."""
        result = self.doc_processor.process_directory(self.resources_dir, recursive=False)

        # Store results in main processing pipeline
        self.processed_files.setdefault("documents", {})
        for file_result in result.get('results', []):
            file_path = file_result['file']
            processing_result = file_result['result']

            if processing_result.get('success'):
                self.processed_files["documents"][file_path] = {
                    "markdown_file": processing_result.get('output_file'),
                    "method": processing_result.get('method'),
                    "processed_date": datetime.now().isoformat(),
                    "character_count": processing_result.get('character_count', 0)
                }
```

## Processing Statistics

The system provides comprehensive statistics:

```python
stats = processor.get_statistics()
print(f"Total processed: {stats['total_processed']}")
print(f"Success rate: {stats['success_rate']}")
print(f"Processing rate: {stats['processing_rate']}")
print(f"Files by type: {stats['by_type']}")
```

## Error Handling

The system includes robust error handling:

- **Graceful Degradation**: Falls back to alternative methods if primary fails
- **Detailed Logging**: Comprehensive logging for debugging
- **Progress Tracking**: Maintains processing state across runs
- **Error Reporting**: Clear error messages and recovery suggestions

## Performance Considerations

### Optimization Features

- **File Type Detection**: Efficient extension-based routing
- **Memory Management**: Streaming processing for large files
- **Parallel Processing**: Multi-file processing capability
- **Caching**: Avoids reprocessing existing files

### Recommended Settings

- **Batch Size**: Process 50-100 files at a time
- **Memory**: 4GB+ RAM for large document processing
- **Storage**: Ensure adequate space for temporary files

## Troubleshooting

### Common Issues

1. **pdftotext not found**:

   ```bash
   sudo apt install poppler-utils
   ```

2. **Tesseract not found**:

   ```bash
   sudo apt install tesseract-ocr tesseract-ocr-eng
   ```

3. **Python module not found**:

   ```bash
   pip install python-docx python-pptx pytesseract
   ```

4. **FFmpeg not available**:
   ```bash
   sudo apt install ffmpeg
   ```

### Log Analysis

Check processing logs for detailed error information:

```bash
tail -f processed_documents/document_processing.log
```

## Future Enhancements

### Planned Features

- **Additional Languages**: Multi-language OCR support
- **Advanced PDF**: Form field extraction
- **Excel Support**: Spreadsheet processing
- **Batch Optimization**: Improved large-scale processing
- **Cloud Integration**: S3/Google Drive support

### API Extensions

- **REST API**: HTTP endpoint for document processing
- **Webhook Support**: Notification system for completed processing
- **Queue Management**: Background processing with Redis

## Security Considerations

- **File Validation**: Extension and content type checking
- **Sandboxing**: Isolated processing environment
- **Memory Limits**: Prevents resource exhaustion
- **Access Control**: File permission validation

## License and Support

This document processing system is part of the Creatio AI Knowledge Hub project.
For support, issues, or feature requests, please refer to the main project
documentation.

---

_Last Updated: July 23, 2025_
