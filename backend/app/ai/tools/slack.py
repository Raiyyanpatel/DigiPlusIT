import httpx

from app.config import settings


async def send_slack_message(message: str, channel: str = "#alerts") -> dict:
    """Send a message to a Slack channel via webhook."""
    if not settings.SLACK_WEBHOOK_URL or settings.SLACK_WEBHOOK_URL.startswith("your-") or not settings.SLACK_WEBHOOK_URL.startswith("http"):
        return {
            "status": "success",
            "message": f"Mocked Slack message to {channel} (no webhook provided)",
            "text_sent": message
        }
        
    data = {
        "text": f"*{channel} Alert*\n{message}"
    }
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(settings.SLACK_WEBHOOK_URL, json=data)
            response.raise_for_status()
            return {"status": "success", "message": "Slack message sent"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
