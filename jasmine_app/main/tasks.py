from urllib.parse import urljoin

import requests
from crawler_utils.utils import url2path
from flask import current_app
from flask_mail import Message

from crawler.crawler_video import HupuVideoCrawler
from crawler.no_crawler import NoCrawler
from jasmine_app.extentions import celery, mail


@celery.task
def test_celery_beat():
    print("beat is ok!")


@celery.task
def fetch_hupu_data():
    hupu_crawler = HupuVideoCrawler()
    hupu_crawler.main()


@celery.task
def send_mail():
    app = current_app._get_current_object()
    message = Message(
        subject="hello,vip",
        recipients=app.config["EMAIL_LIST"],
        sender=app.config["MAIL_SENDER"],
    )
    message.body = "Dear vip user\n" "<h1>please pay your outline bill to Alipay.</h1>"
    mail.send(message)


@celery.task
def mvp_crawler():
    from jasmine_app.models.video import Video

    base_url = current_app.config["NO_MAIN_PAGE_URL"]
    crawler = NoCrawler()
    messages = crawler.page_message_extract(base_url)
    for message in messages:
        Video.create(**message)
        download_video(message["url"])


def download_video(url):
    """
    file_name is replace url '/' to '_'
    """
    res = requests.get(url, stream=True)
    file_path = urljoin("/data/videos/no", url2path(url) + ".mp4")
    with open(file_path, "wb") as opener:
        for chunk in res.iter_content(chunk_size=1024):
            opener.write(chunk)
            opener.flush()
