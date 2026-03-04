# app/agents/mental_health/stt_agent.py

from faster_whisper import WhisperModel
from app.orchestrator.state import OrchestratorState
import os

# Load model once (important)
model = WhisperModel("base", compute_type="int8")

def mental_health_stt_agent(state: OrchestratorState) -> OrchestratorState:
    
    audio_path = state.get("audio_path")
    
    if not audio_path or not os.path.exists(audio_path):
        state["mental_health_input"] = {}
        return state
    
    segments, info = model.transcribe(audio_path)
    
    full_text = ""
    for segment in segments:
        full_text += segment.text + " "
    
    clean_text = full_text.strip().lower()
    
    state["mental_health_input"] = {
        "raw_text": full_text.strip(),
        "clean_text": clean_text,
        "language": info.language,
        "confidence": info.language_probability
    }
    
    return state