from jasmine_app.extentions import redis_cache, usr_cli


@usr_cli.command("redis")
def test_redis_connection():
    print("redis keys{}".format(redis_cache.keys()))
