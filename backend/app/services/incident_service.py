from datetime import datetime

from fastapi import HTTPException
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.audit_log import AuditLog
from app.models.incident import Incident, IncidentPriority, IncidentStatus
from app.models.resolution import Resolution
from app.schemas.incident import IncidentCreate, IncidentUpdate


async def create_incident(db: AsyncSession, incident_in: IncidentCreate, user_id: str) -> Incident:
    # Generate external ID (e.g., INC-1024)
    result = await db.execute(select(func.count(Incident.id)))
    count = result.scalar() or 0
    external_id = f"INC-{1000 + count + 1}"
    
    incident = Incident(
        external_id=external_id,
        title=incident_in.title,
        description=incident_in.description,
        priority=incident_in.priority or IncidentPriority.UNASSIGNED,
        category=incident_in.category,
        status=IncidentStatus.OPEN
    )
    db.add(incident)
    await db.flush() # flush to get the ID
    
    # Log action
    audit_log = AuditLog(
        incident_id=incident.id,
        action="Created",
        actor=f"user:{user_id}",
        metadata_json={"title": incident.title}
    )
    db.add(audit_log)
    await db.commit()
    await db.refresh(incident)
    return incident

async def get_incident(db: AsyncSession, incident_id: str) -> Incident:
    result = await db.execute(select(Incident).where(Incident.id == incident_id))
    incident = result.scalars().first()
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    return incident

async def get_incidents(db: AsyncSession, skip: int = 0, limit: int = 100) -> list[Incident]:
    result = await db.execute(select(Incident).order_by(Incident.created_at.desc()).offset(skip).limit(limit))
    return list(result.scalars().all())

async def update_incident(db: AsyncSession, incident_id: str, incident_in: IncidentUpdate, user_id: str) -> Incident:
    incident = await get_incident(db, incident_id)
    
    update_data = incident_in.model_dump(exclude_unset=True)
    
    # Handle status transition validation (basic)
    if "status" in update_data:
        new_status = update_data["status"]
        if new_status == IncidentStatus.CLOSED and incident.status != IncidentStatus.RESOLVED:
            raise HTTPException(status_code=400, detail="Cannot close an incident that is not resolved")
        if new_status == IncidentStatus.RESOLVED:
            incident.resolved_at = datetime.utcnow()
            # Record resolution
            if "resolution_summary" in update_data:
                resolution = Resolution(
                    incident_id=incident.id,
                    summary=update_data["resolution_summary"],
                    author_id=user_id
                )
                db.add(resolution)
    
    for field, value in update_data.items():
        setattr(incident, field, value)
        
    audit_log = AuditLog(
        incident_id=incident.id,
        action="Updated",
        actor=f"user:{user_id}",
        metadata_json=update_data
    )
    db.add(audit_log)
    await db.commit()
    await db.refresh(incident)
    return incident

async def delete_incident(db: AsyncSession, incident_id: str, user_id: str):
    incident = await get_incident(db, incident_id)
    await db.delete(incident)
    await db.commit()
    return {"message": "Incident deleted"}
