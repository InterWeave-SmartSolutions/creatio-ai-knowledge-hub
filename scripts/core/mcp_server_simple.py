from fastapi import FastAPI, HTTPException, Depends, WebSocket, WebSocketDisconnect, Query
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import asyncio
import json
import os
import glob
import sys
from pathlib import Path
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
import re
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
import hashlib

# Configuration
SECRET_KEY = "your-secret-key-here"  # Change this in production
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)

# Initialize FastAPI app
app = FastAPI(
    title="Creatio Academy MCP Server",
    description="Model Context Protocol server for AI agent access to Creatio Academy content",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add rate limiting middleware
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Pydantic models
class ContentSearchRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=500)
    limit: int = Field(default=10, ge=1, le=100)
    content_type: Optional[str] = Field(default=None, pattern=r"^(documentation|video|all)$")
    
class VideoTranscriptRequest(BaseModel):
    video_id: str = Field(..., min_length=1)
    include_metadata: bool = Field(default=True)
    include_summary: bool = Field(default=False)

class CodeExampleRequest(BaseModel):
    language: Optional[str] = Field(default=None)
    topic: Optional[str] = Field(default=None)
    limit: int = Field(default=10, ge=1, le=50)

class DocumentationQueryRequest(BaseModel):
    doc_id: Optional[str] = Field(default=None)
    section: Optional[str] = Field(default=None)
    search_term: Optional[str] = Field(default=None)
    limit: int = Field(default=10, ge=1, le=100)

class DeveloperCourseRequest(BaseModel):
    content_type: Optional[str] = Field(default=None, pattern=r"^(video|pdf|all)$")
    search_query: Optional[str] = Field(default=None)
    limit: int = Field(default=10, ge=1, le=100)

class WebSocketMessage(BaseModel):
    type: str
    data: Dict[str, Any]

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
    
    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
    
    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)
    
    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except:
                # Remove disconnected clients
                self.disconnect(connection)

manager = ConnectionManager()

# Authentication functions
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
        return username
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")

# Data access functions
def load_transcription_data(video_id: str) -> Optional[Dict]:
    """Load transcription data for a video ID"""
    base_path = Path("transcriptions")
    dev_course_path = Path("ai_optimization/creatio-academy-db/developer_course")
    
    # Try to find the transcription file in legacy location
    transcript_files = list(base_path.glob(f"transcripts/*{video_id}*transcription.json"))
    
    # Also check developer course location
    if not transcript_files and dev_course_path.exists():
        transcript_files = list(dev_course_path.glob(f"transcripts/*{video_id}*transcript.json"))
    
    if not transcript_files:
        return None
    
    try:
        with open(transcript_files[0], 'r', encoding='utf-8') as f:
            transcript_data = json.load(f)
        
        # Load metadata if available
        metadata_files = list(base_path.glob(f"metadata/*{video_id}*metadata.json"))
        if not metadata_files and dev_course_path.exists():
            metadata_files = list(dev_course_path.glob(f"metadata/*{video_id}*metadata.json"))
            
        if metadata_files:
            with open(metadata_files[0], 'r', encoding='utf-8') as f:
                metadata = json.load(f)
            transcript_data['metadata'] = metadata
        
        # Load enhanced summary if available
        summary_files = list(base_path.glob(f"summaries/*{video_id}*enhanced_summary.json"))
        if not summary_files and dev_course_path.exists():
            summary_files = list(dev_course_path.glob(f"summaries/**/*{video_id}*.json"))
            
        if summary_files:
            with open(summary_files[0], 'r', encoding='utf-8') as f:
                summary = json.load(f)
            transcript_data['enhanced_summary'] = summary
        
        return transcript_data
    except Exception as e:
        print(f"Error loading transcription data for {video_id}: {e}")
        return None

