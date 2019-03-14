from flask import Response, abort, jsonify, request
from flask.views import MethodView
from playhouse.shortcuts import model_to_dict


def update_celery(app, celery):
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        # 每次 @celery时会调用call方法。相当于装饰器在被调用时在flask的app context下
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask


def register_api(app, view, endpoint, url, pk="pk", pk_type="int"):
    """
    register_api(UserAPI, 'user_api', '/users/', pk='user_id')
    /users/ list user  post
    /users/1 get delete put
    """
    view_func = view.as_view(endpoint)
    app.add_url_rule(url, defaults={pk: None}, view_func=view_func, methods=["GET"])
    app.add_url_rule(url, view_func=view_func, methods=["POST"])
    app.add_url_rule(
        "%s<%s:%s>" % (url, pk_type, pk),
        view_func=view_func,
        methods=["GET", "PUT", "DELETE"],
    )


def not_exist(error):
    return Response(error, status=404)


class ModelViewSet(MethodView):
    model_class = None

    def get(self, pk):
        query = self.model_class.select()
        if pk is not None:
            query = query.where(self.model_class.id == pk).first()
            return jsonify(model_to_dict(query, recurse=False))
        return jsonify([model_to_dict(q, recurse=False) for q in query])

    def post(self):
        data = request.json
        if not data:
            abort(400)
        model_instance = self.model_class.create(**data)
        res = jsonify(model_to_dict(model_instance, recurse=False)), 201
        return res

    def put(self, pk):
        updated = (
            self.model_class.update(**request.json)
            .where(self.model_class.id == pk)
            .execute()
        )
        return Response(status=204 if updated else 200)

    def delete(self, pk):
        self.model_class.delete_by_id(pk)
        return Response(status=204)
