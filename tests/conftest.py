"""
Test configuration and fixtures for Creatio AI Knowledge Hub
"""
import os
import tempfile
import sqlite3
from pathlib import Path
from typing import Generator, Dict, Any
import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock

# Set test environment
os.environ['ENVIRONMENT'] = 'test'
os.environ['DATABASE_URL'] = 'sqlite:///test_knowledge_hub.db'
os.environ['REDIS_URL'] = 'redis://localhost:6379'


@pytest.fixture(scope="session")
def test_database() -> Generator[str, None, None]:
    """Create a temporary test database"""
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp_file:
        db_path = tmp_file.name
    
    # Initialize test database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create test tables (simplified schema)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS videos (
            id TEXT PRIMARY KEY,
            title TEXT,
            transcript TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pdfs (
            id TEXT PRIMARY KEY,
            title TEXT,
            content TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS commands (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            command TEXT,
            description TEXT,
            category TEXT
        )
    ''')
    
    conn.commit()
    conn.close()
    
    yield db_path
    
    # Cleanup
    os.unlink(db_path)


@pytest.fixture
def test_client(test_database: str) -> TestClient:
    """Create test client for API testing"""
    from ai_knowledge_hub.enhanced_mcp_server import app
    
    # Override database path for testing
    app.dependency_overrides = {}
    
    return TestClient(app)


@pytest.fixture
def sample_video_data() -> Dict[str, Any]:
    """Sample video data for testing"""
    return {
        "id": "test-video-001",
        "file_path": "/test/video.mp4",
        "title": "Test Video",
        "duration": 120.5,
        "transcript": "This is a test video transcript about Creatio development.",
        "summary": "Test video about Creatio",
        "topics": ["creatio", "development", "testing"],
        "complexity_level": "beginner",
        "commands": ["CreateSection", "AddField"],
        "api_references": ["EntitySchema", "UserConnection"],
        "code_examples": [
            {
                "language": "javascript",
                "code": "var schema = this.Ext.create('EntitySchema');"
            }
        ]
    }


@pytest.fixture
def sample_pdf_data() -> Dict[str, Any]:
    """Sample PDF data for testing"""
    return {
        "id": "test-pdf-001",
        "file_path": "/test/document.pdf",
        "title": "Test PDF Document",
        "page_count": 10,
        "content": "This is test PDF content about Creatio development.",
        "sections": [
            {"title": "Introduction", "content": "Introduction content"},
            {"title": "Main Content", "content": "Main content"}
        ],
        "topics": ["creatio", "documentation"],
        "commands": ["CreateEntity", "ModifySchema"],
        "api_references": ["EntitySchema", "ProcessSchema"],
        "code_examples": [
            {
                "language": "csharp",
                "code": "var entity = UserConnection.EntitySchemaManager.GetInstanceByName('Contact');"
            }
        ]
    }


@pytest.fixture
def mock_whisper_model():
    """Mock Whisper model for testing"""
    mock_model = Mock()
    mock_model.transcribe.return_value = {
        "text": "This is a mock transcription of the video content."
    }
    return mock_model


@pytest.fixture
def test_config() -> Dict[str, Any]:
    """Test configuration"""
    return {
        "database_url": "sqlite:///test_knowledge_hub.db",
        "redis_url": "redis://localhost:6379",
        "environment": "test",
        "secret_key": "test-secret-key",
        "api_rate_limit": 1000,
        "whisper_model": "base",
        "chunk_size": 1000,
        "chunk_overlap": 200
    }


@pytest.fixture(autouse=True)
def clean_test_files(tmp_path):
    """Automatically clean up test files after each test"""
    yield
    # Cleanup logic can be added here if needed


class TestDataFactory:
    """Factory for creating test data"""
    
    @staticmethod
    def create_video_content(**kwargs):
        """Create video content for testing"""
        default_data = {
            "video_id": "test-video",
            "file_path": "/test/video.mp4",
            "title": "Test Video",
            "duration": 120.0,
            "transcript": "Test transcript",
            "summary": "Test summary",
            "topics": ["test"],
            "complexity_level": "beginner",
            "commands": [],
            "api_references": [],
            "code_examples": []
        }
        default_data.update(kwargs)
        return default_data
    
    @staticmethod
    def create_pdf_content(**kwargs):
        """Create PDF content for testing"""
        default_data = {
            "pdf_id": "test-pdf",
            "file_path": "/test/doc.pdf",
            "title": "Test PDF",
            "page_count": 5,
            "content": "Test content",
            "sections": [],
            "topics": ["test"],
            "commands": [],
            "api_references": [],
            "code_examples": []
        }
        default_data.update(kwargs)
        return default_data


@pytest.fixture
def test_data_factory():
    """Provide test data factory"""
    return TestDataFactory
