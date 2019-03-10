import os

from flask import Flask

from configs import config
from jasmine_app.extentions import (
    flask_env,
    bootstrap,
    celery,
    redis_cache,
    sentry,
    usr_cli,
    flask_peewee,
    mail,
)
from jasmine_app.utils import update_celery


def create_app():
    app = Flask(__name__, static_folder="", static_url_path="")
    env = os.environ.get("FLASK_ENV", "development")
    app.config.from_object(config[env])
    app.cli.add_command(usr_cli)
    update_celery(app, celery)
    bootstrap.init_app(app)
    flask_env.init_app(app)
    redis_cache.init_app(app)
    flask_peewee.init_app(app)
    mail.init_app(app)
    if env == "production":
        sentry.init_app(
            app, dsn="https://e3c5ddd746d9486d9f0a76b6953d8be2@sentry.io/1327554"
        )
    from .main.views import main as main_blueprint

    app.register_blueprint(main_blueprint)

    from .api import api as api_blueprint

    app.register_blueprint(api_blueprint)
    # commands
    app.cli.add_command(usr_cli)
    return app
