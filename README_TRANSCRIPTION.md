# Video Transcription and Metadata Generation System

## Overview

This comprehensive system provides automated video-to-text transcription and
metadata extraction for educational and business content. Built specifically for
processing Creatio Academy videos, it uses OpenAI's Whisper for accurate
speech-to-text conversion and generates structured metadata files with
AI-powered analysis.

## Features

### 🎯 Core Functionality

- **Automated Transcription**: Uses OpenAI Whisper for accurate speech-to-text
  conversion
- **Multiple Output Formats**: Plain text, JSON, SRT subtitles, and YAML
  metadata
- **Batch Processing**: Process entire directories of video files
- **YouTube Integration**: Extracts metadata from YouTube info.json files
- **Structured Metadata**: Comprehensive metadata including video properties,
  content analysis, and AI insights

### 🤖 AI-Powered Analysis

- **Content Classification**: Automatically categorizes content (tutorial, demo,
  presentation, etc.)
- **Topic Extraction**: Identifies key topics and concepts discussed
- **Keyword Analysis**: Extracts and ranks important terms and phrases
- **Action Items**: Identifies instructions and actionable items
- **Audience Analysis**: Assesses target audience and complexity level
- **Quality Assessment**: Evaluates transcription quality and content clarity

### 📊 Metadata Structure

- **Video Information**: File properties, duration, size, creation dates
- **Content Metadata**: Title, description, categories, tags, topics
- **Source Information**: Channel, uploader, upload date, original URL
- **Processing Information**: Model used, processing time, quality metrics
- **AI Analysis**: Summary, keywords, topics, complexity assessment

## Installation

### Prerequisites

- Python 3.8 or higher
- FFmpeg (for video processing)
- Virtual environment (recommended)

### Setup

```bash
# Clone or download the system files
cd /path/to/your/video/directory

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install required packages
pip install openai-whisper pyyaml tqdm

# Make scripts executable
chmod +x *.py
```

## Quick Start

### Basic Usage

```bash
# Process all videos in current directory
python batch_transcribe.py .

# Process specific directory with enhanced analysis
python batch_transcribe.py ./videos --enhance

# Process with larger model for better accuracy
python batch_transcribe.py ./videos --model large

# Test with limited files
python batch_transcribe.py ./videos --max-files 3 --dry-run
```

### Advanced Usage

```bash
# Force reprocess existing files with custom output directory
python batch_transcribe.py ./videos --force --output ./results

# Process with enhanced summaries and verbose logging
python batch_transcribe.py ./videos --enhance --verbose
```

## File Structure

### Input

The system processes various video formats:

- MP4, MKV, AVI, MOV, WEBM, FLV, M4V, WMV
- Accompanying `.info.json` files (from YouTube downloads)

### Output Structure

```
transcriptions/
├── transcripts/
│   ├── video_name_transcript.txt       # Plain text transcription
│   ├── video_name_transcription.json   # Full transcription with timestamps
│   └── video_name_subtitles.srt        # SRT subtitle format
├── metadata/
│   ├── video_name_metadata.yaml        # Human-readable metadata
│   └── video_name_metadata.json        # Machine-readable metadata
├── summaries/
│   ├── video_name_summary.json         # Basic summary
│   └── video_name_enhanced_summary.json # AI-enhanced analysis
└── processing_report.json              # Processing summary
```

## Configuration

### Whisper Models

- **tiny**: Fastest, least accurate (~37MB)
- **base**: Good balance of speed and accuracy (~139MB)
- **small**: Better accuracy (~242MB)
- **medium**: High accuracy (~769MB)
- **large**: Best accuracy (~1550MB)

### Configuration File

Edit `config.yaml` to customize:

- Output formats and naming patterns
- Processing settings and thresholds
- Topic detection keywords
- Quality assessment parameters

## Command Line Options

### batch_transcribe.py

```bash
usage: batch_transcribe.py [-h] [--model {tiny,base,small,medium,large}]
                           [--output OUTPUT] [--max-files MAX_FILES]
                           [--enhance] [--force] [--verbose] [--dry-run]
                           input_directory

Options:
  input_directory    Directory containing video files to process
  --model MODEL      Whisper model size (default: base)
  --output OUTPUT    Output directory (default: transcriptions)
  --max-files N      Maximum number of files to process
  --enhance          Generate enhanced summaries with LLM analysis
  --force            Force reprocessing of existing files
  --verbose          Enable verbose logging
  --dry-run          Show what would be processed without processing
```

### transcription_processor.py

```bash
usage: transcription_processor.py [-h] [--model {tiny,base,small,medium,large}]
                                  [--output OUTPUT] [--max-files MAX_FILES]
                                  directory

Standalone processor for individual use.
```

### llm_summarizer.py

