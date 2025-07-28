"""
Comprehensive Search Engine Package for Creatio Academy

This package provides multi-level indexing and search capabilities including:
- Full-text search with Elasticsearch/Whoosh
- Semantic search with embeddings
- OCR text extraction from images
- Faceted search with filters
- Autocomplete and suggestion features
"""

from .core import SearchEngineCore
from .indexers import DocumentIndexer, VideoIndexer, CodeIndexer, ImageIndexer
from .semantic_search import SemanticSearchEngine
from .faceted_search import FacetedSearchEngine
from .autocomplete import AutocompleteEngine

__version__ = "1.0.0"
__all__ = [
    "SearchEngineCore",
    "DocumentIndexer", 
    "VideoIndexer",
    "CodeIndexer",
    "ImageIndexer",
    "SemanticSearchEngine",
    "FacetedSearchEngine",
    "AutocompleteEngine"
]
