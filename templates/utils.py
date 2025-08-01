import time
import random

# Rate limiting function

def rate_limiter(min_wait=1, max_wait=3):
    time_to_wait = random.uniform(min_wait, max_wait)
    time.sleep(time_to_wait)

# Error handling function

def handle_error(e):
    print(f"An error occurred: {e}")

