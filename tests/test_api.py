from jasmine_app.models.user import User
from jasmine_app.models.video import Video
from tests.test_utils import fake_api

# fake_api(client, User)


@fake_api(Model=User)
def test_user(client):
    pass


@fake_api(Model=Video, exclude_methods=("PUT",))
def test_video(client):
    # do some complex test
    pass
