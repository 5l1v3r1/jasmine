import requests
from .utils import get_token
import json

access_token = get_token()


def send_message(access_token):
    url = "https://api.weixin.qq.com/cgi-bin/template/api_set_industry?access_token={}".format(
        access_token
    )
    data = {"industry_id1": "1", "industry_id2": "4"}
    json_data = json.dumps(data)
    res = requests.post(url=url, json=json_data)
    print(res.text)


def get_message():
    url = "https://api.weixin.qq.com/cgi-bin/template/get_all_private_template?access_token={}".format(
        access_token
    )
    res = requests.get(url)
    print(res.text)


if __name__ == "__main__":
    # send_message(access_token)
    get_message()
