---
title: '🔧 Troubleshooting FAQ'
tags: [docs]
description:
  'Auto-generated front matter for AI indexing. Improve this description.'
source_path: 'docs/TROUBLESHOOTING_FAQ.md'
last_updated: '2025-08-06'
---

# 🔧 Troubleshooting FAQ

Comprehensive troubleshooting guide with solutions for common issues in the
Creatio AI Knowledge Hub.

## 🚨 Critical Issues

### Q: Server won't start - "Address already in use" error

**Symptoms**: `OSError: [Errno 98] Address already in use` when starting the
server

**Solutions**:

```bash
# Method 1: Find and kill the process using port 8000
lsof -i :8000
kill -9 <PID>

# Method 2: Use a different port
python -m uvicorn ai_knowledge_hub.enhanced_mcp_server:app --port 8001

# Method 3: Kill all Python processes (use carefully)
pkill -f python
```

**Prevention**: Always stop the server properly with `Ctrl+C` instead of closing
the terminal.

---

### Q: Database locked error

**Symptoms**: `sqlite3.OperationalError: database is locked`

**Solutions**:

```bash
# Method 1: Check for open connections
lsof ai_knowledge_hub/knowledge_hub.db

# Method 2: Kill processes accessing the database
ps aux | grep python | grep -v grep
kill -9 <PID>

# Method 3: Restart the system (last resort)
sudo reboot
```

**Root Cause**: Multiple processes trying to access SQLite database
simultaneously.

---

### Q: Import errors - "No module named 'fastapi'"

**Symptoms**: `ModuleNotFoundError: No module named 'fastapi'`

**Solutions**:

```bash
# Check if virtual environment is activated
which python  # Should show path to venv/bin/python

# Activate virtual environment
source venv/bin/activate  # Linux/Mac
# OR
venv\Scripts\activate  # Windows

# Install missing dependencies
pip install fastapi uvicorn

# Verify installation
python -c "import fastapi; print('✅ FastAPI installed')"
```

**Root Cause**: Virtual environment not activated or dependencies not installed.

---

## 🗄️ Database Issues

### Q: Database file not found

**Symptoms**: `sqlite3.OperationalError: unable to open database file`

**Solutions**:

```bash
# Check if database file exists
ls -la ai_knowledge_hub/knowledge_hub.db

# If missing, check if you're in the right directory
pwd  # Should end with creatio-ai-knowledge-hub

# Navigate to project root
cd /path/to/creatio-ai-knowledge-hub

# Create empty database if needed (advanced)
python -c "
import sqlite3
conn = sqlite3.connect('ai_knowledge_hub/knowledge_hub.db')
conn.execute('CREATE TABLE IF NOT EXISTS content (id INTEGER PRIMARY KEY)')
conn.close()
print('✅ Database created')
"
```

---

### Q: Database corruption

**Symptoms**: `sqlite3.DatabaseError: database disk image is malformed`

**Solutions**:

```bash
# Check database integrity
sqlite3 ai_knowledge_hub/knowledge_hub.db "PRAGMA integrity_check;"

# If corrupted, backup and recreate
cp ai_knowledge_hub/knowledge_hub.db ai_knowledge_hub/knowledge_hub.db.backup
sqlite3 ai_knowledge_hub/knowledge_hub.db ".dump" | sqlite3 new_database.db
mv new_database.db ai_knowledge_hub/knowledge_hub.db
```

---

### Q: No data in search results

**Symptoms**: API returns empty results even for broad searches

**Solutions**:

```bash
# Check if database has content
sqlite3 ai_knowledge_hub/knowledge_hub.db "SELECT COUNT(*) FROM content;"

# If empty, you may need to process content
./run_complete_pipeline.sh run

# Check search index
ls -la ai_knowledge_hub/search_index/

# Rebuild search index if needed
python -c "
from ai_knowledge_hub import SearchIndexer
indexer = SearchIndexer()
indexer.build_indexes()
"
```

---

## 🌐 Network and API Issues

### Q: API endpoints return 500 Internal Server Error

**Symptoms**: All API calls return HTTP 500 status

**Diagnostic Steps**:

