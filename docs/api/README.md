---
title: 'API Reference'
tags: [docs, api]
description:
  'Auto-generated front matter for AI indexing. Improve this description.'
source_path: 'docs/api/README.md'
last_updated: '2025-08-06'
---

# API Reference

Complete API reference for the Creatio AI Knowledge Hub MCP Server and related
services.

## Base Information

**Base URL**: `http://localhost:8000`  
**WebSocket URL**: `ws://localhost:8001`  
**API Version**: `v1`  
**Content Type**: `application/json`

## Authentication

### API Key Authentication

```http
Authorization: Bearer your_api_key_here
```

### Session-based Authentication

```http
Cookie: session_id=your_session_id
```

## Core Endpoints

### Health Check

**GET** `/health`

Check server status and basic system information.

**Response:**

```json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2025-01-27T10:30:00Z",
  "uptime": 3600,
  "components": {
    "database": "healthy",
    "search": "healthy",
    "processing": "healthy"
  }
}
```

### Search API

**GET** `/mcp/search`

Search across all indexed content.

**Parameters:**

- `q` (string, required): Search query
- `type` (string, optional): Content type filter (`documentation`, `video`,
  `pdf`, `all`)
- `limit` (integer, optional): Maximum results (default: 10, max: 100)
- `offset` (integer, optional): Result offset for pagination
- `sort` (string, optional): Sort order (`relevance`, `date`, `title`)

**Example:**

```bash
curl "http://localhost:8000/mcp/search?q=Creatio%20installation&type=video&limit=5"
```

**Response:**

```json
{
  "query": "Creatio installation",
  "results": [
    {
      "id": "lf-yWsJ4p0Q",
      "title": "Tech Hour - Installing Local instance of Creatio",
      "content": "Complete installation guide for setting up Creatio locally...",
      "type": "video",
      "source": "youtube",
      "score": 0.95,
      "metadata": {
        "duration": 3600,
        "upload_date": "2024-01-15",
        "tags": ["installation", "tutorial"]
      },
      "url": "https://youtube.com/watch?v=lf-yWsJ4p0Q"
    }
  ],
  "total": 25,
  "page": 1,
  "per_page": 5,
  "query_time": 0.045
}
```

**POST** `/mcp/search/advanced`

Advanced search with complex filtering and facets.

**Request Body:**

```json
{
  "query": "Creatio workflow configuration",
  "filters": {
    "type": ["documentation", "video"],
    "date_range": {
      "start": "2024-01-01",
      "end": "2024-12-31"
    },
    "tags": ["workflow", "configuration"],
    "difficulty": ["beginner", "intermediate"]
  },
  "sort": [
    { "field": "relevance", "order": "desc" },
    { "field": "date", "order": "desc" }
  ],
  "facets": ["type", "tags", "difficulty", "source"],
  "highlight": {
    "fields": ["title", "content"],
    "fragment_size": 150
  },
  "limit": 20,
  "offset": 0
}
```

### Content API

**GET** `/mcp/content/{content_id}`

Retrieve full content details by ID.

**Parameters:**

- `content_id` (string, required): Unique content identifier
- `include_related` (boolean, optional): Include related content
- `format` (string, optional): Response format (`json`, `text`, `markdown`)

**Response:**

```json
{
  "id": "lf-yWsJ4p0Q",
  "title": "Tech Hour - Installing Local instance of Creatio",
  "type": "video",
  "source": "youtube",
  "content": {
    "transcript": "Welcome to Creatio Tech Hour...",
    "summary": "This video covers complete installation...",
    "key_points": [
      "System requirements",
      "Database setup",
      "Application configuration"
    ]
  },
  "metadata": {
    "duration": 3600,
    "upload_date": "2024-01-15",
    "uploader": "Creatio",
    "tags": ["installation", "tutorial"],
    "language": "en",
    "difficulty": "intermediate"
  },
  "related_content": [
    {
      "id": "abc123",
      "title": "Database Configuration Guide",
      "type": "documentation",
      "relevance": 0.85
    }
  ],
  "processing_info": {
    "processed_at": "2024-01-16T10:00:00Z",
    "transcription_model": "whisper-large-v2",
    "analysis_complete": true
  }
}
```

**POST** `/mcp/content/batch`

Retrieve multiple content items in a single request.

**Request Body:**

```json
{
  "ids": ["lf-yWsJ4p0Q", "abc123", "def456"],
  "fields": ["title", "content", "metadata"],
  "include_related": false
}
```

### Processing API

**POST** `/mcp/process/video`

Submit a video for processing.

**Request Body:**

```json
{
  "url": "https://youtube.com/watch?v=VIDEO_ID",
  "options": {
    "transcription": true,
    "analysis": true,
    "summary": true,
    "extract_key_points": true
  },
  "priority": "normal",
  "callback_url": "https://your-app.com/webhook"
}
```

**Response:**

```json
{
  "task_id": "task_12345",
  "status": "queued",
  "estimated_time": 300,
  "created_at": "2024-01-27T10:30:00Z"
}
```

**GET** `/mcp/process/status/{task_id}`

Check processing status.

**Response:**

```json
{
  "task_id": "task_12345",
  "status": "processing",
  "progress": 65,
  "current_stage": "transcription",
  "estimated_remaining": 120,
  "result": null,
  "error": null
}
```

### Analytics API

**GET** `/mcp/analytics/stats`

Get system statistics and usage metrics.

**Response:**

