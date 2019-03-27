from datetime import datetime

from peewee import CharField, ForeignKeyField

from jasmine_app.extentions import db
from jasmine_app.utils import DatetimeTZField


class Author(db.Model):
    name = CharField(null=False, unique=True)
    password = CharField(null=False)
    email = CharField(null=False)
    profile = CharField()
    created_at = DatetimeTZField(default=datetime.now())


class Tag(db.Model):
    name = CharField(null=False, unique=True)


class Article(db.Model):
    author_name = ForeignKeyField(Author, Author.name)
    title = CharField()
    tag_name = ForeignKeyField(Tag, Tag.name)
    created_at = DatetimeTZField(default=datetime.now())
