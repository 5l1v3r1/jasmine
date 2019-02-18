import click
from flask import Flask

app = Flask(__name__)


@app.cli.command()
@click.argument("name")
def create_user(name):
    print("this is name {}".format(name))


if __name__ == "__main__":
    app.run()
