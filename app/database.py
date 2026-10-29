import redis
from app.config import settings
from app.logger import logger

redis_client = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    socket_timeout=2,
    decode_responses=True
)


def check_db_connection() -> bool:
    try:
        return redis_client.ping()
    except Exception as e:
        logger.error(f"Readiness check failed - Redis unreachable: {str(e)}")
        return False