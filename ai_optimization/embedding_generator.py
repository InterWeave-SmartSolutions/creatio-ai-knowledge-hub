#!/usr/bin/env python3
"""
Advanced embedding generation system for AI-optimized content.
Integrates with the document chunker and provides multiple embedding strategies.
"""

import json
import numpy as np
import faiss
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
import logging
import hashlib

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import torch

from document_chunker import DocumentChunk

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class EmbeddingMetadata:
    """Metadata for embeddings."""
    embedding_id: str
    chunk_id: str
    model_name: str
    embedding_dimension: int
    created_timestamp: str
    similarity_cluster: Optional[int] = None
    topic_keywords: Optional[List[str]] = None


class AdvancedEmbeddingGenerator:
    """
    Advanced embedding generation system with multiple strategies and optimizations.
    """
    
    def __init__(self, 
                 model_name: str = "all-MiniLM-L6-v2",
                 output_path: str = "./embeddings",
                 batch_size: int = 32):
        """
        Initialize the embedding generator.
        
        Args:
            model_name: Sentence transformer model to use
            output_path: Path to store embeddings and indices
            batch_size: Batch size for processing
        """
        self.model_name = model_name
        self.output_path = Path(output_path)
        self.batch_size = batch_size
        
        # Create output directories
        self.output_path.mkdir(parents=True, exist_ok=True)
        (self.output_path / "vectors").mkdir(exist_ok=True)
        (self.output_path / "indices").mkdir(exist_ok=True)
        (self.output_path / "metadata").mkdir(exist_ok=True)
        (self.output_path / "clusters").mkdir(exist_ok=True)
        
        # Initialize models
        self.embedding_model = SentenceTransformer(model_name)
        self.embedding_dim = self.embedding_model.get_sentence_embedding_dimension()
        
        # Initialize FAISS indices
        self.indices = {}
        self.embeddings_cache = {}
        self.metadata_cache = {}
        
        logger.info(f"Initialized embedding generator with model: {model_name}")
        logger.info(f"Embedding dimension: {self.embedding_dim}")
    
    def generate_embeddings_for_chunks(self, 
                                     chunks: List[DocumentChunk],
                                     content_type: str = "mixed") -> Dict[str, Any]:
        """
        Generate embeddings for document chunks with advanced processing.
        
        Args:
            chunks: List of DocumentChunk objects
            content_type: Type of content for specialized processing
            
        Returns:
            Dictionary with embedding results and metadata
        """
        logger.info(f"Generating embeddings for {len(chunks)} chunks")
        
        if not chunks:
            return {"embeddings": [], "metadata": [], "index_path": None}
        
        # Prepare texts for embedding
        texts = []
        chunk_metadata = []
        
        for chunk in chunks:
            # Enhanced text preprocessing based on chunk type
            processed_text = self.preprocess_text_for_embedding(chunk)
            texts.append(processed_text)
            
            # Create metadata
            metadata = EmbeddingMetadata(
                embedding_id=self.generate_embedding_id(chunk.chunk_id),
                chunk_id=chunk.chunk_id,
                model_name=self.model_name,
                embedding_dimension=self.embedding_dim,
                created_timestamp=datetime.now().isoformat()
            )
            chunk_metadata.append(metadata)
        
        # Generate embeddings in batches
        all_embeddings = []
        
        for i in range(0, len(texts), self.batch_size):
            batch_texts = texts[i:i + self.batch_size]
            batch_embeddings = self.embedding_model.encode(
                batch_texts,
                batch_size=self.batch_size,
                show_progress_bar=True,
                normalize_embeddings=True
            )
            all_embeddings.extend(batch_embeddings)
        
        embeddings_array = np.array(all_embeddings, dtype=np.float32)
        
        # Perform clustering for topic discovery
        cluster_labels = self.perform_semantic_clustering(embeddings_array, chunks)
        
        # Update metadata with cluster information
        for i, metadata in enumerate(chunk_metadata):
            metadata.similarity_cluster = int(cluster_labels[i])
            metadata.topic_keywords = self.extract_topic_keywords_from_chunk(chunks[i])
        
        # Create and save FAISS index
        index_path = self.create_faiss_index(embeddings_array, content_type)
        
        # Save embeddings and metadata
        embeddings_file = self.output_path / "vectors" / f"{content_type}_embeddings.npy"
        metadata_file = self.output_path / "metadata" / f"{content_type}_metadata.json"
        
        np.save(embeddings_file, embeddings_array)
        
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump([asdict(meta) for meta in chunk_metadata], f, indent=2, ensure_ascii=False)
        
        # Generate embedding statistics
        stats = self.calculate_embedding_statistics(embeddings_array, chunk_metadata)
        
        result = {
            "total_embeddings": len(all_embeddings),
            "embedding_dimension": self.embedding_dim,
            "embeddings_file": str(embeddings_file),
            "metadata_file": str(metadata_file),
            "index_path": index_path,
            "statistics": stats,
            "clusters": {
                "total_clusters": len(set(cluster_labels)),
                "cluster_distribution": self.analyze_cluster_distribution(cluster_labels, chunks)
            }
        }
        
        logger.info(f"Generated {len(all_embeddings)} embeddings with {len(set(cluster_labels))} clusters")
        return result
    
    def preprocess_text_for_embedding(self, chunk: DocumentChunk) -> str:
        """
        Preprocess text based on chunk type for optimal embeddings.
        """
        text = chunk.content
        
        # Add context information for better embeddings
        context_parts = []
        
        # Add heading context if available
        if chunk.context.get('heading'):
            context_parts.append(f"Section: {chunk.context['heading']}")
        
        # Add chunk type context
        if chunk.chunk_type != 'paragraph':
            context_parts.append(f"Content type: {chunk.chunk_type}")
        
        # Special handling for code chunks
        if chunk.chunk_type == 'code' and chunk.context.get('languages'):
            languages = [lang for lang in chunk.context['languages'] if lang]
            if languages:
                context_parts.append(f"Programming languages: {', '.join(languages)}")
        
        # Combine context with content
        if context_parts:
            context_prefix = " | ".join(context_parts) + " | "
            return context_prefix + text
        
        return text
    
    def perform_semantic_clustering(self, 
                                   embeddings: np.ndarray, 
                                   chunks: List[DocumentChunk],
                                   max_clusters: int = None) -> np.ndarray:
        """
        Perform semantic clustering on embeddings to discover topics.
        """
        if max_clusters is None:
            # Dynamic cluster number based on content size
            max_clusters = min(50, max(5, len(chunks) // 20))
        
        # Use K-means clustering
        kmeans = KMeans(n_clusters=max_clusters, random_state=42, n_init=10)
        cluster_labels = kmeans.fit_predict(embeddings)
        
        # Save cluster information
        cluster_info = {
            'cluster_centers': kmeans.cluster_centers_.tolist(),
            'cluster_labels': cluster_labels.tolist(),
            'n_clusters': max_clusters,
            'inertia': float(kmeans.inertia_)
        }
        
        cluster_file = self.output_path / "clusters" / "semantic_clusters.json"
        with open(cluster_file, 'w', encoding='utf-8') as f:
            json.dump(cluster_info, f, indent=2)
        
        logger.info(f"Created {max_clusters} semantic clusters")
        return cluster_labels
    
    def extract_topic_keywords_from_chunk(self, chunk: DocumentChunk) -> List[str]:
        """
        Extract topic keywords from chunk content using simple heuristics.
        """
        # Common technical keywords relevant to Creatio development
        technical_keywords = [
            'schema', 'entity', 'business process', 'workflow', 'integration',
            'api', 'database', 'configuration', 'customization', 'development',
            'module', 'package', 'section', 'page', 'detail', 'lookup',
            'javascript', 'c#', 'sql', 'json', 'xml', 'web service',
            'client', 'server', 'data', 'record', 'field', 'column',
            'user', 'security', 'permission', 'role', 'access'
        ]
        
        text_lower = chunk.content.lower()
        found_keywords = []
        
        for keyword in technical_keywords:
            if keyword in text_lower:
                found_keywords.append(keyword)
        
        # Add chunk-specific keywords based on type
        if chunk.chunk_type == 'code':
            found_keywords.append('code_example')
        elif chunk.chunk_type == 'table':
            found_keywords.append('data_structure')
        
        return found_keywords[:10]  # Limit to top 10 keywords
    
    def create_faiss_index(self, embeddings: np.ndarray, content_type: str) -> str:
        """
        Create and save FAISS index for efficient similarity search.
        """
        # Create FAISS index
        index = faiss.IndexFlatIP(self.embedding_dim)  # Inner product for cosine similarity
        
        # Normalize embeddings for cosine similarity
        faiss.normalize_L2(embeddings)
        
        # Add embeddings to index
        index.add(embeddings)
        
        # Save index
        index_path = self.output_path / "indices" / f"{content_type}_index.faiss"
        faiss.write_index(index, str(index_path))
        
        # Cache index
        self.indices[content_type] = index
        
        logger.info(f"Created FAISS index with {index.ntotal} vectors: {index_path}")
        return str(index_path)
    
    def calculate_embedding_statistics(self, 
                                     embeddings: np.ndarray, 
                                     metadata: List[EmbeddingMetadata]) -> Dict[str, Any]:
        """
        Calculate comprehensive statistics about the embeddings.
        """
        # Basic statistics
        stats = {
            'mean_embedding_norm': float(np.mean(np.linalg.norm(embeddings, axis=1))),
            'std_embedding_norm': float(np.std(np.linalg.norm(embeddings, axis=1))),
            'embedding_shape': embeddings.shape,
            'content_type_distribution': {}
        }
        
        # Calculate pairwise similarities sample
        if len(embeddings) > 1:
            sample_size = min(100, len(embeddings))
            sample_indices = np.random.choice(len(embeddings), sample_size, replace=False)
            sample_embeddings = embeddings[sample_indices]
            
            similarities = cosine_similarity(sample_embeddings)
            
            # Remove diagonal (self-similarities)
            similarities_no_diag = similarities[~np.eye(similarities.shape[0], dtype=bool)]
            
            stats['similarity_statistics'] = {
                'mean_similarity': float(np.mean(similarities_no_diag)),
                'std_similarity': float(np.std(similarities_no_diag)),
                'min_similarity': float(np.min(similarities_no_diag)),
                'max_similarity': float(np.max(similarities_no_diag))
            }
        
        # Model information
        stats['model_info'] = {
            'model_name': self.model_name,
            'embedding_dimension': self.embedding_dim,
            'normalization': 'L2'
        }
        
        return stats
    
    def analyze_cluster_distribution(self, 
                                   cluster_labels: np.ndarray, 
                                   chunks: List[DocumentChunk]) -> Dict[str, Any]:
        """
        Analyze the distribution of chunks across clusters.
        """
        unique_labels, counts = np.unique(cluster_labels, return_counts=True)
        
        distribution = {}
        for label, count in zip(unique_labels, counts):
            # Get sample chunk titles from this cluster
            cluster_chunks = [chunks[i] for i in range(len(chunks)) if cluster_labels[i] == label]
            sample_titles = [chunk.context.get('heading', 'No title')[:50] 
                           for chunk in cluster_chunks[:3]]
            
            distribution[f"cluster_{label}"] = {
                'chunk_count': int(count),
                'percentage': float(count / len(cluster_labels) * 100),
                'sample_titles': sample_titles
            }
        
        return distribution
    
    def semantic_search(self, 
                       query: str, 
                       content_type: str = "mixed",
                       top_k: int = 10,
                       similarity_threshold: float = 0.5) -> List[Dict[str, Any]]:
        """
        Perform semantic search using the generated embeddings.
        """
        if content_type not in self.indices:
            # Try to load existing index
            index_path = self.output_path / "indices" / f"{content_type}_index.faiss"
            if index_path.exists():
                self.indices[content_type] = faiss.read_index(str(index_path))
            else:
                logger.error(f"No index found for content type: {content_type}")
                return []
        
        # Generate query embedding
        query_embedding = self.embedding_model.encode([query], normalize_embeddings=True)
        query_embedding = query_embedding.astype(np.float32)
        
        # Search
        scores, indices = self.indices[content_type].search(query_embedding, top_k)
        
        # Load metadata
        metadata_file = self.output_path / "metadata" / f"{content_type}_metadata.json"
        if metadata_file.exists():
            with open(metadata_file, 'r', encoding='utf-8') as f:
                metadata_list = json.load(f)
        else:
            metadata_list = []
        
        # Prepare results
        results = []
        for score, idx in zip(scores[0], indices[0]):
            if score >= similarity_threshold and idx < len(metadata_list):
                result = {
                    'chunk_id': metadata_list[idx]['chunk_id'],
                    'similarity_score': float(score),
                    'cluster': metadata_list[idx].get('similarity_cluster'),
                    'topic_keywords': metadata_list[idx].get('topic_keywords', []),
                    'metadata': metadata_list[idx]
                }
                results.append(result)
        
        return results
    
    def generate_embedding_id(self, chunk_id: str) -> str:
        """Generate unique embedding ID."""
        content = f"{chunk_id}_{self.model_name}_{datetime.now().isoformat()}"
        return hashlib.md5(content.encode()).hexdigest()[:12]
    
    def create_unified_index(self, content_types: List[str]) -> str:
        """
        Create a unified index combining multiple content types.
        """
        all_embeddings = []
        all_metadata = []
        
        for content_type in content_types:
            embeddings_file = self.output_path / "vectors" / f"{content_type}_embeddings.npy"
            metadata_file = self.output_path / "metadata" / f"{content_type}_metadata.json"
            
            if embeddings_file.exists() and metadata_file.exists():
                embeddings = np.load(embeddings_file)
                with open(metadata_file, 'r', encoding='utf-8') as f:
                    metadata = json.load(f)
                
                all_embeddings.append(embeddings)
                all_metadata.extend(metadata)
        
        if not all_embeddings:
            logger.error("No embeddings found to create unified index")
            return ""
        
        # Combine all embeddings
        unified_embeddings = np.vstack(all_embeddings)
        
        # Create unified index
        unified_index_path = self.create_faiss_index(unified_embeddings, "unified")
        
        # Save unified metadata
        unified_metadata_file = self.output_path / "metadata" / "unified_metadata.json"
        with open(unified_metadata_file, 'w', encoding='utf-8') as f:
            json.dump(all_metadata, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Created unified index with {len(unified_embeddings)} embeddings")
        return unified_index_path
    
    def export_for_rag(self, content_type: str = "unified") -> str:
        """
        Export embeddings in RAG-compatible format.
        """
        embeddings_file = self.output_path / "vectors" / f"{content_type}_embeddings.npy"
        metadata_file = self.output_path / "metadata" / f"{content_type}_metadata.json"
        
        if not embeddings_file.exists() or not metadata_file.exists():
            logger.error(f"Required files not found for content type: {content_type}")
            return ""
        
        # Load data
        embeddings = np.load(embeddings_file)
        with open(metadata_file, 'r', encoding='utf-8') as f:
            metadata = json.load(f)
        
        # Create RAG export format
        rag_export = {
            'format_version': '1.0',
            'model_name': self.model_name,
            'embedding_dimension': self.embedding_dim,
            'total_chunks': len(embeddings),
            'created_timestamp': datetime.now().isoformat(),
            'embeddings': embeddings.tolist(),
            'metadata': metadata,
            'index_info': {
                'similarity_metric': 'cosine',
                'normalization': 'L2',
                'search_backend': 'faiss'
            }
        }
        
        # Save RAG export
        rag_file = self.output_path / f"{content_type}_rag_export.json"
        with open(rag_file, 'w', encoding='utf-8') as f:
            json.dump(rag_export, f, indent=2, ensure_ascii=False)
        
        logger.info(f"RAG export created: {rag_file}")
        return str(rag_file)


def process_developer_course_embeddings():
    """Process embeddings for the Developer Course materials."""
    
    # Load processed chunks
    chunks_dir = Path("./creatio-academy-db/developer_course/chunks")
    if not chunks_dir.exists():
        logger.error("Developer course chunks not found. Run developer_course_processor.py first.")
        return
    
    # Initialize embedding generator
    generator = AdvancedEmbeddingGenerator(
        model_name="all-MiniLM-L6-v2",
        output_path="./creatio-academy-db/developer_course/embeddings"
    )
    
    # Load all chunks
    all_chunks = []
    for chunk_file in chunks_dir.glob("*_chunks.json"):
        with open(chunk_file, 'r', encoding='utf-8') as f:
            chunks_data = json.load(f)
            
        for chunk_data in chunks_data:
            # Reconstruct DocumentChunk objects
            chunk = DocumentChunk(
                chunk_id=chunk_data['chunk_id'],
                document_id=chunk_data['document_id'],
                content=chunk_data['content'],
                chunk_type=chunk_data['chunk_type'],
                chunk_index=chunk_data['chunk_index'],
                metadata=chunk_data['metadata'],
                word_count=chunk_data['word_count'],
                token_count=chunk_data['token_count'],
                context=chunk_data['context']
            )
            all_chunks.append(chunk)
    
    logger.info(f"Loaded {len(all_chunks)} chunks for embedding generation")
    
    # Generate embeddings
    result = generator.generate_embeddings_for_chunks(all_chunks, "developer_course")
    
    # Create unified index
    unified_index = generator.create_unified_index(["developer_course"])
    
    # Export for RAG
    rag_export = generator.export_for_rag("developer_course")
    
    print("\nEmbedding Generation Summary:")
    print(f"Total embeddings generated: {result['total_embeddings']}")
    print(f"Embedding dimension: {result['embedding_dimension']}")
    print(f"Number of semantic clusters: {result['clusters']['total_clusters']}")
    print(f"FAISS index created: {result['index_path']}")
    print(f"RAG export: {rag_export}")
    
    return result


if __name__ == "__main__":
    process_developer_course_embeddings()
