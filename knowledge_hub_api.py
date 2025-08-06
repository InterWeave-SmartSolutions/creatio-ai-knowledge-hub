#!/usr/bin/env python3
"""
Creatio Knowledge Hub API
Provides AI-ready access to integrated content
Supports queries, search, and structured data retrieval
"""

import json
import sqlite3
import re
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional, Any
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CreatioKnowledgeHubAPI:
    def __init__(self, base_dir: str = "/home/andrewwork/creatio-ai-knowledge-hub"):
        self.base_dir = Path(base_dir)
        self.db_path = self.base_dir / "ai_knowledge_hub" / "integrated_knowledge_hub.db"
        self.search_index_path = self.base_dir / "ai_knowledge_hub" / "solutions_hub" / "search_data" / "ai_search_index.json"
        
        # Load search index for fast queries
        self.search_index = self._load_search_index()
        
    def _load_search_index(self) -> List[Dict]:
        """Load the AI search index into memory"""
        try:
            if self.search_index_path.exists():
                with open(self.search_index_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                logger.warning("Search index not found")
                return []
        except Exception as e:
            logger.error(f"Error loading search index: {str(e)}")
            return []
    
    def _get_db_connection(self):
        """Get database connection"""
        return sqlite3.connect(str(self.db_path))
    
    def search_content(self, query: str, category: Optional[str] = None, 
                      difficulty: Optional[str] = None, limit: int = 10) -> List[Dict]:
        """
        Search knowledge base content
        
        Args:
            query: Search query string
            category: Optional category filter
            difficulty: Optional difficulty filter
            limit: Maximum number of results
            
        Returns:
            List of matching content entries
        """
        query_lower = query.lower()
        results = []
        
        for entry in self.search_index:
            # Check category filter
            if category and entry.get('category') != category:
                continue
                
            # Check difficulty filter
            if difficulty and entry.get('difficulty') != difficulty:
                continue
            
            # Search in searchable text
            searchable_text = entry.get('searchable_text', '').lower()
            if query_lower in searchable_text:
                # Calculate relevance score
                score = self._calculate_relevance(query_lower, entry)
                entry_copy = entry.copy()
                entry_copy['relevance_score'] = score
                results.append(entry_copy)
        
        # Sort by relevance score
        results.sort(key=lambda x: x.get('relevance_score', 0), reverse=True)
        
        return results[:limit]
    
    def _calculate_relevance(self, query: str, entry: Dict) -> float:
        """Calculate relevance score for search results"""
        score = 0.0
        
        # Title match (highest weight)
        if query in entry.get('title', '').lower():
            score += 10.0
            
        # Description match
        if query in entry.get('description', '').lower():
            score += 5.0
            
        # Summary match
        if query in entry.get('summary', '').lower():
            score += 3.0
            
        # Tags match
        ai_tags = entry.get('ai_tags', [])
        for tag in ai_tags:
            if query in tag.lower():
                score += 2.0
                
        # Key concepts match
        key_concepts = entry.get('key_concepts', [])
        for concept in key_concepts:
            if query in concept.lower():
                score += 1.5
        
        return score
    
    def get_by_category(self, category: str, limit: int = 20) -> List[Dict]:
        """Get content by category"""
        return [entry for entry in self.search_index 
                if entry.get('category') == category][:limit]
    
    def get_by_difficulty(self, difficulty: str, limit: int = 20) -> List[Dict]:
        """Get content by difficulty level"""
        return [entry for entry in self.search_index 
                if entry.get('difficulty') == difficulty][:limit]
    
    def get_by_tags(self, tags: List[str], limit: int = 20) -> List[Dict]:
        """Get content by AI tags"""
        results = []
        tags_lower = [tag.lower() for tag in tags]
        
        for entry in self.search_index:
            entry_tags = [tag.lower() for tag in entry.get('ai_tags', [])]
            if any(tag in entry_tags for tag in tags_lower):
                results.append(entry)
                
        return results[:limit]
    
    def get_related_content(self, content_id: int, limit: int = 10) -> List[Dict]:
        """Get content related to a specific entry"""
        # Find the source entry
        source_entry = None
        for entry in self.search_index:
            if entry.get('id') == content_id:
                source_entry = entry
                break
                
        if not source_entry:
            return []
        
        # Find related content based on common tags and concepts
        source_tags = source_entry.get('ai_tags', [])
        source_concepts = source_entry.get('key_concepts', [])
        source_category = source_entry.get('category')
        
        related = []
        for entry in self.search_index:
            if entry.get('id') == content_id:
                continue  # Skip the source entry
                
            score = 0.0
            
            # Same category bonus
            if entry.get('category') == source_category:
                score += 2.0
                
            # Common tags
            entry_tags = entry.get('ai_tags', [])
            common_tags = set(source_tags) & set(entry_tags)
            score += len(common_tags) * 1.0
            
            # Common concepts
            entry_concepts = entry.get('key_concepts', [])
            common_concepts = set(source_concepts) & set(entry_concepts)
            score += len(common_concepts) * 1.5
            
            if score > 0:
                entry_copy = entry.copy()
                entry_copy['relation_score'] = score
                related.append(entry_copy)
        
        # Sort by relation score
        related.sort(key=lambda x: x.get('relation_score', 0), reverse=True)
        
        return related[:limit]
    
    def get_full_content(self, content_id: int) -> Optional[Dict]:
        """Get full content including complete text"""
        try:
            conn = self._get_db_connection()
            cursor = conn.execute('''
                SELECT kc.*, arc.summary, arc.key_concepts, arc.use_cases, 
                       arc.related_topics, arc.difficulty_level, arc.ai_tags,
                       arc.structured_data
                FROM knowledge_content kc
                JOIN ai_ready_content arc ON kc.id = arc.knowledge_id
                WHERE kc.id = ?
            ''', (content_id,))
            
            row = cursor.fetchone()
            conn.close()
            
            if not row:
                return None
            
            # Convert to dictionary
            columns = [desc[0] for desc in cursor.description]
            result = dict(zip(columns, row))
            
            # Parse JSON fields
            json_fields = ['key_concepts', 'use_cases', 'related_topics', 'ai_tags', 'structured_data']
            for field in json_fields:
                if result.get(field):
                    try:
                        result[field] = json.loads(result[field])
                    except:
                        result[field] = []
            
            return result
            
        except Exception as e:
            logger.error(f"Error getting full content: {str(e)}")
            return None
    
    def get_categories(self) -> List[Dict]:
        """Get all available categories with counts"""
        categories = {}
        for entry in self.search_index:
            category = entry.get('category', 'unknown')
            if category not in categories:
                categories[category] = 0
            categories[category] += 1
        
        return [{'category': k, 'count': v} for k, v in categories.items()]
    
    def get_difficulty_levels(self) -> List[Dict]:
        """Get all difficulty levels with counts"""
        difficulties = {}
        for entry in self.search_index:
            difficulty = entry.get('difficulty', 'unknown')
            if difficulty not in difficulties:
                difficulties[difficulty] = 0
            difficulties[difficulty] += 1
        
        return [{'difficulty': k, 'count': v} for k, v in difficulties.items()]
    
    def get_all_tags(self) -> List[Dict]:
        """Get all AI tags with usage counts"""
        tag_counts = {}
        for entry in self.search_index:
            tags = entry.get('ai_tags', [])
            for tag in tags:
                if tag not in tag_counts:
                    tag_counts[tag] = 0
                tag_counts[tag] += 1
        
        return [{'tag': k, 'count': v} for k, v in sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)]
    
    def suggest_content(self, user_profile: Dict) -> List[Dict]:
        """
        Suggest content based on user profile
        
        Args:
            user_profile: Dictionary with keys like 'interests', 'skill_level', 'role'
        """
        interests = user_profile.get('interests', [])
        skill_level = user_profile.get('skill_level', 'beginner')
        role = user_profile.get('role', 'general')
        
        suggestions = []
        
        # Role-based suggestions
        role_categories = {
            'developer': ['development', 'customization', 'reference'],
            'administrator': ['administration', 'getting-started'],
            'business_user': ['applications', 'solutions', 'getting-started'],
            'consultant': ['solutions', 'applications', 'troubleshooting']
        }
        
        preferred_categories = role_categories.get(role, ['getting-started'])
        
        for entry in self.search_index:
            score = 0.0
            
            # Category match
            if entry.get('category') in preferred_categories:
                score += 3.0
                
            # Difficulty match
            if entry.get('difficulty') == skill_level:
                score += 2.0
            elif skill_level == 'beginner' and entry.get('difficulty') == 'intermediate':
                score += 1.0
                
            # Interest match
            entry_tags = entry.get('ai_tags', [])
            for interest in interests:
                if interest.lower() in [tag.lower() for tag in entry_tags]:
                    score += 2.0
            
            if score > 0:
                entry_copy = entry.copy()
                entry_copy['suggestion_score'] = score
                suggestions.append(entry_copy)
        
        # Sort by suggestion score
        suggestions.sort(key=lambda x: x.get('suggestion_score', 0), reverse=True)
        
        return suggestions[:10]
    
    def get_learning_path(self, topic: str) -> List[Dict]:
        """Generate a learning path for a specific topic"""
        # Find content related to the topic
        related_content = self.search_content(topic, limit=20)
        
        if not related_content:
            return []
        
        # Organize by difficulty
        path = {
            'beginner': [],
            'intermediate': [],
            'advanced': []
        }
        
        for content in related_content:
            difficulty = content.get('difficulty', 'beginner')
            if difficulty in path:
                path[difficulty].append(content)
        
        # Create sequential learning path
        learning_path = []
        for level in ['beginner', 'intermediate', 'advanced']:
            if path[level]:
                learning_path.extend(sorted(path[level], 
                                          key=lambda x: x.get('relevance_score', 0), 
                                          reverse=True)[:5])
        
        return learning_path
    
    def export_content_summary(self) -> Dict:
        """Export a summary of all content for AI analysis"""
        summary = {
            'total_entries': len(self.search_index),
            'categories': self.get_categories(),
            'difficulty_levels': self.get_difficulty_levels(),
            'top_tags': self.get_all_tags()[:20],
            'content_overview': []
        }
        
        # Add overview of each entry
        for entry in self.search_index[:100]:  # Limit to first 100 for overview
            overview = {
                'id': entry.get('id'),
                'title': entry.get('title'),
                'category': entry.get('category'),
                'difficulty': entry.get('difficulty'),
                'key_concepts': entry.get('key_concepts', [])[:5],
                'summary': entry.get('summary', '')[:200]
            }
            summary['content_overview'].append(overview)
        
        return summary

