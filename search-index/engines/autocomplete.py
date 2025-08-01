from typing import List, Dict, Set
import json
import redis
from collections import defaultdict, Counter
import re

class AutocompleteEngine:
    def __init__(self, redis_host='localhost', redis_port=6379, redis_db=0):
        """
        Initialize autocomplete engine with Redis backend.
        
        Args:
            redis_host: Redis server host
            redis_port: Redis server port
            redis_db: Redis database number
        """
        try:
            self.redis_client = redis.Redis(host=redis_host, port=redis_port, db=redis_db)
            self.use_redis = True
        except:
            self.redis_client = None
            self.use_redis = False
            print("Redis not available, using in-memory storage")
        
        # In-memory storage as fallback
        self.terms_index = defaultdict(set)  # prefix -> set of terms
        self.term_frequencies = Counter()  # term -> frequency
        self.phrase_index = defaultdict(set)  # prefix -> set of phrases
        
    def build_autocomplete_index(self, documents: List[Dict]) -> None:
        """
        Build autocomplete index from documents.
        
        Args:
            documents: List of documents with 'content', 'title', etc.
        """
        print(f"Building autocomplete index for {len(documents)} documents...")
        
        all_terms = set()
        all_phrases = set()
        
        for doc in documents:
            # Extract terms from content and title
            content = doc.get('content', '') + ' ' + doc.get('title', '')
            
            # Extract individual words
            words = self._extract_words(content)
            all_terms.update(words)
            
            # Update term frequencies
            for word in words:
                self.term_frequencies[word] += 1
            
            # Extract phrases (2-4 word combinations)
            phrases = self._extract_phrases(content)
            all_phrases.update(phrases)
        
        # Build prefix index for terms
        for term in all_terms:
            for i in range(1, len(term) + 1):
                prefix = term[:i].lower()
                self.terms_index[prefix].add(term)
                
                if self.use_redis:
                    self.redis_client.sadd(f"terms:{prefix}", term)
        
        # Build prefix index for phrases
        for phrase in all_phrases:
            phrase_lower = phrase.lower()
            for i in range(1, len(phrase_lower) + 1):
                prefix = phrase_lower[:i]
                self.phrase_index[prefix].add(phrase)
                
                if self.use_redis:
                    self.redis_client.sadd(f"phrases:{prefix}", phrase)
        
        # Store term frequencies in Redis
        if self.use_redis:
            for term, freq in self.term_frequencies.items():
                self.redis_client.zadd("term_frequencies", {term: freq})
        
        print(f"Autocomplete index built with {len(all_terms)} terms and {len(all_phrases)} phrases")
    
    def get_suggestions(self, prefix: str, max_suggestions: int = 10, include_phrases: bool = True) -> List[Dict]:
        """
        Get autocomplete suggestions for a prefix.
        
        Args:
            prefix: The prefix to search for
            max_suggestions: Maximum number of suggestions
            include_phrases: Whether to include phrase suggestions
        
        Returns:
            List of suggestion dictionaries
        """
        prefix = prefix.lower().strip()
        if not prefix:
            return []
        
        suggestions = []
        
        # Get term suggestions
        term_suggestions = self._get_term_suggestions(prefix, max_suggestions // 2)
        suggestions.extend(term_suggestions)
        
        # Get phrase suggestions if enabled
        if include_phrases:
            phrase_suggestions = self._get_phrase_suggestions(prefix, max_suggestions // 2)
            suggestions.extend(phrase_suggestions)
        
        # Sort by relevance (frequency * length penalty)
        suggestions.sort(key=lambda x: (-x['frequency'], len(x['text'])))
        
        return suggestions[:max_suggestions]
    
    def _get_term_suggestions(self, prefix: str, max_count: int) -> List[Dict]:
        """Get term-based suggestions."""
        suggestions = []
        
        if self.use_redis:
            # Redis-based lookup
            terms = self.redis_client.smembers(f"terms:{prefix}")
            for term in terms:
                term = term.decode('utf-8')
                freq = self.redis_client.zscore("term_frequencies", term) or 0
                suggestions.append({
                    'text': term,
                    'type': 'term',
                    'frequency': int(freq)
                })
        else:
            # In-memory lookup
            terms = self.terms_index.get(prefix, set())
            for term in terms:
                freq = self.term_frequencies[term]
                suggestions.append({
                    'text': term,
                    'type': 'term',
                    'frequency': freq
                })
        
        return suggestions[:max_count]
    
    def _get_phrase_suggestions(self, prefix: str, max_count: int) -> List[Dict]:
        """Get phrase-based suggestions."""
        suggestions = []
        
        if self.use_redis:
            # Redis-based lookup
            phrases = self.redis_client.smembers(f"phrases:{prefix}")
            for phrase in phrases:
                phrase = phrase.decode('utf-8')
                # Estimate frequency based on phrase length (longer = less frequent)
                freq = max(1, 10 - len(phrase.split()))
                suggestions.append({
                    'text': phrase,
                    'type': 'phrase',
                    'frequency': freq
                })
        else:
            # In-memory lookup
            phrases = self.phrase_index.get(prefix, set())
            for phrase in phrases:
                freq = max(1, 10 - len(phrase.split()))
                suggestions.append({
                    'text': phrase,
                    'type': 'phrase',
                    'frequency': freq
                })
        
        return suggestions[:max_count]
    
    def _extract_words(self, text: str) -> List[str]:
        """Extract words from text for autocomplete."""
        # Remove HTML tags and special characters
        text = re.sub(r'<[^>]+>', ' ', text)
        text = re.sub(r'[^\w\s]', ' ', text)
        
        # Extract words (minimum 3 characters)
        words = [word.lower() for word in text.split() 
                if len(word) >= 3 and word.lower() not in self._get_stopwords()]
        
        return list(set(words))  # Remove duplicates
    
    def _extract_phrases(self, text: str, max_phrase_length: int = 4) -> List[str]:
        """Extract phrases from text for autocomplete."""
        # Clean text
        text = re.sub(r'<[^>]+>', ' ', text)
        text = re.sub(r'[^\w\s]', ' ', text)
        
        words = [word for word in text.lower().split() 
                if len(word) >= 3 and word not in self._get_stopwords()]
        
        phrases = []
        
        # Generate n-grams (2 to max_phrase_length words)
        for n in range(2, min(max_phrase_length + 1, len(words) + 1)):
            for i in range(len(words) - n + 1):
                phrase = ' '.join(words[i:i + n])
                if len(phrase) >= 6:  # Minimum phrase length
                    phrases.append(phrase)
        
        return list(set(phrases))  # Remove duplicates
    
    def _get_stopwords(self) -> Set[str]:
        """Get common stopwords to exclude from autocomplete."""
        return {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 
            'of', 'with', 'by', 'from', 'up', 'about', 'into', 'through', 'during',
            'before', 'after', 'above', 'below', 'between', 'among', 'against',
            'is', 'was', 'are', 'were', 'be', 'been', 'being', 'have', 'has', 'had',
            'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might',
            'must', 'can', 'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she',
            'it', 'we', 'they', 'them', 'their', 'there', 'where', 'when', 'why',
            'how', 'what', 'which', 'who', 'whom', 'whose', 'if', 'than', 'so'
        }
    
    def record_search(self, query: str) -> None:
        """Record a search query to improve suggestions."""
        words = self._extract_words(query)
        phrases = self._extract_phrases(query)
        
        # Update frequencies
        for word in words:
            self.term_frequencies[word] += 1
            if self.use_redis:
                self.redis_client.zincrby("term_frequencies", 1, word)
        
        # Store successful search queries for suggestions
        if self.use_redis:
            self.redis_client.zincrby("search_queries", 1, query.lower())
    
    def get_popular_searches(self, limit: int = 10) -> List[str]:
        """Get most popular search queries."""
        if self.use_redis:
            queries = self.redis_client.zrevrange("search_queries", 0, limit - 1, withscores=True)
            return [query.decode('utf-8') for query, score in queries]
        else:
            # Fallback - return empty for now
            return []
    
    def clear_cache(self) -> None:
        """Clear autocomplete cache."""
        if self.use_redis:
            # Clear Redis keys
            for key in self.redis_client.scan_iter(match="terms:*"):
                self.redis_client.delete(key)
            for key in self.redis_client.scan_iter(match="phrases:*"):
                self.redis_client.delete(key)
            self.redis_client.delete("term_frequencies")
            self.redis_client.delete("search_queries")
        
        # Clear in-memory storage
        self.terms_index.clear()
        self.term_frequencies.clear()
        self.phrase_index.clear()
        
        print("Autocomplete cache cleared")
