from configs.base_config import Config


class ProductionConfig(Config):
    DEBUG = False
    CELERY_RESULT_BACKEND = "redis://redis:6379/1"
    BROKER_URL = "redis://redis:6379/1"
    REDIS_HOST = "redis"
    CACHE_HOST = "redis"

