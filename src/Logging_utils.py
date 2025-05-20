import logging
import functools
import time
from typing import Any, Callable
import json
from datetime import datetime
import os

# Create logs directory if it doesn't exist
os.makedirs('logs', exist_ok=True)

# Configure logging
def setup_logger(name: str) -> logging.Logger:
    """Set up a logger with both file and console handlers."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Prevent adding handlers multiple times
    if not logger.handlers:
        # File handler with detailed formatting
        file_handler = logging.FileHandler(
            f'logs/{name}_{datetime.now().strftime("%Y%m%d")}.log'
        )
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

        # Console handler with simpler formatting
        console_handler = logging.StreamHandler()
        console_formatter = logging.Formatter(
            '%(levelname)s: %(message)s'
        )
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)

    return logger

def get_logger(name: str) -> logging.Logger:
    """Get a logger instance."""
    return setup_logger(name)

def log_model_inference(model_name: str) -> Callable:
    """Decorator to log model inference details."""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            logger = get_logger(f"model.{model_name}")

            start_time = time.time()
            try:
                # Log input parameters (excluding self)
                input_params = {
                    **kwargs,
                    **{f"arg_{i}": arg for i, arg in enumerate(args[1:]) if not isinstance(arg, bytes)}
                }
                logger.info(f"Starting inference with parameters: {json.dumps(input_params)}")

                # Execute the function
                result = func(*args, **kwargs)

                # Calculate execution time
                execution_time = time.time() - start_time

                # Log success
                logger.info(
                    f"Inference completed successfully in {execution_time:.2f}s"
                )

                return result

            except Exception as e:
                # Log failure
                logger.error(
                    f"Inference failed after {time.time() - start_time:.2f}s: {str(e)}",
                    exc_info=True
                )
                raise

        return wrapper
    return decorator

def log_api_call(func: Callable) -> Callable:
    """Decorator to log API calls."""
    @functools.wraps(func)
    async def wrapper(*args: Any, **kwargs: Any) -> Any:
        logger = get_logger("api")

        start_time = time.time()
        try:
            # Log request
            logger.info(f"API call to {func.__name__} started")

            # Execute the function
            result = await func(*args, **kwargs)

            # Calculate execution time
            execution_time = time.time() - start_time

            # Log success
            logger.info(
                f"API call to {func.__name__} completed successfully in {execution_time:.2f}s"
            )

            return result

        except Exception as e:
            # Log failure
            logger.error(
                f"API call to {func.__name__} failed after {time.time() - start_time:.2f}s: {str(e)}",
                exc_info=True
            )
            raise

    return wrapper

# Error logging utility
def log_error(logger: logging.Logger, error: Exception, context: dict = None) -> None:
    """Utility function to log errors with context."""
    error_details = {
        'error_type': type(error).__name__,
        'error_message': str(error),
        'timestamp': datetime.now().isoformat()
    }

    if context:
        error_details['context'] = context

    logger.error(
        f"Error occurred: {json.dumps(error_details, indent=2)}",
        exc_info=True
    )
