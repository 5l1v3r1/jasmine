import datetime
import os

import markdown2
import peewee
import pendulum
from crawler_utils.utils import url2path
from flask import current_app, render_template
from werkzeug.datastructures import FileStorage


def not_exist(error):
    return render_template("errors/404.html")


class DatetimeTZField(peewee.Field):
    field_type = "DATETIME"

    def python_value(self, value):
        if isinstance(value, str):
            return pendulum.parse(value)
        if isinstance(value, datetime.datetime):
            return pendulum.instance(value)
        return value

    def db_value(self, value):
        if value is None:
            return value
        if not isinstance(value, datetime.datetime):
            raise ValueError("datetime instance required")
        if value.utcoffset() is None:
            raise ValueError("timezone aware datetime required")
        if isinstance(value, pendulum.DateTime):
            value = datetime.datetime.fromtimestamp(
                value.timestamp(), tz=value.timezone
            )
        return value.astimezone(datetime.timezone.utc)


ALLOWED_EXTENSIONS = set(["txt", "md"])


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def generate_file(file_path, file_name, file_stream):

    if "static" in file_path:
        file_name = os.path.join(file_path, file_name)
        if isinstance(file_stream, FileStorage):
            file_stream.save(file_name)
    else:
        file_name = os.path.join(file_path, file_name.split(".")[0] + ".html")

        with open(os.path.join(file_path, "blog_template.html"), "r") as reader:
            template = reader.read()
            content = template.split("\n")
            if isinstance(file_stream, FileStorage):
                file_stream.stream.seek(0)
                file_stream = file_stream.stream.read().decode("utf-8")
                file_stream = markdown2.markdown(file_stream)
            content.insert(4, file_stream)
            with open(file_name, "w") as writer:
                writer.write("\n".join(content))


def convert_and_save(file_stream, filename, tagName=None):
    """
    transfer markdown to html and save
    :param file_stream:
    :param filename:
    :param tagName:
    :return:
    """

    if not allowed_file(filename):
        return False
    filename = url2path(filename)
    folder_list = ["static/blog", "templates/blog"]
    for folder_path in folder_list:
        folder_path = os.path.join(current_app.root_path, folder_path)
        if tagName:
            folder_path = os.path.join(folder_path, tagName)
        if not os.path.isdir(folder_path):
            os.mkdir(folder_path)
        generate_file(folder_path, filename, file_stream)
    return True
