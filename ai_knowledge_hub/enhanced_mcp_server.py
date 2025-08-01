#!/usr/bin/env python3
"""
Enhanced MCP Server for Creatio AI Knowledge Hub
Integrates with processed video and PDF content for AI assistance
"""

import sqlite3
import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from fastapi import FastAPI, HTTPException, Query, Response
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware
from monitoring.monitoring import monitor
from monitoring.logging_config import log_request, log_performance
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

app = FastAPI(
    title="Creatio AI Knowledge Hub MCP Server",
    description="Enhanced MCP server with full knowledge hub integration",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration
DB_PATH = "ai_knowledge_hub/knowledge_hub.db"
SEARCH_INDEX_PATH = "ai_knowledge_hub/search_index"

class KnowledgeHubService:
    def __init__(self):
        self.db_path = DB_PATH
        self.search_index_path = Path(SEARCH_INDEX_PATH)
        
    def health_check(self):
        """Run health checks"""
        return monitor.get_health_status()
    
    def search_content(self, query: str, content_type: str = "all", limit: int = 10) -> List[Dict]:
        """Search across all indexed content"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if content_type == "all":
            cursor.execute("""
                SELECT content_type, content_id, title, content, keywords
                FROM search_fts
                WHERE search_fts MATCH ?
                ORDER BY rank
                LIMIT ?
            """, (query, limit))
        else:
            cursor.execute("""
                SELECT content_type, content_id, title, content, keywords
                FROM search_fts
                WHERE search_fts MATCH ? AND content_type = ?
                ORDER BY rank
                LIMIT ?
            """, (query, content_type, limit))
        
        results = []
        for row in cursor.fetchall():
            results.append({
                'content_type': row[0],
                'content_id': row[1],
                'title': row[2],
                'content_snippet': row[3][:500] if row[3] else '',
                'keywords': row[4] if len(row) > 4 else '',
                'relevance_score': 1.0
            })
        
        conn.close()
        return results
    
    def get_commands(self, category: Optional[str] = None, search_term: Optional[str] = None) -> List[Dict]:
        """Get commands from the knowledge base"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        query = "SELECT * FROM commands"
        params = []
        
        conditions = []
        if category:
            conditions.append("category = ?")
            params.append(category)
        
        if search_term:
            conditions.append("(command LIKE ? OR description LIKE ?)")
            params.extend([f"%{search_term}%", f"%{search_term}%"])
        
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        
        query += " ORDER BY command LIMIT 50"
        
        cursor.execute(query, params)
        
        results = []
        for row in cursor.fetchall():
            results.append({
                'id': row[0],
                'command': row[1],
                'description': row[2],
                'category': row[3],
                'source_type': row[4],
                'source_id': row[5],
                'examples': json.loads(row[6]) if row[6] else [],
                'parameters': json.loads(row[7]) if row[7] else []
            })
        
        conn.close()
        return results

knowledge_service = KnowledgeHubService()

@app.get("/api/v1/search")
async def search_content(
    query: str = Query(..., description="Search query"),
    content_type: str = Query("all", description="Content type filter"),
    limit: int = Query(10, description="Maximum results")
):
    """Search across all knowledge hub content"""
    try:
        results = knowledge_service.search_content(query, content_type, limit)
        return {
            "query": query,
            "content_type": content_type,
            "total_results": len(results),
            "results": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/commands")
async def get_commands(
    category: Optional[str] = Query(None, description="Command category"),
    search_term: Optional[str] = Query(None, description="Search term")
):
    """Get commands from knowledge base"""
    try:
        commands = knowledge_service.get_commands(category, search_term)
        return {
            "total_commands": len(commands),
            "commands": commands
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/health")
async def health_check():
    """Returns health status"""
    return knowledge_service.health_check()

@app.get("/api/v1/health/deep")
async def deep_health_check():
    """Returns detailed health status with metrics"""
    health_status = knowledge_service.health_check()
    metrics_summary = monitor.get_metrics_summary()
    
    return {
        "health": health_status,
        "metrics": metrics_summary,
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/metrics")
async def metrics():
    """Prometheus metrics endpoint"""
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
