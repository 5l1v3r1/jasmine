# jasmine

此项目为练习和使用flask一些有趣的扩展和特性的试验田
因为主要作为学习和实验，所以项目的代码不会太多。学习和理解起来也不会有太大的压力
所有的扩展或特性全部基于flask factory模式 create_app


## 已经完成

- ci/cd 到云服务器
- flask factory模式 结合celery 异步任务队列
- flask+redis 配置缓存
- 自动从.env文件加载配置的extention
- flask 每次加载自动刷新js和css文件
- 配置sentry 自动监控 和ignore log设置
- flask-env 从.env文件中加载配置
- flask cli 通过FlaskGroup来管理所有commands
- flask+pytest 进行单元测试,配置数据库

## 待完成

- 微信公众号后台api接口
- 爬虫定时抓取、清洗、显示hupu视频数据+Elasticsearch搜索

## ci/cd 持续发布

通过gitlab ci+docker-compose 完成个人项目的持续发布
ssh为非对称加密，需要在本机上生成公钥和私钥，然后把公钥交给需要登录的机器。然后将私钥以变量
的信息存在gitlab ci中。

### test

在gitlab runner中通过docker镜像和依赖进行测试。进行flak8和pytest单元测试。

### deploy

通过ssh命令更新server下的代码，然后docker-compose rebuild
每次向gitlab push代码的时候，自动触发测试任务，手动触发deploy任务。

## celery

在create_app时，加载update_celery方法。更新config，同时将task放在context下
新建run_celery文件：
```python
from jasmine_app import create_app
from jasmine_app import celery

app = create_app()
app.app_context().push()

``` 
### 运行

celery worker -B -A run_celery.celery --loglevel=info


### 发布镜像到docker.io
docker build --cache-from jasmine:latest -t jasmine:latest .
docker tag jasmine:latest fjl2401/jasmine
docker push fjl2401/jasmine


## flask-env

安装: pip install python-dotenv
在root目录下加入.env文件 .env文件中加入配置

- FLASK_DEBUG=True or False
- FLASK_APP=jasmin_app
- FLASK_ENV=development



## 配置sentry

需要去sentry注册并生成秘钥，官方文档也挺好的。主要给出屏蔽错误信息方法。
有两种方法
1. raven
2. sentry_sdk 

pip install --upgrade sentry-sdk[flask]==0.5.5

```python
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

sentry_sdk.init(
    dsn="https://e3c5ddd746d9486d9f0a76b6953d8be2@sentry.io/1327554",
    integrations=[FlaskIntegration()]
)
```
## flask+commands

在需要跑脚本的时候可以把脚本文件统一放在commands下做处理
通过AppGroup自定义cli，然后import_string()将commands加载进来

```py

# extension文件中
usr_cli = AppGroup("user")
import_string("play_flask.single_app.command")




# 写在commands文件夹中
@usr_cli.command("create_user")
def create_user():
    """
    create user
    """
    print("create user {}".format("cli"))
    print(current_app.config)


# 在init_app时
app.cli.add_command(usr_cli)

```



## gunicorn运行

app中create_app 并运行
gunicorn --bind 0.0.0.0

## 错误处理

celery AttributeError: 'float' object has no attribute 'items'
pyredis=redis-2.10.6 

Refusing to deserialize untrusted content of type pickle (application/x-python-serialize)
Received unregistered task of type 'jasmine_app.main.tasks.add'.
The message has been ignored and discarded.
使用新的导入方式
from proj.module import foo
from .module import foo