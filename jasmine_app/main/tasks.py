from jasmine_app.extentions import celery
from crawler.crawler_video import HupuVideoCrawler
from flask import current_app
from jasmine_app.extentions import mail
from flask_mail import Message
import os


@celery.task
def a():
    print("this is a")


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
        subject="来自樊佳亮的问候",
        recipients=app.config["EMAIL_LIST"],
        sender=app.config["MAIL_SENDER"],
    )
    message.body = "hello first mail"
    mail.send(message)
