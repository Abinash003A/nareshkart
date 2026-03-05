"""
core/redis.py
Redis client for OTP storage. Shared across features.
"""
import redis
from core.config import REDIS_HOST, REDIS_PORT

client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    decode_responses=True,
    socket_connect_timeout=3,
)
