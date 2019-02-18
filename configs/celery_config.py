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
# 任务调度 没十分钟跑次
CELERYBEAT_SCHEDULE = {
    "add": {
        "task": "jasmine_app.main.tasks.add",
        "schedule": timedelta(seconds=10),
        "args": (14, 14),
    },
    # 'send_email': {'task': 'jasmine_app.play.views.send_async_email'},
}
