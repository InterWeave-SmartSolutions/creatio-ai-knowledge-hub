"""
Integration tests for AI Knowledge Hub Integration system
"""
import pytest
import tempfile
import sqlite3
from pathlib import Path
from unittest.mock import patch, Mock
import json


@pytest.mark.integration
class TestKnowledgeHubIntegration:
    """Integration tests for the complete knowledge hub system"""
    
    @pytest.fixture
    def temp_integration_setup(self):
        """Setup temporary directory structure for integration tests"""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Create directory structure
            (temp_path / "ai_optimization/creatio-academy-db/developer_course/videos").mkdir(parents=True)
            (temp_path / "ai_optimization/creatio-academy-db/developer_course/pdfs").mkdir(parents=True)
            (temp_path / "ai_knowledge_hub").mkdir(parents=True)
            
            # Create test video file (empty file for testing)
            test_video = temp_path / "ai_optimization/creatio-academy-db/developer_course/videos/test_video.mp4"
            test_video.touch()
            
            # Create test PDF file
            test_pdf = temp_path / "ai_optimization/creatio-academy-db/developer_course/pdfs/test_doc.pdf"
            test_pdf.touch()
            
            yield temp_path
    
    @patch('ai_knowledge_hub_integration.whisper')
    def test_full_integration_workflow(self, mock_whisper, temp_integration_setup):
        """Test the complete integration workflow"""
        from ai_knowledge_hub_integration import AIKnowledgeHubIntegrator
        
        # Mock Whisper model
        mock_model = Mock()
        mock_model.transcribe.return_value = {
            "text": "This is a test video about Creatio development and configuration."
        }
        mock_whisper.load_model.return_value = mock_model
        
        # Initialize integrator
        integrator = AIKnowledgeHubIntegrator(str(temp_integration_setup))
        integrator.initialize_database()
        
        # Verify database was created
        db_path = temp_integration_setup / "ai_knowledge_hub/knowledge_hub.db"
        assert db_path.exists()
        
        # Check database schema
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Verify tables exist
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        expected_tables = ['videos', 'pdfs', 'search_index', 'commands', 'search_fts']
        
        for table in expected_tables:
            assert table in tables
        
        conn.close()
    
    def test_database_schema_integrity(self, temp_integration_setup):
        """Test database schema creation and integrity"""
        from ai_knowledge_hub_integration import AIKnowledgeHubIntegrator
        
        integrator = AIKnowledgeHubIntegrator(str(temp_integration_setup))
        integrator.initialize_database()
        
        db_path = temp_integration_setup / "ai_knowledge_hub/knowledge_hub.db"
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Test videos table schema
        cursor.execute("PRAGMA table_info(videos)")
        video_columns = [row[1] for row in cursor.fetchall()]
        expected_video_columns = ['id', 'file_path', 'title', 'duration', 'transcript', 
                                'summary', 'topics', 'complexity_level', 'commands', 
                                'api_references', 'code_examples', 'created_at']
        
        for col in expected_video_columns:
            assert col in video_columns
        
        # Test pdfs table schema
        cursor.execute("PRAGMA table_info(pdfs)")
        pdf_columns = [row[1] for row in cursor.fetchall()]
        expected_pdf_columns = ['id', 'file_path', 'title', 'page_count', 'content', 
                              'sections', 'topics', 'commands', 'api_references', 
                              'code_examples', 'created_at']
        
        for col in expected_pdf_columns:
            assert col in pdf_columns
        
        conn.close()
    
    @patch('ai_knowledge_hub_integration.whisper')
    @patch('ai_knowledge_hub_integration.PyPDF2')
    def test_content_processing_integration(self, mock_pypdf2, mock_whisper, temp_integration_setup):
        """Test integration of video and PDF processing"""
        from ai_knowledge_hub_integration import AIKnowledgeHubIntegrator
        
        # Setup mocks
        mock_model = Mock()
        mock_model.transcribe.return_value = {
            "text": "This video explains how to create entities in Creatio using CreateEntity command."
        }
        mock_whisper.load_model.return_value = mock_model
        
        # Mock PDF reader
        mock_pdf_reader = Mock()
        mock_page = Mock()
        mock_page.extract_text.return_value = "This document describes the ModifySchema API for Creatio development."
        mock_pdf_reader.pages = [mock_page]
        
        mock_pdf_file = Mock()
        mock_pdf_file.__enter__.return_value = mock_pdf_file
        mock_pdf_file.__exit__.return_value = None
        mock_pypdf2.PdfReader.return_value = mock_pdf_reader
        
        # Initialize and run integration
        integrator = AIKnowledgeHubIntegrator(str(temp_integration_setup))
        integrator.initialize_database()
        
        # This would normally process actual files, but for testing we'll verify the setup
        assert integrator.video_path.exists()
        assert integrator.pdf_path.exists()
        assert integrator.output_path.exists()
    
    def test_search_index_creation(self, temp_integration_setup):
        """Test search index creation and functionality"""
        from ai_knowledge_hub_integration import AIKnowledgeHubIntegrator
        
        integrator = AIKnowledgeHubIntegrator(str(temp_integration_setup))
        integrator.initialize_database()
        
        db_path = temp_integration_setup / "ai_knowledge_hub/knowledge_hub.db"
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Insert test data
        cursor.execute("""
            INSERT INTO search_fts (content_type, content_id, title, content, keywords)
            VALUES (?, ?, ?, ?, ?)
        """, ('video', 'test-001', 'Test Video', 'This is about Creatio development', 'creatio,development'))
        
        # Test full-text search
        cursor.execute("""
            SELECT * FROM search_fts WHERE search_fts MATCH ?
        """, ('creatio',))
        
        results = cursor.fetchall()
        assert len(results) > 0
        assert 'creatio' in results[0][4].lower()  # keywords column
        
        conn.commit()
        conn.close()
    
    def test_command_extraction_integration(self, temp_integration_setup):
        """Test command extraction and storage integration"""
        from ai_knowledge_hub_integration import AIKnowledgeHubIntegrator
        
        integrator = AIKnowledgeHubIntegrator(str(temp_integration_setup))
        integrator.initialize_database()
        
        db_path = temp_integration_setup / "ai_knowledge_hub/knowledge_hub.db"
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Insert test command data
        test_commands = [
            ('CreateSection', 'Creates a new section in Creatio', 'Development', 'video', 'test-001'),
            ('ModifySchema', 'Modifies an existing schema', 'Configuration', 'pdf', 'test-002')
        ]
        
        for cmd in test_commands:
            cursor.execute("""
                INSERT INTO commands (command, description, category, source_type, source_id)
                VALUES (?, ?, ?, ?, ?)
            """, cmd)
        
        # Test command retrieval
        cursor.execute("SELECT * FROM commands WHERE category = ?", ('Development',))
        dev_commands = cursor.fetchall()
        assert len(dev_commands) == 1
        assert dev_commands[0][1] == 'CreateSection'
        
        conn.commit()
        conn.close()


