from flask import abort, jsonify, make_response, request
from flask.views import MethodView
from playhouse.shortcuts import model_to_dict

from jasmine_app.models.user import User


class UserView(MethodView):
    def get(self):
        user_id = request.args.get("user_id")
        if user_id is None:
            abort(status=400)
        user = User.select().where(User.id == user_id).first()

        res = make_response(jsonify(model_to_dict(user)))
        res.headers["Access-Control-Allow-Origin"] = "*"

        return res

    def post(self):
        data = request.json
        print("this is request json", data)
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
