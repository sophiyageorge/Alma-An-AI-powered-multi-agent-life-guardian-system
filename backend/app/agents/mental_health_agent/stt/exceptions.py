"""
Custom exceptions for STT module.
"""


class STTError(Exception):
    """Base exception for Speech-to-Text errors."""


class AudioFileNotFoundError(STTError):
    """Raised when audio file does not exist."""


class TranscriptionError(STTError):
    """Raised when transcription fails."""