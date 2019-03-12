from jasmine_app.api.views import BookView, UserView, VideosView
from jasmine_app.utils import register_api

from . import api

api.add_url_rule(
    "/book", view_func=BookView.as_view("book_view"), methods=["GET", "POST"]
),
register_api(api, VideosView, "videos_api", "/videos/")
register_api(api, UserView, "users_api", "/users/", pk="user_id")
