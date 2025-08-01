#!/usr/bin/env python3
"""
Advanced content summarization system for AI-optimized knowledge base.
Provides multiple summarization strategies optimized for different content types.
"""

import json
import re
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
import logging
import hashlib
from collections import Counter

from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
import torch
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.tag import pos_tag
import networkx as nx

from document_chunker import DocumentChunk

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Download NLTK data if not present
try:
    import nltk
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
    nltk.download('averaged_perceptron_tagger', quiet=True)
except:
    logger.warning("Could not download NLTK data")


@dataclass
class ContentSummary:
    """Represents a generated summary with metadata."""
    summary_id: str
    content_id: str
    summary_type: str  # 'extractive', 'abstractive', 'hybrid', 'multi_level'
    summary_text: str
    key_points: List[str]
    keywords: List[str]
    topics: List[str]
    summary_length: int
    original_length: int
    compression_ratio: float
    confidence_score: float
    created_timestamp: str
    metadata: Dict[str, Any]


class AdvancedContentSummarizer:
    """
    Advanced content summarization system with multiple strategies.
    """
    
    def __init__(self, 
                 output_path: str = "./summaries",
                 model_name: str = "facebook/bart-large-cnn"):
        """
        Initialize the content summarizer.
        
        Args:
            output_path: Path to store summaries
            model_name: Model for abstractive summarization
        """
        self.output_path = Path(output_path)
        self.model_name = model_name
        
        # Create output directories
        self.output_path.mkdir(parents=True, exist_ok=True)
        (self.output_path / "extractive").mkdir(exist_ok=True)
        (self.output_path / "abstractive").mkdir(exist_ok=True)
        (self.output_path / "hierarchical").mkdir(exist_ok=True)
        (self.output_path / "key_points").mkdir(exist_ok=True)
        (self.output_path / "collection_overview").mkdir(exist_ok=True)
        (self.output_path / "topic_clusters").mkdir(exist_ok=True)
        (self.output_path / "metadata").mkdir(exist_ok=True)
        
        # Initialize models
        self.initialize_models()
        
        # Initialize vectorizer for extractive summarization
        self.tfidf_vectorizer = TfidfVectorizer(
            max_features=1000,
            stop_words='english',
            ngram_range=(1, 2)
        )
        
        logger.info(f"Initialized content summarizer with model: {model_name}")
    
    def initialize_models(self):
        """Initialize summarization models."""
        try:
            # Initialize abstractive summarization pipeline
            # Force CPU usage to avoid CUDA errors
            self.abstractive_summarizer = pipeline(
                "summarization",
                model=self.model_name,
                tokenizer=self.model_name,
                device=-1  # Force CPU usage
            )
            logger.info(f"Loaded abstractive model: {self.model_name}")
        except Exception as e:
            logger.warning(f"Could not load abstractive model: {e}")
            self.abstractive_summarizer = None
        
        # Initialize tokenizer for text processing
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        except Exception as e:
            logger.warning(f"Could not load tokenizer: {e}")
            self.tokenizer = None
    
    def generate_comprehensive_summaries(self, 
                                       chunks: List[DocumentChunk],
                                       content_type: str = "mixed") -> Dict[str, Any]:
        """
        Generate comprehensive summaries using multiple strategies.
        
        Args:
            chunks: List of DocumentChunk objects
            content_type: Type of content for specialized processing
            
        Returns:
            Dictionary with all generated summaries and metadata
        """
        logger.info(f"Generating comprehensive summaries for {len(chunks)} chunks")
        
        if not chunks:
            return {"summaries": [], "metadata": {}}
        
        # Group chunks by document/session
        grouped_chunks = self.group_chunks_by_document(chunks)
        
        all_summaries = []
        processing_stats = {
            'total_chunks': len(chunks),
            'total_documents': len(grouped_chunks),
            'summary_types_generated': [],
            'processing_time': datetime.now().isoformat()
        }
        
        for doc_id, doc_chunks in grouped_chunks.items():
            logger.info(f"Processing document: {doc_id} with {len(doc_chunks)} chunks")
            
            # Generate document-level summaries using different strategies
            doc_summaries = self.generate_document_summaries(doc_chunks, doc_id, content_type)
            all_summaries.extend(doc_summaries)
        
        # Generate collection-level summaries
        collection_summaries = self.generate_collection_summaries(chunks, content_type)
        all_summaries.extend(collection_summaries)
        
        # Save all summaries
        summary_index = self.save_summaries(all_summaries, content_type)
        
        processing_stats['total_summaries'] = len(all_summaries)
        processing_stats['summary_types_generated'] = list(set(s.summary_type for s in all_summaries))
        
        result = {
            'summaries': [asdict(s) for s in all_summaries],
            'summary_index': summary_index,
            'processing_stats': processing_stats
        }
        
        logger.info(f"Generated {len(all_summaries)} summaries across {len(processing_stats['summary_types_generated'])} types")
        return result
    
    def group_chunks_by_document(self, chunks: List[DocumentChunk]) -> Dict[str, List[DocumentChunk]]:
        """Group chunks by their source document."""
        grouped = {}
        for chunk in chunks:
            doc_id = chunk.document_id
            if doc_id not in grouped:
                grouped[doc_id] = []
            grouped[doc_id].append(chunk)
        
        # Sort chunks within each document by index
        for doc_id in grouped:
            grouped[doc_id].sort(key=lambda x: x.chunk_index)
        
        return grouped
    
    def generate_document_summaries(self, 
                                   chunks: List[DocumentChunk], 
                                   doc_id: str,
                                   content_type: str) -> List[ContentSummary]:
        """Generate multiple types of summaries for a single document."""
        summaries = []
        
        # Combine all chunk content
        full_text = "\n\n".join(chunk.content for chunk in chunks)
        
        # 1. Extractive summary
        extractive_summary = self.generate_extractive_summary(full_text, chunks, doc_id)
        if extractive_summary:
            summaries.append(extractive_summary)
        
        # 2. Abstractive summary (if model available)
        if self.abstractive_summarizer:
            abstractive_summary = self.generate_abstractive_summary(full_text, chunks, doc_id)
            if abstractive_summary:
                summaries.append(abstractive_summary)
        
        # 3. Hierarchical summary
        hierarchical_summary = self.generate_hierarchical_summary(chunks, doc_id)
        if hierarchical_summary:
            summaries.append(hierarchical_summary)
        
        # 4. Key points summary
        key_points_summary = self.generate_key_points_summary(chunks, doc_id, content_type)
        if key_points_summary:
            summaries.append(key_points_summary)
        
        return summaries
    
    def generate_extractive_summary(self, 
                                   text: str, 
                                   chunks: List[DocumentChunk], 
                                   doc_id: str) -> Optional[ContentSummary]:
        """Generate extractive summary using sentence ranking."""
        try:
            # Split into sentences
            sentences = sent_tokenize(text)
            if len(sentences) < 3:
                return None
            
            # Calculate sentence scores using TF-IDF and position
            sentence_scores = self.calculate_sentence_scores(sentences, text)
            
            # Select top sentences (aim for ~30% of original)
            target_sentence_count = max(2, min(10, len(sentences) // 3))
            top_sentences = sorted(
                sentence_scores.items(), 
                key=lambda x: x[1], 
                reverse=True
            )[:target_sentence_count]
            
            # Maintain original order
            selected_sentences = []
            for sentence, _ in top_sentences:
                sentence_idx = sentences.index(sentence)
                selected_sentences.append((sentence_idx, sentence))
            
            selected_sentences.sort(key=lambda x: x[0])
            summary_text = " ".join([sent for _, sent in selected_sentences])
            
            # Extract additional metadata
            keywords = self.extract_keywords(text)
            topics = self.extract_topics(chunks)
            
            return ContentSummary(
                summary_id=self.generate_summary_id(doc_id, "extractive"),
                content_id=doc_id,
                summary_type="extractive",
                summary_text=summary_text,
                key_points=self.extract_key_points_from_text(summary_text),
                keywords=keywords,
                topics=topics,
                summary_length=len(summary_text.split()),
                original_length=len(text.split()),
                compression_ratio=len(summary_text.split()) / len(text.split()),
                confidence_score=self.calculate_extractive_confidence(top_sentences),
                created_timestamp=datetime.now().isoformat(),
                metadata={
                    'selected_sentence_count': len(selected_sentences),
                    'total_sentence_count': len(sentences),
                    'method': 'tfidf_position_ranking'
                }
            )
            
        except Exception as e:
            logger.error(f"Error in extractive summarization: {e}")
            return None
    
    def calculate_sentence_scores(self, sentences: List[str], full_text: str) -> Dict[str, float]:
        """Calculate scores for sentences using multiple factors."""
        scores = {}
        
        # TF-IDF scores
        tfidf_matrix = self.tfidf_vectorizer.fit_transform(sentences)
        tfidf_scores = tfidf_matrix.sum(axis=1).A1
        
        # Position scores (earlier sentences get higher scores)
        position_scores = [1.0 / (i + 1) for i in range(len(sentences))]
        
        # Length scores (prefer medium-length sentences)
        length_scores = []
        for sentence in sentences:
            words = len(sentence.split())
            if 10 <= words <= 40:
                length_scores.append(1.0)
            elif words < 10:
                length_scores.append(0.5)
            else:
                length_scores.append(0.7)
        
        # Combine scores
        for i, sentence in enumerate(sentences):
            combined_score = (
                0.5 * tfidf_scores[i] +
                0.3 * position_scores[i] +
                0.2 * length_scores[i]
            )
            scores[sentence] = combined_score
        
        return scores
    
    def generate_abstractive_summary(self, 
                                   text: str, 
                                   chunks: List[DocumentChunk], 
                                   doc_id: str) -> Optional[ContentSummary]:
        """Generate abstractive summary using transformer model."""
        if not self.abstractive_summarizer:
            return None
        
        try:
            # Clean and prepare text
            text = text.strip()
            if len(text) < 50:  # Skip very short texts
                return None
            
            # Truncate text if too long for model
            max_input_length = 800  # Conservative limit
            if self.tokenizer:
                tokens = self.tokenizer.encode(text, truncation=True, max_length=max_input_length)
                text = self.tokenizer.decode(tokens, skip_special_tokens=True)
            else:
                # Fallback: simple word-based truncation
                words = text.split()
                if len(words) > max_input_length:
                    text = " ".join(words[:max_input_length])
            
            # Generate summary with error handling
            summary_result = self.abstractive_summarizer(
                text,
                max_length=150,
                min_length=30,
                do_sample=False,
                truncation=True
            )
            
            if not summary_result or len(summary_result) == 0:
                return None
                
            summary_text = summary_result[0]['summary_text'].strip()
            
            # Extract additional metadata
            keywords = self.extract_keywords(text)
            topics = self.extract_topics(chunks)
            
            return ContentSummary(
                summary_id=self.generate_summary_id(doc_id, "abstractive"),
                content_id=doc_id,
                summary_type="abstractive",
                summary_text=summary_text,
                key_points=self.extract_key_points_from_text(summary_text),
                keywords=keywords,
                topics=topics,
                summary_length=len(summary_text.split()),
                original_length=len(text.split()),
                compression_ratio=len(summary_text.split()) / len(text.split()),
                confidence_score=0.8,  # Model-based confidence
                created_timestamp=datetime.now().isoformat(),
                metadata={
                    'model_name': self.model_name,
                    'method': 'transformer_abstractive'
                }
            )
            
        except Exception as e:
            logger.error(f"Error in abstractive summarization: {e}")
            return None
    
    def generate_hierarchical_summary(self, 
                                    chunks: List[DocumentChunk], 
                                    doc_id: str) -> Optional[ContentSummary]:
        """Generate hierarchical summary showing document structure."""
        try:
            # Organize chunks by headings and types
            structure = self.analyze_document_structure(chunks)
            
            # Create hierarchical summary
            summary_parts = []
            
            if structure['title']:
                summary_parts.append(f"Document: {structure['title']}")
            
            if structure['sections']:
                summary_parts.append("\nMain Sections:")
                for section in structure['sections']:
                    summary_parts.append(f"• {section['heading']}")
                    if section['key_points']:
                        for point in section['key_points'][:2]:  # Top 2 points per section
                            summary_parts.append(f"  - {point}")
            
            if structure['code_sections']:
                summary_parts.append(f"\nCode Examples: {len(structure['code_sections'])} sections")
                for lang in structure['languages']:
                    summary_parts.append(f"• {lang}")
            
            if structure['key_concepts']:
                summary_parts.append(f"\nKey Concepts: {', '.join(structure['key_concepts'][:5])}")
            
            summary_text = "\n".join(summary_parts)
            
            return ContentSummary(
                summary_id=self.generate_summary_id(doc_id, "hierarchical"),
                content_id=doc_id,
                summary_type="hierarchical",
                summary_text=summary_text,
                key_points=structure['key_concepts'],
                keywords=structure['keywords'],
                topics=structure['topics'],
                summary_length=len(summary_text.split()),
                original_length=sum(chunk.word_count for chunk in chunks),
                compression_ratio=len(summary_text.split()) / sum(chunk.word_count for chunk in chunks),
                confidence_score=0.9,  # High confidence for structural analysis
                created_timestamp=datetime.now().isoformat(),
                metadata={
                    'structure': structure,
                    'method': 'hierarchical_structural'
                }
            )
            
        except Exception as e:
            logger.error(f"Error in hierarchical summarization: {e}")
            return None
    
    def generate_key_points_summary(self, 
                                   chunks: List[DocumentChunk], 
                                   doc_id: str,
                                   content_type: str) -> Optional[ContentSummary]:
        """Generate summary focused on key points and actionable items."""
        try:
            all_text = "\n".join(chunk.content for chunk in chunks)
            
            # Extract different types of key points
            key_points = []
            
            # 1. Instructions and procedures
            instructions = self.extract_instructions(all_text)
            key_points.extend([f"INSTRUCTION: {inst}" for inst in instructions[:3]])
            
            # 2. Important concepts
            concepts = self.extract_concepts(all_text, content_type)
            key_points.extend([f"CONCEPT: {concept}" for concept in concepts[:3]])
            
            # 3. Code-related points
            if any(chunk.chunk_type == 'code' for chunk in chunks):
                code_points = self.extract_code_insights(chunks)
                key_points.extend([f"CODE: {point}" for point in code_points[:2]])
            
            # 4. Warnings and important notes
            warnings = self.extract_warnings(all_text)
            key_points.extend([f"NOTE: {warning}" for warning in warnings[:2]])
            
            if not key_points:
                return None
            
            summary_text = "\n".join(key_points)
            keywords = self.extract_keywords(all_text)
            topics = self.extract_topics(chunks)
            
            return ContentSummary(
                summary_id=self.generate_summary_id(doc_id, "key_points"),
                content_id=doc_id,
                summary_type="key_points",
                summary_text=summary_text,
                key_points=key_points,
                keywords=keywords,
                topics=topics,
                summary_length=len(summary_text.split()),
                original_length=sum(chunk.word_count for chunk in chunks),
                compression_ratio=len(summary_text.split()) / sum(chunk.word_count for chunk in chunks),
                confidence_score=0.85,
                created_timestamp=datetime.now().isoformat(),
                metadata={
                    'point_types': ['instructions', 'concepts', 'code', 'warnings'],
                    'method': 'key_points_extraction'
                }
            )
            
        except Exception as e:
            logger.error(f"Error in key points summarization: {e}")
            return None
    
    def generate_collection_summaries(self, 
                                    chunks: List[DocumentChunk], 
                                    content_type: str) -> List[ContentSummary]:
        """Generate summaries for the entire collection of content."""
        summaries = []
        
        try:
            # Overall collection summary
            collection_summary = self.generate_collection_overview(chunks, content_type)
            if collection_summary:
                summaries.append(collection_summary)
            
            # Topic-based clustering summary
            topic_summary = self.generate_topic_cluster_summary(chunks, content_type)
            if topic_summary:
                summaries.append(topic_summary)
            
        except Exception as e:
            logger.error(f"Error generating collection summaries: {e}")
        
        return summaries
    
    def generate_collection_overview(self, 
                                   chunks: List[DocumentChunk], 
                                   content_type: str) -> Optional[ContentSummary]:
        """Generate an overview summary of the entire collection."""
        try:
            # Analyze collection statistics
            stats = self.analyze_collection_statistics(chunks)
            
            # Create overview text
            overview_parts = [
                f"Collection Overview: {content_type.replace('_', ' ').title()}",
                f"Total content items: {stats['total_documents']}",
                f"Total content chunks: {len(chunks)}",
                f"Total words: {stats['total_words']:,}",
                ""
            ]
            
            if stats['content_types']:
                overview_parts.append("Content Types:")
                for ctype, count in stats['content_types'].most_common():
                    percentage = (count / len(chunks)) * 100
                    overview_parts.append(f"• {ctype}: {count} chunks ({percentage:.1f}%)")
                overview_parts.append("")
            
            if stats['main_topics']:
                overview_parts.append(f"Main Topics: {', '.join(stats['main_topics'][:5])}")
            
            if stats['programming_languages']:
                overview_parts.append(f"Programming Languages: {', '.join(stats['programming_languages'])}")
            
            overview_text = "\n".join(overview_parts)
            
            return ContentSummary(
                summary_id=self.generate_summary_id(content_type, "collection_overview"),
                content_id=f"{content_type}_collection",
                summary_type="collection_overview",
                summary_text=overview_text,
                key_points=stats['main_topics'],
                keywords=stats['top_keywords'],
                topics=stats['main_topics'],
                summary_length=len(overview_text.split()),
                original_length=stats['total_words'],
                compression_ratio=len(overview_text.split()) / stats['total_words'],
                confidence_score=0.95,
                created_timestamp=datetime.now().isoformat(),
                metadata={
                    'collection_stats': stats,
                    'method': 'collection_overview'
                }
            )
            
        except Exception as e:
            logger.error(f"Error in collection overview: {e}")
            return None
    
    def analyze_document_structure(self, chunks: List[DocumentChunk]) -> Dict[str, Any]:
        """Analyze the structure of a document from its chunks."""
        structure = {
            'title': '',
            'sections': [],
            'code_sections': [],
            'languages': set(),
            'key_concepts': [],
            'keywords': [],
            'topics': []
        }
        
        current_section = None
        
        for chunk in chunks:
            # Extract title from first chunk or heading
            if not structure['title'] and chunk.context.get('heading'):
                structure['title'] = chunk.context['heading']
            
            # Track sections
            if chunk.context.get('heading') and chunk.chunk_type != 'code':
                if current_section:
                    structure['sections'].append(current_section)
                
                current_section = {
                    'heading': chunk.context['heading'],
                    'key_points': self.extract_key_points_from_text(chunk.content)
                }
            
            # Track code sections
            if chunk.chunk_type == 'code':
                structure['code_sections'].append({
                    'language': chunk.context.get('languages', ['unknown'])[0],
                    'content_preview': chunk.content[:100]
                })
                if chunk.context.get('languages'):
                    structure['languages'].update(chunk.context['languages'])
            
            # Extract concepts and keywords
            concepts = self.extract_concepts(chunk.content, chunk.chunk_type)
            structure['key_concepts'].extend(concepts)
        
        # Add final section
        if current_section:
            structure['sections'].append(current_section)
        
        # Clean up and deduplicate
        structure['languages'] = list(structure['languages'])
        structure['key_concepts'] = list(set(structure['key_concepts']))[:10]
        structure['keywords'] = self.extract_keywords(" ".join(chunk.content for chunk in chunks))
        structure['topics'] = self.extract_topics(chunks)
        
        # Ensure all values are JSON serializable
        structure = self._make_json_serializable(structure)
        
        return structure
    
    def extract_instructions(self, text: str) -> List[str]:
        """Extract instructional content from text."""
        instructions = []
        
        # Patterns that indicate instructions
        instruction_patterns = [
            r'(?:first|second|third|next|then|finally|step \d+)[:\-\s]([^.!?]+[.!?])',
            r'(?:to \w+)[:\-\s]([^.!?]+[.!?])',
            r'(?:you (?:should|must|need to|can))[:\-\s]([^.!?]+[.!?])',
            r'(?:create|configure|set up|install|run)[:\-\s]([^.!?]+[.!?])'
        ]
        
        for pattern in instruction_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            instructions.extend([match.strip() for match in matches])
        
        return instructions[:5]  # Return top 5 instructions
    
    def extract_concepts(self, text: str, content_type: str) -> List[str]:
        """Extract key concepts based on content type."""
        concepts = []
        
        # Creatio-specific concepts
        creatio_concepts = [
            'schema', 'entity', 'business process', 'workflow', 'configuration',
            'customization', 'module', 'package', 'section', 'page', 'detail',
            'lookup', 'integration', 'web service', 'api'
        ]
        
        # Technical concepts
        technical_concepts = [
            'database', 'sql', 'javascript', 'c#', 'json', 'xml',
            'client', 'server', 'data', 'record', 'field', 'column'
        ]
        
        text_lower = text.lower()
        
        for concept in creatio_concepts + technical_concepts:
            if concept in text_lower:
                concepts.append(concept)
        
        return list(set(concepts))[:5]
    
    def extract_code_insights(self, chunks: List[DocumentChunk]) -> List[str]:
        """Extract insights from code chunks."""
        insights = []
        
        code_chunks = [chunk for chunk in chunks if chunk.chunk_type == 'code']
        
        for chunk in code_chunks:
            # Extract function definitions
            if 'function' in chunk.content.lower() or 'def ' in chunk.content:
                insights.append("Contains function definitions")
            
            # Extract API calls
            if any(term in chunk.content.lower() for term in ['api', 'request', 'response', 'http']):
                insights.append("Contains API interactions")
            
            # Extract database operations
            if any(term in chunk.content.upper() for term in ['SELECT', 'INSERT', 'UPDATE', 'DELETE']):
                insights.append("Contains database operations")
        
        return list(set(insights))
    
    def extract_warnings(self, text: str) -> List[str]:
        """Extract warnings and important notes."""
        warnings = []
        
        warning_patterns = [
            r'(?:warning|caution|important|note)[:\-\s]([^.!?]+[.!?])',
            r'(?:be careful|make sure|ensure that)[:\-\s]([^.!?]+[.!?])',
            r'(?:do not|don\'t|avoid)[:\-\s]([^.!?]+[.!?])'
        ]
        
        for pattern in warning_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            warnings.extend([match.strip() for match in matches])
        
        return warnings[:3]
    
    def extract_keywords(self, text: str, top_k: int = 10) -> List[str]:
        """Extract keywords using TF-IDF."""
        try:
            tfidf = TfidfVectorizer(
                max_features=top_k,
                stop_words='english',
                ngram_range=(1, 2)
            )
            tfidf_matrix = tfidf.fit_transform([text])
            feature_names = tfidf.get_feature_names_out()
            scores = tfidf_matrix.toarray()[0]
            
            keyword_scores = list(zip(feature_names, scores))
            keyword_scores.sort(key=lambda x: x[1], reverse=True)
            
            return [keyword for keyword, score in keyword_scores if score > 0]
        except:
            return []
    
    def extract_topics(self, chunks: List[DocumentChunk]) -> List[str]:
        """Extract topics from chunks."""
        topics = set()
        
        for chunk in chunks:
            # Add heading-based topics
            if chunk.context.get('heading'):
                heading_words = chunk.context['heading'].lower().split()
                topics.update([word for word in heading_words if len(word) > 3])
            
            # Add chunk type as topic
            if chunk.chunk_type != 'paragraph':
                topics.add(chunk.chunk_type)
        
        return list(topics)[:8]
    
    def extract_key_points_from_text(self, text: str) -> List[str]:
        """Extract key points from text using sentence ranking."""
        sentences = sent_tokenize(text)
        if len(sentences) <= 3:
            return sentences
        
        # Simple scoring based on sentence position and length
        scored_sentences = []
        for i, sentence in enumerate(sentences):
            score = 1.0 / (i + 1)  # Earlier sentences get higher scores
            if 10 <= len(sentence.split()) <= 25:  # Prefer medium-length sentences
                score *= 1.2
            scored_sentences.append((sentence, score))
        
        # Sort by score and take top 3-5
        scored_sentences.sort(key=lambda x: x[1], reverse=True)
        return [sent for sent, _ in scored_sentences[:min(5, len(sentences) // 2)]]
    
    def calculate_extractive_confidence(self, top_sentences: List[Tuple[str, float]]) -> float:
        """Calculate confidence score for extractive summary."""
        if not top_sentences:
            return 0.0
        
        scores = [score for _, score in top_sentences]
        avg_score = sum(scores) / len(scores)
        score_variance = sum((s - avg_score) ** 2 for s in scores) / len(scores)
        
        # Higher average score and lower variance = higher confidence
        confidence = min(1.0, avg_score * (1.0 - score_variance))
        return confidence
    
    def analyze_collection_statistics(self, chunks: List[DocumentChunk]) -> Dict[str, Any]:
        """Analyze statistics for the entire collection."""
        stats = {
            'total_documents': len(set(chunk.document_id for chunk in chunks)),
            'total_words': sum(chunk.word_count for chunk in chunks),
            'content_types': Counter(chunk.chunk_type for chunk in chunks),
            'main_topics': [],
            'top_keywords': [],
            'programming_languages': set()
        }
        
        # Collect all topics
        all_topics = []
        all_text = []
        
        for chunk in chunks:
            all_text.append(chunk.content)
            all_topics.extend(self.extract_topics([chunk]))
            
            if chunk.context.get('languages'):
                stats['programming_languages'].update(chunk.context['languages'])
        
        # Get most common topics
        topic_counter = Counter(all_topics)
        stats['main_topics'] = [topic for topic, _ in topic_counter.most_common(10)]
        
        # Extract keywords from all text
        combined_text = " ".join(all_text)
        stats['top_keywords'] = self.extract_keywords(combined_text, 15)
        
        stats['programming_languages'] = list(stats['programming_languages'])
        
        return stats
    
    def generate_topic_cluster_summary(self, 
                                     chunks: List[DocumentChunk], 
                                     content_type: str) -> Optional[ContentSummary]:
        """Generate summary based on topic clustering."""
        try:
            if len(chunks) < 5:
                return None
            
            # Prepare texts for clustering
            texts = [chunk.content for chunk in chunks]
            
            # Vectorize texts
            vectorizer = TfidfVectorizer(max_features=100, stop_words='english')
            tfidf_matrix = vectorizer.fit_transform(texts)
            
            # Perform clustering
            n_clusters = min(5, len(chunks) // 3)
            kmeans = KMeans(n_clusters=n_clusters, random_state=42)
            cluster_labels = kmeans.fit_predict(tfidf_matrix)
            
            # Analyze clusters
            cluster_summaries = []
            for i in range(n_clusters):
                cluster_chunks = [chunks[j] for j in range(len(chunks)) if cluster_labels[j] == i]
                if cluster_chunks:
                    cluster_topics = Counter()
                    for chunk in cluster_chunks:
                        cluster_topics.update(self.extract_topics([chunk]))
                    
                    top_topics = [topic for topic, _ in cluster_topics.most_common(3)]
                    cluster_summaries.append(f"Cluster {i+1}: {', '.join(top_topics)} ({len(cluster_chunks)} chunks)")
            
            summary_text = f"Content organized into {n_clusters} main topic clusters:\n" + "\n".join(cluster_summaries)
            
            return ContentSummary(
                summary_id=self.generate_summary_id(content_type, "topic_clusters"),
                content_id=f"{content_type}_clusters",
                summary_type="topic_clusters",
                summary_text=summary_text,
                key_points=cluster_summaries,
                keywords=list(vectorizer.get_feature_names_out()[:10]),
                topics=[],
                summary_length=len(summary_text.split()),
                original_length=sum(chunk.word_count for chunk in chunks),
                compression_ratio=len(summary_text.split()) / sum(chunk.word_count for chunk in chunks),
                confidence_score=0.8,
                created_timestamp=datetime.now().isoformat(),
                metadata={
                    'n_clusters': n_clusters,
                    'clustering_method': 'kmeans_tfidf',
                    'method': 'topic_clustering'
                }
            )
            
        except Exception as e:
            logger.error(f"Error in topic clustering: {e}")
            return None
    
    def save_summaries(self, summaries: List[ContentSummary], content_type: str) -> str:
        """Save summaries and create index."""
        # Save individual summaries by type
        for summary in summaries:
            summary_file = self.output_path / summary.summary_type / f"{summary.summary_id}.json"
            with open(summary_file, 'w', encoding='utf-8') as f:
                # Make sure the summary data is JSON serializable
                summary_dict = self._make_json_serializable(asdict(summary))
                json.dump(summary_dict, f, indent=2, ensure_ascii=False)
        
        # Create summary index
        index = {
            'content_type': content_type,
            'total_summaries': len(summaries),
            'created_timestamp': datetime.now().isoformat(),
            'summaries': []
        }
        
        for summary in summaries:
            index['summaries'].append({
                'summary_id': summary.summary_id,
                'content_id': summary.content_id,
                'summary_type': summary.summary_type,
                'summary_length': summary.summary_length,
                'compression_ratio': summary.compression_ratio,
                'confidence_score': summary.confidence_score,
                'file_path': f"{summary.summary_type}/{summary.summary_id}.json"
            })
        
        # Save index
        index_file = self.output_path / f"{content_type}_summary_index.json"
        with open(index_file, 'w', encoding='utf-8') as f:
            json.dump(index, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Saved {len(summaries)} summaries and index: {index_file}")
        return str(index_file)
    
    def generate_summary_id(self, content_id: str, summary_type: str) -> str:
        """Generate unique summary ID."""
        content_string = f"{summary_type}_{content_id}_{datetime.now().isoformat()}"
        return hashlib.md5(content_string.encode()).hexdigest()[:12]
    
    def _make_json_serializable(self, obj: Any) -> Any:
        """Convert object to JSON serializable format."""
        if isinstance(obj, dict):
            return {str(k): self._make_json_serializable(v) for k, v in obj.items()}
        elif isinstance(obj, (list, tuple, set)):
            return [self._make_json_serializable(item) for item in obj]
        elif isinstance(obj, (str, int, float, bool)) or obj is None:
            return obj
        else:
            return str(obj)


def process_developer_course_summaries():
    """Process summaries for the Developer Course materials."""
    
    # Load processed chunks
    chunks_dir = Path("./creatio-academy-db/developer_course/chunks")
    if not chunks_dir.exists():
        logger.error("Developer course chunks not found. Run developer_course_processor.py first.")
        return
    
    # Initialize summarizer
    summarizer = AdvancedContentSummarizer(
        output_path="./creatio-academy-db/developer_course/summaries"
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
    
    logger.info(f"Loaded {len(all_chunks)} chunks for summarization")
    
    # Generate summaries
    result = summarizer.generate_comprehensive_summaries(all_chunks, "developer_course")
    
    print("\nSummarization Summary:")
    print(f"Total summaries generated: {result['processing_stats']['total_summaries']}")
    print(f"Summary types: {', '.join(result['processing_stats']['summary_types_generated'])}")
    print(f"Documents processed: {result['processing_stats']['total_documents']}")
    print(f"Summary index: {result['summary_index']}")
    
    return result


if __name__ == "__main__":
    process_developer_course_summaries()
