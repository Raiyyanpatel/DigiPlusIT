
from pydantic import BaseModel


class Classification(BaseModel):
    category: str
    priority: str
    confidence: float

class AnalysisResult(BaseModel):
    summary: str
    classification: Classification
    root_cause: str
    recommended_actions: list[str]
    evidence: list[str]
    escalation_required: bool
    external_actions: list[str]

class CopilotRequest(BaseModel):
    message: str

class CopilotResponse(BaseModel):
    response: str
    evidence_used: list[str]

class SimilarIncident(BaseModel):
    incident_id: str
    title: str
    similarity: float
    status: str
