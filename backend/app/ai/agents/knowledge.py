
from app.ai.state import IncidentState
from app.ai.tools.rag import (
    search_knowledge_base,
    search_resolutions,
    search_similar_incidents,
)
from app.database import async_session


async def knowledge_agent(state: IncidentState) -> IncidentState:
    """Gather context for the incident."""
    
    # In a full implementation, we could expose tools to the LLM to let it decide what to search.
    # For a deterministic and fast MVP pipeline, we will perform the RAG searches directly 
    # based on the incident title and category, then pass the results to the next agent.
    
    search_query = f"{state['title']} {state.get('category', '')}"
    
    similar_incidents = []
    knowledge_results = []
    resolution_results = []
    
    try:
        async with async_session() as db:
            similar_incidents = await search_similar_incidents(db, search_query, limit=3)
            knowledge_results = await search_knowledge_base(db, search_query, limit=2)
            resolution_results = await search_resolutions(db, search_query, limit=2)
    except Exception as e:
        print(f"Error in Knowledge Agent DB search: {e}")
        
    return {
        **state,
        "similar_incidents": similar_incidents,
        "knowledge_results": knowledge_results,
        "resolution_results": resolution_results
    }