```bash
usage: llm_summarizer.py [-h] transcriptions_dir

Enhance existing transcriptions with AI analysis.
```

## Output Examples

### Plain Text Transcript

```
This tutorial covers the basics of Creatio CRM configuration.
We'll walk through setting up your first business process...
```

### Metadata YAML

```yaml
video_info:
  filename: 'creatio_tutorial.mp4'
  duration_seconds: 1200
  file_size_mb: 45.2
content_metadata:
  title: 'Creatio CRM Setup Tutorial'
  language: 'en'
  topics: ['crm', 'configuration', 'tutorial']
  key_concepts: ['business process', 'setup', 'configuration']
processing_info:
  transcription_model: 'base'
  transcription_quality: 'good'
  word_count: 850
ai_analysis:
  summary: 'This tutorial teaches users how to configure...'
  key_topics: ['crm', 'configuration']
  estimated_reading_time_minutes: 4
```

### Enhanced Summary

```json
{
  "executive_summary": "This tutorial covers Creatio CRM configuration...",
  "key_points": [
    "Set up business processes for automation",
    "Configure user roles and permissions",
    "Customize dashboard layouts"
  ],
  "technical_concepts": ["CRM", "API", "workflow", "automation"],
  "content_structure": {
    "type": "tutorial",
    "estimated_complexity": "medium"
  },
  "audience_analysis": {
    "target_audience": "intermediate",
    "prerequisite_knowledge": ["CRM system familiarity"]
  }
}
```

## Best Practices

### Processing Guidelines

1. **Start Small**: Test with `--max-files 3` and `--dry-run` first
2. **Model Selection**: Use `base` model for most content, `large` for critical
   accuracy
3. **Storage**: Ensure adequate disk space (transcriptions ~5-10% of video size)
4. **Performance**: Process videos in small batches for better monitoring

### Quality Optimization

1. **Audio Quality**: Better source audio = better transcriptions
2. **Language**: Specify `--language` if auto-detection is poor
3. **Duration**: Very short videos (<30 seconds) may have poor results
4. **Content Type**: Technical content may require manual review

## Troubleshooting

### Common Issues

**Empty Transcriptions**

- Check if video has audible speech
- Try larger Whisper model
- Verify video file is not corrupted

**Poor Quality Detection**

- Audio may be unclear or very short
- Check `transcription_quality` in metadata
- Consider manual verification for critical content

**Memory Issues**

- Use smaller Whisper model (`tiny` or `base`)
- Process fewer files simultaneously
- Close other applications during processing

**File Permissions**

- Ensure scripts are executable: `chmod +x *.py`
- Check write permissions in output directory

### Log Files

- Check `transcription_processor.log` for detailed processing logs
- Review `batch_transcription.log` for batch processing issues
- Processing reports saved in output directory

## Integration

### With Other Systems

The structured metadata can be easily integrated with:

- Content Management Systems
- Learning Management Systems
- Search and Discovery Platforms
- Analytics and Reporting Tools

### API Potential

The system is designed to be easily adapted for:

- Web service APIs
- Automated pipeline integration
- Cloud processing workflows
- Custom business logic

## Advanced Features

### Custom Topic Detection

Modify topic keywords in `config.yaml`:

```yaml
topic_keywords:
  custom_topic:
    - 'keyword1'
    - 'keyword2'
```

### LLM Integration

The system is prepared for integration with:

- OpenAI GPT models
- Anthropic Claude
- Local LLM deployments
- Custom analysis pipelines

### Batch Operations

Process multiple directories:

```bash
for dir in video_dir1 video_dir2 video_dir3; do
  python batch_transcribe.py "$dir" --output "results/$dir"
done
```

## Performance Metrics

### Processing Speed (approximate)

- **tiny model**: ~2x real-time
- **base model**: ~1x real-time
- **large model**: ~0.5x real-time

### Accuracy (typical)

- **Clear speech**: 90-95% accuracy
- **Technical content**: 80-90% accuracy
- **Poor audio**: 60-80% accuracy

## Contributing

### Code Structure

- `transcription_processor.py`: Core processing logic
- `llm_summarizer.py`: AI analysis and enhancement
- `batch_transcribe.py`: Batch processing interface
- `config.yaml`: Configuration settings

### Adding Features

1. Extend metadata structure in processor
2. Add analysis functions in summarizer
3. Update configuration options
4. Test with sample videos

## License and Credits

- Built on OpenAI Whisper (MIT License)
- Uses PyYAML, tqdm, and other open-source libraries
- Designed for Creatio Academy content processing

## Support

For questions or issues:

1. Check troubleshooting section
2. Review log files for error details
3. Test with smaller/simpler video files
4. Verify all dependencies are installed

---

**Version**: 1.0  
**Last Updated**: January 2025  
**Compatible with**: Python 3.8+, Whisper 20240930+
