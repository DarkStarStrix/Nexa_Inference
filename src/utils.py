import logging


def setup_logger(name, log_file, level=logging.INFO):
    """Function to set up a logger with a specific name and log file."""
    formatter = logging.Formatter ('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    handler = logging.FileHandler (log_file)
    handler.setFormatter (formatter)

    logger = logging.getLogger (name)
    logger.setLevel (level)
    logger.addHandler (handler)

    return logger

# Example usage:
# logger = setup_logger('lambda_zero', 'lambda_zero.log')
# logger.info('This is an info message')
# logger.error('This is an error message')
