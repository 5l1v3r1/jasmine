# jasmine

此项目为练习和使用flask一些有趣的扩展和特性的demo。
因为主要作为学习和实验，所以项目的代码不会太多。学习和理解起来也不会有太大的压力
所有的扩展或特性全部基于flask factory模式 create_app


## 已经完成

- 完整的docker+docker-compose+ci/cd流程 一键部署热更新代码到云主机
- flask cli 通过FlaskGroup来管理所有commands，运行脚本
- flask factory模式 结合celery 创建异步任务队列
- flask+redis 配置缓存
- 自动从.env文件加载配置
- flask 每次加载自动刷新js和css文件,提高开发效率
- 配置sentry 自动监控 和ignore log设置
- flask-env 从.env文件中加载配置
- flask+pytest 进行单元测试,配置数据库
- flask和peewee进行集成
- celery定时抓取视频数据，写入数据库，通过 backbone.js+flask 单页面应用和restful api集成

## 待完成

- 微信公众号后台api接口
- 爬虫定时抓取、清洗、显示hupu视频数据+Elasticsearch搜索

## ci/cd 持续集成&持续部署

通过gitlab ci+docker-compose 完成个人项目的持续发布
docker-compose： nginx+mysql+redis 通过Dockerfile将程序运行在容器中
保证每次Push代码，线上的代码可以一键更新。
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
### 运行celery

celery worker -B -A run_celery.celery --loglevel=info
celery beat -A run_celery.celery -l info
将celery添加到docker-compose中执行命令,celery应该拥有代码和安装的资源包


## flask +peewee

peewee是一个好用的轻量级orm,语法简单，文档完善，易扩展
peewee 和flask集成，主要在三个地方
1. 每次请求前before_request和after_request进行connect_db和disconnect
2. 在创建model的时候需要在meta中绑定database。database的初始化放在了FlaskPeewee init_app的时候
通过FLaskPeewee类中继承下peewee的Model，在新的model中声明database为self.database即可。通过cache_property
将Model声明为带缓存的属性。然后在定义model时，直接继承自这个新定义的model即可。

```python
    @cached_property
    def Model(self):
        class BaseModel(Model):
            class Meta:
                database = self.database

        return BaseModel
```
3. migration的管理。目前是通过脚本来手动执行，即在command文件夹中创建cli命令，在这里需要注意下循环依赖
的问题。具体的原因在代码中有说明。

### 发布镜像到docker.io

- docker build --cache-from jasmine:latest -t jasmine:latest .
- docker tag jasmine:latest fjl2401/jasmine
- docker push fjl2401/jasmine


## flask-env

### python-dotenv

适用方法：`flask run`

python-dotenv 在create_app实例前将.env文件载入os的环境变量

安装: pip install python-dotenv
在root目录下加入.env文件 .env文件中加入配置:
- FLASK_DEBUG=True or False
- FLASK_APP=jasmin_app
- FLASK_ENV=development
- FLASK_RUN_PORT=3000

### FlaskEnv

适用方法： `python run.py runserver`

FlaskEnv将.env文件在create_app后加载到app的config中。

flask在工厂模式下创建app,在import_app时，会先create_app 返回app实例，然后再加载配置，重新启动app。
而FaskEnv是在extension文件中,是在通过工厂模式加载extention,是在create_app后。所以debug或者port不会生效。
但会加载一些静态的配置，比如:
- MAIL_SUBJECT_PREFIX = [jasmine]
- MAIL_SENDER = fjl2401@qq.com
在程序运行后，这些配置被载入到app.config中。


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
## pre-commit

在git每次提交的时候运行pre-commit来规范自己的代码，属于静态检查工具，添加的检查工具有:
- flake8
- black
- pre-commit 官方的hook来约束代码的Import格式和空格

### 使用方法

1. pip intsall pre-commit
2. 在项目下pre-commit install
3. 配置.pre-commit-config.yaml 具体内容见: [Github](https://github.com/pre-commit/pre-commit-hooks/)



## gunicorn运行

app中create_app 并运行
gunicorn --bind 0.0.0.0:5001 run:app


## backbone.js

前端mvc框架，学习简单，易使用。作用是在jquery的基础上进行扩展，通过rest api去请求，存储，展示数据。
处理事件响应。

## 错误处理

celery AttributeError: 'float' object has no attribute 'items'
pyredis=redis-2.10.6

Refusing to deserialize untrusted content of type pickle (application/x-python-serialize)
Received unregistered task of type 'jasmine_app.main.tasks.add'.
The message has been ignored and discarded.
使用新的导入方式
from proj.module import foo
from .module import foo
