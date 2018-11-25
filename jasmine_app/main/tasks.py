from jasmine_app.extentions import celery


@celery.task
def a():
    print('this is a')


@celery.task
def add(num1, num2):
    print('add: ', num1 + num2)
