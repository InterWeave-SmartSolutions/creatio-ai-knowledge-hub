---
title: 'Quick Start Guide'
tags: [docs, setup]
description:
  'Auto-generated front matter for AI indexing. Improve this description.'
source_path: 'docs/setup/quick-start.md'
last_updated: '2025-08-06'
---

# Quick Start Guide

Get the Creatio AI Knowledge Hub running in 5 minutes with this step-by-step
guide.

## Prerequisites Checklist

Before starting, ensure you have:

- [ ] **Python 3.8+** installed
- [ ] **Git** installed
- [ ] **4GB+ RAM** available
- [ ] **2GB+ disk space** for initial setup
- [ ] **Internet connection** for dependencies

## 5-Minute Setup

### Step 1: Clone and Navigate

```bash
# Clone the repository
git clone https://github.com/your-org/creatio-ai-knowledge-hub.git
cd creatio-ai-knowledge-hub
```

### Step 2: Quick Environment Setup

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 3: Basic Configuration

```bash
# Copy environment template
cp .env.template .env

# Edit configuration (optional for quick start)
# nano .env
```

### Step 4: Initialize System

```bash
# Run initial setup
python -m ai_knowledge_hub.setup --quick-start

# Start the MCP server
python ai_knowledge_hub/enhanced_mcp_server.py
```

### Step 5: Verify Installation

```bash
# Test the server (in a new terminal)
curl http://localhost:8000/health

# Expected response:
# {"status": "healthy", "version": "1.0.0"}
```

## 🎉 You're Ready!

Your Creatio AI Knowledge Hub is now running at:

- **MCP Server**: http://localhost:8000
- **WebSocket**: ws://localhost:8001

## First Steps

### 1. Test Basic Search

```bash
# Search for content
curl "http://localhost:8000/mcp/search?q=Creatio%20installation"
```

### 2. Process Your First Content

```bash
# Add a video for processing
python -c "
from ai_knowledge_hub import VideoProcessor
processor = VideoProcessor()
result = processor.add_video_url('https://youtube.com/watch?v=YOUR_VIDEO_ID')
print(f'Added: {result}')
"
```

### 3. Explore the Interface

Open your browser and navigate to the web interface (if enabled):

- http://localhost:8000/docs (API documentation)

## Quick Configuration Options

### Essential Environment Variables

Edit `.env` file for basic configuration:

```bash
# OpenAI API Key (for enhanced features)
OPENAI_API_KEY=your_api_key_here

# Server Configuration
MCP_HOST=localhost
MCP_PORT=8000

# Processing Settings
MAX_CONCURRENT_PROCESSES=2
WHISPER_MODEL=base
```

### Quick Commands Reference

```bash
# Start services
./start_services.sh

# Process content
./run_complete_pipeline.sh run

# Check status
./run_complete_pipeline.sh status

# Stop services
./stop_services.sh
```

## Common First-Time Issues

### ❌ Port Already in Use

```bash
# Check what's using port 8000
lsof -i :8000

# Use different port
export MCP_PORT=8080
python ai_knowledge_hub/enhanced_mcp_server.py
```

### ❌ Dependencies Missing

```bash
# Install system dependencies (Ubuntu/Debian)
sudo apt update
sudo apt install python3-dev python3-pip ffmpeg

# Install system dependencies (macOS)
brew install python ffmpeg

# Reinstall Python packages
pip install --upgrade -r requirements.txt
```

### ❌ Permission Errors

```bash
# Fix permissions
chmod +x *.sh
sudo chown -R $USER:$USER .
```

### ❌ Database Initialization Failed

```bash
# Reset database
rm -f ai_knowledge_hub/knowledge_hub.db
python -m ai_knowledge_hub.setup --reset-db
```

## Next Steps

Now that you're up and running:

1. **📚 Add Content**: Start with the
   [Content Processing Guide](../components/content-processing.md)
2. **🔍 Search Setup**: Configure advanced search in
   [Search System Guide](../components/search-system.md)
3. **🎥 Video Processing**: Set up video processing in
   [Video Processing Guide](../components/video-processing.md)
4. **⚙️ Configuration**: Customize your setup in
   [Configuration Guide](configuration.md)

## Production Deployment

For production use, see the [Installation Guide](installation.md) for:

- Security configuration
- Performance optimization
- Monitoring setup
- Backup strategies

## Getting Help

If you encounter issues:

1. **Check logs**: `tail -f logs/mcp_server.log`
2. **Review troubleshooting**: [Troubleshooting Guide](troubleshooting.md)
3. **Test connectivity**: `python -m ai_knowledge_hub.diagnostics`
4. **Reset everything**: `./reset_system.sh`

## Verification Checklist

Confirm your setup is working:

- [ ] Server responds at http://localhost:8000/health
- [ ] Search API returns results
- [ ] Database is accessible
- [ ] Logs show no errors
- [ ] Can process basic content

---

**🚀 Congratulations!** You now have a fully functional Creatio AI Knowledge
Hub.

**Time to completion**: ~5 minutes  
**Next recommended read**: [Configuration Guide](configuration.md)
