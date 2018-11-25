class Config:
    DEBUG = True
    CACHE_BACKEND = "Redis"
    CACHE_PREFIX = "jasmine"
    # CACHE_HOST = "redis"
    CACHE_HOST = "127.0.0.1"
    CACHE_DB = 0
    CACHE_PORT = 6379

    LONG_CACHE_TTL = 1 * 24 * 60 * 60
    SHORT_CACHE_TTL = 10 * 60

    REDIS_HOST = "redis"
    REDIS_HOST = "127.0.0.1"
    REDIS_DB = 2
    REDIS_PORT = 6379

    REDLOCK_TIMEOUT = 10
    REDLOCK_BLOCKING_TIMEOUT = 5
