from configs.base_config import Config


class ProductionConfig(Config):
    DEBUG = True
    CELERY_RESULT_BACKEND = "redis://localhost:6379/1"
    BROKER_URL = "redis://redis:6379/1"
