#!/bin/bash

# Creatio Development Learning - Quick Start Script
# This script helps you get started with your Creatio development learning journey

echo "🚀 Welcome to Creatio Platform Development Learning!"
echo "=================================================="
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Please set up the environment first."
    exit 1
fi

echo "✅ Setting up your learning environment..."

# Activate virtual environment
source venv/bin/activate
echo "✅ Virtual environment activated"

# Check if MCP server is already running
if pgrep -f "enhanced_mcp_server.py" > /dev/null; then
    echo "✅ MCP server is already running"
else
    echo "🔄 Starting AI Knowledge Hub MCP server..."
    python ai_knowledge_hub/enhanced_mcp_server.py &
    sleep 3
    echo "✅ MCP server started on http://localhost:8001"
fi

echo ""
echo "📚 Your Learning Resources:"
echo "=========================="
echo "📹 Videos: ai_optimization/creatio-academy-db/developer_course/videos/"
echo "📄 PDFs: ai_optimization/creatio-academy-db/developer_course/pdfs/"
echo "🔍 AI Assistant: http://localhost:8001/docs"
echo "📖 Learning Guide: CREATIO_DEVELOPMENT_LEARNING_GUIDE.md"
echo ""

echo "🎯 Phase 1 - Week 1 Starting Point:"
echo "==================================="
echo "1. 📹 Watch: ai_optimization/creatio-academy-db/developer_course/videos/Recording1.mp4"
echo "2. 📄 Read: ai_optimization/creatio-academy-db/developer_course/pdfs/Creatio-Developer-1.pdf"
echo "3. 🔍 Use AI Assistant for questions: curl 'http://localhost:8001/api/v1/search?query=platform%20overview'"
echo ""

echo "💡 Quick Test - Search for 'creatio platform':"
echo "=============================================="
curl -s "http://localhost:8001/api/v1/search?query=creatio%20platform&limit=2" | python -m json.tool | head -20

echo ""
echo "🎉 You're all set! Follow the CREATIO_DEVELOPMENT_LEARNING_GUIDE.md for your complete learning path."
echo ""
echo "📋 Quick Commands:"
echo "=================="
echo "# Search the knowledge base:"
echo "curl 'http://localhost:8001/api/v1/search?query=YOUR_TOPIC&limit=5'"
echo ""
echo "# Find commands:"
echo "curl 'http://localhost:8001/api/v1/commands?search_term=YOUR_COMMAND'"
echo ""
echo "# Stop MCP server when done:"
echo "pkill -f enhanced_mcp_server.py"
echo ""
echo "Happy Learning! 🎓"
