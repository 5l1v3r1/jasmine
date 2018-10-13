import os
from jasmine_app import celery, create_app

app = create_app('default')
app.app_context().push()