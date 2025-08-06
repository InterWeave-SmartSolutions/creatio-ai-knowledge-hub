#!/usr/bin/env python3
"""
Utility to query and analyze scraped Creatio Knowledge Hub data
"""

import sqlite3
import argparse
import json
from pathlib import Path
from datetime import datetime

def connect_db():
    """Connect to the knowledge hub database"""
    db_path = Path("ai_knowledge_hub/solutions_hub/knowledge_hub.db")
    if not db_path.exists():
        print(f"Database not found at {db_path}")
        print("Run the scraper first to create the database.")
        return None
    
    return sqlite3.connect(db_path)

def list_pages(conn, limit=10):
    """List scraped pages"""
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, title, url, scraped_at 
        FROM pages 
        ORDER BY scraped_at DESC 
        LIMIT ?
    """, (limit,))
    
    results = cursor.fetchall()
    if not results:
        print("No pages found in database.")
        return
    
    print(f"\nFound {len(results)} pages (showing last {limit}):")
    print("-" * 80)
    
    for page_id, title, url, scraped_at in results:
        print(f"ID: {page_id}")
        print(f"Title: {title}")
        print(f"URL: {url}")
        print(f"Scraped: {scraped_at}")
        print("-" * 80)

def search_content(conn, search_term, limit=5):
    """Search for content in scraped pages"""
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, title, url, 
               substr(content_text, 1, 200) as preview
        FROM pages 
        WHERE content_text LIKE ? OR title LIKE ?
        ORDER BY 
            CASE 
                WHEN title LIKE ? THEN 1 
                ELSE 2 
            END,
            scraped_at DESC
        LIMIT ?
    """, (f'%{search_term}%', f'%{search_term}%', f'%{search_term}%', limit))
    
    results = cursor.fetchall()
    if not results:
        print(f"No results found for '{search_term}'")
        return
    
    print(f"\nFound {len(results)} results for '{search_term}':")
    print("=" * 80)
    
    for page_id, title, url, preview in results:
        print(f"Title: {title}")
        print(f"URL: {url}")
        print(f"Preview: {preview}...")
        print("-" * 80)

def show_stats(conn):
    """Show database statistics"""
    cursor = conn.cursor()
    
    # Page stats
    cursor.execute("SELECT COUNT(*) FROM pages")
    page_count = cursor.fetchone()[0]
    
    # Link stats
    cursor.execute("SELECT COUNT(*) FROM links")
    link_count = cursor.fetchone()[0]
    
    # Media stats
    cursor.execute("SELECT COUNT(*) FROM media")
    media_count = cursor.fetchone()[0]
    
    # Recent activity
    cursor.execute("""
        SELECT DATE(scraped_at) as date, COUNT(*) as count 
        FROM pages 
        GROUP BY DATE(scraped_at) 
        ORDER BY date DESC 
        LIMIT 5
    """)
    recent_activity = cursor.fetchall()
    
    print("\n📊 Database Statistics")
    print("=" * 40)
    print(f"Total Pages: {page_count}")
    print(f"Total Links: {link_count}")
    print(f"Total Media Items: {media_count}")
    
    if recent_activity:
        print("\n📅 Recent Activity:")
        for date, count in recent_activity:
            print(f"  {date}: {count} pages")

def export_content(conn, output_file, format_type='json'):
    """Export scraped content to file"""
    cursor = conn.cursor()
    
    if format_type == 'json':
        cursor.execute("""
            SELECT url, title, content_text, content_markdown, scraped_at
            FROM pages
            ORDER BY scraped_at DESC
        """)
        
        results = cursor.fetchall()
        data = []
        
        for url, title, content_text, content_markdown, scraped_at in results:
            data.append({
                'url': url,
                'title': title,
                'content_text': content_text,
                'content_markdown': content_markdown,
                'scraped_at': scraped_at
            })
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"Exported {len(data)} pages to {output_file}")
    
    elif format_type == 'markdown':
        cursor.execute("""
            SELECT url, title, content_markdown, scraped_at
            FROM pages
            ORDER BY scraped_at DESC
        """)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("# Creatio Knowledge Hub - Scraped Content\n\n")
            f.write(f"Exported on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            for url, title, content_markdown, scraped_at in cursor.fetchall():
                f.write(f"## {title}\n\n")
                f.write(f"**URL:** {url}\n")
                f.write(f"**Scraped:** {scraped_at}\n\n")
                f.write("---\n\n")
                f.write(content_markdown)
                f.write("\n\n---\n\n")
        
        print(f"Exported content to {output_file}")

def show_page_details(conn, page_id):
    """Show detailed information about a specific page"""
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT id, url, title, content_text, content_markdown, scraped_at, metadata
        FROM pages 
        WHERE id = ?
    """, (page_id,))
    
    result = cursor.fetchone()
    if not result:
        print(f"Page with ID {page_id} not found.")
        return
    
    page_id, url, title, content_text, content_markdown, scraped_at, metadata = result
    
    print(f"\n📄 Page Details (ID: {page_id})")
    print("=" * 50)
    print(f"Title: {title}")
    print(f"URL: {url}")
    print(f"Scraped: {scraped_at}")
    
    if metadata:
        try:
            meta = json.loads(metadata)
            print(f"Links Found: {meta.get('links_count', 'N/A')}")
            print(f"Media Items: {meta.get('media_count', 'N/A')}")
        except:
            pass
    
    print(f"\nContent Preview (first 500 chars):")
    print("-" * 30)
    print(content_text[:500] + "..." if len(content_text) > 500 else content_text)
    
    # Show related links
    cursor.execute("""
        SELECT target_url, link_text
        FROM links 
        WHERE source_page_id = ?
        LIMIT 10
    """, (page_id,))
    
    links = cursor.fetchall()
    if links:
        print(f"\nRelated Links ({len(links)} found):")
        print("-" * 30)
        for target_url, link_text in links[:5]:  # Show first 5
            print(f"• {link_text}: {target_url}")

def main():
    """Main CLI interface"""
    parser = argparse.ArgumentParser(description="Query Creatio Knowledge Hub scraped data")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # List command
    list_parser = subparsers.add_parser('list', help='List scraped pages')
    list_parser.add_argument('--limit', type=int, default=10, help='Number of pages to show')
    
    # Search command
    search_parser = subparsers.add_parser('search', help='Search content')
    search_parser.add_argument('term', help='Search term')
    search_parser.add_argument('--limit', type=int, default=5, help='Number of results to show')
    
    # Stats command
    subparsers.add_parser('stats', help='Show database statistics')
    
    # Export command
    export_parser = subparsers.add_parser('export', help='Export content')
    export_parser.add_argument('filename', help='Output filename')
    export_parser.add_argument('--format', choices=['json', 'markdown'], default='json', help='Export format')
    
    # Show command
    show_parser = subparsers.add_parser('show', help='Show page details')
    show_parser.add_argument('page_id', type=int, help='Page ID to show')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    conn = connect_db()
    if not conn:
        return
    
    try:
        if args.command == 'list':
            list_pages(conn, args.limit)
        elif args.command == 'search':
            search_content(conn, args.term, args.limit)
        elif args.command == 'stats':
            show_stats(conn)
        elif args.command == 'export':
            export_content(conn, args.filename, args.format)
        elif args.command == 'show':
            show_page_details(conn, args.page_id)
    
    finally:
        conn.close()

if __name__ == "__main__":
    main()
