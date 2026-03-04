from pydantic import BaseModel
from typing import Optional, Dict

class OrchestratorRequest(BaseModel):
    user_id: str
    health_data: Optional[Dict] = None
    journal_text: Optional[str] = None
