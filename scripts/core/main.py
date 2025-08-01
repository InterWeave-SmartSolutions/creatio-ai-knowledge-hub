# main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

app = FastAPI(
    title="Creatio API",
    description="API for AI agent access to documentation and content",
    version="1.0.0"
)

# CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust as necessary for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


# Example endpoint
@app.get("/api/content-search")
async def content_search(query: str):
    return JSONResponse(content={"message": "Content search results here", "query": query})


@app.get("/api/transcript-access")
async def video_transcript(video_id: str):
    return JSONResponse(content={"message": "Video transcript here", "video_id": video_id})


@app.get("/api/code-examples")
async def code_example_extraction(topic: str):
    return JSONResponse(content={"message": "Code examples here", "topic": topic})


@app.get("/api/doc-queries")
async def documentation_queries(doc_id: str):
    return JSONResponse(content={"message": "Documentation content here", "doc_id": doc_id})


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