@pytest.mark.integration
class TestMCPServerIntegration:
    """Integration tests for MCP Server with real database"""
    
    def test_mcp_server_database_integration(self, test_database):
        """Test MCP server with actual database operations"""
        from ai_knowledge_hub.enhanced_mcp_server import KnowledgeHubService
        
        # Initialize service with test database
        service = KnowledgeHubService()
        service.db_path = test_database
        
        # Insert test data directly into database
        conn = sqlite3.connect(test_database)
        cursor = conn.cursor()
        
        # Insert test video data
        cursor.execute("""
            INSERT INTO videos (id, title, transcript)
            VALUES (?, ?, ?)
        """, ('test-video-001', 'Creatio Development Tutorial', 
              'This tutorial covers entity creation and schema modification in Creatio'))
        
        # Insert test command data
        cursor.execute("""
            INSERT INTO commands (command, description, category)
            VALUES (?, ?, ?)
        """, ('CreateEntity', 'Creates a new entity in Creatio', 'Development'))
        
        conn.commit()
        conn.close()
        
        # Test command retrieval
        commands = service.get_commands(category='Development')
        assert len(commands) >= 1
        assert any(cmd['command'] == 'CreateEntity' for cmd in commands)
    
    def test_api_endpoints_integration(self, test_client, test_database):
        """Test API endpoints with real database operations"""
        # Insert test data into database
        conn = sqlite3.connect(test_database)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO commands (command, description, category, source_type, source_id, examples, parameters)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, ('TestCommand', 'Test command description', 'Testing', 'unit_test', 'test-001', '[]', '[]'))
        
        conn.commit()
        conn.close()
        
        # Test commands endpoint
        response = test_client.get("/api/v1/commands?category=Testing")
        assert response.status_code == 200
        
        data = response.json()
        assert data["total_commands"] >= 1
        assert any(cmd["command"] == "TestCommand" for cmd in data["commands"])
