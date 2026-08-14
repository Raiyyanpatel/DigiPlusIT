import json

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI

from app.ai.prompts.system_prompts import TRIAGE_PROMPT
from app.ai.state import IncidentState
from app.config import settings


async def triage_agent(state: IncidentState) -> IncidentState:
    """Triage the incident to categorize and prioritize it."""
    
    # We use gpt-4o-mini as specified
    # Using JSON mode to ensure structured output    
    llm = ChatGoogleGenerativeAI(
        api_key=settings.GEMINI_API_KEY, 
        model="gemini-flash-lite-latest",
        temperature=0
    ).bind(
        response_format={"type": "json_object"}
    )
    
    sys_msg = SystemMessage(content=TRIAGE_PROMPT + "\n\nRespond with a JSON object containing keys: 'category' (string), 'priority' (string: P1, P2, P3), 'urgency' (string: High, Medium, Low), and 'triage_confidence' (float).")
    
    human_msg = HumanMessage(content=f"Incident Title: {state['title']}\n\nDescription: {state['description']}")
    
    try:
        response = await llm.ainvoke([sys_msg, human_msg])
        content = response.content
        if isinstance(content, list):
            content = content[0].get("text", "")
        result = json.loads(content)
        
        # Update state
        return {
            **state,
            "category": result.get("category", "General"),
            "priority": result.get("priority", "P3"),
            "urgency": result.get("urgency", "Low"),
            "triage_confidence": float(result.get("triage_confidence", 0.5))
        }
    except Exception as e:
        print(f"Error in Triage Agent: {e}")
        return {
            **state,
            "category": "General",
            "priority": "P3",
            "urgency": "Low",
            "triage_confidence": 0.0
        }
