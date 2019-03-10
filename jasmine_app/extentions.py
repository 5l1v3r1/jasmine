import os

import redis
from celery import Celery
from flask.cli import AppGroup
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from peewee import Model
from playhouse.db_url import connect
from raven.contrib.flask import Sentry
from werkzeug.utils import cached_property, import_string

bootstrap = Bootstrap()

celery = Celery(__name__)


class FlaskEnv:
    def __init__(self, app=None):
        self.app = app
        if app:
            self.init_app(app)

    def init_app(self, app):
        if self.app is None:
            self.app = app
        env_file = os.path.join(os.getcwd(), ".env")
        if not env_file:
            raise FileNotFoundError(".env file not found")
        self.__import_vars(env_file)

    def __import_vars(self, env_file):
        # read file
        # parse the str
        # write in config
        with open(env_file) as opener:
            lines = opener.readlines()
            for line in lines:
                line = line.replace("'", "")
                line = line.strip("\n")
                # export
                if not line:
                    continue
                if line.split(" ")[0] == "export":
                    line = line.split(" ")[1]
                config_list = line.split("=")
                key, value = config_list[0], config_list[1]
                if value.isdigit():
                    value = int(value)
                self.app.config[key] = value


flask_env = FlaskEnv()


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


class FlaskPeewee:
    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def connect_db(self):
        if self.database.is_closed():
            self.database.connect()

    def disconnect_db(self, exc):
        if not self.database.is_closed():
            self.database.close()

    @cached_property
    def Model(self):
        class BaseModel(Model):
            class Meta:
                database = self.database

        return BaseModel

    def init_app(self, app):
        self.database = connect(url=app.config["DATABASE_URL"])
        app.database = self.database
        self._register_handlers(app)

    def _register_handlers(self, app):
        app.before_request(self.connect_db)
        app.teardown_request(self.disconnect_db)


flask_peewee = FlaskPeewee()

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
