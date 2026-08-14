from typing import Any, TypedDict


class IncidentState(TypedDict):
    # Original Incident Data
    incident_id: str
    title: str
    description: str

    # Triage Agent output
    category: str
    priority: str
    urgency: str
    triage_confidence: float

    # Knowledge Agent output
    similar_incidents: list[dict]
    knowledge_results: list[dict]
    resolution_results: list[dict]

    # Investigation Agent output
    root_cause: str
    investigation_confidence: float
    recommended_actions: list[str]
    evidence_used: list[str]
    escalation_required: bool
    
    # Action Agent output
    external_actions: list[dict]

    # Final combined response for the API
    final_response: dict[str, Any]
