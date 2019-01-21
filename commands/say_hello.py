import click
from flask.cli import FlaskGroup

from jasmine_app import create_app


# cli = FlaskGroup(create_app=create_app)


@click.group(cls=FlaskGroup, create_app=create_app)
def hello():
    print('sd')
