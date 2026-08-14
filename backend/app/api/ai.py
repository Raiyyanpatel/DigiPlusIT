
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.auth import get_current_user
from app.database import get_db
from app.models.user import User
from app.schemas.ai import (
    AnalysisResult,
    CopilotRequest,
    CopilotResponse,
    SimilarIncident,
)
from app.services import incident_service

router = APIRouter()

@router.post("/{incident_id}/analyze", response_model=AnalysisResult)
async def analyze_incident(
    incident_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Fetch incident
    incident = await incident_service.get_incident(db, incident_id)
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
        
    # Check cache
    from app.services.cache_service import cache_service
    cached = await cache_service.get(f"incident_analysis_{incident_id}")
    if cached:
        return AnalysisResult(**cached)
    
    # Run LangGraph pipeline
    from app.ai.graph import process_incident
    
    result = await process_incident(
        incident_id=incident.external_id,
        title=incident.title,
        description=incident.description
    )
    
    if result.get("status") == "error":
        raise HTTPException(status_code=500, detail=result.get("message"))
        
    # Format to schema
    analysis = AnalysisResult(
        summary=result.get("summary", ""),
        root_cause=result.get("root_cause", ""),
        recommended_actions=result.get("recommended_actions", []),
        escalation_required=result.get("escalation_required", False),
        external_actions_taken=[str(action) for action in result.get("external_actions", [])]
    )
    
    # Save to incident
    incident_update = incident_service.IncidentUpdate(
        ai_analysis=analysis.model_dump()
    )
    await incident_service.update_incident(db, incident_id, incident_update, current_user.id)
    
    # Set Cache
    await cache_service.set(f"incident_analysis_{incident_id}", analysis.model_dump(), 3600)
    
    return analysis

@router.post("/{incident_id}/copilot", response_model=CopilotResponse)
async def copilot_chat(
    incident_id: str,
    request: CopilotRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    from langchain_core.messages import HumanMessage, SystemMessage
    from langchain_openai import ChatOpenAI

    from app.config import settings
    
    incident = await incident_service.get_incident(db, incident_id)
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
        
    llm = ChatOpenAI(
        api_key=settings.OPENAI_API_KEY, 
        model="gpt-4o-mini"
    )
    
    sys_msg = SystemMessage(content=f"You are the ResolveAI Copilot. Help the engineer resolve this incident: {incident.title}. Description: {incident.description}.\n\nIMPORTANT: Do NOT use markdown formatting (such as *, #, or `). Output clean, readable plain text only, separated by newlines.")
    human_msg = HumanMessage(content=request.message)
    messages = [sys_msg, human_msg]
    
    try:
        response = await llm.ainvoke(messages)
        content = response.content
        if isinstance(content, list):
            content = content[0].get("text", "")
            
        return CopilotResponse(
            response=content,
            evidence_used=[]
        )
    except Exception as e:
        return CopilotResponse(response=f"Error communicating with AI: {e}")

@router.get("/{incident_id}/similar", response_model=list[SimilarIncident])
async def get_similar_incidents(
    incident_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # TODO: Implement semantic search for similar incidents
    raise HTTPException(status_code=501, detail="Not implemented yet")
