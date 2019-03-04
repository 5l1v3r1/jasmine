class Config:
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
    REDIS_DB = 0
    REDIS_PORT = 6379

    REDLOCK_TIMEOUT = 10
    REDLOCK_BLOCKING_TIMEOUT = 5

    # celery
    from datetime import timedelta

    # redis 作为消息队列
    # CELERY_ACCEPT_CONTENT = ['pickle']
    # CELERY_TASK_SERIALIZER = 'pickle'
    # CELERY_RESULT_SERIALIZER = 'pickle'
    BROKER_URL = "redis://localhost:6379/0"
    # BROKER_URL = 'amqp://user:newpass@localhost:5672//'
    CELERY_TASK_PROTOCOL = 1
    # result_backend = 'redis://localhost:6379/1'
    CELERY_RESULT_BACKEND = "redis://localhost:6379/1"

    CELERY_ACCEPT_CONTENT = ["json"]
    CELERY_BEAT_SCHEDULE = {
        "add": {
            "task": "jasmine_app.main.tasks.add",
            "schedule": timedelta(seconds=1),
            "args": (14, 14),
        },
        # spider get hupu data every_day
        "fetch_hupu_data": {
            "task": "jasmine_app.main.tasks.fetch_hupu_data",
            "schedule": timedelta(days=1),
        }
        # 'send_email': {'task': 'jasmine_app.play.views.send_async_email'},
    }
    # database
    DB_CLIENT_CHARSET = "utf8mb4"
    DB_HOST = "mysql"
    DB_USER = "root"
    DB_PASSWORD = "newpass"
    DB_NAME = "jasmine"
    DATABASE_URL = "mysql+pool://{user}:{password}@{host}/{name}".format(
        host=DB_HOST, user=DB_USER, password=DB_PASSWORD, name=DB_NAME
    )
    PW_CONN_PARAMS = {"charset": DB_CLIENT_CHARSET, "stale_timeout": 1800}
