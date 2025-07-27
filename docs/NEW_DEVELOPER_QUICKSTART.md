# 🚀 New Developer Quick Start Guide

Welcome to the Creatio AI Knowledge Hub! This guide will get you up and running in under 15 minutes.

## 📋 Prerequisites Checklist

Before you begin, ensure you have:

- [ ] **Python 3.8+** installed (`python --version`)
- [ ] **Git** installed (`git --version`)
- [ ] **4GB+ RAM** available
- [ ] **5GB+ disk space** for development setup
- [ ] **Internet connection** for dependencies
- [ ] **Code editor** (VS Code recommended)

## ⚡ 5-Minute Setup

### 1. Clone and Navigate
```bash
# Clone the repository
git clone https://github.com/your-org/creatio-ai-knowledge-hub.git
cd creatio-ai-knowledge-hub

# Verify project structure
ls -la
```

### 2. Environment Setup
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Verify activation (should show venv path)
which python
```

### 3. Install Core Dependencies
```bash
# Install minimum required packages for quick start
pip install fastapi uvicorn websockets python-multipart pydantic python-dotenv aiofiles sqlite3

# Verify installation
python -c "import fastapi, uvicorn, sqlite3; print('✅ Core dependencies installed')"
```

### 4. Database Check
```bash
# Verify database is accessible
python -c "
import sqlite3
conn = sqlite3.connect('ai_knowledge_hub/knowledge_hub.db')
cursor = conn.cursor()
cursor.execute('SELECT COUNT(*) FROM sqlite_master WHERE type=\"table\"')
print(f'✅ Database has {cursor.fetchone()[0]} tables')
conn.close()
"
```

### 5. Start Development Server
```bash
# Start the server in development mode
python -m uvicorn ai_knowledge_hub.enhanced_mcp_server:app --reload --port 8000

# You should see:
# INFO:     Uvicorn running on http://127.0.0.1:8000
```

### 6. Verify Setup
Open a new terminal and test:
```bash
# Test health endpoint
curl http://localhost:8000/health

# Expected response:
# {"status": "healthy", "version": "1.0.0", "timestamp": "..."}
```

## 🎉 You're Ready!

Your development environment is now set up! Here's what you have:

- **API Server**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs (when server is running)
- **Database**: SQLite database with existing content
- **Hot Reload**: Server automatically restarts when you make changes

## 🛠️ Development Workflow

### Making Your First Change

1. **Edit a file** (try changing the version in `ai_knowledge_hub/enhanced_mcp_server.py`)
2. **Save the file** (server will automatically reload)
3. **Test your change** by visiting http://localhost:8000/health

### Running Tests
```bash
# Install test dependencies
pip install pytest

# Run basic tests
python -c "
import sys, sqlite3, json
from pathlib import Path

print('🧪 Running basic tests...')

# Test 1: Database connectivity
try:
    conn = sqlite3.connect('ai_knowledge_hub/knowledge_hub.db')
    conn.close()
    print('✅ Database connection test passed')
except Exception as e:
    print(f'❌ Database test failed: {e}')

# Test 2: File structure
critical_files = ['README.md', 'ai_knowledge_hub/enhanced_mcp_server.py']
for file in critical_files:
    if Path(file).exists():
        print(f'✅ File exists: {file}')
    else:
        print(f'❌ Missing: {file}')

print('🎉 Basic tests complete!')
"
```

### Project Structure Overview
```
creatio-ai-knowledge-hub/
├── 📁 ai_knowledge_hub/          # Main application code
│   ├── enhanced_mcp_server.py    # FastAPI server
│   ├── knowledge_hub.db          # SQLite database
│   └── mcp_server_config.json    # Configuration
├── 📁 docs/                      # Documentation
│   ├── setup/                    # Setup guides
│   └── components/               # Component documentation
├── 📁 scripts/                   # Utility scripts
├── 📁 tests/                     # Test files
├── 📁 monitoring/                # Monitoring setup
├── requirements.txt              # Python dependencies
└── README.md                     # Project overview
```

## 🔧 Common Development Tasks

### Add a New API Endpoint
1. Open `ai_knowledge_hub/enhanced_mcp_server.py`
2. Add your new endpoint:
```python
@app.get("/api/v1/my-endpoint")
async def my_new_endpoint():
    return {"message": "Hello from my new endpoint!"}
```
3. Test: `curl http://localhost:8000/api/v1/my-endpoint`

