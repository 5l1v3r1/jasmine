from jasmine_app.models.user import User
from jasmine_app.models.video import Video
from jasmine_app.utils import ModelViewSet


class UserView(ModelViewSet):
    model_class = User


class Video(ModelViewSet):
    model_class = Video