```bash
# Check server logs
tail -f logs/mcp_server.log

# Test with verbose error output
python -m uvicorn ai_knowledge_hub.enhanced_mcp_server:app --log-level debug

# Test specific endpoint
curl -v http://localhost:8000/health
```

**Common Causes & Solutions**:

- **Database connection**: Restart server after database is available
- **Missing dependencies**: `pip install -r requirements.txt`
- **Configuration error**: Check `ai_knowledge_hub/mcp_server_config.json`

---

### Q: CORS errors in browser

**Symptoms**: `Access-Control-Allow-Origin` errors when accessing from web app

**Solution**:

```python
# Add to enhanced_mcp_server.py
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

### Q: Slow API responses

**Symptoms**: API calls take >10 seconds to respond

**Performance Optimization**:

```bash
# Check database size
du -h ai_knowledge_hub/knowledge_hub.db

# Optimize database
sqlite3 ai_knowledge_hub/knowledge_hub.db "VACUUM; ANALYZE;"

# Add database indexes (if not present)
sqlite3 ai_knowledge_hub/knowledge_hub.db "
CREATE INDEX IF NOT EXISTS idx_content_type ON content(type);
CREATE INDEX IF NOT EXISTS idx_content_source ON content(source);
"

# Monitor resource usage
top -p $(pgrep -f mcp_server)
```

---

## 🐍 Python Environment Issues

### Q: Wrong Python version

**Symptoms**: `SyntaxError` or features not working as expected

**Solutions**:

```bash
# Check Python version
python --version  # Should be 3.8+

# Check virtual environment Python
source venv/bin/activate
which python
python --version

# Create new virtual environment with specific Python version
python3.9 -m venv venv39
source venv39/bin/activate
```

---

### Q: Virtual environment issues

**Symptoms**: Packages installed globally instead of in venv

**Solutions**:

```bash
# Check if venv is activated (should show (venv) in prompt)
echo $VIRTUAL_ENV

# Recreate virtual environment
deactivate
rm -rf venv
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

### Q: Permission denied errors

**Symptoms**: `PermissionError` when running scripts or accessing files

**Solutions**:

```bash
# Fix script permissions
chmod +x scripts/*.sh

# Fix directory permissions
chmod 755 ai_knowledge_hub/
chmod 644 ai_knowledge_hub/*.py

# Fix ownership (if running as wrong user)
sudo chown -R $USER:$USER .
```

---

## 💾 Installation and Setup Issues

### Q: pip install fails with compiler errors

**Symptoms**: `error: Microsoft Visual C++ 14.0 is required` (Windows) or `gcc`
errors (Linux)

**Solutions**:

**Windows**:

```bash
# Install Visual Studio Build Tools
# Download from: https://visualstudio.microsoft.com/visual-cpp-build-tools/

# Or use pre-compiled wheels
pip install --only-binary=all package_name
```

**Linux/Mac**:

```bash
# Install build tools
# Ubuntu/Debian:
sudo apt-get install build-essential python3-dev

# CentOS/RHEL:
sudo yum groupinstall "Development Tools"
sudo yum install python3-devel

# macOS:
xcode-select --install
```

---

### Q: Docker-related issues

**Symptoms**: Docker commands fail or containers won't start

**Solutions**:

```bash
# Check Docker daemon is running
docker --version
docker ps

# Fix Docker permissions (Linux)
sudo usermod -aG docker $USER
newgrp docker

# Clean up Docker resources
docker system prune -a

# Rebuild Docker image
docker build --no-cache -t creatio-ai-hub .
```

---

## 🔍 Search and Content Issues

### Q: Search returns irrelevant results

**Symptoms**: Search queries return unrelated content

**Solutions**:

```bash
# Check search index status
python -c "
import os
search_dir = 'ai_knowledge_hub/search_index'
if os.path.exists(search_dir):
    files = os.listdir(search_dir)
    print(f'Search index files: {files}')
else:
    print('Search index directory missing')
"

# Rebuild search index with better configuration
python -c "
from ai_knowledge_hub import SearchIndexer
indexer = SearchIndexer()
indexer.rebuild_with_optimization()
"
```

---

### Q: Video processing fails

