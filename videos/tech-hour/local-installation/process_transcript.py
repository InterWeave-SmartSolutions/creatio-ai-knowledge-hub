#!/usr/bin/env python3
"""
VTT Transcript Processor for Creatio AI Knowledge Hub
Converts WebVTT subtitle files into clean, AI-friendly formats
"""

import re
import json
import os
from datetime import datetime

def clean_vtt_text(text):
    """Clean VTT formatting tags from text"""
    # Remove HTML-like tags
    text = re.sub(r'<[^>]*>', '', text)
    # Remove timestamp tags like <00:00:02.159>
    text = re.sub(r'<\d{2}:\d{2}:\d{2}\.\d{3}>', '', text)
    # Clean up extra whitespace
    text = ' '.join(text.split())
    return text.strip()

def parse_timestamp(timestamp_str):
    """Convert VTT timestamp to seconds"""
    # Format: 00:00:01.839
    parts = timestamp_str.split(':')
    hours = int(parts[0])
    minutes = int(parts[1])
    seconds_parts = parts[2].split('.')
    seconds = int(seconds_parts[0])
    milliseconds = int(seconds_parts[1]) if len(seconds_parts) > 1 else 0
    
    total_seconds = hours * 3600 + minutes * 60 + seconds + milliseconds / 1000
    return total_seconds

def process_vtt_file(input_file, output_prefix):
    """Process VTT file and create multiple output formats"""
    
    segments = []
    current_text = ""
    current_start = None
    
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # Look for timestamp lines
        if ' --> ' in line:
            # Parse timestamp
            start_time, end_time = line.split(' --> ')
            start_time = start_time.split()[0]  # Remove align:start position:0%
            end_time = end_time.split()[0]
            
            # Collect text until next timestamp or empty line
            text_lines = []
            i += 1
            while i < len(lines):
                text_line = lines[i].strip()
                if not text_line or ' --> ' in text_line:
                    break
                text_lines.append(text_line)
                i += 1
            
            if text_lines:
                text = ' '.join(text_lines)
                clean_text = clean_vtt_text(text)
                
                if clean_text:  # Only add non-empty segments
                    segments.append({
                        'start_time': start_time,
                        'end_time': end_time,
                        'start_seconds': parse_timestamp(start_time),
                        'end_seconds': parse_timestamp(end_time),
                        'text': clean_text
                    })
            continue
        
        i += 1
    
    # Generate different output formats
    
    # 1. Clean plain text transcript
    with open(f"{output_prefix}_transcript.txt", 'w', encoding='utf-8') as f:
        f.write("CREATIO TECH HOUR - INSTALLING LOCAL INSTANCE\n")
        f.write("=" * 50 + "\n\n")
        
        full_text = ""
        for segment in segments:
            if segment['text'] not in full_text[-100:]:  # Simple deduplication
                full_text += segment['text'] + " "
        
        # Clean up and format
        sentences = full_text.split('. ')
        for sentence in sentences:
            if sentence.strip():
                f.write(sentence.strip() + ".\n")
    
    # 2. Timestamped transcript
    with open(f"{output_prefix}_timestamped.txt", 'w', encoding='utf-8') as f:
        f.write("CREATIO TECH HOUR - TIMESTAMPED TRANSCRIPT\n")
        f.write("=" * 50 + "\n\n")
        
        for segment in segments:
            minutes = int(segment['start_seconds'] // 60)
            seconds = int(segment['start_seconds'] % 60)
            f.write(f"[{minutes:02d}:{seconds:02d}] {segment['text']}\n")
    
    # 3. JSON format for AI/API consumption
    output_data = {
        'metadata': {
            'title': 'Tech Hour - Installing Local instance of Creatio',
            'duration': f"{int(segments[-1]['end_seconds'] // 60):02d}:{int(segments[-1]['end_seconds'] % 60):02d}" if segments else "00:00",
            'processed_date': datetime.now().isoformat(),
            'source': 'https://www.youtube.com/watch?v=lf-yWsJ4p0Q',
            'type': 'technical_tutorial',
            'tags': ['creatio', 'installation', 'local-deployment', 'tutorial']
        },
        'segments': segments,
        'full_transcript': ' '.join([seg['text'] for seg in segments]),
        'key_topics': extract_key_topics(segments)
    }
    
    with open(f"{output_prefix}_data.json", 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
    
    # 4. Markdown format
    with open(f"{output_prefix}_guide.md", 'w', encoding='utf-8') as f:
        f.write("# Creatio Tech Hour: Installing Local Instance\n\n")
        f.write("## Video Information\n")
        f.write(f"- **Source**: [YouTube](https://www.youtube.com/watch?v=lf-yWsJ4p0Q)\n")
        f.write(f"- **Duration**: {output_data['metadata']['duration']}\n")
        f.write(f"- **Type**: Technical Tutorial\n\n")
        
        f.write("## Key Topics Covered\n")
        for topic in output_data['key_topics']:
            f.write(f"- {topic}\n")
        f.write("\n")
        
        f.write("## Full Transcript\n\n")
        current_time = 0
        for segment in segments:
            if segment['start_seconds'] - current_time > 300:  # 5-minute breaks
                minutes = int(segment['start_seconds'] // 60)
                f.write(f"\n### {minutes:02d}:{int(segment['start_seconds'] % 60):02d}\n\n")
                current_time = segment['start_seconds']
            f.write(f"{segment['text']} ")
    
    print(f"✅ Processed {len(segments)} transcript segments")
    print(f"📄 Generated files:")
    print(f"   - {output_prefix}_transcript.txt (Clean text)")
    print(f"   - {output_prefix}_timestamped.txt (With timestamps)")
    print(f"   - {output_prefix}_data.json (AI/API format)")
    print(f"   - {output_prefix}_guide.md (Markdown guide)")

def extract_key_topics(segments):
    """Extract key topics from transcript segments"""
    text = ' '.join([seg['text'] for seg in segments]).lower()
    
    # Common Creatio/installation related keywords
    topics = []
    
    keywords_map = {
        'System Requirements': ['requirements', 'system', 'prerequisites', 'minimum'],
        'Database Setup': ['database', 'sql server', 'postgresql', 'oracle', 'db'],
        'IIS Configuration': ['iis', 'internet information services', 'web server'],
        'Installation Process': ['install', 'setup', 'deployment', 'configure'],
        'Troubleshooting': ['error', 'troubleshoot', 'problem', 'issue', 'fix'],
        'Redis Configuration': ['redis', 'cache', 'session'],
        'SSL/Security': ['ssl', 'certificate', 'security', 'https'],
        'Performance': ['performance', 'optimization', 'tuning'],
        'Licensing': ['license', 'activation', 'key'],
        'Updates': ['update', 'upgrade', 'patch', 'version']
    }
    
    for topic, keywords in keywords_map.items():
        if any(keyword in text for keyword in keywords):
            topics.append(topic)
    
    return topics if topics else ['Installation', 'Configuration', 'Setup']

if __name__ == "__main__":
    vtt_file = "Tech Hour - Installing Local instance of Creatio [lf-yWsJ4p0Q].en.vtt"
    output_prefix = "creatio_installation"
    
    if os.path.exists(vtt_file):
        process_vtt_file(vtt_file, output_prefix)
    else:
        print(f"❌ VTT file not found: {vtt_file}")
