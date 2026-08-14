import httpx

from app.config import settings


async def create_asana_task(name: str, notes: str, project_id: str = "default_project") -> dict:
    """Create a task in Asana."""
    # In a real implementation, this would call the Asana API
    # Since we might not have a real Asana token during the demo, we'll mock it if the token is missing
    if not settings.ASANA_ACCESS_TOKEN or settings.ASANA_ACCESS_TOKEN.startswith("your-") or settings.ASANA_PROJECT_ID == "your-asana-project-id":
        return {
            "status": "success",
            "message": "Mocked Asana task creation (no token provided)",
            "task_id": "mock_task_123",
            "name": name
        }
        
    # Always use the project ID from environment variables instead of what the AI guesses
    actual_project_id = settings.ASANA_PROJECT_ID
        
    url = "https://app.asana.com/api/1.0/tasks"
    headers = {
        "Authorization": f"Bearer {settings.ASANA_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    
    # Normally we need a workspace ID, just mocking the request structure for now
    data = {
        "data": {
            "name": name,
            "notes": notes,
            "projects": [actual_project_id]
        }
    }
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=data)
            response.raise_for_status()
            return {"status": "success", "data": response.json().get("data", {})}
    except Exception as e:
        return {"status": "error", "message": str(e)}