**Symptoms**: Video transcription or processing errors

**Solutions**:

```bash
# Check ffmpeg installation
ffmpeg -version

# Install ffmpeg if missing
# Ubuntu/Debian:
sudo apt-get install ffmpeg

# macOS:
brew install ffmpeg

# Windows: Download from https://ffmpeg.org/

# Test video processing manually
python -c "
import subprocess
result = subprocess.run(['ffmpeg', '-version'], capture_output=True)
print('✅ FFmpeg available' if result.returncode == 0 else '❌ FFmpeg missing')
"
```

---

## 🎛️ Configuration Issues

### Q: Environment variables not loading

**Symptoms**: App uses default values instead of configured values

**Solutions**:

```bash
# Check if .env file exists
ls -la .env

# Create .env file if missing
cat > .env << EOF
OPENAI_API_KEY=your_key_here
MCP_HOST=localhost
MCP_PORT=8000
DEBUG=true
EOF

# Verify environment variables are loaded
python -c "
import os
from dotenv import load_dotenv
load_dotenv()
print('API Key:', 'Set' if os.getenv('OPENAI_API_KEY') else 'Not set')
print('Debug:', os.getenv('DEBUG', 'Not set'))
"
```

---

### Q: JSON configuration file errors

**Symptoms**: `JSONDecodeError` when loading configuration

**Solutions**:

```bash
# Validate JSON syntax
python -m json.tool ai_knowledge_hub/mcp_server_config.json

# Fix common JSON issues
# - Remove trailing commas
# - Ensure proper quotes (double quotes only)
# - Check for missing brackets/braces

# Reset to default configuration
cp config/defaults/mcp_server_config.json ai_knowledge_hub/
```

---

## 🧪 Testing Issues

### Q: Tests fail in CI but pass locally

**Common Causes & Solutions**:

**1. Environment Differences**:

```bash
# Use consistent Python version
python --version

# Check installed packages
pip freeze > local_requirements.txt
# Compare with CI environment
```

**2. Time-dependent tests**:

```python
# Use fixed timestamps in tests
from freezegun import freeze_time

@freeze_time("2024-01-01")
def test_time_dependent_function():
    pass
```

**3. Race conditions**:

```python
# Add proper test isolation
import pytest

@pytest.fixture(autouse=True)
def cleanup():
    # Setup
    yield
    # Cleanup
```

---

### Q: Performance tests fail

**Symptoms**: Tests timeout or fail performance thresholds

**Solutions**:

```bash
# Run performance tests locally
./scripts/run-tests.sh performance

# Adjust performance thresholds
# Edit tests/performance/locustfile.py

# Profile slow functions
python -m cProfile -o profile.stats your_script.py
python -c "
import pstats
p = pstats.Stats('profile.stats')
p.sort_stats('cumulative').print_stats(10)
"
```

---

## 📊 Real-time Diagnostics

### Quick Health Check Script

```bash
#!/bin/bash
# Save as quick_diagnosis.sh

echo "🔍 Quick System Diagnosis"
echo "========================"

# Check Python environment
echo "1. Python Environment:"
python --version
echo "Virtual env: ${VIRTUAL_ENV:-Not activated}"

# Check key files
echo -e "\n2. Critical Files:"
for file in "ai_knowledge_hub/enhanced_mcp_server.py" "ai_knowledge_hub/knowledge_hub.db"; do
    if [ -f "$file" ]; then
        echo "✅ $file"
    else
        echo "❌ $file MISSING"
    fi
done

# Check database
echo -e "\n3. Database Status:"
python -c "
import sqlite3
try:
    conn = sqlite3.connect('ai_knowledge_hub/knowledge_hub.db')
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM sqlite_master WHERE type=\"table\"')
    count = cursor.fetchone()[0]
    print(f'✅ Database accessible ({count} tables)')
    conn.close()
except Exception as e:
    print(f'❌ Database error: {e}')
" 2>/dev/null

# Check server
echo -e "\n4. Server Status:"
if curl -s http://localhost:8000/health >/dev/null 2>&1; then
    echo "✅ Server responding"
else
    echo "❌ Server not responding"
fi

echo -e "\n5. Port Usage:"
lsof -i :8000 2>/dev/null | head -5 || echo "Port 8000 is free"

echo -e "\nDiagnosis complete!"
```

