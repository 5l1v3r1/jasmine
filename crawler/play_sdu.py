import requests

cookies = "JSESSIONID=abcne4W3I4ZjbhpYqkhLw; sduxk=435fede2ec4e12552892902a4096f24d; index=1; j_username=201500301304; j_password=771803"
url = "http://bkjws.sdu.edu.cn/f/common/main"
res = requests.session().get(url=url, headers={"Cookie": cookies})
