from flask import Flask
from flask_bootstrap import Bootstrap

from configs import config
from jasmine_app.extentions import celery, Flask_env
from jasmine_app.utils import update_celery

bootstrap = Bootstrap()
flask_env = Flask_env()


def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    app.config.from_pyfile('../configs/celery_config.py')
    update_celery(app, celery)

    bootstrap.init_app(app)
    flask_env.init_app(app)
    from .main.views import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
