from search_engine.core import SearchEngineCore
from whoosh.qparser import QueryParser
import json
import os
import re
from bs4 import BeautifulSoup
import pytesseract
from PIL import Image

class DocumentIndexer:
    def __init__(self, core: SearchEngineCore):
        self.core = core

    def index_html_documents(self, directory='creatio-academy-archive/pages/raw'):
        writer = self.core.ix.writer()
        for filename in os.listdir(directory):
            if filename.endswith('.html'):
                filepath = os.path.join(directory, filename)
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    soup = BeautifulSoup(content, 'html.parser')
                    text_content = soup.get_text()
                    title = soup.title.string if soup.title else filename
                    writer.add_document(title=title, path=filepath, content=text_content)
        writer.commit()
    
    def index_developer_course_documents(self, directory='ai_optimization/creatio-academy-db/developer_course'):
        """Index developer course PDF and video content chunks"""
        writer = self.core.ix.writer()
        
        # Load master index to get content info
        master_index_path = os.path.join(directory, 'master_index.json')
        if not os.path.exists(master_index_path):
            print(f"Master index not found at {master_index_path}")
            return
            
        with open(master_index_path, 'r', encoding='utf-8') as f:
            master_index = json.load(f)
        
        # Index content from chunks files
        for doc_id, doc_info in master_index.get('content_index', {}).items():
            chunks_file = os.path.join(directory, doc_info.get('chunks_file', ''))
            if os.path.exists(chunks_file):
                with open(chunks_file, 'r', encoding='utf-8') as f:
                    chunks_data = json.load(f)
                
                for chunk in chunks_data.get('chunks', []):
                    chunk_content = chunk.get('content', '')
                    if chunk_content:
                        title = f"{doc_info.get('title', 'Unknown')} - Chunk {chunk.get('id', '')}"
                        writer.add_document(
                            title=title,
                            path=chunks_file,
                            content=chunk_content,
                            content_type=doc_info.get('type', 'unknown'),
                            source_file=doc_info.get('source_file', '')
                        )
        writer.commit()

class VideoIndexer:
    def __init__(self, core: SearchEngineCore):
        self.core = core

    def index_transcriptions(self, directory='transcriptions/transcripts'):
        writer = self.core.ix.writer()
        if os.path.exists(directory):
            for filename in os.listdir(directory):
                if filename.endswith('.json'):
                    filepath = os.path.join(directory, filename)
                    with open(filepath, 'r', encoding='utf-8') as f:
                        transcript_data = json.load(f)
                        transcript_text = transcript_data.get('text', '')
                        if transcript_text:
                            writer.add_document(title=filename, path=filepath, content=transcript_text)
        
        # Also index developer course transcripts
        dev_course_transcripts = 'ai_optimization/creatio-academy-db/developer_course/transcripts'
        if os.path.exists(dev_course_transcripts):
            for filename in os.listdir(dev_course_transcripts):
                if filename.endswith('.json'):
                    filepath = os.path.join(dev_course_transcripts, filename)
                    with open(filepath, 'r', encoding='utf-8') as f:
                        transcript_data = json.load(f)
                        transcript_text = transcript_data.get('text', '')
                        if transcript_text:
                            title = transcript_data.get('title', filename)
                            writer.add_document(
                                title=title, 
                                path=filepath, 
                                content=transcript_text,
                                content_type='video_transcript'
                            )
        writer.commit()

class CodeIndexer:
    def __init__(self, core: SearchEngineCore):
        self.core = core

    def index_code_samples(self, document_path='creatio-academy-archive/pages/raw'):
        writer = self.core.ix.writer()
        for filename in os.listdir(document_path):
            if filename.endswith('.html'):
                filepath = os.path.join(document_path, filename)
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    soup = BeautifulSoup(content, 'html.parser')
                    code_blocks = soup.find_all(['pre', 'code'])
                    for code_block in code_blocks:
                        code_text = code_block.get_text()
                        if len(code_text) > 20:  # Arbitrary length filter
                            writer.add_document(title=filename, path=filepath, content=code_text)
        writer.commit()

class ImageIndexer:
    def __init__(self, core: SearchEngineCore):
        self.core = core

    def index_images(self, directory='images', ocr_enabled=True):
        writer = self.core.ix.writer()
        for filename in os.listdir(directory):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                filepath = os.path.join(directory, filename)
                if ocr_enabled:
                    text = pytesseract.image_to_string(Image.open(filepath))
                    writer.add_document(title=filename, path=filepath, content=text)
        writer.commit()
