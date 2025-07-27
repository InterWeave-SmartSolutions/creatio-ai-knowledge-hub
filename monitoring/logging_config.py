#!/usr/bin/env python3
"""
Centralized Logging Configuration
Provides structured logging with multiple outputs and log aggregation
"""

import os
import sys
import json
import logging
import logging.handlers
from datetime import datetime
from typing import Dict, Any, Optional
from pathlib import Path
from pythonjsonlogger import jsonlogger

class StructuredLogger:
    """Structured logging with JSON output and contextual information"""
    
    def __init__(self, name: str = "creatio-ai-knowledge-hub"):
        self.name = name
        self.setup_logging()
    
    def setup_logging(self):
        """Configure logging with multiple handlers and formats"""
        
        # Create logs directory
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        # Root logger configuration
        root_logger = logging.getLogger()
        root_logger.setLevel(logging.INFO)
        
        # Clear existing handlers
        root_logger.handlers.clear()
        
        # Console handler with color formatting
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_formatter = ColoredFormatter(
            '%(levelname)s:     %(asctime)s - %(name)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        console_handler.setFormatter(console_formatter)
        root_logger.addHandler(console_handler)
        
        # JSON file handler for structured logging
        json_handler = logging.handlers.RotatingFileHandler(
            log_dir / "application.json",
            maxBytes=50*1024*1024,  # 50MB
            backupCount=10
        )
        json_handler.setLevel(logging.DEBUG)
        json_formatter = jsonlogger.JsonFormatter(
            '%(asctime)s %(name)s %(levelname)s %(module)s %(funcName)s %(lineno)d %(message)s',
            datefmt='%Y-%m-%dT%H:%M:%S'
        )
        json_handler.setFormatter(json_formatter)
        root_logger.addHandler(json_handler)
        
        # Error file handler
        error_handler = logging.handlers.RotatingFileHandler(
            log_dir / "errors.log",
            maxBytes=25*1024*1024,  # 25MB
            backupCount=5
        )
        error_handler.setLevel(logging.ERROR)
        error_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s\n'
            'Location: %(pathname)s:%(lineno)d in %(funcName)s\n'
            '---',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        error_handler.setFormatter(error_formatter)
        root_logger.addHandler(error_handler)
        
        # Performance log handler
        perf_handler = logging.handlers.RotatingFileHandler(
            log_dir / "performance.log",
            maxBytes=25*1024*1024,
            backupCount=5
        )
        perf_handler.setLevel(logging.INFO)
        perf_formatter = logging.Formatter(
            '%(asctime)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        perf_handler.setFormatter(perf_formatter)
        
        # Create performance logger
        perf_logger = logging.getLogger('performance')
        perf_logger.setLevel(logging.INFO)
        perf_logger.addHandler(perf_handler)
        perf_logger.propagate = False
        
        # Access log handler for API requests
        access_handler = logging.handlers.RotatingFileHandler(
            log_dir / "access.log",
            maxBytes=50*1024*1024,
            backupCount=10
        )
        access_handler.setLevel(logging.INFO)
        access_formatter = logging.Formatter(
            '%(asctime)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        access_handler.setFormatter(access_formatter)
        
        # Create access logger
        access_logger = logging.getLogger('access')
        access_logger.setLevel(logging.INFO)
        access_logger.addHandler(access_handler)
        access_logger.propagate = False
        
        # Security log handler
        security_handler = logging.handlers.RotatingFileHandler(
            log_dir / "security.log",
            maxBytes=25*1024*1024,
            backupCount=10
        )
        security_handler.setLevel(logging.WARNING)
        security_formatter = logging.Formatter(
            '%(asctime)s - SECURITY - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        security_handler.setFormatter(security_formatter)
        
        # Create security logger
        security_logger = logging.getLogger('security')
        security_logger.setLevel(logging.WARNING)
        security_logger.addHandler(security_handler)
        security_logger.propagate = False
    
    def get_logger(self, name: str) -> logging.Logger:
        """Get a logger instance with the specified name"""
        return logging.getLogger(name)
    
    def log_request(self, request_data: Dict[str, Any]):
        """Log API request with structured data"""
        access_logger = logging.getLogger('access')
        log_entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'type': 'request',
            **request_data
        }
        access_logger.info(json.dumps(log_entry))
    
    def log_performance(self, operation: str, duration: float, **kwargs):
        """Log performance metrics"""
        perf_logger = logging.getLogger('performance')
        log_entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'operation': operation,
            'duration_seconds': duration,
            **kwargs
        }
        perf_logger.info(json.dumps(log_entry))
    
    def log_security_event(self, event_type: str, details: Dict[str, Any]):
        """Log security-related events"""
        security_logger = logging.getLogger('security')
        log_entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'event_type': event_type,
            'details': details
        }
        security_logger.warning(json.dumps(log_entry))

class ColoredFormatter(logging.Formatter):
    """Custom formatter with colors for console output"""
    
    COLORS = {
        'DEBUG': '\033[36m',    # Cyan
        'INFO': '\033[32m',     # Green
        'WARNING': '\033[33m',  # Yellow
        'ERROR': '\033[31m',    # Red
        'CRITICAL': '\033[35m', # Magenta
        'RESET': '\033[0m'      # Reset
    }
    
    def format(self, record):
        log_message = super().format(record)
        return f"{self.COLORS.get(record.levelname, '')}{log_message}{self.COLORS['RESET']}"

class LogAggregator:
    """Log aggregation and analysis utilities"""
    
    def __init__(self, log_dir: str = "logs"):
        self.log_dir = Path(log_dir)
    
    def get_recent_errors(self, hours: int = 24) -> list:
        """Get recent error logs"""
        error_file = self.log_dir / "errors.log"
        if not error_file.exists():
            return []
        
        cutoff_time = datetime.utcnow().timestamp() - (hours * 3600)
        errors = []
        
        try:
            with open(error_file, 'r') as f:
                for line in f.readlines()[-1000:]:  # Last 1000 lines
                    if line.strip():
                        errors.append(line.strip())
        except Exception as e:
            logging.error(f"Error reading error log: {e}")
        
        return errors[-50:]  # Return last 50 errors
    
    def get_performance_summary(self, hours: int = 24) -> Dict[str, Any]:
        """Get performance metrics summary"""
        perf_file = self.log_dir / "performance.log"
        if not perf_file.exists():
            return {}
        
        summary = {
            'total_operations': 0,
            'avg_duration': 0,
            'slow_operations': [],
            'operations_by_type': {}
        }
        
        try:
            durations = []
            with open(perf_file, 'r') as f:
                for line in f.readlines()[-1000:]:
                    try:
                        if ' - {' in line:
                            json_part = line.split(' - ', 1)[1]
                            data = json.loads(json_part)
                            duration = data.get('duration_seconds', 0)
                            operation = data.get('operation', 'unknown')
                            
                            durations.append(duration)
                            summary['total_operations'] += 1
                            
                            if operation not in summary['operations_by_type']:
                                summary['operations_by_type'][operation] = {
                                    'count': 0,
                                    'total_duration': 0
                                }
                            
                            summary['operations_by_type'][operation]['count'] += 1
                            summary['operations_by_type'][operation]['total_duration'] += duration
                            
                            if duration > 1.0:  # Slow operations > 1 second
                                summary['slow_operations'].append({
                                    'operation': operation,
                                    'duration': duration,
                                    'timestamp': data.get('timestamp', '')
                                })
                    
                    except (json.JSONDecodeError, KeyError):
                        continue
            
            if durations:
                summary['avg_duration'] = sum(durations) / len(durations)
            
            # Calculate averages for each operation type
            for op_type, data in summary['operations_by_type'].items():
                if data['count'] > 0:
                    data['avg_duration'] = data['total_duration'] / data['count']
        
        except Exception as e:
            logging.error(f"Error analyzing performance log: {e}")
        
        return summary
    
    def get_log_stats(self) -> Dict[str, Any]:
        """Get general log file statistics"""
        stats = {}
        
        for log_file in self.log_dir.glob("*.log"):
            try:
                file_stats = log_file.stat()
                stats[log_file.name] = {
                    'size_mb': round(file_stats.st_size / (1024 * 1024), 2),
                    'last_modified': datetime.fromtimestamp(file_stats.st_mtime).isoformat()
                }
            except Exception as e:
                stats[log_file.name] = {'error': str(e)}
        
        return stats

# Global logger instance
structured_logger = StructuredLogger()
log_aggregator = LogAggregator()

# Convenience functions
def get_logger(name: str) -> logging.Logger:
    """Get a configured logger instance"""
    return structured_logger.get_logger(name)

def log_request(request_data: Dict[str, Any]):
    """Log API request"""
    structured_logger.log_request(request_data)

def log_performance(operation: str, duration: float, **kwargs):
    """Log performance metrics"""
    structured_logger.log_performance(operation, duration, **kwargs)

def log_security_event(event_type: str, details: Dict[str, Any]):
    """Log security event"""
    structured_logger.log_security_event(event_type, details)
