
from pydantic import BaseModel

from typing import Optional

class Classification(BaseModel):
    category: str
    priority: str
    confidence: float

class AnalysisResult(BaseModel):
    summary: Optional[str] = None
    classification: Optional[Classification] = None
    root_cause: str
    recommended_actions: list[str]
    evidence: Optional[list[str]] = None
    escalation_required: bool
    external_actions_taken: list[str]

class CopilotRequest(BaseModel):
    message: str

class CopilotResponse(BaseModel):
    response: str
    evidence_used: Optional[list[str]] = None

class SimilarIncident(BaseModel):
    incident_id: str
    title: str
    similarity: float
    status: str