def search_content(query: str, content_type: str = "all", limit: int = 10) -> List[Dict]:
    """Search across documentation and video content"""
    results = []
    query_lower = query.lower()
    
    # Search documentation if requested
    if content_type in ["documentation", "all"]:
        doc_results = search_documentation(query_lower, limit // 2 if content_type == "all" else limit)
        results.extend(doc_results)
    
    # Search video transcripts if requested
    if content_type in ["video", "all"]:
        video_results = search_videos(query_lower, limit // 2 if content_type == "all" else limit)
        results.extend(video_results)
    
    # Sort by relevance (simplified scoring)
    results.sort(key=lambda x: x.get('relevance_score', 0), reverse=True)
    
    return results[:limit]

def search_documentation(query: str, limit: int) -> List[Dict]:
    """Search HTML documentation files"""
    results = []
    doc_path = Path("creatio-academy-archive/pages/raw")
    
    if not doc_path.exists():
        return results
    
    html_files = list(doc_path.glob("*.html"))
    
    for html_file in html_files[:100]:  # Limit to avoid performance issues
        try:
            with open(html_file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            soup = BeautifulSoup(content, 'html.parser')
            text_content = soup.get_text().lower()
            
            if query in text_content:
                title = soup.find('title')
                title_text = title.get_text() if title else html_file.name
                
                # Simple relevance scoring
                relevance_score = text_content.count(query)
                
                results.append({
                    'type': 'documentation',
                    'title': title_text,
                    'file_path': str(html_file),
                    'relevance_score': relevance_score,
                    'snippet': extract_snippet(text_content, query)
                })
                
                if len(results) >= limit:
                    break
        except Exception as e:
            continue
    
    return results

def search_videos(query: str, limit: int) -> List[Dict]:
    """Search video transcriptions"""
    results = []
    transcripts_path = Path("transcriptions/transcripts")
    
    if not transcripts_path.exists():
        return results
    
    transcript_files = list(transcripts_path.glob("*.json"))
    
    for transcript_file in transcript_files:
        try:
            with open(transcript_file, 'r', encoding='utf-8') as f:
                transcript_data = json.load(f)
            
            # Search in transcript text
            text_content = transcript_data.get('text', '').lower()
            
            if query in text_content:
                # Load metadata for better results
                video_id = transcript_file.stem.replace('_transcription', '')
                metadata = load_video_metadata(video_id)
                
                relevance_score = text_content.count(query)
                
                results.append({
                    'type': 'video',
                    'video_id': video_id,
                    'title': metadata.get('content_metadata', {}).get('title', 'Unknown') if metadata else 'Unknown',
                    'relevance_score': relevance_score,
                    'snippet': extract_snippet(text_content, query),
                    'duration': transcript_data.get('duration', 0)
                })
                
                if len(results) >= limit:
                    break
        except Exception as e:
            continue
    
    return results

def load_video_metadata(video_id: str) -> Optional[Dict]:
    """Load metadata for a video"""
    metadata_path = Path("transcriptions/metadata")
    metadata_files = list(metadata_path.glob(f"*{video_id}*metadata.json"))
    
    if not metadata_files:
        return None
    
    try:
        with open(metadata_files[0], 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return None

def extract_snippet(content: str, query: str, context_length: int = 200) -> str:
    """Extract a snippet around the query match"""
    query_pos = content.find(query)
    if query_pos == -1:
        return content[:context_length] + "..." if len(content) > context_length else content
    
    start = max(0, query_pos - context_length // 2)
    end = min(len(content), query_pos + context_length // 2)
    
    snippet = content[start:end]
    if start > 0:
        snippet = "..." + snippet
    if end < len(content):
        snippet += "..."
    
    return snippet

def extract_code_examples(language: Optional[str] = None, topic: Optional[str] = None, limit: int = 10) -> List[Dict]:
    """Extract code examples from documentation"""
    results = []
    doc_path = Path("creatio-academy-archive/pages/raw")
    
    if not doc_path.exists():
        return results
    
    html_files = list(doc_path.glob("*.html"))
    
    for html_file in html_files[:50]:  # Limit files to process
        try:
            with open(html_file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            soup = BeautifulSoup(content, 'html.parser')
            
            # Find code blocks
            code_blocks = soup.find_all(['pre', 'code', 'div'], 
                                      class_=re.compile(r'.*code.*|.*highlight.*|.*language.*', re.I))
            
            for code_block in code_blocks:
                code_text = code_block.get_text().strip()
                if len(code_text) > 20:  # Filter out very short code blocks
                    # Detect language if not specified
                    detected_language = detect_code_language(code_text, code_block)
                    
                    # Filter by language if specified
                    if language and detected_language.lower() != language.lower():
                        continue
                    
                    # Filter by topic if specified (simple keyword matching)
                    if topic and topic.lower() not in code_text.lower():
                        continue
                    
                    results.append({
                        'language': detected_language,
                        'code': code_text,
                        'source_file': str(html_file),
                        'context': extract_code_context(soup, code_block)
                    })
                    
                    if len(results) >= limit:
                        return results
        except Exception as e:
            continue
    
    return results

def detect_code_language(code_text: str, code_element) -> str:
    """Detect programming language of code block"""
    # Check class attributes for language hints
    classes = code_element.get('class', [])
    for cls in classes:
        if 'javascript' in cls.lower() or 'js' in cls.lower():
            return 'JavaScript'
        elif 'python' in cls.lower() or 'py' in cls.lower():
            return 'Python'
        elif 'csharp' in cls.lower() or 'c#' in cls.lower():
            return 'C#'
        elif 'sql' in cls.lower():
            return 'SQL'
        elif 'xml' in cls.lower():
            return 'XML'
        elif 'json' in cls.lower():
            return 'JSON'
    
    # Simple heuristic detection based on content
    if 'function' in code_text and '{' in code_text:
        return 'JavaScript'
    elif 'def ' in code_text or 'import ' in code_text:
        return 'Python'
    elif 'SELECT' in code_text.upper() or 'FROM' in code_text.upper():
        return 'SQL'
    elif code_text.strip().startswith('<') and code_text.strip().endswith('>'):
        return 'XML'
    elif code_text.strip().startswith('{') and code_text.strip().endswith('}'):
        return 'JSON'
    
    return 'Unknown'

def extract_code_context(soup, code_element) -> str:
    """Extract context around code block"""
    # Find preceding heading or paragraph
    context_elements = []
    
    # Look for preceding heading
    for tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
        heading = code_element.find_previous(tag)
        if heading:
            context_elements.append(heading.get_text().strip())
            break
    
    # Look for preceding paragraph
    preceding_p = code_element.find_previous('p')
    if preceding_p:
        context_elements.append(preceding_p.get_text().strip()[:200])
    
    return ' | '.join(context_elements) if context_elements else 'No context available'

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
    
    # Search through content index
    for doc_id, doc_info in master_index.get('content_index', {}).items():
        try:
            # Filter by content type if specified
            if content_type != "all" and doc_info.get('type') != content_type:
                continue
            
            # Load chunks file for content search
            chunks_file = dev_course_path / doc_info.get('chunks_file', '')
            if chunks_file.exists():
                with open(chunks_file, 'r', encoding='utf-8') as f:
                    chunks_data = json.load(f)
                
                for chunk in chunks_data.get('chunks', []):
                    chunk_content = chunk.get('content', '').lower()
                    
                    # If query is provided, filter by query
                    if query and query.lower() not in chunk_content:
                        continue
                    
                    # Calculate relevance score
                    relevance_score = chunk_content.count(query.lower()) if query else 1
                    
                    results.append({
                        'type': 'developer_course',
                        'content_type': doc_info.get('type'),
                        'document_id': doc_id,
                        'title': doc_info.get('title'),
                        'chunk_id': chunk.get('id'),
                        'relevance_score': relevance_score,
                        'snippet': extract_snippet(chunk_content, query.lower() if query else ''),
                        'metadata': chunk.get('metadata', {}),
                        'source_file': doc_info.get('source_file')
                    })
                    
                    if len(results) >= limit:
                        break
                        
            if len(results) >= limit:
                break
                
        except Exception as e:
            print(f"Error processing document {doc_id}: {e}")
            continue
    
    # Sort by relevance score
    results.sort(key=lambda x: x.get('relevance_score', 0), reverse=True)
    
    return results[:limit]

# API Endpoints
@app.get("/", tags=["Root"])
@limiter.limit("100/minute")
async def root(request):
    return {
        "message": "Creatio Academy MCP Server",
        "version": "1.0.0",
        "endpoints": [
            "/content-search",
            "/video-transcripts/{video_id}",
            "/code-examples",
            "/documentation-queries",
            "/developer-course",
            "/ws/stream"
        ]
    }

# Health check endpoint
@app.get("/health", tags=["System"])
@limiter.limit("60/minute")
async def health_check(request):
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0"
    }

# Authentication endpoint
@app.post("/auth/token", tags=["Authentication"])
@limiter.limit("5/minute")
async def login(request, username: str, password: str):
    """Get access token for API authentication"""
    # Simple authentication - replace with proper user management in production
    if username == "admin" and password == "password":  # Change this!
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": username}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}
    else:
        raise HTTPException(status_code=401, detail="Incorrect username or password")

@app.post("/content-search", tags=["Content"])
@limiter.limit("30/minute")
async def content_search_endpoint(request, search_request: ContentSearchRequest, username: str = Depends(verify_token)):
    """Search across all content types"""
    try:
        results = search_content(
            query=search_request.query,
            content_type=search_request.content_type or "all",
            limit=search_request.limit
        )
        
        return {
            "query": search_request.query,
            "total_results": len(results),
            "results": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")

@app.get("/video-transcripts/{video_id}", tags=["Videos"])
@limiter.limit("60/minute")
async def get_video_transcript(request, video_id: str, include_metadata: bool = True, include_summary: bool = False, username: str = Depends(verify_token)):
    """Get video transcript by ID"""
    try:
        transcript_data = load_transcription_data(video_id)
        
        if not transcript_data:
            raise HTTPException(status_code=404, detail=f"Transcript not found for video {video_id}")
        
        response_data = {
            "video_id": video_id,
            "transcript": transcript_data
        }
        
        if not include_metadata and 'metadata' in transcript_data:
            del response_data['transcript']['metadata']
        
        if not include_summary and 'enhanced_summary' in transcript_data:
            del response_data['transcript']['enhanced_summary']
        
        return response_data
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve transcript: {str(e)}")

@app.post("/code-examples", tags=["Code"])
@limiter.limit("20/minute")
async def get_code_examples(request, code_request: CodeExampleRequest, username: str = Depends(verify_token)):
    """Extract code examples from documentation"""
    try:
        results = extract_code_examples(
            language=code_request.language,
            topic=code_request.topic,
            limit=code_request.limit
        )
        
        return {
            "language_filter": code_request.language,
            "topic_filter": code_request.topic,
            "total_examples": len(results),
            "examples": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Code extraction failed: {str(e)}")

@app.post("/developer-course", tags=["Developer Course"])
@limiter.limit("30/minute")
async def query_developer_course(request, course_request: DeveloperCourseRequest, username: str = Depends(verify_token)):
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

@app.post("/documentation-queries", tags=["Documentation"])
@limiter.limit("40/minute")
async def query_documentation(request, doc_request: DocumentationQueryRequest, username: str = Depends(verify_token)):
    """Query documentation content"""
    try:
        if doc_request.search_term:
            # Use existing search functionality
            results = search_documentation(doc_request.search_term.lower(), doc_request.limit)
        elif doc_request.doc_id:
            # Get specific document
            doc_path = Path("creatio-academy-archive/pages/raw") / f"{doc_request.doc_id}.html"
            if not doc_path.exists():
                raise HTTPException(status_code=404, detail=f"Document {doc_request.doc_id} not found")
            
            with open(doc_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            soup = BeautifulSoup(content, 'html.parser')
            results = [{
                'type': 'documentation',
                'doc_id': doc_request.doc_id,
                'title': soup.find('title').get_text() if soup.find('title') else 'No title',
                'content': soup.get_text()[:2000],  # Limit content length
                'full_path': str(doc_path)
            }]
        else:
            # List available documents
            doc_path = Path("creatio-academy-archive/pages/raw")
            html_files = list(doc_path.glob("*.html"))[:doc_request.limit]
            
            results = []
            for html_file in html_files:
                try:
                    with open(html_file, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                    soup = BeautifulSoup(content, 'html.parser')
                    title = soup.find('title')
                    
                    results.append({
                        'type': 'documentation',
                        'doc_id': html_file.stem,
                        'title': title.get_text() if title else html_file.name,
                        'file_path': str(html_file)
                    })
                except Exception:
                    continue
        
        return {
            "query_parameters": doc_request.dict(),
            "total_results": len(results),
            "results": results
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Documentation query failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
