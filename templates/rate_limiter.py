"""
Rate Limiting Template for Web Scraping
This module provides various rate limiting strategies to respect website policies
and avoid being blocked.
"""

import time
import random
from functools import wraps
from datetime import datetime, timedelta
from collections import deque


class RateLimiter:
    """
    A flexible rate limiter that can be used to control request frequency.
    """
    
    def __init__(self, max_requests=10, time_window=60):
        """
        Initialize the rate limiter.
        
        Args:
            max_requests (int): Maximum number of requests allowed
            time_window (int): Time window in seconds
        """
        self.max_requests = max_requests
        self.time_window = time_window
        self.requests = deque()
    
    def wait_if_needed(self):
        """
        Check if we need to wait before making the next request.
        """
        now = datetime.now()
        
        # Remove old requests outside the time window
        while self.requests and (now - self.requests[0]) > timedelta(seconds=self.time_window):
            self.requests.popleft()
        
        # If we've hit the limit, wait
        if len(self.requests) >= self.max_requests:
            sleep_time = (self.requests[0] + timedelta(seconds=self.time_window) - now).total_seconds()
            if sleep_time > 0:
                print(f"Rate limit reached. Sleeping for {sleep_time:.2f} seconds...")
                time.sleep(sleep_time)
        
        # Record this request
        self.requests.append(now)


def random_delay(min_seconds=1, max_seconds=3):
    """
    Add a random delay between requests to appear more human-like.
    
    Args:
        min_seconds (float): Minimum delay in seconds
        max_seconds (float): Maximum delay in seconds
    """
    delay = random.uniform(min_seconds, max_seconds)
    time.sleep(delay)


def exponential_backoff(attempt, base_delay=1, max_delay=60):
    """
    Calculate exponential backoff delay.
    
    Args:
        attempt (int): Current attempt number (starting from 1)
        base_delay (float): Base delay in seconds
        max_delay (float): Maximum delay in seconds
    
    Returns:
        float: Delay in seconds
    """
    delay = min(base_delay * (2 ** (attempt - 1)), max_delay)
    # Add some randomness to avoid thundering herd
    delay = delay * (0.5 + random.random())
    return delay


def rate_limit_decorator(calls_per_minute=30):
    """
    Decorator to rate limit function calls.
    
    Args:
        calls_per_minute (int): Maximum calls per minute
    
    Usage:
        @rate_limit_decorator(calls_per_minute=20)
        def scrape_page(url):
            # Your scraping code here
            pass
    """
    min_interval = 60.0 / calls_per_minute
    
    def decorator(func):
        last_called = [0.0]
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            elapsed = time.time() - last_called[0]
            left_to_wait = min_interval - elapsed
            if left_to_wait > 0:
                time.sleep(left_to_wait)
            ret = func(*args, **kwargs)
            last_called[0] = time.time()
            return ret
        
        return wrapper
    
    return decorator


# Example usage
if __name__ == "__main__":
    # Example 1: Using RateLimiter class
    rate_limiter = RateLimiter(max_requests=5, time_window=10)
    
    for i in range(10):
        rate_limiter.wait_if_needed()
        print(f"Request {i+1} sent at {datetime.now()}")
    
    # Example 2: Using decorator
    @rate_limit_decorator(calls_per_minute=6)
    def make_request(url):
        print(f"Requesting {url} at {datetime.now()}")
        return f"Response from {url}"
    
    # This will be rate limited to 6 calls per minute
    for i in range(3):
        make_request(f"http://example.com/page{i}")
