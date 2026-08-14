import json
from typing import Any

import redis.asyncio as redis

from app.config import settings


class CacheService:
    def __init__(self):
        self.redis = redis.from_url(settings.REDIS_URL, encoding="utf-8", decode_responses=True)

    async def get(self, key: str) -> Any | None:
        val = await self.redis.get(key)
        if val:
            return json.loads(val)
        return None

    async def set(self, key: str, value: Any, ttl_seconds: int = 3600):
        await self.redis.set(key, json.dumps(value), ex=ttl_seconds)
        
    async def delete(self, key: str):
        await self.redis.delete(key)

cache_service = CacheService()
