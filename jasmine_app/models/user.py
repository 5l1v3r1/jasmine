from peewee import CharField

from jasmine_app.extentions import flask_peewee


class SerializerMixin:
    pass


class User(flask_peewee.Model, SerializerMixin):
    name = CharField(max_length=255)
    password = CharField(max_length=32, null=False)
