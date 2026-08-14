"""
🤖 ResolveAI — Configuration
"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "postgresql+asyncpg://resolveai:resolveai@postgres:5432/resolveai"
    DATABASE_URL_SYNC: str = "postgresql://resolveai:resolveai@postgres:5432/resolveai"

    # Redis
    REDIS_URL: str = "redis://redis:6379/0"

    # JWT
    JWT_SECRET: str = "change-me-to-a-secure-random-string"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 480

    # OpenAI
    OPENAI_API_KEY: str = ""

    # Asana
    ASANA_ACCESS_TOKEN: str = ""
    ASANA_PROJECT_ID: str = ""

    # GitHub
    GITHUB_TOKEN: str = ""
    GITHUB_OWNER: str = ""
    GITHUB_REPO: str = ""

    # Slack
    SLACK_WEBHOOK_URL: str = ""

    # App
    APP_ENV: str = "development"
    LOG_LEVEL: str = "INFO"
    FRONTEND_URL: str = "http://localhost:3000"

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
