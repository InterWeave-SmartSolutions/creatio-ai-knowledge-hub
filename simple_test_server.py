#!/usr/bin/env python3
"""
Simple test server for validating basic functionality
"""

from fastapi import FastAPI, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
import json
import os
from pathlib import Path
from typing import List, Optional, Dict
from pydantic import BaseModel

# Initialize FastAPI app
app = FastAPI(
    title="Simple Creatio Academy Test Server",
    description="Simple test server for validation",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class DeveloperCourseRequest(BaseModel):
    content_type: Optional[str] = "all"
    search_query: Optional[str] = None
    limit: int = 10

class ContentSearchRequest(BaseModel):
    query: str
    content_type: Optional[str] = "all"
    limit: int = 10

# Simple search function for developer course content
def search_developer_course(query: Optional[str] = None, content_type: str = "all", limit: int = 10) -> List[Dict]:
    """Search developer course content"""
    results = []
    dev_course_path = Path("ai_optimization/creatio-academy-db/developer_course")
    
    if not dev_course_path.exists():
        return results
    
    # Load master index
    master_index_path = dev_course_path / "master_index.json"
    if not master_index_path.exists():
        return results
    
    try:
        with open(master_index_path, 'r', encoding='utf-8') as f:
            master_index = json.load(f)
    except Exception as e:
        print(f"Error loading master index: {e}")
        return results
    
    # Get content statistics
    content_index = master_index.get('content_index', {})
    
    for doc_id, doc_info in list(content_index.items())[:limit]:
        try:
            # Filter by content type if specified
            if content_type != "all" and doc_info.get('type') != content_type:
                continue
            
            # Simple content matching
            title = doc_info.get('title', 'Unknown')
            
            # If query is provided, do basic matching
            if query:
                query_lower = query.lower()
                if (query_lower not in title.lower() and 
                    query_lower not in doc_info.get('source_file', '').lower()):
                    continue
            
            results.append({
                'type': 'test_result',
                'content_type': doc_info.get('type'),
                'document_id': doc_id,
                'title': title,
                'source_file': doc_info.get('source_file'),
                'metadata': {
                    'type': doc_info.get('type'),
                    'chunks_available': bool(doc_info.get('chunks_file'))
                }
            })
            
        except Exception as e:
            print(f"Error processing document {doc_id}: {e}")
            continue
    
    return results

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "message": "Simple test server is running"
    }

# Authentication endpoint (simple mock)
@app.post("/auth/token")
async def login(username: str = Form(...), password: str = Form(...)):
    """Mock authentication"""
    if username == "admin" and password == "password":
        return {"access_token": "test-token", "token_type": "bearer"}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")

# Content search endpoint (simple mock)
@app.post("/content-search")
async def content_search(search_request: ContentSearchRequest):
    """Simple content search"""
    try:
        # Mock search across different content types
        results = []
        
        # Search developer course
        dev_results = search_developer_course(
            search_request.query, 
            search_request.content_type, 
            search_request.limit
        )
        results.extend(dev_results)
        
        return {
            "query": search_request.query,
            "total_results": len(results),
            "results": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")

# Developer course endpoint
@app.post("/developer-course")
async def query_developer_course(course_request: DeveloperCourseRequest):
    """Query developer course content"""
    try:
        results = search_developer_course(
            query=course_request.search_query,
            content_type=course_request.content_type or "all",
            limit=course_request.limit
        )
        
        return {
            "content_type": course_request.content_type,
            "search_query": course_request.search_query,
            "total_results": len(results),
            "results": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Developer course query failed: {str(e)}")

# Video transcript endpoint (simple mock)
@app.get("/video-transcripts/{video_id}")
async def get_video_transcript(video_id: str, include_metadata: bool = True, include_summary: bool = False):
    """Get video transcript by ID"""
    try:
        # Check developer course transcripts
        dev_course_path = Path("ai_optimization/creatio-academy-db/developer_course/transcripts")
        transcript_files = list(dev_course_path.glob(f"*{video_id}*transcript.json"))
        
        if not transcript_files:
            # Check text files too
            transcript_files = list(dev_course_path.glob(f"*{video_id}*text.txt"))
        
        if not transcript_files:
            raise HTTPException(status_code=404, detail=f"Transcript not found for video {video_id}")
        
        # Load the transcript
        transcript_file = transcript_files[0]
        
        if transcript_file.suffix == '.json':
            with open(transcript_file, 'r', encoding='utf-8') as f:
                transcript_data = json.load(f)
        else:
            # Text file
            with open(transcript_file, 'r', encoding='utf-8') as f:
                text_content = f.read()
            transcript_data = {
                'text': text_content,
                'video_id': video_id,
                'source_file': str(transcript_file)
            }
        
        return {
            "video_id": video_id,
            "transcript": transcript_data,
            "source": str(transcript_file)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve transcript: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
