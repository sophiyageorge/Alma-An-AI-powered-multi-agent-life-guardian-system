"""
utils.py
Utility functions for Exercise Agent.
"""

import logging

def setup_logger(name: str = "ExerciseAgentLogger") -> logging.Logger:
    """
    Setup a structured logger for Exercise Agent.

    Args:
        name (str): Logger name

    Returns:
        logging.Logger: Configured logger
    """
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger