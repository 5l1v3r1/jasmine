from flask import Blueprint, render_template

from jasmine_app.main.tasks import no_video_crawler

main = Blueprint("run", __name__)


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
