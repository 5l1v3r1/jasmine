from jasmine_app.api.views import BookView, UserView

from . import api

api.add_url_rule(
    "/user", view_func=UserView.as_view("hello_view"), methods=["GET", "POST"]
)
api.add_url_rule(
    "/book", view_func=BookView.as_view("book_view"), methods=["GET", "POST"]
)
