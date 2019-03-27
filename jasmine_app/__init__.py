import os

from flask import Flask
from peewee import DoesNotExist
from .main.views import main as main_blueprint
from .api import api as api_blueprint

from configs import config
from jasmine_app.extentions import (
    # flask_env,
    redis_cache,
    sentry,
    usr_cli,
    db,
    mail,
)

# load command
from jasmine_app.main.tasks import celery
from jasmine_app.utils import not_exist
from flask_utils import update_celery


def create_app():
    app = Flask(__name__)
    env = os.environ.get("FLASK_ENV", "development")
    app.config.from_object(config[env])
    app.cli.add_command(usr_cli)
    update_celery(app, celery)
    # flask_env.init_app(app)
    redis_cache.init_app(app)
    db.init_app(app)
    app.register_error_handler(DoesNotExist, not_exist)
    mail.init_app(app)
    if env == "production":
        sentry.init_app(
            app, dsn="https://e3c5ddd746d9486d9f0a76b6953d8be2@sentry.io/1327554"
        )
    app.register_blueprint(main_blueprint)
    app.register_blueprint(api_blueprint)
    # commands
    app.cli.add_command(usr_cli)
    return app
