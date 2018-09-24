import requests
from utils import get_token, get_token_from_wechat
from config import test_app_id, test_app_secret

# token = get_token_from_wechat(app_id=test_app_id, app_secret=test_app_secret)


token=get_token()
res = requests.post('https://api.weixin.qq.com/cgi-bin/user/info/batchget?access_token={}'.format(token))

print(res.json())
print(res.text)
