from . import api
from jasmine_app.api.views import HelloView

api.add_url_rule('/hello', view_func=HelloView.as_view('hello_view'), methods=["GET"])
