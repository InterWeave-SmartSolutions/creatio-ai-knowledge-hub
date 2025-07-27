# Creatio Academy Knowledge Database & MCP Server

A comprehensive knowledge management system for Creatio Academy content,
featuring AI-powered content processing, semantic search, and Model Context
Protocol (MCP) server integration for seamless AI agent access.

## 🌟 Complete System Overview

This system provides both **content processing capabilities** and a
**production-ready MCP server** for AI agents:

- 🌐 **Complete Content Processing**: Downloads and processes ALL content from
  academy.creatio.com
- 🎥 **Video Intelligence**: Full video transcription and AI-powered analysis
- 🚀 **MCP Server**: RESTful API with WebSocket support for real-time AI agent
  interaction
- 🔍 **Advanced Search**: Semantic search across all content types
- 📊 **Content Analytics**: AI-powered summaries, topic detection, and
  complexity assessment

## 🚀 Quick Start

### Run Complete Processing Pipeline

```bash
./run_complete_pipeline.sh run
```

This single command will:

1. Crawl all pages from academy.creatio.com
2. Extract all video URLs from every page
3. Download all videos with metadata
4. Transcribe all videos to text using AI
5. Convert all web pages to markdown
6. Download all resources (PDFs, docs, etc.)
7. Create comprehensive AI-readable index
8. Generate detailed processing report

### Check Status

```bash
./run_complete_pipeline.sh status
```

### Check Dependencies

```bash
./run_complete_pipeline.sh check
```

### Clean Cache

```bash
./run_complete_pipeline.sh clean
```

## 📁 Output Structure

After processing, all content will be organized in `processed_content/`:

```
processed_content/
├── 🎥 videos/                    # All downloaded videos
│   ├── video_id_title.mp4
│   ├── video_id_title.info.json
│   └── video_id_title.webp
├── 📝 transcripts/               # AI-generated transcriptions
│   ├── video_id_transcript.txt
│   └── video_id_detailed_transcript.json
├── 📄 pages/                     # Web pages as markdown
│   ├── page1.md
│   └── page2.md
├── 📋 resources/                 # Downloaded resources
│   ├── document1.pdf
│   └── image1.png
├── 🔍 ai_content_index.json      # Structured content index
├── 📖 searchable_content.txt     # Complete AI-readable content
└── 📊 processing_report.md       # Detailed processing report
```

## 🎯 Key Features

### Complete Content Coverage

- **Web Crawling**: Uses `wget` to recursively download all connected pages
- **Video Detection**: Finds videos from YouTube, Vimeo, direct MP4 links,
  iframes
- **Resource Extraction**: Downloads PDFs, documents, images, and other
  resources
- **Smart Organization**: Categorizes content by type and source

### AI-Powered Processing

- **Video Transcription**: Uses OpenAI Whisper for accurate speech-to-text
- **Content Conversion**: Converts HTML to clean markdown
- **Searchable Index**: Creates unified searchable content for AI analysis
- **Metadata Preservation**: Maintains source URLs, timestamps, and descriptions

### Robust Download System

- **Rate Limiting**: Prevents overwhelming servers
- **Retry Logic**: Handles temporary failures automatically
- **Progress Tracking**: Resumes interrupted downloads
- **Integrity Verification**: Validates downloaded content

## 🛠️ Technical Components

### Core Scripts

- `run_complete_pipeline.sh` - Master control script
- `content_processor.py` - Main Python processing engine
- `youtube_downloader.py` - Specialized YouTube video downloader
- `run_download.sh` - Video download management

### Dependencies

- **Python 3.8+** with virtual environment
- **wget** - Web crawling
- **yt-dlp** - Video downloading
- **ffmpeg** - Audio/video processing
- **OpenAI Whisper** - AI transcription
- **BeautifulSoup4** - HTML parsing
- **requests** - HTTP requests

## 📊 Processing Pipeline

### Phase 1: Discovery

1. Crawl academy.creatio.com recursively
2. Parse all HTML pages
3. Extract video URLs from all sources
4. Identify downloadable resources

### Phase 2: Content Download

1. Download all videos with metadata
2. Download all resources (PDFs, images, etc.)
3. Verify download integrity
4. Organize by category

### Phase 3: AI Processing

1. Extract audio from videos
2. Transcribe using Whisper AI
3. Convert HTML pages to markdown
4. Create structured metadata

### Phase 4: AI Optimization

1. Combine all content into searchable format
2. Create comprehensive index
3. Generate processing report
4. Optimize for AI queries

## 🔍 AI-Ready Output

The system produces several AI-optimized files:

### `searchable_content.txt`

- **Complete unified content** from all sources
- **Clean text format** optimized for AI processing
- **Structured sections** for pages and video transcripts
- **Source attribution** for all content

### `ai_content_index.json`

- **Structured metadata** for all processed content
- **File paths and relationships**
- **Processing timestamps and status**
- **Content summaries and statistics**

## 🎥 Video Processing Features

### Comprehensive Video Discovery

- YouTube embedded videos
- Direct video file links (.mp4, .webm, .mov)
- Vimeo embedded content
- iFrame video sources

### Rich Metadata Extraction

- Video titles and descriptions
- Upload dates and durations
- Thumbnail images
- Channel information
- View counts and ratings

### AI Transcription

- High-accuracy speech-to-text using Whisper
- Timestamped transcripts
- Multiple language support
- Automatic subtitle embedding

## 📈 Usage Statistics

After processing, you'll have access to:

- **Total pages processed**
- **Videos downloaded and transcribed**
- **Resources collected**
- **Total content volume**
- **Processing time and efficiency**

## 🔧 Advanced Usage

### Custom Processing

Edit `content_processor.py` to:

- Change crawling domains
- Modify video quality preferences
- Adjust transcription settings
- Customize output formats

### Manual Video Downloads

Use the standalone video downloader:

```bash
./run_download.sh start
```

### Selective Processing

Process specific content types by modifying the pipeline phases in the main
script.

## 🚨 Important Notes

### Processing Time

- **Complete processing can take several hours** depending on content volume
- **Video transcription is CPU-intensive** and takes time
- **Large files require significant disk space**

### Resource Requirements

- **Disk Space**: Several GB for complete content
- **CPU**: Multi-core recommended for faster transcription
- **Memory**: 8GB+ recommended for large video processing

### Network Considerations

- **Rate limiting is implemented** to be respectful of servers
- **Large downloads may take time** with rate limiting
- **Interrupted downloads can be resumed**

## 🎯 Perfect for AI Applications

The processed content is optimized for:

- **AI Training Data**: Clean, structured, and attributed
- **Knowledge Base Systems**: Searchable and cross-referenced
- **Content Analysis**: All formats unified and accessible
- **Research Applications**: Complete coverage with source tracking

---

**Ready to process all Creatio Academy content?**

Run: `./run_complete_pipeline.sh run`

The system will guide you through the complete processing pipeline and deliver
comprehensive, AI-ready content for analysis and learning.
