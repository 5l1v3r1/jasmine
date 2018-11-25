from flask import Flask
from jasmine_app.extentions import flask_env, bootstrap, celery, redis_cache
from jasmine_app.utils import update_celery
from configs import config
import sentry_sdk
import os

from flask.cli import FlaskGroup
import click


def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    app.config.from_pyfile('../configs/celery_config.py')
    update_celery(app, celery)
    bootstrap.init_app(app)
    flask_env.init_app(app)
    redis_cache.init_app(app)
    from sentry_sdk.integrations.flask import FlaskIntegration

    sentry_sdk.init(
        dsn="https://e3c5ddd746d9486d9f0a76b6953d8be2@sentry.io/1327554",
        integrations=[FlaskIntegration()],
    )
    from .main.views import main as main_blueprint

    app.register_blueprint(main_blueprint)

    from .api import api as api_blueprint

    app.register_blueprint(api_blueprint)
    return app


@click.group(cls=FlaskGroup, create_app=create_app)
def cli():
    """Management script for the Wiki application."""
