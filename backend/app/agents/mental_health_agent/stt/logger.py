"""
Logger configuration for STT module.
"""

from loguru import logger
import sys


def setup_logger() -> None:
    """
    Configure structured logger.
    """
    logger.remove()
    logger.add(
        sys.stdout,
        format="{time} | {level} | {name}:{function}:{line} | {message}",
        level="INFO"
    )