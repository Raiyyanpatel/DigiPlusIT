from datetime import datetime

from pydantic import BaseModel


class KnowledgeDocCreate(BaseModel):
    title: str
    content: str
    category: str | None = None
    source: str | None = None

class KnowledgeDocResponse(BaseModel):
    id: str
    title: str
    content: str
    category: str | None = None
    source: str | None = None
    created_at: datetime

    class Config:
        from_attributes = True
