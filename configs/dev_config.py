from configs.base_config import Config


class DevConfig(Config):
    DEBUG = False
    DATABASE_URL = "mysql://root:newpass@localhost/jasmine"
