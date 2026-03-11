# app/orchestrator/store.py
from typing import Dict
from app.orchestrator.state import OrchestratorState

# Key: user_id, Value: OrchestratorState
orchestrator_store: Dict[int, OrchestratorState] = {}