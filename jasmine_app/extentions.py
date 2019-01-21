import os

import redis
from celery import Celery
from flask.cli import AppGroup
from flask_bootstrap import Bootstrap
from raven.contrib.flask import Sentry
from werkzeug.utils import import_string

bootstrap = Bootstrap()

celery = Celery(__name__)


class Flask_env:
    def __init__(self, app=None):
        self.app = app
        if app:
            self.init_app(app)

    def init_app(self, app):
        if self.app is None:
            self.app = app
        env_file = os.path.join(os.getcwd(), '.env')
        if not env_file:
            raise FileNotFoundError('.env file not found')
        self.__import_vars(env_file)

    def __import_vars(self, env_file):
        # read file
        # parse the str
        # write in config
        print('load .env file from parent dir')
        with open(env_file) as opener:
            lines = opener.readlines()
            for line in lines:
                line = line.replace('\'', '')
                line = line.strip('\n')
                # export
                if not line:
                    continue
                if line.split(' ')[0] is 'export':
                    line = line.split(' ')[1]
                config_list = line.split('=')
                key, value = config_list[0], config_list[1]
                if self.app.config.get(key):
                    print(
                        'overwrite an exist key : {} {} ---> {}'.format(
                            key, self.app.config[key], value
                        )
                    )
                if value.isdigit():
                    value = int(value)
                self.app.config[key] = value


flask_env = Flask_env()


class RedisCache:
    def __init__(self, ns='REDIS_'):
        self.ns = ns
        self.client = None

    def init_app(self, app):
        # 找到redis配置文件，加载redis配置
        opts = app.config.get_namespace(self.ns)
        # 生成redis客户端
        self._pool = redis.ConnectionPool(**opts)
        self._client = redis.StrictRedis(connection_pool=self._pool)

        return getattr(self._client, name)


redis_cache = RedisCache()
sentry = Sentry()

usr_cli = AppGroup('user')


# 加载commands文件夹下的commands
def load_commands():
    import_string('commands')

    base_dir = os.path.dirname(__file__)
    commands_dir = os.path.join(os.path.dirname(base_dir), "commands")
    for file_name in os.listdir(commands_dir):
        if file_name.endswith('py'):
            import_name = "commands." + file_name[:-3]
            import_string(import_name)


load_commands()
