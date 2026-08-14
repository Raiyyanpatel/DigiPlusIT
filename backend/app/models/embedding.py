import uuid

from pgvector.sqlalchemy import Vector
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class IncidentEmbedding(Base):
    __tablename__ = "incident_embeddings"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    incident_id: Mapped[str] = mapped_column(String, ForeignKey("incidents.id", ondelete="CASCADE"), unique=True, nullable=False)
    
    # 3072 is the dimension for Gemini's gemini-embedding-2
    embedding = mapped_column(Vector(3072), nullable=False)
    text_hash: Mapped[str] = mapped_column(String, nullable=False) # To check if we need to re-embed
    
    # incident: Mapped["Incident"] = relationship()
