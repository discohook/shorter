import ipaddress
from datetime import datetime
from typing import Any, Optional

from aioredis import Redis, create_redis
from quart import request
from quart_rate_limiter import RateLimiter
from quart_rate_limiter.store import RateLimiterStoreABC

from shorter import config


class RedisStore(RateLimiterStoreABC):
    async def get(self, key: str, default: datetime):
        result = await self.redis.get(key)
        if result is None:
            return default
        else:
            return datetime.fromtimestamp(float(result))

    async def set(self, key: str, tat: datetime):
        await self.redis.set(key, tat.timestamp())
        await self.redis.expire(key, (tat - datetime.utcnow()).total_seconds() + 5.0)

    async def before_serving(self):
        self.redis = await create_redis(config.redis_address, encoding="utf-8")

    async def after_serving(self):
        self.redis.close()
        await self.redis.wait_closed()
        self.redis = None


async def get_rate_limit_key():
    ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    addr = ipaddress.ip_address(ip)
    if isinstance(addr, ipaddress.IPv6Address):
        addr = ipaddress.IPv6Network(f"{addr}/64", strict=False).network_address

    return str(addr)


rate_limiter = RateLimiter(store=RedisStore(), key_function=get_rate_limit_key)
