from peewee import AutoField, CharField, IntegerField, SmallIntegerField

from jasmine_app.extentions import flask_peewee


class SerializerMixin:
    pass


class Video(flask_peewee.Model, SerializerMixin):
    id = AutoField(primary_key=True)
    url = CharField(max_length=500, index=True)
    title = CharField(null=False, unique=True)
    published_time = CharField(null=False)
    author = CharField(null=False)
    video_length = CharField()
    view_times = IntegerField()
    favorite_nums = IntegerField()
    comments_nums = IntegerField()
    points = IntegerField()
    level = SmallIntegerField(default=0)
