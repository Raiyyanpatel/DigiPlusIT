import httpx

from app.config import settings


async def create_github_issue(title: str, body: str, repo: str = "resolveai/demo") -> dict:
    """Create an issue in GitHub."""
    actual_repo = f"{settings.GITHUB_OWNER}/{settings.GITHUB_REPO}"
    if not settings.GITHUB_TOKEN or settings.GITHUB_TOKEN.startswith("your-"):
        return {
            "status": "success",
            "message": f"Mocked GitHub issue creation in {actual_repo} (no token provided)",
            "issue_url": f"https://github.com/{actual_repo}/issues/mock_456",
            "title": title
        }
        
    url = f"https://api.github.com/repos/{actual_repo}/issues"
    headers = {
        "Authorization": f"token {settings.GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    data = {
        "title": title,
        "body": body
    }
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=data)
            response.raise_for_status()
            return {"status": "success", "data": response.json()}
    except Exception as e:
        return {"status": "error", "message": str(e)}
