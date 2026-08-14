from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.auth import get_current_user
from app.database import get_db
from app.models.user import User
from app.schemas.integration import AsanaTask, GitHubIssue, SlackNotification

router = APIRouter()

@router.post("/asana/task")
async def create_asana_task_endpoint(
    task: AsanaTask,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # TODO: Implement Asana integration
    raise HTTPException(status_code=501, detail="Not implemented yet")

@router.post("/github/issue")
async def create_github_issue_endpoint(
    issue: GitHubIssue,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # TODO: Implement GitHub integration
    raise HTTPException(status_code=501, detail="Not implemented yet")

@router.post("/slack/notify")
async def send_slack_notification_endpoint(
    notification: SlackNotification,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # TODO: Implement Slack integration
    raise HTTPException(status_code=501, detail="Not implemented yet")
