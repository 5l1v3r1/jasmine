from configs.base_config import Config


class DevConfig(Config):
    DEBUG = True
    DB_HOST = "localhost"
    DATABASE_URL = "mysql://root:newpass@localhost/jasmine"
