import os
from elasticsearch import Elasticsearch
from whoosh.index import create_in
from whoosh.fields import Schema, TEXT, ID
from whoosh.analysis import StemmingAnalyzer

class SearchEngineCore:
    def __init__(self, es_host='localhost', es_port=9200, index_dir='indexdir'):
        self.es = Elasticsearch([{'host': es_host, 'port': es_port}])
        self.index_dir = index_dir
        self.schema = Schema(title=TEXT(stored=True, analyzer=StemmingAnalyzer()), 
                             path=ID(stored=True), 
                             content=TEXT(analyzer=StemmingAnalyzer(), stored=True))
        
        if not os.path.exists(index_dir):
            os.mkdir(index_dir)
            
        self.ix = create_in(index_dir, self.schema)

    def create_es_index(self, index_name='creatio_index'):
        if not self.es.indices.exists(index=index_name):
            self.es.indices.create(index=index_name)

    def delete_es_index(self, index_name='creatio_index'):
        if self.es.indices.exists(index=index_name):
            self.es.indices.delete(index=index_name)

    def init_full_text_index(self):
        # Whoosh: Initialize index for full-text search
        if not os.path.exists(self.index_dir):
            os.mkdir(self.index_dir)
            create_in(self.index_dir, self.schema)
