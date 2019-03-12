from flask import abort, jsonify, make_response, request
from flask.views import MethodView
from playhouse.shortcuts import model_to_dict

from jasmine_app.models.user import User
from jasmine_app.models.video import Video


class UserView(MethodView):
    def get(self, user_id):
        if user_id is None:
            abort(status=400)
        user = User.select().where(User.id == user_id).get()
        res = make_response(jsonify(model_to_dict(user)))
        res.headers["Access-Control-Allow-Origin"] = "*"

        return res

    def post(self):
        data = request.json
        if not data:
            abort(400)
        user = User.create(**data)
        res = make_response(jsonify(model_to_dict(user)))
        res.headers["Access-Control-Allow-Origin"] = "*"
        # res.headers['Access-Control-Allow-Credentials'] = True
        return res


class BookView(MethodView):
    def get(self):
        return jsonify([{"name": "book1"}, {"name": "book2"}, {"name": "book3"}])


class VideosView(MethodView):
    def get(self, id):
        videos = Video.select()
        if id is not None:
            video = videos.where(Video.id == id).get()
            return jsonify(model_to_dict(video))
        return jsonify([model_to_dict(video) for video in videos])