### Auto-Fix Common Issues Script

```bash
#!/bin/bash
# Save as auto_fix.sh

echo "🔧 Auto-fixing common issues..."

# Fix 1: Ensure virtual environment
if [ -z "$VIRTUAL_ENV" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate 2>/dev/null || {
        echo "Creating virtual environment..."
        python -m venv venv
        source venv/bin/activate
    }
fi

# Fix 2: Install core dependencies
echo "Installing core dependencies..."
pip install -q fastapi uvicorn sqlite3 2>/dev/null

# Fix 3: Fix permissions
echo "Fixing permissions..."
chmod +x scripts/*.sh 2>/dev/null
chmod 755 ai_knowledge_hub/ 2>/dev/null

# Fix 4: Kill conflicting processes
echo "Checking for port conflicts..."
lsof -i :8000 >/dev/null 2>&1 && {
    echo "Killing processes on port 8000..."
    lsof -ti :8000 | xargs kill -9 2>/dev/null
}

echo "✅ Auto-fix complete!"
```

---

## 📞 When to Escalate

### Contact Support If:

1. **Data Loss**: Database corruption with no backup
2. **Security Issue**: Potential security vulnerability discovered
3. **Performance**: System consistently slow despite optimization
4. **Infrastructure**: Cloud or hosting environment issues

### Information to Provide:

```bash
# Gather diagnostic information
echo "System Information:" > diagnosis.txt
echo "==================" >> diagnosis.txt
uname -a >> diagnosis.txt
python --version >> diagnosis.txt
echo >> diagnosis.txt

echo "Project Status:" >> diagnosis.txt
echo "===============" >> diagnosis.txt
git status >> diagnosis.txt
echo >> diagnosis.txt

echo "Recent Logs:" >> diagnosis.txt
echo "============" >> diagnosis.txt
tail -20 logs/mcp_server.log >> diagnosis.txt 2>/dev/null || echo "No logs found" >> diagnosis.txt

echo "Package Versions:" >> diagnosis.txt
echo "=================" >> diagnosis.txt
pip freeze >> diagnosis.txt

echo "Diagnosis saved to diagnosis.txt"
```

---

## 🔄 Maintenance Commands

### Weekly Maintenance

```bash
#!/bin/bash
# Weekly maintenance script

echo "🧹 Weekly Maintenance"

# Update dependencies
pip list --outdated

# Clean up logs
find logs/ -name "*.log" -mtime +7 -delete 2>/dev/null

# Database maintenance
sqlite3 ai_knowledge_hub/knowledge_hub.db "VACUUM; ANALYZE;"

# Check disk space
df -h .

# Backup database
cp ai_knowledge_hub/knowledge_hub.db "backups/weekly_backup_$(date +%Y%m%d).db"

echo "✅ Maintenance complete"
```

### System Reset (Nuclear Option)

```bash
#!/bin/bash
# Complete system reset - use only when everything else fails

echo "⚠️  NUCLEAR RESET - This will delete everything!"
read -p "Are you sure? (type 'yes'): " confirm

if [ "$confirm" = "yes" ]; then
    echo "Backing up database..."
    cp ai_knowledge_hub/knowledge_hub.db backup_before_reset.db 2>/dev/null

    echo "Resetting environment..."
    deactivate 2>/dev/null
    rm -rf venv/
    rm -rf __pycache__/
    rm -rf ai_knowledge_hub/__pycache__/

    echo "Recreating environment..."
    python -m venv venv
    source venv/bin/activate
    pip install fastapi uvicorn sqlite3

    echo "✅ Nuclear reset complete. Database backed up as backup_before_reset.db"
else
    echo "Reset cancelled."
fi
```

---

**💡 Pro Tip**: Most issues can be resolved by:

1. Ensuring virtual environment is activated
2. Checking the database file exists and is accessible
3. Verifying no other process is using port 8000
4. Installing missing dependencies

For issues not covered here, check the
[main troubleshooting guide](setup/troubleshooting.md) or create an issue in the
repository.
