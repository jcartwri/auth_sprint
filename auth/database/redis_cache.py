import redis
from core.config import TestSettings

settings = TestSettings()


redis_cache = redis.Redis(
    host=settings.REDIS_HOST, port=int(settings.REDIS_PORT), db=0, decode_responses=True
)
