import logging
import os

import requests
from bs4 import BeautifulSoup
from concurrent import futures
from crawler_utils.mongo_cache import MongoCache
from crawler_utils.utils import Http404Exception, url2path
from requests.exceptions import ReadTimeout

dir_path = os.path.dirname(__file__)


# 目的
# 抽出一个通用的爬虫框架
# 对于91视频和虎扑视频，只需改变首页Url和指定规则即可
class NoCrawler:
    def __init__(self, index_url, cache):
        self.index_url = index_url
        self.max_page = 0
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko)"
            " Chrome/72.0.3626.121 Safari/537.36"
        }
        self.cache = cache
        self.list_queue = [index_url]
        self.threshold = 0

    def run(self):
        """
        抓取每个视频html Url
        """
        list_url = "https://93.91p26.space/v.php?next=watch&page={}"
        while self.list_queue:
            url = self.list_queue.pop()
            try:
                res = requests.get(url=url, headers=self.headers, timeout=5)
            except ReadTimeout as e:
                logging.error(e.args, url)

            html = res.text
            # get list video
            self.extract_list_video_message(html)
            soup = BeautifulSoup(res.text, "html.parser")
            next_page = soup.find("div", {"class": "pagingnav"}).find("a").txt
            logging.info("下一页".format(next_page))
            self.list_queue.append(list_url.format(int(next_page)))

    def extract_list_video_message(self, html):
        """
        抓取列表页的html信息，保存
        :param html:
        :return:
        """

        def extract_url(video_url):
            try:
                res = requests.get(video_url, headers=self.headers, timeout=5)
            except ReadTimeout as e:
                logging.error(e.args, video_url)
            bs4 = BeautifulSoup(res.text, "html.parser")
            mp4_url = bs4.find("source")["src"]
            return mp4_url

        def parse_level(message):
            if message == "Not yet rated" or message == "还未被评分":
                return 0
            return len(message.split("\xa0")) - 1

        # return
        soup = BeautifulSoup(html, "html.parser")
        channels = soup.find_all("div", {"class": "listchannel"})
        message_list = []
        key_list = [
            "video_length",
            "published_time",
            "author",
            "view_times",
            "favorite_nums",
            "comments_nums",
            "points",
        ]
        for channel in channels:
            video_html_url = channel.find("a")["href"]
            if self.cache[video_html_url]:
                continue
            message_dict = {
                "url": extract_url(video_html_url),
                "title": channel.find("span", {"class": "title"}).text.strip(),
                "level": parse_level(
                    channel.find("div", {"class": "startratebox"}).find("span").text
                ),
            }
            # get video html url and enter get video url
            span_info = channel.find_all("span", {"class": "info"})
            for key, each_span in zip(key_list, span_info):
                message_dict[key] = each_span.next_element.next_element.strip()
            self.cache[video_html_url] = message_dict
            message_list.append(message_dict)
            print("success list_length:", len(message_list))
            # save in mysql
            self.save_in_database(message_list)
            # download_video
            self.download_videos([message["url"] for message in message_list])

    def save_in_database(self, message_list):
        from jasmine_app.models.video import Video

        for message in message_list:
            Video.update_or_create(url=message["url"], defaults=message)

    def download_videos(self, video_urls):
        with futures.ThreadPoolExecutor(3) as executor:
            executor.map(self._download_video, video_urls)

    def _download_video(self, url):
        if self.cache[url]:
            logging.error("视频已存在! 缓存出错 video_url: {}".format(url))
            return
        res = requests.get(url, stream=True)
        if res.status_code == 404:
            raise Http404Exception
        video_name = "{}.mp4".format(url2path(url))
        video_path = os.path.join("/data/videos/novideo", video_name)
        with open(video_path, "ab") as f:
            for chuck in res.iter_content(chunk_size=1024):
                f.write(chuck)
        logging.info("写入成功: {}".format(url))
        # url 和 path 进行映射
        self.cache[url] = video_path
        self.threshold += 1
        if self.threshold == 10:
            exit(0)

    def login(self):
        pass


def main():
    cache = MongoCache(db_name="hupu", collection_name="hupu")
    index_url = "http://93.91p26.space/v.php?next=watch"
    crawler = NoCrawler(index_url=index_url, cache=cache)
    crawler.run()


if __name__ == "__main__":
    main()
