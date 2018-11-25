## jasmine

此项目为练习和使用flask一些有趣的扩展和特性的试验田
因为主要作为学习和实验，所以项目的代码不会太多。学习和理解起来也不会有太大的压力

## 已经完成或者正在进行的实验
所有的扩展或特性全部基于flask 工厂模式来 create app
- flask 结合bootstrap
- flask 结合celery 异步任务队列
- 微信api接口
- 自动从.env文件加载配置的extention
- flask视频直播(无声音)
- flask Elasticsearch
- flask路由管理和view实现api接口
- flask 每次加载自动刷新js和css文件


CELERY_TASK_PROTOCOL = 1


### 运行worker
celery worker -B -A run_celery.celery --loglevel=info



## 错误处理

celery AttributeError: 'float' object has no attribute 'items'
pyredis=redis-2.10.6 

Refusing to deserialize untrusted content of type pickle (application/x-python-serialize)

Received unregistered task of type 'jasmine_app.main.tasks.add'.
The message has been ignored and discarded.
使用新的导入方式
from proj.module import foo
from .module import foo

## flask click

运行flask flask run 安装python-dotenv 然后在.env文件中写入配置，就会自动加载

pip install -e .  安装本地module到当前pip环境