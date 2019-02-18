from flask.views import MethodView
from flask import Response
from jasmine_app.api import api
from jasmine_app.extentions import redis_cache


class HelloView(MethodView):
    def get(self):
        redis_cache.set("name", "hello_redis_cache")
        return Response(redis_cache.get("name"))


@api.route("/hello_world")
def index():
    return Response("this is index")
