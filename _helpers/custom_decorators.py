import time
from functools import wraps

from flask import current_app


def time_it(func):
    """Wraps a function and then gives the time taken to execute the function."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()  # Record the start time
        result = func(*args, **kwargs)  # Execute the method
        end_time = time.time()  # Record the end time
        duration = end_time - start_time  # Calculate the duration
        current_app.logger.info(f"Time taken to execute {func.__name__}: {duration:.6f} seconds")
        return result

    return wrapper
