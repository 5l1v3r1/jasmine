from flask_utils.restframework import ModelViewSet

from jasmine_app.models.video import Video


class Video(ModelViewSet):
    model_class = Video
