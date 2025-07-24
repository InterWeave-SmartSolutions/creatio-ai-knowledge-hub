#!/usr/bin/env python3
"""
LLM-Powered Summarizer for Video Transcriptions
Enhanced AI analysis using language models for better content understanding
"""

import json
import logging
from typing import Dict, List, Any
from pathlib import Path
import re

logger = logging.getLogger(__name__)

class LLMSummarizer:
    def __init__(self, provider: str = "mock"):
        """
        Initialize the LLM summarizer
        
        Args:
            provider: LLM provider (mock, openai, anthropic, etc.)
        """
        self.provider = provider
        
    def generate_enhanced_summary(self, transcription_text: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate enhanced summary using LLM capabilities
        
        Args:
            transcription_text: Full transcription text
            metadata: Video metadata
            
        Returns:
            Enhanced summary with AI analysis
        """
        # For now, we'll use a mock implementation
        # In production, this would call actual LLM APIs
        
        if self.provider == "mock":
            return self._mock_llm_summary(transcription_text, metadata)
        else:
            # Placeholder for actual LLM integration
            return self._mock_llm_summary(transcription_text, metadata)
    
    def _mock_llm_summary(self, text: str, metadata: Dict) -> Dict[str, Any]:
        """
        Mock LLM summary - simulates what a real LLM would produce
        This is a sophisticated rule-based summary that mimics LLM output
        """
        
        # Analyze text structure
        sentences = self._split_sentences(text)
        paragraphs = text.split('\n\n')
        words = text.split()
        
        # Extract key information
        key_phrases = self._extract_key_phrases(text)
        technical_terms = self._extract_technical_terms(text)
        action_items = self._extract_action_items(text)
        questions = self._extract_questions(text)
        
        # Determine content type and structure
        content_type = self._classify_content_type(text, metadata)
        main_topics = self._extract_main_topics(text)
        
        # Generate structured summary
        summary = {
            "executive_summary": self._generate_executive_summary(sentences, content_type),
            "key_points": self._generate_key_points(key_phrases, sentences),
            "technical_concepts": technical_terms,
            "action_items": action_items,
            "questions_raised": questions,
            "content_structure": {
                "type": content_type,
                "main_sections": self._identify_sections(paragraphs),
                "estimated_complexity": self._assess_complexity(text, technical_terms),
            },
            "audience_analysis": {
                "target_audience": self._identify_target_audience(text, technical_terms),
                "prerequisite_knowledge": self._assess_prerequisites(technical_terms),
                "learning_objectives": self._extract_learning_objectives(text),
            },
            "content_quality": {
                "clarity_score": self._assess_clarity(sentences),
                "information_density": self._calculate_info_density(text, key_phrases),
                "engagement_level": self._assess_engagement(text, questions),
            },
            "ai_generated_tags": self._generate_ai_tags(main_topics, technical_terms, content_type),
            "related_concepts": self._suggest_related_concepts(technical_terms, main_topics),
        }
        
        return summary
    
    def _split_sentences(self, text: str) -> List[str]:
        """Split text into sentences"""
        sentences = re.split(r'[.!?]+', text)
        return [s.strip() for s in sentences if s.strip()]
    
    def _extract_key_phrases(self, text: str) -> List[str]:
        """Extract key phrases from the text"""
        # Simple approach: look for repeated phrases and important patterns
        words = text.lower().split()
        
        # Extract 2-3 word phrases that appear multiple times
        phrases = {}
        for i in range(len(words) - 1):
            phrase = ' '.join(words[i:i+2])
            if len(phrase) > 5:  # Skip very short phrases
                phrases[phrase] = phrases.get(phrase, 0) + 1
        
        # Return most frequent phrases
        frequent_phrases = sorted(phrases.items(), key=lambda x: x[1], reverse=True)
        return [phrase for phrase, count in frequent_phrases[:10] if count > 1]
    
    def _extract_technical_terms(self, text: str) -> List[str]:
        """Extract technical terms and jargon"""
        # Common technical terms in CRM/BPM/software domain
        technical_patterns = [
            r'\b[A-Z]{2,}\b',  # Acronyms
            r'\b\w*api\w*\b',  # API related terms
            r'\b\w*config\w*\b',  # Configuration terms
            r'\b\w*integrat\w*\b',  # Integration terms
            r'\b\w*automat\w*\b',  # Automation terms
            r'\b\w*dashboard\w*\b',  # Dashboard terms
            r'\b\w*workflow\w*\b',  # Workflow terms
        ]
        
        technical_terms = set()
        for pattern in technical_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            technical_terms.update(matches)
        
        # Add domain-specific terms
        domain_terms = ['CRM', 'BPM', 'API', 'integration', 'workflow', 'automation', 
                       'dashboard', 'configuration', 'customization', 'Creatio']
        
        found_terms = []
        for term in domain_terms:
            if term.lower() in text.lower():
                found_terms.append(term)
        
        technical_terms.update(found_terms)
        return list(technical_terms)[:15]  # Limit to top 15
    
    def _extract_action_items(self, text: str) -> List[str]:
        """Extract action items and instructions"""
        action_patterns = [
            r'(you need to|you should|you must|you have to|make sure to|remember to|don\'t forget to)[^.!?]*[.!?]',
            r'(step \d+|first|second|third|next|then|finally)[^.!?]*[.!?]',
            r'(click|select|choose|configure|set up|install|create|add)[^.!?]*[.!?]',
        ]
        
        action_items = []
        for pattern in action_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            action_items.extend(matches)
        
        return action_items[:10]  # Limit to top 10
    
    def _extract_questions(self, text: str) -> List[str]:
        """Extract questions from the text"""
        questions = re.findall(r'[^.!?]*\?', text)
        return [q.strip() + '?' for q in questions if q.strip()][:10]
    
    def _classify_content_type(self, text: str, metadata: Dict) -> str:
        """Classify the type of content"""
        content_indicators = {
            'tutorial': ['tutorial', 'how to', 'step by step', 'guide', 'learn', 'teach'],
            'demo': ['demo', 'demonstration', 'show you', 'example', 'walkthrough'],
            'presentation': ['presentation', 'slide', 'overview', 'introduction', 'agenda'],
            'webinar': ['webinar', 'live', 'q&a', 'questions', 'audience'],
            'training': ['training', 'course', 'lesson', 'module', 'exercise'],
            'documentation': ['documentation', 'reference', 'specification', 'manual'],
        }
        
        text_lower = text.lower()
        scores = {}
        
        for content_type, indicators in content_indicators.items():
            score = sum(1 for indicator in indicators if indicator in text_lower)
            if score > 0:
                scores[content_type] = score
        
        return max(scores.items(), key=lambda x: x[1])[0] if scores else 'general'
    
    def _extract_main_topics(self, text: str) -> List[str]:
        """Extract main topics discussed in the content"""
        # Topic keywords for business software domain
        topic_keywords = {
            'user_management': ['user', 'role', 'permission', 'access', 'authentication'],
            'data_management': ['data', 'import', 'export', 'migration', 'database'],
            'customization': ['customize', 'configuration', 'settings', 'personalize'],
            'integration': ['integration', 'api', 'connector', 'sync', 'webhook'],
            'automation': ['automation', 'workflow', 'business process', 'trigger'],
            'reporting': ['report', 'dashboard', 'analytics', 'metrics', 'chart'],
            'sales': ['sales', 'opportunity', 'lead', 'deal', 'pipeline'],
            'marketing': ['marketing', 'campaign', 'email', 'lead generation'],
            'customer_service': ['service', 'support', 'ticket', 'case', 'help desk'],
        }
        
        text_lower = text.lower()
        found_topics = []
        
        for topic, keywords in topic_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                found_topics.append(topic.replace('_', ' '))
        
        return found_topics
    
    def _generate_executive_summary(self, sentences: List[str], content_type: str) -> str:
        """Generate an executive summary"""
        if not sentences:
            return "No content available for summary."
        
        # Take first few sentences and last few sentences for context
        key_sentences = sentences[:2] + sentences[-1:]
        summary = ' '.join(key_sentences[:3])  # Limit to 3 sentences
        
        # Add content type context
        type_intro = {
            'tutorial': 'This tutorial covers',
            'demo': 'This demonstration shows',
            'presentation': 'This presentation discusses',
            'webinar': 'This webinar explores',
            'training': 'This training session teaches',
            'documentation': 'This documentation explains',
            'general': 'This content covers',
        }
        
        intro = type_intro.get(content_type, 'This content covers')
        return f"{intro}: {summary}"
    
    def _generate_key_points(self, key_phrases: List[str], sentences: List[str]) -> List[str]:
        """Generate key points from the content"""
        # Simple approach: find sentences containing key phrases
        key_points = []
        
        for phrase in key_phrases[:5]:  # Top 5 key phrases
            for sentence in sentences:
                if phrase in sentence.lower() and len(sentence.split()) > 5:
                    key_points.append(sentence)
                    break
        
        # If we don't have enough key points, add some of the longer sentences
        if len(key_points) < 3:
            longer_sentences = [s for s in sentences if len(s.split()) > 10]
            key_points.extend(longer_sentences[:3-len(key_points)])
        
        return key_points[:5]  # Limit to 5 key points
    
    def _identify_sections(self, paragraphs: List[str]) -> List[str]:
        """Identify main sections in the content"""
        sections = []
        
        for para in paragraphs:
            if len(para.split()) > 5:  # Skip very short paragraphs
                # Try to identify section headers or main topics
                first_sentence = para.split('.')[0]
                if len(first_sentence.split()) < 10:  # Likely a header or intro
                    sections.append(first_sentence[:100])  # Limit length
        
        return sections[:5]  # Limit to 5 main sections
    
    def _assess_complexity(self, text: str, technical_terms: List[str]) -> str:
        """Assess the complexity level of the content"""
        word_count = len(text.split())
        tech_density = len(technical_terms) / word_count * 100 if word_count > 0 else 0
        avg_sentence_length = word_count / len(self._split_sentences(text)) if self._split_sentences(text) else 0
        
        if tech_density > 3 or avg_sentence_length > 25:
            return "high"
        elif tech_density > 1 or avg_sentence_length > 15:
            return "medium"
        else:
            return "low"
    
    def _identify_target_audience(self, text: str, technical_terms: List[str]) -> str:
        """Identify the target audience"""
        beginner_indicators = ['basic', 'introduction', 'getting started', 'beginner', 'first time']
        advanced_indicators = ['advanced', 'expert', 'complex', 'detailed', 'in-depth']
        
        text_lower = text.lower()
        
        if any(indicator in text_lower for indicator in beginner_indicators):
            return "beginner"
        elif any(indicator in text_lower for indicator in advanced_indicators) or len(technical_terms) > 10:
            return "advanced"
        else:
            return "intermediate"
    
    def _assess_prerequisites(self, technical_terms: List[str]) -> List[str]:
        """Assess prerequisite knowledge needed"""
        prerequisites = []
        
        if any(term.lower() in ['api', 'integration', 'webhook'] for term in technical_terms):
            prerequisites.append("Basic understanding of APIs and integrations")
        
        if any(term.lower() in ['configuration', 'setup', 'customize'] for term in technical_terms):
            prerequisites.append("System administration knowledge")
        
        if any(term.lower() in ['crm', 'sales', 'opportunity'] for term in technical_terms):
            prerequisites.append("CRM system familiarity")
        
        if any(term.lower() in ['bpm', 'workflow', 'process'] for term in technical_terms):
            prerequisites.append("Business process understanding")
        
        return prerequisites
    
    def _extract_learning_objectives(self, text: str) -> List[str]:
        """Extract learning objectives from the content"""
        objective_patterns = [
            r'(you will learn|you\'ll learn|by the end|after this|objective)[^.!?]*[.!?]',
            r'(learn how to|understand how|discover how)[^.!?]*[.!?]',
        ]
        
        objectives = []
        for pattern in objective_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            objectives.extend(matches)
        
        return objectives[:5]
    
    def _assess_clarity(self, sentences: List[str]) -> int:
        """Assess content clarity (1-10 scale)"""
        if not sentences:
            return 1
        
        avg_length = sum(len(s.split()) for s in sentences) / len(sentences)
        
        # Penalize very long or very short sentences
        if avg_length > 30 or avg_length < 5:
            return 5
        elif avg_length > 25 or avg_length < 8:
            return 7
        else:
            return 9
    
    def _calculate_info_density(self, text: str, key_phrases: List[str]) -> float:
        """Calculate information density"""
        word_count = len(text.split())
        info_indicators = len(key_phrases)
        
        return round(info_indicators / word_count * 100, 2) if word_count > 0 else 0
    
    def _assess_engagement(self, text: str, questions: List[str]) -> str:
        """Assess engagement level"""
        engagement_indicators = len(questions) + text.lower().count('example') + text.lower().count('imagine')
        
        if engagement_indicators > 5:
            return "high"
        elif engagement_indicators > 2:
            return "medium"
        else:
            return "low"
    
    def _generate_ai_tags(self, topics: List[str], technical_terms: List[str], content_type: str) -> List[str]:
        """Generate AI-suggested tags"""
        tags = [content_type]
        tags.extend(topics[:5])
        tags.extend([term.lower() for term in technical_terms[:5]])
        
        # Add some generic helpful tags
        generic_tags = ['business software', 'tutorial', 'training', 'software guide']
        tags.extend([tag for tag in generic_tags if tag not in tags])
        
        return list(set(tags))[:15]  # Remove duplicates and limit
    
    def _suggest_related_concepts(self, technical_terms: List[str], topics: List[str]) -> List[str]:
        """Suggest related concepts that might be of interest"""
        concept_map = {
            'crm': ['customer relationship management', 'sales pipeline', 'lead management'],
            'bpm': ['business process management', 'workflow automation', 'process optimization'],
            'api': ['system integration', 'data synchronization', 'web services'],
            'dashboard': ['data visualization', 'business intelligence', 'reporting'],
            'automation': ['workflow automation', 'business rules', 'triggers'],
        }
        
        related = []
        all_terms = [term.lower() for term in technical_terms] + [topic.lower() for topic in topics]
        
        for term in all_terms:
            if term in concept_map:
                related.extend(concept_map[term])
        
        return list(set(related))[:10]


def enhance_existing_summaries(transcriptions_dir: str):
    """
    Enhance existing summary files with LLM analysis
    """
    transcriptions_path = Path(transcriptions_dir)
    summaries_dir = transcriptions_path / "summaries"
    transcripts_dir = transcriptions_path / "transcripts"
    
    if not summaries_dir.exists() or not transcripts_dir.exists():
        logger.error("Transcriptions directory structure not found")
        return
    
    summarizer = LLMSummarizer()
    
    # Find all transcript files
    for transcript_file in transcripts_dir.glob("*_transcript.txt"):
        base_name = transcript_file.stem.replace("_transcript", "")
        summary_file = summaries_dir / f"{base_name}_summary.json"
        enhanced_file = summaries_dir / f"{base_name}_enhanced_summary.json"
        
        if enhanced_file.exists():
            logger.info(f"Enhanced summary already exists for {base_name}")
            continue
        
        try:
            # Read transcript
            with open(transcript_file, 'r', encoding='utf-8') as f:
                transcript_text = f.read()
            
            # Read existing summary if available
            metadata = {}
            if summary_file.exists():
                with open(summary_file, 'r', encoding='utf-8') as f:
                    metadata = json.load(f)
            
            # Generate enhanced summary
            enhanced = summarizer.generate_enhanced_summary(transcript_text, metadata)
            
            # Save enhanced summary
            with open(enhanced_file, 'w', encoding='utf-8') as f:
                json.dump(enhanced, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Generated enhanced summary for {base_name}")
            
        except Exception as e:
            logger.error(f"Failed to enhance summary for {base_name}: {e}")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Enhance video summaries with LLM analysis")
    parser.add_argument("transcriptions_dir", help="Directory containing transcription files")
    
    args = parser.parse_args()
    enhance_existing_summaries(args.transcriptions_dir)
