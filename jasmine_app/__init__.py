import logging

import click
from flask import Flask
from flask.cli import FlaskGroup
from raven import Client
from raven.conf import setup_logging
from raven.handlers.logging import SentryHandler
from werkzeug.utils import import_string

from jasmine_app.extentions import flask_env, bootstrap, celery, redis_cache, sentry, usr_cli
from jasmine_app.utils import update_celery


def create_app():
    app = Flask(__name__)
    config_1 = import_string('configs.dev_config')
    app.config.from_object(config_1)
    app.config.from_pyfile('../configs/celery_config.py')
    app.cli.add_command(usr_cli)
    update_celery(app, celery)
    bootstrap.init_app(app)
    flask_env.init_app(app)
    redis_cache.init_app(app)

    # old solution
    client = Client('https://e3c5ddd746d9486d9f0a76b6953d8be2:4902b914e65b46748d84e960ce122eba@sentry.io/1327554')
    handler = SentryHandler(client)
    handler.setLevel(logging.ERROR)
    # setup_logging(handler, exclude=['oss2.api'])
    setup_logging(handler)
    logger = logging.getLogger("oss2.api")
    logger.propagate = False
    logger.addHandler(logging.StreamHandler())
    # new solution
    # from sentry_sdk.integrations.flask import FlaskIntegration
    # sentry_sdk.init(
    #     dsn="https://e3c5ddd746d9486d9f0a76b6953d8be2@sentry.io/1327554",
    #     integrations=[FlaskIntegration()],
    # )
    # ignore_logger('test_loger')
    # ignore_logger('oss2.api')
    # sentry.init_app(app, dsn='https://e3c5ddd746d9486d9f0a76b6953d8be2@sentry.io/1327554')
    from .main.views import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint)
    # commnands
    app.cli.add_command(usr_cli)
    return app


@click.group(cls=FlaskGroup, create_app=create_app)
def cli():
    """Management script for the Wiki application."""
