import click
from cli import cli


@cli.command()
@click.option("--path", help="file path")
def insert_premature_code(path):
    print(path)
