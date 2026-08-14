import json

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI

from app.ai.prompts.system_prompts import ACTION_PROMPT
from app.ai.state import IncidentState
from app.ai.tools.asana import create_asana_task
from app.ai.tools.github import create_github_issue
from app.ai.tools.slack import send_slack_message
from app.config import settings

# We wrap the async functions in sync wrappers for the LLM tool bindings if needed,
# or we can parse JSON and call them directly. For a deterministic MVP pipeline,
# we'll use function calling or simple JSON instruction parsing.

async def action_agent(state: IncidentState) -> IncidentState:
    """Execute external actions if recommended."""
    
    # If no escalation or external actions are explicitly requested, we can just return
    if not state.get("recommended_actions"):
        return state
        
    llm = ChatGoogleGenerativeAI(
        api_key=settings.GEMINI_API_KEY, 
        model="gemini-flash-lite-latest",
        temperature=0
    ).bind(
        response_format={"type": "json_object"}
    )
    
    sys_msg = SystemMessage(content=ACTION_PROMPT + "\n\nRespond with a JSON object containing a list called 'actions_to_take'. Each action should be an object with 'tool' (asana, github, slack) and 'args' (dict of arguments).")
    
    context = f"Incident: {state['title']}\nRecommended Actions: {json.dumps(state.get('recommended_actions', []))}\nEscalation Required: {state.get('escalation_required')}"
    human_msg = HumanMessage(content=context)
    
    executed_actions = []
    try:
        response = await llm.ainvoke([sys_msg, human_msg])
        content = response.content
        if isinstance(content, list):
            content = content[0].get("text", "")
        result = json.loads(content)
        
        actions = result.get("actions_to_take", [])
        
        for action in actions:
            tool_name = action.get("tool")
            args = action.get("args", {})
            
            if tool_name == "asana":
                res = await create_asana_task(name=args.get("name", "Task"), notes=args.get("notes", ""))
                executed_actions.append({"tool": "asana", "result": res})
            elif tool_name == "github":
                res = await create_github_issue(title=args.get("title", "Issue"), body=args.get("body", ""))
                executed_actions.append({"tool": "github", "result": res})
            elif tool_name == "slack":
                res = await send_slack_message(message=args.get("message", "Alert"))
                executed_actions.append({"tool": "slack", "result": res})
                
    except Exception as e:
        print(f"Error in Action Agent: {e}")
        executed_actions.append({"tool": "error", "message": str(e)})
        
    return {
        **state,
        "external_actions": executed_actions
    }
