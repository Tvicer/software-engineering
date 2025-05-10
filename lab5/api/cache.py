import redis
import pickle

REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_DB = 0
CACHE_EXPIRE_SECONDS = 300  # 5 минут

redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    db=REDIS_DB,
    decode_responses=False
)

def get_from_cache(key: str):
    """Получить данные из кеша"""
    cached_data = redis_client.get(key)
    if cached_data is not None:
        return pickle.loads(cached_data)
    return None

def set_to_cache(key: str, data, expire: int = CACHE_EXPIRE_SECONDS):
    """Сохранить данные в кеш"""
    redis_client.setex(key, expire, pickle.dumps(data))

def invalidate_cache(pattern: str):
    """Удалить данные из кеша по шаблону"""
    keys = redis_client.keys(pattern)
    if keys:
        redis_client.delete(*keys)