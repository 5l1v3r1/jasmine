from jasmine_app import create_app
from jasmine_app import celery

app = create_app('default')
app.app_context().push()
