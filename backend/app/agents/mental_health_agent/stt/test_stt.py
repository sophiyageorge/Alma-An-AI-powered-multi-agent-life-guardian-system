"""
Manual test script for STT engine.
"""

from app.agents.mental_health_agent.stt.config import STTConfig
from app.agents.mental_health_agent.stt.speech_to_text import SpeechToTextEngine


def main() -> None:
    config = STTConfig(
        model_size="base",
        device="cpu"
    )

    base_path = Path(__file__).parent
    audio_file = base_path / "sample_audio.m4a"

    engine = SpeechToTextEngine(config=config)

    result = engine.transcribe(str(audio_file))

    print("\nTranscription Result:")
    print(result["text"])
    print(f"Language: {result['language']}")
    print(f"Duration: {result['duration']}")


if __name__ == "__main__":
    main()