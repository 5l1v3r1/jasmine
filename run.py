from flask_script import Manager, Shell

from jasmine_app import create_app

app = create_app()
print(app.static_url_path)
manager = Manager(app)

manager.add_command("shell", Shell())
if __name__ == "__main__":
    manager.run()
