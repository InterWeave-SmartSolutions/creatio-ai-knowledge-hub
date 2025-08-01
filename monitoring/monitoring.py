#!/usr/bin/env python3
"""
Application Performance Monitoring
Provides metrics collection, health checks, and performance monitoring
"""

import time
import psutil
import sqlite3
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
from prometheus_client import Counter, Histogram, Gauge, generate_latest
from fastapi import Request, Response
from contextlib import asynccontextmanager
import logging
import json

# Prometheus metrics
REQUEST_COUNT = Counter(
    'app_requests_total',
    'Total number of requests',
    ['method', 'endpoint', 'status_code']
)

REQUEST_DURATION = Histogram(
    'app_request_duration_seconds',
    'Request duration in seconds',
    ['method', 'endpoint']
)

ACTIVE_CONNECTIONS = Gauge(
    'app_active_connections',
    'Number of active connections'
)

DATABASE_QUERY_DURATION = Histogram(
    'database_query_duration_seconds',
    'Database query duration in seconds',
    ['query_type']
)

DATABASE_CONNECTIONS = Gauge(
    'database_connections_active',
    'Active database connections'
)

SEARCH_QUERY_COUNT = Counter(
    'search_queries_total',
    'Total number of search queries',
    ['content_type']
)

SEARCH_QUERY_DURATION = Histogram(
    'search_query_duration_seconds',
    'Search query duration in seconds',
    ['content_type']
)

# System metrics
CPU_USAGE = Gauge('system_cpu_usage_percent', 'CPU usage percentage')
MEMORY_USAGE = Gauge('system_memory_usage_bytes', 'Memory usage in bytes')
DISK_USAGE = Gauge('system_disk_usage_bytes', 'Disk usage in bytes')

class PerformanceMonitor:
    """Application performance monitoring and metrics collection"""
    
    def __init__(self, db_path: str = "ai_knowledge_hub/knowledge_hub.db"):
        self.db_path = db_path
        self.logger = logging.getLogger(__name__)
        self._start_system_monitoring()
    
    def _start_system_monitoring(self):
        """Start collecting system metrics"""
        def update_system_metrics():
            try:
                # CPU usage
                cpu_percent = psutil.cpu_percent(interval=1)
                CPU_USAGE.set(cpu_percent)
                
                # Memory usage
                memory = psutil.virtual_memory()
                MEMORY_USAGE.set(memory.used)
                
                # Disk usage
                disk = psutil.disk_usage('/')
                DISK_USAGE.set(disk.used)
                
            except Exception as e:
                self.logger.error(f"Error updating system metrics: {e}")
        
        # Update metrics every 30 seconds
        import threading
        def metrics_updater():
            while True:
                update_system_metrics()
                time.sleep(30)
        
        thread = threading.Thread(target=metrics_updater, daemon=True)
        thread.start()
    
    @asynccontextmanager
    async def monitor_request(self, request: Request):
        """Context manager to monitor request performance"""
        start_time = time.time()
        method = request.method
        endpoint = str(request.url.path)
        
        ACTIVE_CONNECTIONS.inc()
        
        try:
            yield
            status_code = "200"  # Default success
        except Exception as e:
            status_code = "500"
            self.logger.error(f"Request error: {e}")
            raise
        finally:
            duration = time.time() - start_time
            REQUEST_DURATION.labels(method=method, endpoint=endpoint).observe(duration)
            REQUEST_COUNT.labels(method=method, endpoint=endpoint, status_code=status_code).inc()
            ACTIVE_CONNECTIONS.dec()
    
    def monitor_database_query(self, query_type: str):
        """Decorator to monitor database query performance"""
        def decorator(func):
            async def wrapper(*args, **kwargs):
                start_time = time.time()
                DATABASE_CONNECTIONS.inc()
                
                try:
                    result = await func(*args, **kwargs) if asyncio.iscoroutinefunction(func) else func(*args, **kwargs)
                    return result
                finally:
                    duration = time.time() - start_time
                    DATABASE_QUERY_DURATION.labels(query_type=query_type).observe(duration)
                    DATABASE_CONNECTIONS.dec()
            
            return wrapper
        return decorator
    
    def monitor_search_query(self, content_type: str):
        """Monitor search query performance"""
        def decorator(func):
            async def wrapper(*args, **kwargs):
                start_time = time.time()
                SEARCH_QUERY_COUNT.labels(content_type=content_type).inc()
                
                try:
                    result = await func(*args, **kwargs) if asyncio.iscoroutinefunction(func) else func(*args, **kwargs)
                    return result
                finally:
                    duration = time.time() - start_time
                    SEARCH_QUERY_DURATION.labels(content_type=content_type).observe(duration)
            
            return wrapper
        return decorator
    
    def get_health_status(self) -> Dict[str, Any]:
        """Get comprehensive health status"""
        health_data = {
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "checks": {}
        }
        
        try:
            # Database health check
            conn = sqlite3.connect(self.db_path, timeout=5)
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            conn.close()
            health_data["checks"]["database"] = {"status": "healthy", "response_time_ms": 0}
        except Exception as e:
            health_data["checks"]["database"] = {"status": "unhealthy", "error": str(e)}
            health_data["status"] = "unhealthy"
        
        # System resource checks
        try:
            cpu_percent = psutil.cpu_percent()
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            health_data["checks"]["system"] = {
                "status": "healthy" if cpu_percent < 90 and memory.percent < 90 and disk.percent < 90 else "degraded",
                "cpu_percent": cpu_percent,
                "memory_percent": memory.percent,
                "disk_percent": disk.percent
            }
            
            if health_data["checks"]["system"]["status"] == "degraded":
                health_data["status"] = "degraded"
                
        except Exception as e:
            health_data["checks"]["system"] = {"status": "unhealthy", "error": str(e)}
            health_data["status"] = "unhealthy"
        
        # Search index health check
        try:
            from pathlib import Path
            search_index_path = Path("ai_knowledge_hub/search_index")
            if search_index_path.exists():
                health_data["checks"]["search_index"] = {"status": "healthy"}
            else:
                health_data["checks"]["search_index"] = {"status": "degraded", "error": "Search index not found"}
                health_data["status"] = "degraded"
        except Exception as e:
            health_data["checks"]["search_index"] = {"status": "unhealthy", "error": str(e)}
            health_data["status"] = "unhealthy"
        
        return health_data
    
    def get_metrics_summary(self) -> Dict[str, Any]:
        """Get metrics summary for dashboard"""
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "system": {
                "cpu_usage": psutil.cpu_percent(),
                "memory_usage": psutil.virtual_memory().percent,
                "disk_usage": psutil.disk_usage('/').percent
            },
            "application": {
                "active_connections": ACTIVE_CONNECTIONS._value._value,
                "total_requests": sum([counter._value._value for counter in REQUEST_COUNT._metrics.values()]),
                "database_connections": DATABASE_CONNECTIONS._value._value
            }
        }

# Global monitor instance
monitor = PerformanceMonitor()

import asyncio
