import logging

def setup_logging():
    """Set up logging for the application."""
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    return logger
