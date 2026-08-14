import enum
import uuid
from datetime import datetime
from typing import Any

from sqlalchemy import JSON, DateTime, Enum, String, text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class IncidentStatus(str, enum.Enum):
    OPEN = "OPEN"
    TRIAGED = "TRIAGED"
    IN_PROGRESS = "IN_PROGRESS"
    ESCALATED = "ESCALATED"
    RESOLVED = "RESOLVED"
    CLOSED = "CLOSED"


class IncidentPriority(str, enum.Enum):
    P1 = "P1"
    P2 = "P2"
    P3 = "P3"
    P4 = "P4"
    UNASSIGNED = "UNASSIGNED"


class Incident(Base):
    __tablename__ = "incidents"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    external_id: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)  # e.g., INC-0001
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[IncidentStatus] = mapped_column(Enum(IncidentStatus), default=IncidentStatus.OPEN, nullable=False)
    priority: Mapped[IncidentPriority] = mapped_column(Enum(IncidentPriority), default=IncidentPriority.UNASSIGNED, nullable=False)
    category: Mapped[str] = mapped_column(String, nullable=True)
    subcategory: Mapped[str] = mapped_column(String, nullable=True)
    team: Mapped[str] = mapped_column(String, nullable=True)
    
    # Stores the raw JSON output from the AI agents (LangGraph final state)
    ai_analysis: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=True)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=text("now()"), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=text("now()"), onupdate=datetime.utcnow, nullable=False)
    resolved_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    
    # Relationships (to be populated as other models are defined)
    # comments: Mapped[list["Comment"]] = relationship(back_populates="incident", cascade="all, delete-orphan")
    # resolution: Mapped["Resolution"] = relationship(back_populates="incident", uselist=False, cascade="all, delete-orphan")
    # external_tasks: Mapped[list["ExternalTask"]] = relationship(back_populates="incident", cascade="all, delete-orphan")
