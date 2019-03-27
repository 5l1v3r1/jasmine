from jasmine_app.extentions import db
from jasmine_app.models.user import Article, Author, Tag


def migrate_up():
    print("run successful!")
    db.database.create_tables([Author, Tag, Article])


def rollback():
    pass
