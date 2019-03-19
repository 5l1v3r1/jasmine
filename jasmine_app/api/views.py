from flask_utils.restframework import ModelViewSet

from jasmine_app.models.user import User
from jasmine_app.models.video import Video


class UserView(ModelViewSet):
    model_class = User


class Video(ModelViewSet):
    model_class = Video
