from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field

from app.models.incident import IncidentPriority, IncidentStatus


class IncidentCreate(BaseModel):
    title: str = Field(..., min_length=1)
    description: str = Field(..., min_length=1)
    priority: IncidentPriority | None = IncidentPriority.UNASSIGNED
    category: str | None = None

class IncidentUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: IncidentStatus | None = None
    priority: IncidentPriority | None = None
    category: str | None = None
    subcategory: str | None = None
    team: str | None = None

class IncidentResponse(BaseModel):
    id: str
    external_id: str
    title: str
    description: str
    status: IncidentStatus
    priority: IncidentPriority
    category: str | None = None
    subcategory: str | None = None
    team: str | None = None
    ai_analysis: dict[str, Any] | None = None
    created_at: datetime
    updated_at: datetime
    resolved_at: datetime | None = None

    class Config:
        from_attributes = True
