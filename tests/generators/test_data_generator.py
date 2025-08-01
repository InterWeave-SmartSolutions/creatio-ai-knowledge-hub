"""
Test data generation utilities for Creatio AI Knowledge Hub
"""
import json
import random
import sqlite3
import tempfile
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional
from faker import Faker
from factory import Factory, Sequence, LazyAttribute, fuzzy

fake = Faker()


class VideoContentFactory(Factory):
    """Factory for generating video content test data"""
    
    id = Sequence(lambda n: f"video-{n:04d}")
    title = LazyAttribute(lambda obj: fake.sentence(nb_words=4)[:-1])
    file_path = LazyAttribute(lambda obj: f"/videos/{obj.id}.mp4")
    duration = fuzzy.FuzzyFloat(30.0, 1800.0)  # 30 seconds to 30 minutes
    transcript = LazyAttribute(lambda obj: fake.text(max_nb_chars=2000))
    summary = LazyAttribute(lambda obj: fake.paragraph(nb_sentences=3))
    complexity_level = fuzzy.FuzzyChoice(['beginner', 'intermediate', 'advanced'])
    created_at = fuzzy.FuzzyDateTime(
        start_dt=datetime.now() - timedelta(days=365),
        end_dt=datetime.now()
    )
    
    @LazyAttribute
    def topics(obj):
        topics = ['creatio', 'bpm', 'crm', 'development', 'javascript', 'c#', 'configuration']
        return random.sample(topics, k=random.randint(2, 5))
    
    @LazyAttribute
    def commands(obj):
        commands = [
            'CreateSection', 'AddField', 'ConfigureProcess', 'SetupIntegration',
            'CreateEntity', 'ModifySchema', 'AddBusinessRule', 'CreateLookup'
        ]
        return random.sample(commands, k=random.randint(1, 4))
    
    @LazyAttribute
    def api_references(obj):
        apis = [
            'EntitySchema', 'UserConnection', 'ProcessSchema', 'ServiceApi',
            'ConfigurationService', 'MessagePublisher', 'EntitySchemaManager'
        ]
        return random.sample(apis, k=random.randint(1, 3))
    
    @LazyAttribute
    def code_examples(obj):
        examples = []
        languages = ['javascript', 'csharp', 'sql']
        for lang in random.sample(languages, k=random.randint(1, 2)):
            if lang == 'javascript':
                code = "var schema = this.Ext.create('EntitySchema', { name: 'Contact' });"
            elif lang == 'csharp':
                code = "var entity = UserConnection.EntitySchemaManager.GetInstanceByName('Contact');"
            else:
                code = "SELECT Id, Name FROM Contact WHERE CreatedOn > @StartDate"
            
            examples.append({
                'language': lang,
                'code': code,
                'description': fake.sentence()
            })
        return examples


class PDFContentFactory(Factory):
    """Factory for generating PDF content test data"""
    
    id = Sequence(lambda n: f"pdf-{n:04d}")
    title = LazyAttribute(lambda obj: fake.sentence(nb_words=6)[:-1])
    file_path = LazyAttribute(lambda obj: f"/pdfs/{obj.id}.pdf")
    page_count = fuzzy.FuzzyInteger(5, 50)
    content = LazyAttribute(lambda obj: fake.text(max_nb_chars=5000))
    created_at = fuzzy.FuzzyDateTime(
        start_dt=datetime.now() - timedelta(days=365),
        end_dt=datetime.now()
    )
    
    @LazyAttribute
    def sections(obj):
        sections = []
        section_count = random.randint(3, 8)
        for i in range(section_count):
            sections.append({
                'title': fake.sentence(nb_words=4)[:-1],
                'content': fake.paragraph(nb_sentences=5),
                'page_number': random.randint(1, obj.page_count)
            })
        return sections
    
    @LazyAttribute
    def topics(obj):
        topics = ['creatio', 'documentation', 'api', 'configuration', 'development', 'architecture']
        return random.sample(topics, k=random.randint(2, 4))


class CommandFactory(Factory):
    """Factory for generating command test data"""
    
    id = Sequence(lambda n: n)
    command = LazyAttribute(lambda obj: fake.word().title() + random.choice(['Section', 'Field', 'Process', 'Rule']))
    description = LazyAttribute(lambda obj: fake.sentence())
    category = fuzzy.FuzzyChoice(['UI', 'Business Logic', 'Integration', 'Configuration', 'Data'])
    parameters = LazyAttribute(lambda obj: [fake.word() for _ in range(random.randint(0, 3))])


