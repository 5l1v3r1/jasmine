import os

from celery.schedules import crontab


class Config:
    CACHE_PREFIX = "jasmine"
    CACHE_HOST = "localhost"
    CACHE_DB = 0
    CACHE_PORT = 6379

    LONG_CACHE_TTL = 1 * 24 * 60 * 60
    SHORT_CACHE_TTL = 10 * 60

    REDIS_HOST = "localhost"
    REDIS_DB = 0
    REDIS_PORT = 6379

    REDLOCK_TIMEOUT = 10
    REDLOCK_BLOCKING_TIMEOUT = 5
    timezone = "Asia/Shanghai"

    # celery
    from datetime import timedelta

    # redis 作为消息队列
    BROKER_URL = "redis://localhost:6379/1"
    CELERY_TASK_PROTOCOL = 1
    CELERY_RESULT_BACKEND = "redis://localhost:6379/1"

    CELERY_ACCEPT_CONTENT = ["json"]
    CELERYBEAT_SCHEDULE = {
        "test_celery_beat": {
            "task": "jasmine_app.main.tasks.test_celery_beat",
            "schedule": timedelta(seconds=10),
        },
        # spider get hupu data every_day
        "fetch_hupu_data": {
            "task": "jasmine_app.main.tasks.fetch_hupu_data",
            "schedule": crontab(hour=20),
        },
        "send_mail_to_vip": {
            "task": "jasmine_app.main.tasks.send_mail",
            "schedule": crontab(day_of_month=15, hour=12),
        },
        # mvp No_video crawler
        "mvp": {
            "task": "jasmine_app.main.tasks.mvp_crawler",
            "schedule": crontab(hour=8),
        },
    }
    # database
    DB_CLIENT_CHARSET = "utf8mb4"
    DATABASE_URL = "mysql+pool://root:newpass@localhost/jasmine"
    PW_CONN_PARAMS = {"charset": DB_CLIENT_CHARSET, "stale_timeout": 1800}

    # email
    MAIL_SERVER = "smtp.qq.com"
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USERNAME = "fjl2401@qq.com"
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    EMAIL_LIST = ["fjl2401@163.com", "826077013@qq.com", "441070584@qq.com"]
    SECRET_KEY = "hard to guess"
    MAIL_SENDER = "fjl2401@qq.com"
    MAIL_USE_SSL = True

    # crawler begin page
    NO_MAIN_PAGE_URL = "http://93.91p26.space/v.php?next=watch"
