"""
Unit tests for the Enhanced MCP Server
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, Mock


@pytest.mark.unit
class TestMCPServerAPI:
    """Test the MCP Server API endpoints"""
    
    def test_search_content_success(self, test_client: TestClient):
        """Test successful content search"""
        with patch('ai_knowledge_hub.enhanced_mcp_server.knowledge_service') as mock_service:
            mock_service.search_content.return_value = [
                {
                    'content_type': 'video',
                    'content_id': 'test-001',
                    'title': 'Test Video',
                    'content_snippet': 'This is a test video about Creatio',
                    'keywords': 'creatio, development',
                    'relevance_score': 0.95
                }
            ]
            
            response = test_client.get(
                "/api/v1/search",
                params={"query": "creatio development", "content_type": "all", "limit": 10}
            )
            
            assert response.status_code == 200
            data = response.json()
            assert data["query"] == "creatio development"
            assert data["content_type"] == "all"
            assert data["total_results"] == 1
            assert len(data["results"]) == 1
            assert data["results"][0]["title"] == "Test Video"
    
    def test_search_content_empty_query(self, test_client: TestClient):
        """Test search with empty query"""
        response = test_client.get("/api/v1/search")
        assert response.status_code == 422  # Validation error
    
    def test_search_content_filtered_by_type(self, test_client: TestClient):
        """Test content search filtered by type"""
        with patch('ai_knowledge_hub.enhanced_mcp_server.knowledge_service') as mock_service:
            mock_service.search_content.return_value = []
            
            response = test_client.get(
                "/api/v1/search",
                params={"query": "test", "content_type": "video", "limit": 5}
            )
            
            assert response.status_code == 200
            mock_service.search_content.assert_called_once_with("test", "video", 5)
    
    def test_get_commands_success(self, test_client: TestClient):
        """Test successful command retrieval"""
        with patch('ai_knowledge_hub.enhanced_mcp_server.knowledge_service') as mock_service:
            mock_service.get_commands.return_value = [
                {
                    'id': 1,
                    'command': 'CreateSection',
                    'description': 'Create a new section in Creatio',
                    'category': 'Development',
                    'source_type': 'video',
                    'source_id': 'test-001',
                    'examples': ['CreateSection("TestSection")'],
                    'parameters': ['name', 'type']
                }
            ]
            
            response = test_client.get("/api/v1/commands")
            
            assert response.status_code == 200
            data = response.json()
            assert data["total_commands"] == 1
            assert len(data["commands"]) == 1
            assert data["commands"][0]["command"] == "CreateSection"
    
    def test_get_commands_with_filters(self, test_client: TestClient):
        """Test command retrieval with filters"""
        with patch('ai_knowledge_hub.enhanced_mcp_server.knowledge_service') as mock_service:
            mock_service.get_commands.return_value = []
            
            response = test_client.get(
                "/api/v1/commands",
                params={"category": "Development", "search_term": "Create"}
            )
            
            assert response.status_code == 200
            mock_service.get_commands.assert_called_once_with("Development", "Create")
    
    def test_search_content_database_error(self, test_client: TestClient):
        """Test search when database error occurs"""
        with patch('ai_knowledge_hub.enhanced_mcp_server.knowledge_service') as mock_service:
            mock_service.search_content.side_effect = Exception("Database connection failed")
            
            response = test_client.get(
                "/api/v1/search",
                params={"query": "test"}
            )
            
            assert response.status_code == 500
            assert "Database connection failed" in response.json()["detail"]


@pytest.mark.unit
class TestKnowledgeHubService:
    """Test the KnowledgeHubService class"""
    
    @patch('ai_knowledge_hub.enhanced_mcp_server.sqlite3.connect')
    def test_search_content_all_types(self, mock_connect):
        """Test searching across all content types"""
        from ai_knowledge_hub.enhanced_mcp_server import KnowledgeHubService
        
        # Mock database connection and cursor
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [
            ('video', 'test-001', 'Test Video', 'Test content', 'test, video')
        ]
        
        service = KnowledgeHubService()
        results = service.search_content("test query", "all", 10)
        
        assert len(results) == 1
        assert results[0]['content_type'] == 'video'
        assert results[0]['content_id'] == 'test-001'
        assert results[0]['title'] == 'Test Video'
        
        # Verify database query
        mock_cursor.execute.assert_called_once()
        args = mock_cursor.execute.call_args[0]
        assert "search_fts MATCH ?" in args[0]
        assert args[1] == ("test query", 10)
    
    @patch('ai_knowledge_hub.enhanced_mcp_server.sqlite3.connect')
    def test_search_content_specific_type(self, mock_connect):
        """Test searching for specific content type"""
        from ai_knowledge_hub.enhanced_mcp_server import KnowledgeHubService
        
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = []
        
        service = KnowledgeHubService()
        service.search_content("test", "video", 5)
        
        # Verify the query includes content type filter
        args = mock_cursor.execute.call_args[0]
        assert "content_type = ?" in args[0]
        assert args[1] == ("test", "video", 5)
    
    @patch('ai_knowledge_hub.enhanced_mcp_server.sqlite3.connect')
    def test_get_commands_no_filters(self, mock_connect):
        """Test getting commands without filters"""
        from ai_knowledge_hub.enhanced_mcp_server import KnowledgeHubService
        
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [
            (1, 'CreateSection', 'Create section', 'Development', 'video', 'test-001', '[]', '[]')
        ]
        
        service = KnowledgeHubService()
        results = service.get_commands()
        
        assert len(results) == 1
        assert results[0]['command'] == 'CreateSection'
        
        # Verify query without conditions
        args = mock_cursor.execute.call_args[0]
        assert "WHERE" not in args[0]
    
    @patch('ai_knowledge_hub.enhanced_mcp_server.sqlite3.connect')
    def test_get_commands_with_filters(self, mock_connect):
        """Test getting commands with category and search filters"""
        from ai_knowledge_hub.enhanced_mcp_server import KnowledgeHubService
        
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = []
        
        service = KnowledgeHubService()
        service.get_commands(category="Development", search_term="Create")
        
        # Verify query includes both filters
        args = mock_cursor.execute.call_args[0]
        assert "WHERE" in args[0]
        assert "category = ?" in args[0]
        assert "command LIKE ?" in args[0]
        assert "description LIKE ?" in args[0]
        assert args[1] == ["Development", "%Create%", "%Create%"]
