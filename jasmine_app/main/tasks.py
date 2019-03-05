from jasmine_app.extentions import celery
from crawler.crawler_video import HupuVideoCrawler
from flask import current_app
from jasmine_app.extentions import mail
from flask_mail import Message


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
    print(app.config['MAIL_SENDER'])
    message = Message(
        subject="来自樊佳亮的问候",
        recipients=app.config["EMAIL_LIST"],
        sender='fjl <fjl2401@163.com>'
    )
    message.body = "hello first mail"

    mail.send(message)
