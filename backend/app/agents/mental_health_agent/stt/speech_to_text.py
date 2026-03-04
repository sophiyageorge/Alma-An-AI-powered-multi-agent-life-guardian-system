"""
Speech-to-Text Engine using Faster-Whisper.
"""

import os
from typing import Dict, Any
from faster_whisper import WhisperModel

from .config import STTConfig
from .exceptions import AudioFileNotFoundError, TranscriptionError
from .logger import setup_logger
from loguru import logger


class SpeechToTextEngine:
    """
    Handles audio transcription using Faster-Whisper.
    """

    def __init__(self, config: STTConfig) -> None:
        """
        Initialize Whisper model with configuration.
        """
        setup_logger()
        self.config = config

        try:
            logger.info("Loading Whisper model...")
            self.model = WhisperModel(
                model_size_or_path=config.model_size,
                device=config.device,
                compute_type=config.compute_type
            )
            logger.info("Whisper model loaded successfully.")
        except Exception as exc:
            logger.exception("Failed to load Whisper model.")
            raise TranscriptionError("Model initialization failed.") from exc

    def transcribe(self, audio_path: str) -> Dict[str, Any]:
        """
        Transcribe audio file to text.

        :param audio_path: Path to audio file.
        :return: Dictionary containing transcription result.
        :raises AudioFileNotFoundError: If file not found.
        :raises TranscriptionError: If transcription fails.
        """
        if not os.path.exists(audio_path):
            logger.error(f"Audio file not found: {audio_path}")
            raise AudioFileNotFoundError(
                f"Audio file does not exist: {audio_path}"
            )

        try:
            logger.info(f"Starting transcription for {audio_path}")

            segments, info = self.model.transcribe(audio_path)

            transcript = " ".join([segment.text for segment in segments])

            logger.info("Transcription completed successfully.")

            return {
                "text": transcript.strip(),
                "language": info.language,
                "duration": info.duration
            }

        except Exception as exc:
            logger.exception("Transcription failed.")
            raise TranscriptionError(
                "Error occurred during transcription."
            ) from exc