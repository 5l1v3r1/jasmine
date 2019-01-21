from jasmine_app import create_app
from jasmine_app import celery

app = create_app()
app.app_context().push()
