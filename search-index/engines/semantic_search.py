import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
import pickle
import os
import json
from typing import List, Dict, Tuple, Optional
from pathlib import Path

class SemanticSearchEngine:
    def __init__(self, model_name='all-MiniLM-L6-v2', index_path='embeddings'):
        """
        Initialize semantic search engine with sentence transformers.
        
        Args:
            model_name: The sentence transformer model to use
            index_path: Path to store FAISS index and embeddings
        """
        self.model = SentenceTransformer(model_name)
        self.index_path = Path(index_path)
        self.index_path.mkdir(exist_ok=True)
        
        self.index = None
        self.documents = []
        self.embeddings = None
        
        # Load existing index if available
        self.load_index()
    
    def embed_text(self, text: str) -> np.ndarray:
        """Create embedding for a single text."""
        return self.model.encode([text])[0]
    
    def embed_batch(self, texts: List[str]) -> np.ndarray:
        """Create embeddings for a batch of texts."""
        return self.model.encode(texts)
    
    def create_document_embeddings(self, documents: List[Dict]) -> None:
        """
        Create embeddings for a list of documents.
        
        Args:
            documents: List of dicts with keys 'id', 'content', 'metadata'
        """
        print(f"Creating embeddings for {len(documents)} documents...")
        
        # Extract text content
        texts = [doc['content'] for doc in documents]
        
        # Create embeddings
        embeddings = self.embed_batch(texts)
        
        # Create FAISS index
        dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatIP(dimension)  # Inner product (cosine similarity)
        
        # Normalize embeddings for cosine similarity
        faiss.normalize_L2(embeddings)
        
        # Add to index
        self.index.add(embeddings.astype('float32'))
        
        # Store documents and embeddings
        self.documents = documents
        self.embeddings = embeddings
        
        # Save index
        self.save_index()
        print("Embeddings created and saved successfully!")
    
    def add_document(self, document: Dict) -> None:
        """Add a single document to the index."""
        # Create embedding
        embedding = self.embed_text(document['content'])
        embedding = embedding.reshape(1, -1)
        
        # Normalize for cosine similarity
        faiss.normalize_L2(embedding)
        
        if self.index is None:
            # Create new index
            dimension = embedding.shape[1]
            self.index = faiss.IndexFlatIP(dimension)
            self.embeddings = embedding
        else:
            # Add to existing index
            self.embeddings = np.vstack([self.embeddings, embedding])
        
        self.index.add(embedding.astype('float32'))
        self.documents.append(document)
        
        # Save updated index
        self.save_index()
    
    def search(self, query: str, top_k: int = 10, min_score: float = 0.5) -> List[Dict]:
        """
        Perform semantic search.
        
        Args:
            query: Search query text
            top_k: Number of results to return
            min_score: Minimum similarity score (0-1)
        
        Returns:
            List of search results with scores
        """
        if self.index is None or len(self.documents) == 0:
            return []
        
        # Create query embedding
        query_embedding = self.embed_text(query).reshape(1, -1)
        faiss.normalize_L2(query_embedding)
        
        # Search
        scores, indices = self.index.search(query_embedding.astype('float32'), top_k)
        
        results = []
        for score, idx in zip(scores[0], indices[0]):
            if score >= min_score and idx < len(self.documents):
                result = self.documents[idx].copy()
                result['semantic_score'] = float(score)
                results.append(result)
        
        return results
    
    def hybrid_search(self, query: str, traditional_results: List[Dict], 
                     alpha: float = 0.7, top_k: int = 10) -> List[Dict]:
        """
        Combine semantic search with traditional search results.
        
        Args:
            query: Search query
            traditional_results: Results from traditional search
            alpha: Weight for semantic scores (1-alpha for traditional)
            top_k: Number of results to return
        
        Returns:
            Combined and ranked results
        """
        semantic_results = self.search(query, top_k * 2)
        
        # Create score maps
        semantic_scores = {r['id']: r['semantic_score'] for r in semantic_results}
        
        # Normalize traditional scores (assuming relevance_score field)
        if traditional_results:
            max_trad_score = max(r.get('relevance_score', 0) for r in traditional_results)
            if max_trad_score > 0:
                for r in traditional_results:
                    r['normalized_traditional_score'] = r.get('relevance_score', 0) / max_trad_score
        
        # Combine results
        combined_results = {}
        
        # Add semantic results
        for result in semantic_results:
            doc_id = result['id']
            combined_results[doc_id] = {
                **result,
                'combined_score': alpha * result['semantic_score']
            }
        
        # Add/update with traditional results
        for result in traditional_results:
            doc_id = result.get('id', result.get('path', str(hash(result.get('content', '')))))
            
            if doc_id in combined_results:
                # Update existing
                trad_score = result.get('normalized_traditional_score', 0)
                combined_results[doc_id]['combined_score'] += (1 - alpha) * trad_score
                combined_results[doc_id].update({k: v for k, v in result.items() 
                                               if k not in combined_results[doc_id]})
            else:
                # Add new
                semantic_score = semantic_scores.get(doc_id, 0)
                trad_score = result.get('normalized_traditional_score', 0)
                combined_results[doc_id] = {
                    **result,
                    'id': doc_id,
                    'semantic_score': semantic_score,
                    'combined_score': alpha * semantic_score + (1 - alpha) * trad_score
                }
        
        # Sort by combined score and return top_k
        sorted_results = sorted(combined_results.values(), 
                              key=lambda x: x['combined_score'], 
                              reverse=True)
        
        return sorted_results[:top_k]
    
    def find_similar_documents(self, document_id: str, top_k: int = 5) -> List[Dict]:
        """Find documents similar to a given document."""
        # Find the document
        doc_idx = None
        for i, doc in enumerate(self.documents):
            if doc['id'] == document_id:
                doc_idx = i
                break
        
        if doc_idx is None:
            return []
        
        # Use the document's embedding as query
        if self.embeddings is not None and doc_idx < len(self.embeddings):
            query_embedding = self.embeddings[doc_idx].reshape(1, -1)
            scores, indices = self.index.search(query_embedding.astype('float32'), top_k + 1)
            
            results = []
            for score, idx in zip(scores[0], indices[0]):
                if idx != doc_idx and idx < len(self.documents):  # Exclude self
                    result = self.documents[idx].copy()
                    result['similarity_score'] = float(score)
                    results.append(result)
            
            return results[:top_k]
        
        return []
    
    def save_index(self) -> None:
        """Save FAISS index and associated data."""
        if self.index is not None:
            # Save FAISS index
            faiss.write_index(self.index, str(self.index_path / 'faiss.index'))
            
            # Save documents
            with open(self.index_path / 'documents.json', 'w') as f:
                json.dump(self.documents, f)
            
            # Save embeddings
            if self.embeddings is not None:
                np.save(self.index_path / 'embeddings.npy', self.embeddings)
    
    def load_index(self) -> bool:
        """Load existing FAISS index and associated data."""
        try:
            index_file = self.index_path / 'faiss.index'
            documents_file = self.index_path / 'documents.json'
            embeddings_file = self.index_path / 'embeddings.npy'
            
            if index_file.exists() and documents_file.exists():
                # Load FAISS index
                self.index = faiss.read_index(str(index_file))
                
                # Load documents
                with open(documents_file, 'r') as f:
                    self.documents = json.load(f)
                
                # Load embeddings if available
                if embeddings_file.exists():
                    self.embeddings = np.load(embeddings_file)
                
                print(f"Loaded existing index with {len(self.documents)} documents")
                return True
        except Exception as e:
            print(f"Could not load existing index: {e}")
        
        return False
    
    def get_stats(self) -> Dict:
        """Get statistics about the semantic search index."""
        return {
            'total_documents': len(self.documents),
            'embedding_dimension': self.embeddings.shape[1] if self.embeddings is not None else 0,
            'model_name': self.model._modules['0'].get_sentence_embedding_dimension() if hasattr(self.model, '_modules') else 'unknown',
            'index_exists': self.index is not None
        }
