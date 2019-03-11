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


def register_api(app, view, endpoint, url, pk="id", pk_type="int"):
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