class TestDataGenerator:
    """Main test data generator class"""
    
    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path or tempfile.mktemp(suffix='.db')
        self.conn = None
    
    def setup_database(self):
        """Setup test database with schema"""
        self.conn = sqlite3.connect(self.db_path)
        cursor = self.conn.cursor()
        
        # Create videos table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS videos (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                file_path TEXT NOT NULL,
                duration REAL,
                transcript TEXT,
                summary TEXT,
                topics TEXT,
                complexity_level TEXT,
                commands TEXT,
                api_references TEXT,
                code_examples TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create pdfs table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS pdfs (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                file_path TEXT NOT NULL,
                page_count INTEGER,
                content TEXT,
                sections TEXT,
                topics TEXT,
                commands TEXT,
                api_references TEXT,
                code_examples TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create commands table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS commands (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                command TEXT NOT NULL,
                description TEXT,
                category TEXT,
                parameters TEXT
            )
        ''')
        
        self.conn.commit()
    
    def generate_videos(self, count: int = 50) -> List[Dict[str, Any]]:
        """Generate video test data"""
        videos = []
        for _ in range(count):
            video_data = VideoContentFactory()
            videos.append({
                'id': video_data.id,
                'title': video_data.title,
                'file_path': video_data.file_path,
                'duration': video_data.duration,
                'transcript': video_data.transcript,
                'summary': video_data.summary,
                'topics': json.dumps(video_data.topics),
                'complexity_level': video_data.complexity_level,
                'commands': json.dumps(video_data.commands),
                'api_references': json.dumps(video_data.api_references),
                'code_examples': json.dumps(video_data.code_examples),
                'created_at': video_data.created_at.isoformat()
            })
        return videos
    
    def generate_pdfs(self, count: int = 30) -> List[Dict[str, Any]]:
        """Generate PDF test data"""
        pdfs = []
        for _ in range(count):
            pdf_data = PDFContentFactory()
            pdfs.append({
                'id': pdf_data.id,
                'title': pdf_data.title,
                'file_path': pdf_data.file_path,
                'page_count': pdf_data.page_count,
                'content': pdf_data.content,
                'sections': json.dumps(pdf_data.sections),
                'topics': json.dumps(pdf_data.topics),
                'commands': json.dumps([]),
                'api_references': json.dumps([]),
                'code_examples': json.dumps([]),
                'created_at': pdf_data.created_at.isoformat()
            })
        return pdfs
    
    def generate_commands(self, count: int = 20) -> List[Dict[str, Any]]:
        """Generate command test data"""
        commands = []
        for _ in range(count):
            command_data = CommandFactory()
            commands.append({
                'command': command_data.command,
                'description': command_data.description,
                'category': command_data.category,
                'parameters': json.dumps(command_data.parameters)
            })
        return commands
    
    def populate_database(self, video_count: int = 50, pdf_count: int = 30, command_count: int = 20):
        """Populate database with test data"""
        if not self.conn:
            self.setup_database()
        
        cursor = self.conn.cursor()
        
        # Insert videos
        videos = self.generate_videos(video_count)
        for video in videos:
            cursor.execute('''
                INSERT INTO videos (id, title, file_path, duration, transcript, summary, 
                                  topics, complexity_level, commands, api_references, 
                                  code_examples, created_at)
                VALUES (:id, :title, :file_path, :duration, :transcript, :summary,
                       :topics, :complexity_level, :commands, :api_references,
                       :code_examples, :created_at)
            ''', video)
        
        # Insert PDFs
        pdfs = self.generate_pdfs(pdf_count)
        for pdf in pdfs:
            cursor.execute('''
                INSERT INTO pdfs (id, title, file_path, page_count, content, sections,
                                topics, commands, api_references, code_examples, created_at)
                VALUES (:id, :title, :file_path, :page_count, :content, :sections,
                       :topics, :commands, :api_references, :code_examples, :created_at)
            ''', pdf)
        
        # Insert commands
        commands = self.generate_commands(command_count)
        for command in commands:
            cursor.execute('''
                INSERT INTO commands (command, description, category, parameters)
                VALUES (:command, :description, :category, :parameters)
            ''', command)
        
        self.conn.commit()
    
    def export_to_json(self, output_path: str):
        """Export test data to JSON file"""
        if not self.conn:
            raise ValueError("Database not setup")
        
        cursor = self.conn.cursor()
        
        # Get all data
        cursor.execute('SELECT * FROM videos')
        videos = [dict(zip([col[0] for col in cursor.description], row)) for row in cursor.fetchall()]
        
        cursor.execute('SELECT * FROM pdfs')
        pdfs = [dict(zip([col[0] for col in cursor.description], row)) for row in cursor.fetchall()]
        
        cursor.execute('SELECT * FROM commands')
        commands = [dict(zip([col[0] for col in cursor.description], row)) for row in cursor.fetchall()]
        
        test_data = {
            'videos': videos,
            'pdfs': pdfs,
            'commands': commands,
            'metadata': {
                'generated_at': datetime.now().isoformat(),
                'video_count': len(videos),
                'pdf_count': len(pdfs),
                'command_count': len(commands)
            }
        }
        
        with open(output_path, 'w') as f:
            json.dump(test_data, f, indent=2, default=str)
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()


def main():
    """Generate test data"""
    generator = TestDataGenerator()
    generator.setup_database()
    generator.populate_database(video_count=100, pdf_count=50, command_count=30)
    
    # Export to JSON
    output_path = Path(__file__).parent / 'test_data.json'
    generator.export_to_json(str(output_path))
    
    print(f"Test data generated and saved to {output_path}")
    print(f"Database saved to {generator.db_path}")
    
    generator.close()


if __name__ == '__main__':
    main()
