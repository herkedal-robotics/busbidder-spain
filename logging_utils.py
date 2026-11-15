import logging
from functools import wraps

# WHAT DOES log_call DO:
# logging.basicConfig() configures logging to the file busbidder.log.
# @wraps(function) preserves the original function's name and metadata.
# *args and **kwargs allow the decorator to work with functions that accept different arguments.
# logging.info() records when a function starts and finishes.
# logging.exception() records an unexpected exception, including its traceback.
# raise passes the exception back to the original error-handling code

logging.basicConfig(
    filename="busbidder.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s")

def log_call(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        logging.info(f"Calling {function.__name__}")
        try:
            result = function(*args, **kwargs)
            logging.info(f"Finished {function.__name__}")
            return result
        except Exception:
            logging.exception(f"Error in {function.__name__}")
            raise
    return wrapper