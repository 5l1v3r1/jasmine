# @Time    : 2018/9/24 下午2:14


from app import create_app

app = create_app()

if __name__ == '__main__':

    app.run(debug=True)
