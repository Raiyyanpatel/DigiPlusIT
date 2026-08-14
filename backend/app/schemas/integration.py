
from pydantic import BaseModel


class AsanaTask(BaseModel):
    name: str
    notes: str
    projects: list[str]

class GitHubIssue(BaseModel):
    title: str
    body: str

class SlackNotification(BaseModel):
    text: str
