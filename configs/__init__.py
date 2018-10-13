# @Time    : 2018/9/24 下午1:34
from configs.dev_config import Dev_Config
from configs.production_config import Production_config

config = {
    'developement': Dev_Config,
    # 'testing': TestConfig,
    'production': Production_config,
    'default': Dev_Config,
}
