# @Time    : 2018/9/24 下午1:41

from flask import Flask
from app.extentions import celery
from configs import config


def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    app.config.from_pyfile('../configs/celery_config.py')

    from .main.views import main as main_blueprint
    app.register_blueprint(main_blueprint)


    return app
