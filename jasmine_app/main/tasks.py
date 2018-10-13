import time
from jasmine_app.extentions import celery


@celery.task
def add(a, b):
    print(a + b)
    return a + b


@celery.task
def sout():
    print('报时: ', time.time())
