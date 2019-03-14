from jasmine_app.api.views import UserView, Video
from jasmine_app.utils import register_api

from . import api

register_api(api, Video, "video_api", "/video/")
register_api(api, UserView, "user_api", "/user/")
