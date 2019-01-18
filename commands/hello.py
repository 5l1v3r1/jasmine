import click
from cli import cli
from jasmine_app.extentions import usr_cli
from flask import current_app


@usr_cli.command('create_user')
def create_user():
    '''
    create user
    '''
    print('create user {}'.format("cli"))
    print(current_app.config)
