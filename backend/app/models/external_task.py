import enum
import uuid
from datetime import datetime
from typing import Any

from sqlalchemy import JSON, DateTime, Enum, ForeignKey, String, text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class TaskProvider(str, enum.Enum):
    ASANA = "asana"
    GITHUB = "github"
    SLACK = "slack"


class ExternalTask(Base):
    __tablename__ = "external_tasks"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    incident_id: Mapped[str] = mapped_column(String, ForeignKey("incidents.id", ondelete="CASCADE"), nullable=False)
    
    provider: Mapped[TaskProvider] = mapped_column(Enum(TaskProvider), nullable=False)
    external_id: Mapped[str] = mapped_column(String, nullable=True) # ID in the external system
    url: Mapped[str] = mapped_column(String, nullable=True) # Link to the task/issue/message
    status: Mapped[str] = mapped_column(String, nullable=False) # e.g., 'created', 'failed'
    
    metadata_json: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=True)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=text("now()"), nullable=False)

    # incident: Mapped["Incident"] = relationship(back_populates="external_tasks")
