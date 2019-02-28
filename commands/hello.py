from jasmine_app.extentions import usr_cli, redis_cache, flask_peewee


@usr_cli.command("create_user")
def create_user():
    """
    创建user table
    """
    # 避免循环引用 create_app依赖 extensions extensions需要加载command command需要先create_app
    # 产生了循环依赖，所以应该在已经create_app成功后import app，而且app.database也是依赖于create_app完成
    from run import app

    with app.app_context():
        from jasmine_app.models.user import User

        with app.database:
            app.database.create_tables([User])


@usr_cli.command("redis")
def test_redis_connection():
    print("redis keys{}".format(redis_cache.keys()))
