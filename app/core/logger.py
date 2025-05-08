"""
Logger configuration module.
Provides a pre-configured logger for the application.
"""
from loguru import logger
import sys
import json
from datetime import datetime

# Configure loguru logger
logger.remove()  # Remove default handlers
logger.add(
    sys.stdout,
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
    level="INFO",
    serialize=False,
)

# Add a JSON file logger for structured logging
logger.add(
    "logs/app.json", 
    format=lambda record: json.dumps({
        "timestamp": datetime.fromtimestamp(record["time"].timestamp()).isoformat(),
        "level": record["level"].name,
        "message": record["message"],
        "module": record["name"],
        "line": record["line"],
        "function": record["function"],
    }), 
    level="INFO",
)

def get_logger():
    """Return the configured logger instance."""
    return logger