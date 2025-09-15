"""
Logging configuration for the Padawan Integration application.
"""

import logging
import sys
from typing import Optional


def setup_logger(name: str = 'padawan_app', level: str = 'INFO') -> logging.Logger:
    """
    Set up a logger with consistent formatting.

    Args:
        name: Logger name
        level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)

    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)

    # Avoid adding multiple handlers if logger is already configured
    if logger.handlers:
        return logger

    # Set log level
    numeric_level = getattr(logging, level.upper(), logging.INFO)
    logger.setLevel(numeric_level)

    # Create console handler
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(numeric_level)

    # Create formatter
    formatter = logging.Formatter(
        fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    handler.setFormatter(formatter)

    # Add handler to logger
    logger.addHandler(handler)

    return logger


def get_logger(name: str, level: Optional[str] = None) -> logging.Logger:
    """
    Get a logger instance with optional level override.

    Args:
        name: Logger name
        level: Optional log level override

    Returns:
        Logger instance
    """
    if level:
        return setup_logger(name, level)

    # Return existing logger or create new one with default level
    logger = logging.getLogger(name)
    if not logger.handlers:
        return setup_logger(name)
    return logger
