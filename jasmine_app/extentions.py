import os

import redis
from celery import Celery
from flask.cli import AppGroup
from flask_mail import Mail
from playhouse.flask_utils import FlaskDB
from raven.contrib.flask import Sentry
from werkzeug.utils import import_string

celery = Celery(__name__)

# flask_env = FlaskEnv()


class RedisCache:
    def __init__(self, ns="REDIS_"):
        self.ns = ns
        self.client = None

    def init_app(self, app):
        # 找到redis配置文件，加载redis配置
        opts = app.config.get_namespace(self.ns)
        # 生成redis客户端
        self._pool = redis.ConnectionPool(**opts)
        self._client = redis.StrictRedis(connection_pool=self._pool)

    def __getattr__(self, name):
        return getattr(self._client, name)


redis_cache = RedisCache()
sentry = Sentry()

db = FlaskDB()

usr_cli = AppGroup("user")


# 加载commands文件夹下的commands
def load_commands():
    import_string("commands")

    base_dir = os.path.dirname(__file__)
    commands_dir = os.path.join(os.path.dirname(base_dir), "commands")
    for file_name in os.listdir(commands_dir):
        if file_name.endswith("py"):
            import_name = "commands." + file_name[:-3]
            import_string(import_name)


load_commands()

mail = Mail()
