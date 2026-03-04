from fastapi import APIRouter
from app.schemas.request import OrchestratorRequest
from app.orchestrator.flow import build_orchestrator

router = APIRouter()
orchestrator = build_orchestrator()

@router.post("/orchestrate")
def run_orchestrator(payload: OrchestratorRequest):
    state = payload.dict()
    # commented for testing
    # result = orchestrator.invoke(state)
    return state
