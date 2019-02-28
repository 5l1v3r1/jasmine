from peewee import CharField, IntegerField

from jasmine_app.extentions import flask_peewee

import peeweext


class User(flask_peewee.Model):

    name = CharField(max_length=255)
    id = IntegerField()