# Example usage functions for AI/API integration
def create_api_interface():
    """Create the main API interface"""
    return CreatioKnowledgeHubAPI()

def quick_search(query: str, limit: int = 5) -> List[Dict]:
    """Quick search function for AI agents"""
    api = create_api_interface()
    return api.search_content(query, limit=limit)

def get_development_content(limit: int = 10) -> List[Dict]:
    """Get development-focused content"""
    api = create_api_interface()
    return api.get_by_category('development', limit=limit)

def get_beginner_content(limit: int = 10) -> List[Dict]:
    """Get beginner-friendly content"""
    api = create_api_interface()
    return api.get_by_difficulty('beginner', limit=limit)

def find_related(content_id: int) -> List[Dict]:
    """Find content related to a specific entry"""
    api = create_api_interface()
    return api.get_related_content(content_id)

if __name__ == "__main__":
    # Test the API
    api = CreatioKnowledgeHubAPI()
    
    print("Creatio Knowledge Hub API Test")
    print("=" * 40)
    
    # Test search
    results = api.search_content("business process", limit=3)
    print(f"Search results for 'business process': {len(results)} found")
    for result in results:
        print(f"  - {result['title']} (Category: {result['category']})")
    
    print()
    
    # Test categories
    categories = api.get_categories()
    print("Available categories:")
    for cat in categories:
        print(f"  - {cat['category']}: {cat['count']} entries")
    
    print()
    
    # Test suggestions
    user_profile = {
        'interests': ['development', 'integration'],
        'skill_level': 'intermediate',
        'role': 'developer'
    }
    suggestions = api.suggest_content(user_profile)
    print(f"Content suggestions for developer: {len(suggestions)} found")
    for suggestion in suggestions[:3]:
        print(f"  - {suggestion['title']} (Score: {suggestion.get('suggestion_score', 0):.1f})")
    
    print("\nAPI ready for AI/Agent integration!")
