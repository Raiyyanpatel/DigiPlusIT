from datetime import datetime

from pydantic import BaseModel


class ResolutionCreate(BaseModel):
    root_cause: str
    actions_taken: str
    summary: str
    verification: str | None = None

class ResolutionResponse(BaseModel):
    id: str
    incident_id: str
    root_cause: str
    actions_taken: str
    summary: str
    verification: str | None = None
    created_at: datetime

    class Config:
        from_attributes = True
