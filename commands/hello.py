from jasmine_app.extentions import usr_cli


@usr_cli.command('hello_cli')
def create_user():
    '''
    create user
    '''
    print('use cli correctly!')
