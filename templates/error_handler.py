"""
Error Handling Template for Web Scraping
This module provides comprehensive error handling strategies for robust web scraping.
"""

import logging
import traceback
import time
from functools import wraps
from typing import Optional, Callable, Any
import requests
from selenium.common.exceptions import (
    WebDriverException, TimeoutException, NoSuchElementException,
    StaleElementReferenceException, ElementNotInteractableException
)


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('../logs/scraper.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class ScraperError(Exception):
    """Base exception for scraper errors"""
    pass


class RateLimitError(ScraperError):
    """Raised when rate limit is exceeded"""
    pass


class DataValidationError(ScraperError):
    """Raised when scraped data fails validation"""
    pass


def retry_on_exception(
    max_retries: int = 3,
    delay: float = 1.0,
    backoff: float = 2.0,
    exceptions: tuple = (Exception,),
    log_errors: bool = True
):
    """
    Decorator that retries a function on specified exceptions.
    
    Args:
        max_retries: Maximum number of retry attempts
        delay: Initial delay between retries in seconds
        backoff: Multiplier for delay after each retry
        exceptions: Tuple of exceptions to catch and retry on
        log_errors: Whether to log errors
    
    Usage:
        @retry_on_exception(max_retries=3, delay=2)
        def scrape_page(url):
            # Your scraping code here
            pass
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            current_delay = delay
            last_exception = None
            
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt < max_retries:
                        if log_errors:
                            logger.warning(
                                f"Attempt {attempt + 1}/{max_retries + 1} failed for {func.__name__}: {str(e)}"
                            )
                        time.sleep(current_delay)
                        current_delay *= backoff
                    else:
                        if log_errors:
                            logger.error(
                                f"All {max_retries + 1} attempts failed for {func.__name__}: {str(e)}"
                            )
            
            raise last_exception
        
        return wrapper
    return decorator


class ErrorHandler:
    """
    Comprehensive error handler for web scraping operations.
    """
    
    def __init__(self, log_to_file: bool = True):
        """
        Initialize the error handler.
        
        Args:
            log_to_file: Whether to log errors to file
        """
        self.log_to_file = log_to_file
        self.error_count = {}
    
    def handle_request_error(self, error: requests.RequestException, url: str) -> Optional[str]:
        """
        Handle various request errors.
        
        Args:
            error: The request exception
            url: The URL that caused the error
        
        Returns:
            Action to take ('retry', 'skip', 'abort')
        """
        error_type = type(error).__name__
        self.error_count[error_type] = self.error_count.get(error_type, 0) + 1
        
        if isinstance(error, requests.HTTPError):
            status_code = error.response.status_code if error.response else None
            
            if status_code == 429:  # Too Many Requests
                logger.warning(f"Rate limit hit for {url}. Waiting...")
                return 'retry'
            elif status_code == 404:  # Not Found
                logger.warning(f"Page not found: {url}")
                return 'skip'
            elif status_code >= 500:  # Server Error
                logger.error(f"Server error {status_code} for {url}")
                return 'retry'
            elif status_code == 403:  # Forbidden
                logger.error(f"Access forbidden for {url}. Check if you need authentication.")
                return 'abort'
        
        elif isinstance(error, requests.Timeout):
            logger.warning(f"Timeout occurred for {url}")
            return 'retry'
        
        elif isinstance(error, requests.ConnectionError):
            logger.error(f"Connection error for {url}")
            return 'retry'
        
        else:
            logger.error(f"Unexpected error for {url}: {str(error)}")
            logger.debug(traceback.format_exc())
            return 'skip'
    
    def handle_selenium_error(self, error: WebDriverException, element_desc: str = "") -> Optional[str]:
        """
        Handle Selenium-specific errors.
        
        Args:
            error: The Selenium exception
            element_desc: Description of the element being accessed
        
        Returns:
            Action to take ('retry', 'skip', 'abort')
        """
        error_type = type(error).__name__
        self.error_count[error_type] = self.error_count.get(error_type, 0) + 1
        
        if isinstance(error, TimeoutException):
            logger.warning(f"Timeout waiting for element: {element_desc}")
            return 'retry'
        
        elif isinstance(error, NoSuchElementException):
            logger.warning(f"Element not found: {element_desc}")
            return 'skip'
        
        elif isinstance(error, StaleElementReferenceException):
            logger.warning(f"Stale element reference: {element_desc}")
            return 'retry'
        
        elif isinstance(error, ElementNotInteractableException):
            logger.warning(f"Element not interactable: {element_desc}")
            return 'skip'
        
        else:
            logger.error(f"Selenium error: {str(error)}")
            logger.debug(traceback.format_exc())
            return 'skip'
    
    def log_summary(self):
        """Log a summary of all errors encountered."""
        if self.error_count:
            logger.info("Error Summary:")
            for error_type, count in self.error_count.items():
                logger.info(f"  {error_type}: {count} occurrences")
        else:
            logger.info("No errors encountered.")


def safe_get(dictionary: dict, keys: list, default=None):
    """
    Safely get nested dictionary values.
    
    Args:
        dictionary: The dictionary to search
        keys: List of keys representing the path
        default: Default value if key not found
    
    Returns:
        The value at the specified path or default
    
    Usage:
        data = {'user': {'profile': {'name': 'John'}}}
        name = safe_get(data, ['user', 'profile', 'name'], 'Unknown')
    """
    try:
        value = dictionary
        for key in keys:
            value = value[key]
        return value
    except (KeyError, TypeError, AttributeError):
        return default


def validate_scraped_data(data: dict, required_fields: list) -> bool:
    """
    Validate that scraped data contains required fields.
    
    Args:
        data: The scraped data dictionary
        required_fields: List of required field names
    
    Returns:
        True if all required fields are present and non-empty
    
    Raises:
        DataValidationError: If validation fails
    """
    missing_fields = []
    empty_fields = []
    
    for field in required_fields:
        if field not in data:
            missing_fields.append(field)
        elif not data[field]:
            empty_fields.append(field)
    
    if missing_fields:
        raise DataValidationError(f"Missing required fields: {', '.join(missing_fields)}")
    
    if empty_fields:
        raise DataValidationError(f"Empty required fields: {', '.join(empty_fields)}")
    
    return True


# Example usage
if __name__ == "__main__":
    # Example 1: Using retry decorator
    @retry_on_exception(max_retries=3, delay=1, exceptions=(requests.RequestException,))
    def fetch_page(url):
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text
    
    # Example 2: Using error handler
    error_handler = ErrorHandler()
    
    try:
        response = requests.get("http://example.com/nonexistent", timeout=5)
        response.raise_for_status()
    except requests.RequestException as e:
        action = error_handler.handle_request_error(e, "http://example.com/nonexistent")
        print(f"Suggested action: {action}")
    
    # Example 3: Data validation
    scraped_data = {
        'title': 'Example Product',
        'price': '$29.99',
        'description': ''
    }
    
    try:
        validate_scraped_data(scraped_data, ['title', 'price', 'description'])
    except DataValidationError as e:
        print(f"Validation error: {e}")
