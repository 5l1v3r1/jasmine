from flask_utils.views import register_api

from jasmine_app.api.views import UserView, Video

from . import api

register_api(api, Video, "video_api", "/video/")
register_api(api, UserView, "user_api", "/user/")
