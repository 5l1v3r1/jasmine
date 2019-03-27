import os

from flask import (
    Blueprint,
    abort,
    current_app,
    redirect,
    render_template,
    request,
    url_for,
)
from jinja2.exceptions import TemplateNotFound

from jasmine_app.main.tasks import no_video_crawler
from jasmine_app.utils import convert_and_save, not_exist

main = Blueprint("run", __name__)
main.register_error_handler(TemplateNotFound, not_exist)


@main.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "GET":
        return redirect(url_for(".index"))
    file = request.files.get("file")
    if not file or not convert_and_save(file, file.filename):
        abort(400)
    return redirect(url_for(".blog", values=format(file.filename.split(".")[0])))


@main.route("/blog/<string:blog_name>")
def blog(blog_name):
    return render_template("blog/{}.html".format(blog_name))


@main.route("/")
def index():
    return render_template("index.html")


@main.route("/video")
def videos():
    return render_template("videos.html")


@main.route("/no_crawler")
def no_crawler():
    no_video_crawler.delay()
    return render_template("index.html")


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
