"""
Performance tests for Creatio AI Knowledge Hub using Locust
"""
import random
from locust import HttpUser, task, between


class KnowledgeHubUser(HttpUser):
    """Simulate user behavior for performance testing"""
    
    wait_time = between(1, 3)  # Wait 1-3 seconds between requests
    
    def on_start(self):
        """Called when a user starts"""
        self.search_queries = [
            "creatio development",
            "entity schema",
            "process design",
            "configuration",
            "API reference",
            "business process",
            "user interface",
            "data model",
            "integration",
            "customization"
        ]
        
        self.command_categories = [
            "Development",
            "Configuration", 
            "Integration",
            "UI",
            "Data"
        ]
    
    @task(3)
    def search_content(self):
        """Test content search endpoint (most common operation)"""
        query = random.choice(self.search_queries)
        content_type = random.choice(["all", "video", "pdf"])
        limit = random.randint(5, 20)
        
        self.client.get(
            "/api/v1/search",
            params={
                "query": query,
                "content_type": content_type,
                "limit": limit
            },
            name="search_content"
        )
    
    @task(2)
    def get_commands(self):
        """Test commands endpoint"""
        # Sometimes filter by category, sometimes not
        if random.random() < 0.5:
            category = random.choice(self.command_categories)
            params = {"category": category}
            name = "get_commands_filtered"
        else:
            params = {}
            name = "get_commands_all"
        
        self.client.get("/api/v1/commands", params=params, name=name)
    
    @task(1)
    def search_commands(self):
        """Test command search with search term"""
        search_terms = ["Create", "Modify", "Get", "Set", "Add", "Delete"]
        search_term = random.choice(search_terms)
        
        self.client.get(
            "/api/v1/commands",
            params={"search_term": search_term},
            name="search_commands"
        )
    
    @task(1)
    def complex_search(self):
        """Test complex search scenarios"""
        query = random.choice(self.search_queries)
        
        # Simulate pagination-like behavior
        for limit in [5, 10, 15]:
            self.client.get(
                "/api/v1/search",
                params={
                    "query": query,
                    "content_type": "all",
                    "limit": limit
                },
                name="complex_search"
            )


class AdminUser(HttpUser):
    """Simulate admin user with heavier operations"""
    
    wait_time = between(2, 5)
    weight = 1  # Lower weight = fewer admin users
    
    @task
    def bulk_search_operations(self):
        """Simulate bulk operations that admins might perform"""
        queries = ["comprehensive review", "advanced configuration", "system integration"]
        
        for query in queries:
            self.client.get(
                "/api/v1/search",
                params={
                    "query": query,
                    "content_type": "all",
                    "limit": 50
                },
                name="admin_bulk_search"
            )
    
    @task
    def comprehensive_command_review(self):
        """Simulate reviewing all commands"""
        categories = ["Development", "Configuration", "Integration", "UI", "Data"]
        
        for category in categories:
            self.client.get(
                "/api/v1/commands",
                params={"category": category},
                name="admin_command_review"
            )


class APIOnlyUser(HttpUser):
    """User that only makes API calls (no web interface)"""
    
    wait_time = between(0.5, 2)
    weight = 2
    
    @task(5)
    def rapid_searches(self):
        """Simulate rapid API searches"""
        queries = ["quick", "fast", "instant", "immediate"]
        query = random.choice(queries)
        
        self.client.get(
            "/api/v1/search",
            params={"query": query, "limit": 5},
            name="rapid_search"
        )
    
    @task(2)
    def api_commands(self):
        """API-focused command requests"""
        self.client.get("/api/v1/commands", name="api_commands")


# Stress test user for extreme load testing
class StressTestUser(HttpUser):
    """High-frequency user for stress testing"""
    
    wait_time = between(0.1, 0.5)
    weight = 1
    
    @task
    def stress_search(self):
        """High-frequency search requests"""
        query = "stress test query"
        self.client.get(
            "/api/v1/search",
            params={"query": query, "limit": 1},
            name="stress_search"
        )
    
    @task
    def stress_commands(self):
        """High-frequency command requests"""
        self.client.get("/api/v1/commands", name="stress_commands")
