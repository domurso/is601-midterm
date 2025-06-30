import logging
import os
from logging.handlers import TimedRotatingFileHandler
from dotenv import load_dotenv
from datetime import datetime

# Set up a fallback console logger for errors during initialization
fallback_logger = logging.getLogger('fallback')
fallback_logger.setLevel(logging.ERROR)
if not any(isinstance(h, logging.StreamHandler) for h in fallback_logger.handlers):
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.ERROR)
    console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s'))
    fallback_logger.addHandler(console_handler)

# Load environment variables from .env file in the parent directory
script_dir = os.path.dirname(os.path.abspath(__file__))  # Directory of logger.py
parent_dir = os.path.dirname(script_dir)  # Parent directory (my_project/)
try:
    if not os.path.exists(parent_dir):
        os.makedirs(parent_dir)  # Create parent directory if it doesn't exist
        fallback_logger.info(f"Created parent directory: {parent_dir}")
    dotenv_path = os.path.join(parent_dir, '.env')
    if not os.path.isfile(dotenv_path):
        raise FileNotFoundError(f".env file not found at: {dotenv_path}")
    load_dotenv(dotenv_path)
except Exception as e:
    fallback_logger.error(f"Failed to load .env file: {str(e)}")
    # Set defaults if .env loading fails
    LOG_LEVEL = 'INFO'
    LOG_FILE_PREFIX = 'app'
else:
    # Get configuration from environment variables
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO').upper()
    LOG_FILE_PREFIX = os.getenv('LOG_FILE_PREFIX', 'app')

# Validate log level
valid_log_levels = {'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'}
if LOG_LEVEL not in valid_log_levels:
    fallback_logger.error(f"Invalid LOG_LEVEL '{LOG_LEVEL}' in .env; defaulting to INFO")
    LOG_LEVEL = 'INFO'

# Create a shared TimedRotatingFileHandler for all loggers
log_dir = os.path.join(parent_dir, 'logs')  # Log directory (my_project/logs/)
# Set initial log file with today's date
today = datetime.now().strftime('%Y-%m-%d')
log_file = os.path.join(log_dir, f"{LOG_FILE_PREFIX}-{today}.log")
try:
    # Ensure the log directory exists
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
        fallback_logger.info(f"Created log directory: {log_dir}")
    file_handler = TimedRotatingFileHandler(
        log_file,
        when="midnight",  # Rotate at midnight
        interval=1,       # Rotate every 1 day
        backupCount=0,    # Keep all rotated files (no deletion)
        utc=False         # Use local time for rotation
    )
    file_handler.setLevel(getattr(logging, LOG_LEVEL))
    file_handler.suffix = "-%Y-%m-%d.log"
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')
    file_handler.setFormatter(formatter)
except Exception as e:
    fallback_logger.error(f"Failed to create log file {log_file}: {str(e)}")
    file_handler = None  # Fallback to console-only logging

def get_logger(module_name):
    """Return a configured logger for the specified module."""
    # Create or get logger for the module
    logger = logging.getLogger(module_name)
    logger.setLevel(getattr(logging, LOG_LEVEL))
    
    # Add shared file handler if not already added and file_handler was created
    if file_handler and not any(isinstance(h, TimedRotatingFileHandler) for h in logger.handlers):
        logger.addHandler(file_handler)
    
    # Add console handler if not already added
    if not any(isinstance(h, logging.StreamHandler) for h in logger.handlers):
        console_handler = logging.StreamHandler()
        console_handler.setLevel(getattr(logging, LOG_LEVEL))
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    
    return logger