```json
{
  "content_stats": {
    "total_items": 1500,
    "by_type": {
      "video": 145,
      "documentation": 1200,
      "pdf": 155
    },
    "processing_queue": 5,
    "last_updated": "2024-01-27T09:00:00Z"
  },
  "search_stats": {
    "total_queries": 25000,
    "avg_response_time": 0.045,
    "popular_queries": [
      "Creatio installation",
      "workflow configuration",
      "API integration"
    ]
  },
  "system_stats": {
    "uptime": 86400,
    "memory_usage": "1.2GB",
    "disk_usage": "15.5GB",
    "cpu_usage": "25%"
  }
}
```

## WebSocket API

### Connection

Connect to the WebSocket server for real-time updates:

```javascript
const ws = new WebSocket('ws://localhost:8001/mcp/stream');
```

### Message Format

All WebSocket messages use JSON format:

```json
{
  "type": "message_type",
  "data": {},
  "timestamp": "2024-01-27T10:30:00Z",
  "id": "msg_12345"
}
```

### Message Types

#### Search Streaming

**Client → Server:**

```json
{
  "type": "search_stream",
  "data": {
    "query": "Creatio configuration",
    "stream_results": true,
    "max_results": 50
  }
}
```

**Server → Client:**

```json
{
  "type": "search_result",
  "data": {
    "result": {
      "id": "abc123",
      "title": "Configuration Guide",
      "score": 0.92
    },
    "position": 1,
    "total_expected": 25
  }
}
```

#### Processing Updates

**Server → Client:**

```json
{
  "type": "processing_update",
  "data": {
    "task_id": "task_12345",
    "status": "transcribing",
    "progress": 45,
    "message": "Transcribing video segment 3 of 8"
  }
}
```

#### System Notifications

**Server → Client:**

```json
{
  "type": "system_notification",
  "data": {
    "level": "info",
    "message": "Search index updated with 150 new items",
    "category": "index_update"
  }
}
```

## Error Handling

### Error Response Format

```json
{
  "error": {
    "code": "INVALID_QUERY",
    "message": "Search query cannot be empty",
    "details": {
      "field": "query",
      "provided": "",
      "expected": "non-empty string"
    },
    "request_id": "req_12345",
    "timestamp": "2024-01-27T10:30:00Z"
  }
}
```

### Common Error Codes

| Code                  | HTTP Status | Description                          |
| --------------------- | ----------- | ------------------------------------ |
| `INVALID_QUERY`       | 400         | Search query is invalid or malformed |
| `CONTENT_NOT_FOUND`   | 404         | Requested content ID does not exist  |
| `RATE_LIMIT_EXCEEDED` | 429         | API rate limit exceeded              |
| `PROCESSING_FAILED`   | 422         | Content processing failed            |
| `UNAUTHORIZED`        | 401         | Invalid or missing authentication    |
| `FORBIDDEN`           | 403         | Insufficient permissions             |
| `INTERNAL_ERROR`      | 500         | Server internal error                |
| `SERVICE_UNAVAILABLE` | 503         | Service temporarily unavailable      |

## Rate Limiting

### Limits

| Endpoint Category | Requests per Minute | Authenticated | Anonymous |
| ----------------- | ------------------- | ------------- | --------- |
| Search API        | 100                 | 1000          | 60        |
| Content API       | 200                 | 2000          | 100       |
| Processing API    | 20                  | 100           | 10        |
| Analytics API     | 60                  | 300           | 30        |

### Rate Limit Headers

```http
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 85
X-RateLimit-Reset: 1643280000
X-RateLimit-Window: 60
```

## SDKs and Examples

### Python SDK

```python
from creatio_ai_hub import MCPClient

client = MCPClient(
    base_url="http://localhost:8000",
    api_key="your_api_key"
)

# Search content
results = client.search(
    query="Creatio installation",
    content_type="video",
    limit=10
)

# Get content details
content = client.get_content("lf-yWsJ4p0Q")

# Process video
task = client.process_video(
    url="https://youtube.com/watch?v=VIDEO_ID",
    options={"transcription": True, "analysis": True}
)

# Monitor processing
status = client.get_processing_status(task.id)
```

### JavaScript SDK

```javascript
import { MCPClient } from '@creatio/ai-hub-sdk';

const client = new MCPClient({
  baseUrl: 'http://localhost:8000',
  apiKey: 'your_api_key',
});

// Search with async/await
const results = await client.search({
  query: 'Creatio installation',
  type: 'video',
  limit: 10,
});

// WebSocket streaming
const stream = client.createSearchStream();
stream.on('result', result => {
  console.log('New result:', result);
});
stream.search('Creatio configuration');
```

### cURL Examples

**Basic Search:**

```bash
curl -X GET \
  "http://localhost:8000/mcp/search?q=Creatio%20installation&limit=5" \
  -H "Authorization: Bearer your_api_key"
```

**Advanced Search:**

```bash
curl -X POST \
  "http://localhost:8000/mcp/search/advanced" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your_api_key" \
  -d '{
    "query": "workflow configuration",
    "filters": {"type": ["documentation"]},
    "limit": 10
  }'
```

**Process Video:**

```bash
curl -X POST \
  "http://localhost:8000/mcp/process/video" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your_api_key" \
  -d '{
    "url": "https://youtube.com/watch?v=VIDEO_ID",
    "options": {"transcription": true}
  }'
```

## OpenAPI Specification

The complete OpenAPI 3.0 specification is available at:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## Changelog

### v1.0.0 (2025-01-27)

- Initial API release
- Search, content, and processing endpoints
- WebSocket support for real-time updates
- Authentication and rate limiting

### v1.1.0 (Planned)

- Batch processing endpoints
- Enhanced analytics
- GraphQL support
- Webhook notifications

---

For more examples and detailed integration guides, see the
[Integration Examples](../examples/) section.
