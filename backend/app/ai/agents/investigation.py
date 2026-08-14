import json

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI

from app.ai.prompts.system_prompts import INVESTIGATION_PROMPT
from app.ai.state import IncidentState
from app.config import settings


async def investigation_agent(state: IncidentState) -> IncidentState:
    """Analyze the incident and RAG context to determine root cause and actions."""
    
    llm = ChatGoogleGenerativeAI(
        api_key=settings.GEMINI_API_KEY, 
        model="gemini-1.5-flash",
        temperature=0
    ).bind(
        response_format={"type": "json_object"}
    )
    
    sys_msg = SystemMessage(content=INVESTIGATION_PROMPT + "\n\nRespond with a JSON object containing keys: 'root_cause' (string), 'investigation_confidence' (float), 'recommended_actions' (list of strings), 'evidence_used' (list of strings), and 'escalation_required' (boolean).")
    
    # Construct context block
    context = f"Incident: {state['title']}\nDescription: {state['description']}\nCategory: {state.get('category', '')}\nPriority: {state.get('priority', '')}\n\n"
    
    if state.get("knowledge_results"):
        context += "--- Knowledge Base ---\n"
        for kb in state["knowledge_results"]:
            context += f"Title: {kb['title']}\nContent: {kb['content']}\n\n"
            
    if state.get("similar_incidents"):
        context += "--- Similar Past Incidents ---\n"
        for inc in state["similar_incidents"]:
            context += f"ID: {inc['incident_id']}\nTitle: {inc['title']}\nDescription: {inc['description']}\n\n"
            
    if state.get("resolution_results"):
        context += "--- Past Resolutions ---\n"
        for res in state["resolution_results"]:
            context += f"Root Cause: {res['root_cause']}\nActions: {res['actions_taken']}\nSummary: {res['resolution_summary']}\n\n"
            
    human_msg = HumanMessage(content=context)
    
    try:
        response = await llm.ainvoke([sys_msg, human_msg])
        result = json.loads(response.content)
        
        return {
            **state,
            "root_cause": result.get("root_cause", "Unable to determine"),
            "investigation_confidence": float(result.get("investigation_confidence", 0.0)),
            "recommended_actions": result.get("recommended_actions", []),
            "evidence_used": result.get("evidence_used", []),
            "escalation_required": bool(result.get("escalation_required", True))
        }
    except Exception as e:
        print(f"Error in Investigation Agent: {e}")
        return {
            **state,
            "root_cause": "Error during analysis",
            "investigation_confidence": 0.0,
            "recommended_actions": ["Investigate manually"],
            "evidence_used": [],
            "escalation_required": True
        }
