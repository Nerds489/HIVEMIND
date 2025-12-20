"""
Cache memory layer using Redis.

Provides fast session context storage and temporary data caching.
"""

from __future__ import annotations

from hivemind.memory.cache.redis import RedisCache

__all__ = ["RedisCache"]
