from jasmine_app import create_app
from jasmine_app import celery

app = create_app()
app.app_context().push()
print(app.config.get_namespace(namespace='CELERY'))
