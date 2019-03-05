import os

from flask import render_template, url_for, Blueprint, current_app, flash
from jasmine_app.models.user import User
from jasmine_app.main.tasks import send_mail

main = Blueprint("main", __name__)


@main.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)


def dated_url_for(endpoint, **values):
    if endpoint == "static":
        filename = values.get("filename", None)
        if filename:
            file_path = os.path.join(current_app.root_path, endpoint, filename)
            values["q"] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)


@main.route("/")
def index():
    users = User.select()
    user_numbers = len(users)
    if user_numbers == 0:
        user_data = {"name": "icecola", "id": 1}
        User.create(**user_data)
    # logger = logging.getLogger('test_loger')
    # logger.log(level=logging.ERROR, msg='this is test logger')
    return render_template("main/base.html")


@main.route("/send_mailssss")
def send_email():
    send_mail.delay()
    flash("发送成功")
    return render_template("main/base.html")
