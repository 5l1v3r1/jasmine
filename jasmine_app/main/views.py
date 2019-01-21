import os
from flask import render_template, url_for, Blueprint, current_app
from jasmine_app.main.tasks import add
import logging
import oss2
import io

main = Blueprint('main', __name__)


@main.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)


def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(current_app.root_path, endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)


@main.route('/')
def index():
    # add.delay(2, 3)
    # logger = logging.getLogger('test_loger')
    # logger.log(level=logging.ERROR, msg='this is test logger')
    ali_access_id = '6Ex0OMIU0dxMuhUO'
    MEDIA_ALIYUN_SECRET_KEY = 'cw0M0ZEsuTNXIKMfOFJ79lo5WO137t'
    MEDIA_ALIYUN_INTERNAL_HOST = "oss-cn-hangzhou.aliyuncs.com"
    bucket_name = 'sbay-debug'

    oss2_auth = oss2.Auth(
        ali_access_id, MEDIA_ALIYUN_SECRET_KEY)
    bucket = oss2.Bucket(oss2_auth, MEDIA_ALIYUN_INTERNAL_HOST, bucket_name)
    key_1 = '2_redeem_redeemer/1/1_sad_12_2018-11-22_2018-11-22.csv'
    key_2 = 'redeem_redeemer/1/1_sad_12_2018-11-23_2018-11-23ddd.txt'

    data = io.BytesIO(b'sd')

    data.seek(0)
    res = bucket.object_exists(key_2)
    return render_template('main/base.html')
