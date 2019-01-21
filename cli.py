import os
import sys

import click
from werkzeug.utils import import_string


@click.group()
def cli():
    print('this is cki')
    pass


def _load_jobs():
    path = os.getcwd()
    sys.path.append(path)
    # load app jobs
    appjobs = os.path.join(path, 'commands')
    if os.path.exists(appjobs):
        import_string('commands')
        for m in os.listdir(appjobs):
            if m != '__init__.py' and m.endswith('.py'):
                import_string('commands.{}'.format(m[:-3]))


def main():
    _load_jobs()
    cli()
