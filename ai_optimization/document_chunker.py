import re
import json
import hashlib
from typing import List, Dict, Any, Optional, Tuple
from pathlib import Path
from dataclasses import dataclass
from bs4 import BeautifulSoup
import tiktoken


@dataclass
class DocumentChunk:
    """Represents a chunk of document content optimized for AI consumption."""
    chunk_id: str
    document_id: str
    content: str
    chunk_type: str  # 'heading', 'paragraph', 'code', 'list', 'table'
    chunk_index: int
    metadata: Dict[str, Any]
    word_count: int
    token_count: int
    context: Dict[str, Any]  # Surrounding context information


class SemanticDocumentChunker:
    """
    Intelligent document chunker that creates semantic chunks optimized for AI agents.
    """
    
    def __init__(self, max_chunk_size: int = 1000, overlap_size: int = 200, 
                 encoding_name: str = "cl100k_base"):
        """
        Initialize the document chunker.
        
        Args:
            max_chunk_size: Maximum tokens per chunk
            overlap_size: Overlap between chunks in tokens
            encoding_name: Tokenizer encoding to use
        """
        self.max_chunk_size = max_chunk_size
        self.overlap_size = overlap_size
        self.encoding = tiktoken.get_encoding(encoding_name)
        
        # Chunk type priorities for semantic preservation
        self.chunk_priorities = {
            'heading': 1,
            'code': 2,
            'table': 3,
            'list': 4,
            'paragraph': 5
        }
    
    def chunk_html_document(self, html_content: str, document_id: str, 
                           metadata: Optional[Dict] = None) -> List[DocumentChunk]:
        """
        Chunk an HTML document into semantic sections.
        
        Args:
            html_content: Raw HTML content
            document_id: Unique identifier for the document
            metadata: Additional document metadata
            
        Returns:
            List of DocumentChunk objects
        """
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Extract document structure
        structure = self._extract_document_structure(soup)
        
        # Create semantic chunks
        chunks = []
        chunk_index = 0
        
        for section in structure['sections']:
            section_chunks = self._chunk_section(
                section, document_id, chunk_index, metadata or {}
            )
            chunks.extend(section_chunks)
            chunk_index += len(section_chunks)
        
        return chunks
    
    def chunk_text_document(self, text_content: str, document_id: str,
                           metadata: Optional[Dict] = None) -> List[DocumentChunk]:
        """
        Chunk plain text document with intelligent boundary detection.
        """
        # Split by paragraphs and headings
        sections = self._split_text_by_structure(text_content)
        
        chunks = []
        chunk_index = 0
        
        for section in sections:
            section_chunks = self._chunk_text_section(
                section, document_id, chunk_index, metadata or {}
            )
            chunks.extend(section_chunks)
            chunk_index += len(section_chunks)
        
        return chunks
    
    def _extract_document_structure(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Extract hierarchical structure from HTML document."""
        structure = {
            'title': self._extract_title(soup),
            'sections': []
        }
        
        # Find all structural elements
        structural_elements = soup.find_all([
            'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
            'p', 'div', 'section', 'article',
            'pre', 'code', 'table', 'ul', 'ol'
        ])
        
        current_section = None
        current_heading = None
        
        for element in structural_elements:
            if element.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                # Start new section
                if current_section:
                    structure['sections'].append(current_section)
                
                current_heading = {
                    'level': int(element.name[1]),
                    'text': element.get_text().strip(),
                    'element': element
                }
                
                current_section = {
                    'heading': current_heading,
                    'content_elements': []
                }
            
            elif current_section:
                # Add to current section
                current_section['content_elements'].append(element)
            else:
                # Create section without heading
                if not current_section:
                    current_section = {
                        'heading': None,
                        'content_elements': []
                    }
                current_section['content_elements'].append(element)
        
        # Add final section
        if current_section:
            structure['sections'].append(current_section)
        
        return structure
    
    def _chunk_section(self, section: Dict, document_id: str, 
                      start_index: int, metadata: Dict) -> List[DocumentChunk]:
        """Chunk a document section intelligently."""
        chunks = []
        
        # Extract section text and structure
        heading_text = ""
        if section['heading']:
            heading_text = section['heading']['text']
        
        content_elements = []
        for element in section['content_elements']:
            element_info = self._analyze_element(element)
            content_elements.append(element_info)
        
        # Group elements into chunks based on token limits
        current_chunk_elements = []
        current_tokens = 0
        
        # Add heading to context if present
        heading_tokens = len(self.encoding.encode(heading_text)) if heading_text else 0
        
        for element_info in content_elements:
            element_tokens = element_info['token_count']
            
            # Check if adding this element would exceed limit
            if (current_tokens + element_tokens + heading_tokens > self.max_chunk_size 
                and current_chunk_elements):
                
                # Create chunk from current elements
                chunk = self._create_chunk_from_elements(
                    current_chunk_elements, document_id, 
                    start_index + len(chunks), heading_text, metadata
                )
                chunks.append(chunk)
                
                # Start new chunk with overlap
                current_chunk_elements = self._get_overlap_elements(
                    current_chunk_elements, self.overlap_size
                )
                current_tokens = sum(el['token_count'] for el in current_chunk_elements)
            
            current_chunk_elements.append(element_info)
            current_tokens += element_tokens
        
        # Create final chunk
        if current_chunk_elements:
            chunk = self._create_chunk_from_elements(
                current_chunk_elements, document_id,
                start_index + len(chunks), heading_text, metadata
            )
            chunks.append(chunk)
        
        return chunks
    
    def _analyze_element(self, element) -> Dict[str, Any]:
        """Analyze an HTML element for chunking purposes."""
        text = element.get_text().strip()
        
        element_info = {
            'tag': element.name,
            'text': text,
            'word_count': len(text.split()),
            'token_count': len(self.encoding.encode(text)),
            'type': self._classify_element_type(element),
            'attributes': dict(element.attrs) if element.attrs else {},
            'element': element
        }
        
        # Special handling for code blocks
        if element.name in ['pre', 'code']:
            element_info['language'] = self._detect_code_language(text, element)
        
        # Special handling for tables
        if element.name == 'table':
            element_info['table_structure'] = self._analyze_table_structure(element)
        
        return element_info
    
    def _classify_element_type(self, element) -> str:
        """Classify element type for chunking strategy."""
        if element.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            return 'heading'
        elif element.name in ['pre', 'code']:
            return 'code'
        elif element.name == 'table':
            return 'table'
        elif element.name in ['ul', 'ol']:
            return 'list'
        else:
            return 'paragraph'
    
    def _detect_code_language(self, code_text: str, element) -> str:
        """Detect programming language of code block."""
        # Check class attributes first
        classes = element.get('class', [])
        for cls in classes:
            if 'language-' in cls:
                return cls.replace('language-', '')
            elif 'lang-' in cls:
                return cls.replace('lang-', '')
        
        # Simple heuristic detection
        if 'function' in code_text and '{' in code_text:
            return 'javascript'
        elif 'def ' in code_text or 'import ' in code_text:
            return 'python'
        elif 'SELECT' in code_text.upper() or 'FROM' in code_text.upper():
            return 'sql'
        elif code_text.strip().startswith('<') and code_text.strip().endswith('>'):
            return 'xml'
        elif code_text.strip().startswith('{') and code_text.strip().endswith('}'):
            return 'json'
        
        return 'text'
    
    def _analyze_table_structure(self, table_element) -> Dict[str, Any]:
        """Analyze table structure for better chunking."""
        rows = table_element.find_all('tr')
        
        structure = {
            'row_count': len(rows),
            'has_header': False,
            'columns': []
        }
        
        if rows:
            # Check for header
            first_row = rows[0]
            if first_row.find('th'):
                structure['has_header'] = True
                headers = [th.get_text().strip() for th in first_row.find_all('th')]
                structure['columns'] = headers
            else:
                # Estimate columns from first row
                cells = first_row.find_all(['td', 'th'])
                structure['columns'] = [f'Column_{i+1}' for i in range(len(cells))]
        
        return structure
    
    def _create_chunk_from_elements(self, elements: List[Dict], document_id: str,
                                   chunk_index: int, heading_context: str,
                                   metadata: Dict) -> DocumentChunk:
        """Create a DocumentChunk from a list of elements."""
        # Combine element texts
        content_parts = []
        if heading_context:
            content_parts.append(f"# {heading_context}")
        
        for element in elements:
            content_parts.append(element['text'])
        
        content = '\n\n'.join(content_parts)
        
        # Calculate statistics
        word_count = len(content.split())
        token_count = len(self.encoding.encode(content))
        
        # Determine primary chunk type
        element_types = [el['type'] for el in elements]
        primary_type = min(set(element_types), key=lambda x: self.chunk_priorities.get(x, 10))
        
        # Create chunk ID
        chunk_id = hashlib.md5(f"{document_id}_{chunk_index}_{content[:100]}".encode()).hexdigest()
        
        # Build context information
        context = {
            'heading': heading_context,
            'element_types': element_types,
            'position_in_document': chunk_index,
            'languages': [el.get('language') for el in elements if el.get('language')],
            'has_code': any(el['type'] == 'code' for el in elements),
            'has_table': any(el['type'] == 'table' for el in elements)
        }
        
        # Combine metadata
        chunk_metadata = {
            **metadata,
            'chunk_statistics': {
                'element_count': len(elements),
                'primary_tags': list(set(el['tag'] for el in elements)),
                'complexity_score': self._calculate_complexity_score(elements)
            }
        }
        
        return DocumentChunk(
            chunk_id=chunk_id,
            document_id=document_id,
            content=content,
            chunk_type=primary_type,
            chunk_index=chunk_index,
            metadata=chunk_metadata,
            word_count=word_count,
            token_count=token_count,
            context=context
        )
    
    def _calculate_complexity_score(self, elements: List[Dict]) -> float:
        """Calculate complexity score for chunk prioritization."""
        score = 0.0
        
        for element in elements:
            # Base score by type
            type_scores = {
                'heading': 2.0,
                'code': 3.0,
                'table': 2.5,
                'list': 1.5,
                'paragraph': 1.0
            }
            score += type_scores.get(element['type'], 1.0)
            
            # Bonus for longer content
            if element['word_count'] > 100:
                score += 0.5
            
            # Bonus for code with specific languages
            if element.get('language') in ['python', 'javascript', 'sql', 'csharp']:
                score += 1.0
        
        return score / len(elements) if elements else 0.0
    
    def _get_overlap_elements(self, elements: List[Dict], overlap_tokens: int) -> List[Dict]:
        """Get elements for chunk overlap."""
        overlap_elements = []
        current_tokens = 0
        
        # Start from the end and work backwards
        for element in reversed(elements):
            if current_tokens + element['token_count'] <= overlap_tokens:
                overlap_elements.insert(0, element)
                current_tokens += element['token_count']
            else:
                break
        
        return overlap_elements
    
    def _extract_title(self, soup: BeautifulSoup) -> str:
        """Extract document title."""
        title_tag = soup.find('title')
        if title_tag:
            return title_tag.get_text().strip()
        
        # Fallback to first h1
        h1_tag = soup.find('h1')
        if h1_tag:
            return h1_tag.get_text().strip()
        
        return "Untitled Document"
    
    def _split_text_by_structure(self, text: str) -> List[Dict]:
        """Split plain text into structural sections."""
        sections = []
        
        # Split by double newlines (paragraph boundaries)
        paragraphs = re.split(r'\n\s*\n', text)
        
        current_section = {'heading': None, 'content': []}
        
        for paragraph in paragraphs:
            paragraph = paragraph.strip()
            if not paragraph:
                continue
            
            # Check if this looks like a heading
            if self._is_text_heading(paragraph):
                # Start new section
                if current_section['content']:
                    sections.append(current_section)
                
                current_section = {
                    'heading': paragraph,
                    'content': []
                }
            else:
                current_section['content'].append(paragraph)
        
        # Add final section
        if current_section['content']:
            sections.append(current_section)
        
        return sections
    
    def _is_text_heading(self, text: str) -> bool:
        """Determine if text line is likely a heading."""
        # Simple heuristics for heading detection
        if len(text) > 100:  # Too long to be a heading
            return False
        
        # Check for heading patterns
        heading_patterns = [
            r'^[A-Z][^.!?]*$',  # ALL CAPS or Title Case without punctuation
            r'^\d+\.?\s+[A-Z]',  # Numbered headings
            r'^#{1,6}\s+',       # Markdown-style headings
        ]
        
        for pattern in heading_patterns:
            if re.match(pattern, text):
                return True
        
        return False
    
    def _chunk_text_section(self, section: Dict, document_id: str,
                           start_index: int, metadata: Dict) -> List[DocumentChunk]:
        """Chunk a plain text section."""
        chunks = []
        
        heading = section.get('heading', '')
        content_paragraphs = section.get('content', [])
        
        # Combine paragraphs into chunks
        current_chunk_content = []
        current_tokens = 0
        
        heading_tokens = len(self.encoding.encode(heading)) if heading else 0
        
        for paragraph in content_paragraphs:
            paragraph_tokens = len(self.encoding.encode(paragraph))
            
            if (current_tokens + paragraph_tokens + heading_tokens > self.max_chunk_size 
                and current_chunk_content):
                
                # Create chunk
                chunk = self._create_text_chunk(
                    current_chunk_content, document_id,
                    start_index + len(chunks), heading, metadata
                )
                chunks.append(chunk)
                
                # Start new chunk with overlap
                overlap_content = self._get_text_overlap(current_chunk_content, self.overlap_size)
                current_chunk_content = overlap_content
                current_tokens = sum(len(self.encoding.encode(p)) for p in current_chunk_content)
            
            current_chunk_content.append(paragraph)
            current_tokens += paragraph_tokens
        
        # Create final chunk
        if current_chunk_content:
            chunk = self._create_text_chunk(
                current_chunk_content, document_id,
                start_index + len(chunks), heading, metadata
            )
            chunks.append(chunk)
        
        return chunks
    
    def _create_text_chunk(self, paragraphs: List[str], document_id: str,
                          chunk_index: int, heading: str, metadata: Dict) -> DocumentChunk:
        """Create a DocumentChunk from text paragraphs."""
        content_parts = []
        if heading:
            content_parts.append(f"# {heading}")
        content_parts.extend(paragraphs)
        
        content = '\n\n'.join(content_parts)
        
        word_count = len(content.split())
        token_count = len(self.encoding.encode(content))
        
        chunk_id = hashlib.md5(f"{document_id}_{chunk_index}_{content[:100]}".encode()).hexdigest()
        
        context = {
            'heading': heading,
            'paragraph_count': len(paragraphs),
            'position_in_document': chunk_index
        }
        
        return DocumentChunk(
            chunk_id=chunk_id,
            document_id=document_id,
            content=content,
            chunk_type='paragraph',
            chunk_index=chunk_index,
            metadata=metadata,
            word_count=word_count,
            token_count=token_count,
            context=context
        )
    
    def _get_text_overlap(self, paragraphs: List[str], overlap_tokens: int) -> List[str]:
        """Get paragraphs for text overlap."""
        overlap_paragraphs = []
        current_tokens = 0
        
        for paragraph in reversed(paragraphs):
            paragraph_tokens = len(self.encoding.encode(paragraph))
            if current_tokens + paragraph_tokens <= overlap_tokens:
                overlap_paragraphs.insert(0, paragraph)
                current_tokens += paragraph_tokens
            else:
                break
        
        return overlap_paragraphs
    
    def export_chunks_for_rag(self, chunks: List[DocumentChunk], 
                             output_path: Path) -> None:
        """Export chunks in RAG-compatible format."""
        rag_data = []
        
        for chunk in chunks:
            rag_entry = {
                'id': chunk.chunk_id,
                'document_id': chunk.document_id,
                'content': chunk.content,
                'metadata': {
                    **chunk.metadata,
                    'chunk_type': chunk.chunk_type,
                    'chunk_index': chunk.chunk_index,
                    'word_count': chunk.word_count,
                    'token_count': chunk.token_count,
                    'context': chunk.context
                }
            }
            rag_data.append(rag_entry)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(rag_data, f, indent=2, ensure_ascii=False)
