"""
Configuration file for Speech-to-Text module.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class STTConfig:
    """
    Configuration settings for STT engine.
    """
    model_size: str = "base"
    device: str = "cpu"   # "cuda" if GPU available
    compute_type: str = "int8"