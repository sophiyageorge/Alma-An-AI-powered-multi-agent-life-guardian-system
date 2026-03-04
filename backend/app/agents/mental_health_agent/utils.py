"""
utils.py
Utility functions for Mental Health Agent.
"""

import logging
from typing import Optional


def setup_logger(
    name: str = "MentalHealthAgentLogger",
    level: int = logging.INFO,
) -> logging.Logger:
    """
    Setup a structured logger for Mental Health Agent.

    Args:
        name (str): Logger name
        level (int): Logging level

    Returns:
        logging.Logger: Configured logger
    """
    logger = logging.getLogger(name)

    # Prevent duplicate handlers in multi-import environments
    if not logger.handlers:
        logger.setLevel(level)

        formatter = logging.Formatter(
            "%(asctime)s | %(name)s | %(levelname)s | %(message)s"
        )

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)

        logger.addHandler(stream_handler)
        logger.propagate = False  # Prevent duplicate logs from root logger

    return logger


def safe_execute(func, *args, **kwargs) -> Optional[dict]:
    """
    Safely execute a function and catch exceptions.

    Args:
        func: Function to execute
        *args: Positional arguments
        **kwargs: Keyword arguments

    Returns:
        Optional[dict]: Function result or error dictionary
    """
    logger = logging.getLogger("MentalHealthAgentLogger")

    try:
        return func(*args, **kwargs)
    except Exception as e:
        logger.exception("Unhandled exception occurred.")
        return {
            "status": "error",
            "message": str(e)
        }