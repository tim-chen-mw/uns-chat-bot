import logging

# Create a new logger instance
logger = logging.getLogger(__name__)

# Configure logging
logger.setLevel(logging.DEBUG)

# Create a console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

# Create a formatter and set it for the handlers
formatter = logging.Formatter(
    '{"timestamp": "%(asctime)s", "level": "%(levelname)s", "message": "%(message)s"}', "%Y-%m-%d %H:%M:%S")
console_handler.setFormatter(formatter)

# Add the handlers to the logger
logger.addHandler(console_handler)
