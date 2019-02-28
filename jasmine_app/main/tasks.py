from jasmine_app.extentions import celery
from crawler.crawler_video import HupuVideoCrawler


@celery.task
def a():
    print("this is a")


@celery.task
def add(num1, num2):
    print("add: ", num1 + num2)


@celery.task
def fetch_hupu_data():
    hupu_crawler = HupuVideoCrawler()
    hupu_crawler.main()
