# encoding=utf-8
# @Time    : 2018/9/24 下午1:35
from flask import render_template, Response, url_for, Blueprint

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return Response('hello')



