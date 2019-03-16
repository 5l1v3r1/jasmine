import requests

login_url = "https://93.91p26.space/login.php"

HEADERS = {
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv",
    # "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "accept-language": " zh-CN,zh;q=0.9,en;q=0.8",
    # "Accept-Encoding": "gzip, deflate",
}

res = requests.get(login_url, headers=HEADERS)
