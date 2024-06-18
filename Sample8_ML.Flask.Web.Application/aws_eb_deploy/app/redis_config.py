from log_config import logger
from redis import Redis, RedisError


def rate_limiter(fapp, key, limit, duration):
    try:
        redis = Redis(
            username=fapp.config['REDIS_USERNAME'],
            host=fapp.config['REDIS_HOST'],
            port=fapp.config['REDIS_PORT'],
            db=fapp.config['REDIS_DB'],
            password=fapp.config['SUPER_SECRET_PASSWORD']
        )

        redis.ping()
        logger.info("Redis() connection established ...")

        current_count = redis.incr(key)
        logger.info(f"Key: {key}, Current Count: {current_count}")

        redis.expire(name=key, time=duration)

        if current_count > limit:
            return False
        return True

    except RedisError as e:
        logger.error(f'Failed to connect to Redis and configure Limiter: {e}', exc_info=True)
