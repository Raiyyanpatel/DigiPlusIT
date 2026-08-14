from langgraph.graph import END, StateGraph

from app.ai.agents.action import action_agent
from app.ai.agents.investigation import investigation_agent
from app.ai.agents.knowledge import knowledge_agent
from app.ai.agents.triage import triage_agent
from app.ai.state import IncidentState


def build_graph():
    """Build the LangGraph pipeline for the service desk."""
    
    # Define a new graph
    workflow = StateGraph(IncidentState)
    
    # Add nodes
    workflow.add_node("triage", triage_agent)
    workflow.add_node("knowledge", knowledge_agent)
    workflow.add_node("investigation", investigation_agent)
    workflow.add_node("action", action_agent)
    
    def finalizer(state: IncidentState) -> IncidentState:
        """Format the final response."""
        return {
            **state,
            "final_response": {
                "category": state.get("category"),
                "priority": state.get("priority"),
                "root_cause": state.get("root_cause"),
                "recommended_actions": state.get("recommended_actions"),
                "escalation_required": state.get("escalation_required"),
                "external_actions": state.get("external_actions", [])
            }
        }
        
    workflow.add_node("finalizer", finalizer)
    
    # Define edges (Strictly linear sequence for the MVP pipeline)
    workflow.set_entry_point("triage")
    workflow.add_edge("triage", "knowledge")
    workflow.add_edge("knowledge", "investigation")
    workflow.add_edge("investigation", "action")
    workflow.add_edge("action", "finalizer")
    workflow.add_edge("finalizer", END)
    
    # Compile
    return workflow.compile()

# Global graph instance
app_graph = build_graph()

async def process_incident(incident_id: str, title: str, description: str) -> dict:
    """Entry point for processing a new incident through the graph."""
    
    initial_state = {
        "incident_id": incident_id,
        "title": title,
        "description": description,
        "category": "",
        "priority": "",
        "urgency": "",
        "triage_confidence": 0.0,
        "similar_incidents": [],
        "knowledge_results": [],
        "resolution_results": [],
        "root_cause": "",
        "investigation_confidence": 0.0,
        "recommended_actions": [],
        "evidence_used": [],
        "escalation_required": False,
        "external_actions": [],
        "final_response": {}
    }
    
    # Run the graph
    try:
        final_state = await app_graph.ainvoke(initial_state)
        return final_state.get("final_response", {})
    except Exception as e:
        print(f"Error in LangGraph execution: {e}")
        return {"status": "error", "message": str(e)}
