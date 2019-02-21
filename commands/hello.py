from jasmine_app.extentions import usr_cli


@usr_cli.command("hello_cli")
def create_user():
    """
    测试cli运行
    """
    print("use cli correctly!")
