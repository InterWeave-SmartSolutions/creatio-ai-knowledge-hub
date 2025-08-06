#!/usr/bin/env python3
"""
Creatio Knowledge Hub - AI Usage Demonstration
Shows how AI agents and APIs can effectively use the integrated knowledge base
"""

import json
from knowledge_hub_api import CreatioKnowledgeHubAPI

def demonstrate_ai_usage():
    """Demonstrate various ways AI can consume the knowledge hub"""
    
    print("🤖 CREATIO AI KNOWLEDGE HUB DEMONSTRATION")
    print("=" * 50)
    
    # Initialize the API
    api = CreatioKnowledgeHubAPI()
    
    # 1. AI AGENT SCENARIO: User asks about business processes
    print("\n📋 SCENARIO 1: AI Agent answering 'How do I create business processes in Creatio?'")
    print("-" * 60)
    
    bp_results = api.search_content("business process", limit=3)
    print(f"Found {len(bp_results)} relevant articles:")
    
    for i, result in enumerate(bp_results, 1):
        print(f"\n{i}. **{result['title']}**")
        print(f"   Category: {result['category']} | Difficulty: {result['difficulty']}")
        print(f"   Relevance Score: {result['relevance_score']:.1f}")
        print(f"   Summary: {result['summary'][:150]}...")
        print(f"   Key Concepts: {', '.join(result['key_concepts'][:3])}")
        print(f"   🔗 {result['url']}")
    
    # 2. CONTENT RECOMMENDATION SCENARIO
    print("\n\n🎯 SCENARIO 2: Personalized Content Recommendations")
    print("-" * 60)
    
    user_profiles = [
        {
            'name': 'New Developer',
            'profile': {
                'interests': ['development', 'api', 'integration'],
                'skill_level': 'beginner',
                'role': 'developer'
            }
        },
        {
            'name': 'System Administrator',
            'profile': {
                'interests': ['administration', 'security', 'setup'],
                'skill_level': 'intermediate',
                'role': 'administrator'
            }
        }
    ]
    
    for user in user_profiles:
        print(f"\n👤 Recommendations for {user['name']}:")
        suggestions = api.suggest_content(user['profile'])
        
        for i, suggestion in enumerate(suggestions[:3], 1):
            print(f"   {i}. {suggestion['title'][:60]}...")
            print(f"      Score: {suggestion['suggestion_score']:.1f} | {suggestion['category']}")
    
    # 3. LEARNING PATH GENERATION
    print("\n\n📚 SCENARIO 3: Learning Path Generation")
    print("-" * 60)
    
    topics = ['integration', 'mobile development']
    
    for topic in topics:
        print(f"\n📖 Learning Path for '{topic}':")
        learning_path = api.get_learning_path(topic)
        
        if learning_path:
            for i, content in enumerate(learning_path[:4], 1):
                difficulty_emoji = {'beginner': '🟢', 'intermediate': '🟡', 'advanced': '🔴'}
                emoji = difficulty_emoji.get(content['difficulty'], '⚪')
                print(f"   {i}. {emoji} {content['title'][:50]}...")
                print(f"      {content['difficulty'].title()} Level")
        else:
            print("   No learning path found for this topic.")
    
    # 4. CATEGORY-BASED CONTENT ACCESS
    print("\n\n📂 SCENARIO 4: Category-Based Content Discovery")
    print("-" * 60)
    
    categories = api.get_categories()
    print("Available Knowledge Categories:")
    
    for cat in categories:
        print(f"\n📁 {cat['category'].title()} ({cat['count']} entries)")
        
        # Get sample content from each category
        sample_content = api.get_by_category(cat['category'], limit=2)
        for content in sample_content:
            print(f"   • {content['title'][:55]}...")
    
    # 5. RELATED CONTENT DISCOVERY
    print("\n\n🔗 SCENARIO 5: Related Content Discovery")
    print("-" * 60)
    
    # Get a sample content item
    sample_search = api.search_content("development", limit=1)
    if sample_search:
        sample_content = sample_search[0]
        print(f"Base Content: {sample_content['title']}")
        
        related = api.get_related_content(sample_content['id'], limit=3)
        print(f"\nFound {len(related)} related articles:")
        
        for i, rel in enumerate(related, 1):
            relation_score = rel.get('relation_score', 0)
            print(f"   {i}. {rel['title'][:50]}...")
            print(f"      Relation Score: {relation_score:.1f} | {rel['category']}")
    
    # 6. FULL CONTENT ACCESS
    print("\n\n📄 SCENARIO 6: Full Content Retrieval for Deep Analysis")
    print("-" * 60)
    
    if sample_search:
        content_id = sample_search[0]['id']
        full_content = api.get_full_content(content_id)
        
        if full_content:
            print(f"Content Analysis for: {full_content['title']}")
            print(f"Word Count: {full_content['word_count']}")
            print(f"Category: {full_content['category']}")
            print(f"Difficulty: {full_content['difficulty_level']}")
            print(f"Key Concepts: {', '.join(full_content['key_concepts'][:5])}")
            print(f"Use Cases: {', '.join(full_content['use_cases'][:3])}")
            print(f"Content Preview: {full_content['content'][:200]}...")
    
    # 7. ANALYTICS AND INSIGHTS
    print("\n\n📊 SCENARIO 7: Knowledge Base Analytics")
    print("-" * 60)
    
    summary = api.export_content_summary()
    
    print(f"Knowledge Base Overview:")
    print(f"• Total Entries: {summary['total_entries']}")
    print(f"• Categories: {len(summary['categories'])}")
    print(f"• Difficulty Levels: {len(summary['difficulty_levels'])}")
    
    print(f"\nTop AI Tags:")
    for tag in summary['top_tags'][:10]:
        print(f"   • {tag['tag']} ({tag['count']} uses)")
    
    print(f"\nCategory Distribution:")
    for cat in summary['categories']:
        bar_length = int(cat['count'] / max([c['count'] for c in summary['categories']]) * 20)
        bar = "█" * bar_length
        print(f"   {cat['category']:<15} {bar} {cat['count']}")
    
    # 8. API INTEGRATION EXAMPLES
    print("\n\n🔌 SCENARIO 8: API Integration Patterns")
    print("-" * 60)
    
    print("Example API calls for different use cases:")
    
    api_examples = [
        {
            'use_case': 'Chatbot answering specific questions',
            'code': 'api.search_content("how to configure user permissions", limit=3)'
        },
        {
            'use_case': 'Getting beginner-friendly content',
            'code': 'api.get_by_difficulty("beginner", limit=5)'
        },
        {
            'use_case': 'Finding development tutorials',
            'code': 'api.get_by_tags(["tutorial", "development"], limit=5)'
        },
        {
            'use_case': 'Building learning curriculum',
            'code': 'api.get_learning_path("creatio development")'
        }
    ]
    
    for example in api_examples:
        print(f"\n   Use Case: {example['use_case']}")
        print(f"   API Call: {example['code']}")
    
    print("\n\n✅ DEMONSTRATION COMPLETE")
    print("=" * 50)
    print("The Creatio AI Knowledge Hub is ready for:")
    print("• AI Agents and Chatbots")
    print("• Content Recommendation Systems")  
    print("• Learning Management Platforms")
    print("• Search and Discovery APIs")
    print("• Knowledge Management Systems")
    print("\nAll content is optimized for AI consumption with structured metadata,")
    print("semantic search capabilities, and comprehensive relationship mapping.")

if __name__ == "__main__":
    demonstrate_ai_usage()
