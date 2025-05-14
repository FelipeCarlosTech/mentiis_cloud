"""
Logger configuration module.
Provides a pre-configured logger for the application.
"""

from loguru import logger
import sys
import os

# Ensure logs directory exists
os.makedirs("logs", exist_ok=True)

# Configure loguru logger
logger.remove()  # Remove default handlers

# Add console logger
logger.add(
    sys.stdout,
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
    level="INFO",
)

# Add file logger (plain text)
logger.add(
    "logs/app.log",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
    level="INFO",
)


def get_logger():
    """Return the configured logger instance."""
    return logger
