import os

import pytest

from jasmine_app import create_app


def pytest_sessionstart(session):
    os.environ["FLASK_ENV"] = "testing"
    create_app()


@pytest.fixture(scope="session")
def app():
    os.environ["FLASK_ENV"] = "testing"
    app = create_app()
    # 必须在create_app后 model user才能用。。
    from jasmine_app.models.user import User
    from jasmine_app.models.video import Video

    with app.app_context():
        app.database.create_tables([User, Video])
        yield app
        app.database.drop_tables([User, Video])


@pytest.fixture
def client(app):
    client = app.test_client()
    return client
