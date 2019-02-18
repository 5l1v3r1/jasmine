import requests


def get_token():
    try:
        with open("token.txt", "r") as opener:
            token = opener.read()
    except FileNotFoundError:
        print("token file not found! please check the file path")
        return
    return token


get_token()


def get_token_from_wechat(app_id, app_secret):
    res = requests.get(
        url="https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={}&secret={}".format(
            app_id, app_secret
        )
    )
    access_token = res.json()["access_token"]

    with open("token.txt", "w") as opener:
        opener.write(access_token)
    return access_token
