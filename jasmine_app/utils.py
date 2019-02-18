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


def test_oss2():
    pass
    # ali_access_id = '6Ex0OMIU0dxMuhUO'
    # MEDIA_ALIYUN_SECRET_KEY = 'cw0M0ZEsuTNXIKMfOFJ79lo5WO137t'
    # MEDIA_ALIYUN_INTERNAL_HOST = "oss-cn-hangzhou.aliyuncs.com"
    # bucket_name = 'sbay-debug'
    #
    # oss2_auth = oss2.Auth(
    #     ali_access_id, MEDIA_ALIYUN_SECRET_KEY)
    # bucket = oss2.Bucket(oss2_auth, MEDIA_ALIYUN_INTERNAL_HOST, bucket_name)
    # key_1 = '2_redeem_redeemer/1/1_sad_12_2018-11-22_2018-11-22.csv'
    # key_2 = 'redeem_redeemer/1/1_sad_12_2018-11-23_2018-11-23ddd.txt'
    #
    # data = io.BytesIO(b'sd')
    #
    # data.seek(0)
    # res = bucket.object_exists(key_2)
