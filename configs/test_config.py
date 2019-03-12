from configs.base_config import Config


class TestConfig(Config):
    DATABASE_URL = "mysql+pool://root:newpass@mysql/jasmine_test"

    DEBUG = True