### Query the Database
```python
import sqlite3

# Connect to database
conn = sqlite3.connect('ai_knowledge_hub/knowledge_hub.db')
cursor = conn.cursor()

# List all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print("Tables:", tables)

# Query content
cursor.execute("SELECT COUNT(*) FROM content LIMIT 5")
content_count = cursor.fetchone()[0]
print(f"Content records: {content_count}")

conn.close()
```

### View API Documentation
1. Start the server: `python -m uvicorn ai_knowledge_hub.enhanced_mcp_server:app --reload`
2. Open browser: http://localhost:8000/docs
3. Explore the interactive API documentation

## 🚨 Troubleshooting

### Server Won't Start
```bash
# Check if port is in use
lsof -i :8000

# Kill process if needed
kill -9 <PID>

# Start on different port
python -m uvicorn ai_knowledge_hub.enhanced_mcp_server:app --port 8001
```

### Import Errors
```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install --upgrade fastapi uvicorn

# Check Python path
python -c "import sys; print(sys.path)"
```

### Database Issues
```bash
# Check database file exists
ls -la ai_knowledge_hub/knowledge_hub.db

# Test database manually
sqlite3 ai_knowledge_hub/knowledge_hub.db ".tables"
```

### Permission Errors
```bash
# Fix file permissions
chmod +x scripts/*.sh

# Fix directory permissions
chmod 755 ai_knowledge_hub/
```

## 📚 Next Steps

Now that you're set up, explore these areas:

### 1. **Learn the Codebase** (30 minutes)
- Read `README.md` for project overview
- Explore `ai_knowledge_hub/enhanced_mcp_server.py` for main server logic
- Check `docs/components/` for detailed component documentation

### 2. **Make Your First Contribution** (60 minutes)
- Find an issue labeled "good first issue" 
- Create a new branch: `git checkout -b feature/my-feature`
- Make your changes and test locally
- Submit a pull request

### 3. **Set Up Full Development Environment** (60 minutes)
- Install all dependencies: `pip install -r requirements.txt`
- Set up monitoring: `./scripts/setup-monitoring.sh`
- Run full test suite: `./scripts/run-tests.sh`

### 4. **Advanced Topics**
- [🏗️ Architecture Overview](docs/architecture/README.md)
- [🔍 Search System](docs/components/search-system.md)
- [🎥 Video Processing](docs/components/video-processing.md)
- [🔧 Configuration Guide](docs/setup/configuration.md)

## 🆘 Getting Help

### Quick Help Commands
```bash
# Check system health
python -c "
import sqlite3, requests
try:
    # Test database
    conn = sqlite3.connect('ai_knowledge_hub/knowledge_hub.db')
    conn.close()
    print('✅ Database OK')
    
    # Test server (if running)
    resp = requests.get('http://localhost:8000/health', timeout=5)
    print('✅ Server OK' if resp.status_code == 200 else '❌ Server Issue')
except Exception as e:
    print(f'⚠️ Issue detected: {e}')
"

# Run diagnostics
./scripts/smoke-tests.sh development

# Reset environment (if stuck)
deactivate
rm -rf venv
python -m venv venv
source venv/bin/activate
```

### Documentation
- **Detailed Setup**: [docs/setup/installation.md](docs/setup/installation.md)
- **Troubleshooting**: [docs/setup/troubleshooting.md](docs/setup/troubleshooting.md)
- **API Reference**: [docs/api/README.md](docs/api/README.md)

### Community Support
- **GitHub Issues**: Report bugs and request features
- **Discussions**: Ask questions and share ideas
- **Wiki**: Community-maintained documentation

## ✅ Success Checklist

Before you start development, ensure:

- [ ] Server starts without errors
- [ ] Health endpoint responds: `curl http://localhost:8000/health`
- [ ] Database is accessible
- [ ] You can make a simple code change and see it reflected
- [ ] Tests run successfully
- [ ] You understand the project structure

## 🎯 Development Best Practices

### Code Quality
- Follow PEP 8 style guide
- Add docstrings to functions
- Write tests for new features
- Use type hints where possible

### Git Workflow
- Create feature branches: `git checkout -b feature/description`
- Make small, focused commits
- Write clear commit messages
- Test before pushing

### Testing
- Run tests before committing: `python -m pytest`
- Add tests for new functionality
- Check code coverage
- Test API endpoints manually

---

**🚀 Ready to contribute?** You're all set! Start by exploring the codebase and finding an area that interests you.

**⏱️ Total setup time**: ~10-15 minutes  
**🎯 Next step**: Read the [Architecture Overview](docs/architecture/README.md) to understand how everything fits together.

Welcome to the team! 🎉
