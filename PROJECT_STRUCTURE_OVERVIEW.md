# Creatio Academy Knowledge Database - Project Structure Overview

## Overview

This project contains a comprehensive, AI-accessible knowledge database built
from the Creatio Academy websites. The project has been fully reorganized for
optimal searchability, maintainability, and AI integration.

## 🏗️ Final Project Structure

```
creatio-ai-knowledge-hub/
├── 📁 videos/                          # Video content and processing
│   ├── live_sessions/                  # Live stream recordings
│   ├── tutorials/                      # Tutorial videos
│   ├── transcripts/                    # Video transcriptions (TXT, JSON, SRT)
│   ├── summaries/                      # AI-generated summaries
│   └── metadata/                       # Video metadata (YAML, JSON)
│
├── 📁 documentation/                   # Documentation content
│   └── metadata/                       # Documentation metadata and manifests
│
├── 📁 scripts/                         # Python scripts organized by purpose
│   ├── core/                          # Core application scripts
│   │   ├── mcp_server.py              # MCP server implementation
│   │   ├── main.py                    # Main application entry
│   │   └── content_processor.py       # Content processing engine
│   └── utilities/                     # Utility scripts
│       ├── docs_8x_scraper.py         # Documentation scraper
│       ├── youtube_downloader.py      # Video downloader
│       ├── transcription_processor.py # Transcription processor
│       ├── filename_normalizer.py     # File normalizer
│       ├── website_tester.py          # Website validator
│       └── [other utilities]
│
├── 📁 search-index/                    # Search engine components
│   └── engines/                       # Search engine implementations
│       ├── semantic_search.py         # Semantic search engine
│       ├── faceted_search.py          # Faceted search engine
│       ├── autocomplete.py            # Autocomplete functionality
│       └── [other search components]
│
├── 📁 creatio-academy-archive/         # Raw archived content
│   ├── pages/raw/                     # Raw HTML pages
│   ├── resources/images/              # Downloaded images
│   ├── metadata/                      # Archive metadata
│   └── scripts/                       # Archive-specific scripts
│
├── 📁 creatio-academy-db/              # Structured knowledge database
│   ├── api/                          # API documentation structure
│   ├── code-examples/                # Code examples repository
│   ├── documentation/                # Structured documentation
│   └── search-index/                 # Search configuration
│
├── 📁 config/                          # Configuration files
├── 📁 venv/                           # Python virtual environment
└── 📄 [various config and log files]
```

## 🎯 Key Features

### 1. Video Processing Pipeline

- **Complete video archive**: All Creatio Academy videos downloaded and
  organized
- **AI transcriptions**: Using OpenAI Whisper for accurate transcription
- **Multiple formats**: TXT, JSON, SRT subtitle formats
- **AI summaries**: Generated summaries and key concept extraction
- **Rich metadata**: YAML and JSON metadata with timestamps, descriptions, tags

### 2. Documentation Archive

- **Complete documentation**: All pages from `academy.creatio.com/docs/8.x/`
- **1,004+ pages**: Comprehensive coverage of Creatio documentation
- **Organized structure**: Logical categorization and indexing
- **Search-ready**: Preprocessed for AI and search engine consumption

### 3. Search & AI Integration

- **Semantic search**: Vector-based semantic search using sentence transformers
- **Faceted search**: Multi-dimensional filtering capabilities
- **Autocomplete**: Smart suggestion system
- **MCP server**: Model Context Protocol server for AI agent integration
- **RESTful API**: FastAPI-based server with authentication and rate limiting

### 4. Clean Organization

- **No duplicates**: All duplicate files identified and removed (387+ duplicates
  cleaned)
- **Logical structure**: Clear separation of concerns
- **Easy navigation**: Hierarchical organization with indexes
- **Space optimized**: Redundant virtual environments and empty directories
  removed

## 📊 Content Statistics

### Video Content

- **Live Sessions**: 2 videos (creatio Live Stream recordings)
- **Tutorials**: 12+ tutorial videos covering various Creatio topics
- **Total Transcriptions**: All videos transcribed with timestamps
- **Summaries**: AI-generated summaries and key concepts extracted

### Documentation

- **Pages**: 1,004+ unique documentation pages
- **Topics Covered**:
  - Development on Creatio Platform
  - No-code Customization
  - Setup and Administration
  - Mobile Development
  - Creatio Apps

### Technical Assets

- **Images**: Thousands of screenshots and diagrams
- **Code Examples**: Extracted from documentation
- **Scripts**: 12+ utility and core scripts
- **Search Engines**: 5 different search implementations

## 🔧 Usage Guide

### Starting the MCP Server

```bash
cd /home/andrewwork/creatio-ai-knowledge-hub
source venv/bin/activate
python scripts/core/mcp_server.py
```

### Running Video Processing

```bash
python scripts/utilities/transcription_processor.py
```

### Searching Content

The search functionality is available through:

- **Semantic Search**: Vector-based similarity search
- **Faceted Search**: Multi-dimensional filtering
- **Autocomplete**: Smart suggestions
- **API Endpoints**: RESTful API access

### Accessing Documentation

- Raw HTML: `creatio-academy-archive/pages/raw/`
- Structured: `creatio-academy-db/documentation/`
- Search indexes: `search-index/`

## 📁 Important Files

### Configuration

- `config.yaml`: Main processing configuration
- `requirements.txt`: Python dependencies
- `video_sources.json`: Video source definitions

### Reports & Logs

- `final_structure_report.json`: Complete structure analysis
- `duplicate_files_report.json`: Duplicate file analysis
- `docs_8x_scraping_report.md`: Documentation scraping report
- `reorganization.log`: Reorganization process log
- `cleanup.log`: Cleanup process log

### Entry Points

- `scripts/core/mcp_server.py`: Main MCP server
- `scripts/core/main.py`: Alternative entry point
- `run_complete_pipeline.sh`: Complete processing pipeline
- `run_download.sh`: Video download pipeline

## 🔍 Search Capabilities

### Available Search Types

1. **Full-text search**: Traditional keyword-based search
2. **Semantic search**: AI-powered contextual search
3. **Faceted search**: Multi-dimensional filtering
4. **Code search**: Specialized code example search
5. **Video content search**: Searchable transcriptions

### API Endpoints

- `/content-search`: Main search endpoint
- `/video-transcripts`: Video transcription access
- `/code-examples`: Code example retrieval
- `/autocomplete`: Search suggestions
- `/documentation`: Documentation queries

## 🚀 Next Steps

### Immediate Use

The project is ready for:

- AI agent integration via MCP server
- Content search and retrieval
- Video transcription access
- Documentation querying

### Potential Enhancements

- Elasticsearch integration for advanced search
- Web interface for content browsing
- Additional video sources
- Real-time content updates
- Enhanced metadata extraction

## 📋 Maintenance

### Regular Tasks

- Update video content from YouTube
- Refresh documentation from website
- Rebuild search indexes
- Clean up logs and temporary files

### Monitoring

- Check `*.log` files for processing status
- Monitor disk space usage
- Verify search index integrity
- Test API endpoints

---

**Project Completed**: July 22, 2025 **Total Processing Time**: Multiple hours
of automated processing **Content Volume**: 1.4GB+ of organized, AI-accessible
knowledge

This project represents a comprehensive, AI-ready knowledge base of all Creatio
Academy content, optimized for search, retrieval, and integration with AI agents
and systems.
