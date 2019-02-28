import logging
from functools import wraps
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from crawler_utils import MongoCache
from fake_useragent import FakeUserAgent
from utils.redis_keys import HUPU_PAGE_INDEX_KEY
from redis import Redis
import logging.handlers

base_video_url = "https://bbs.hupu.com/4858-{}"
base_url = "https://bbs.hupu.com"


def set_logger(logger_name):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    handler = logging.handlers.RotatingFileHandler(logger_name, maxBytes=102400)
    # logger.addHandler(handler)
    return logger


class HupuVideoCrawler:
    def __init__(self, cache=None):
        self.user_agent = FakeUserAgent()
        self.headers = {"user-agent": self.user_agent.random}
        if cache:
            self.cache = cache
        else:
            self.cache = MongoCache(
                db_name="hupu_crawler", username="root", password="newpass"
            )
        self.logger = set_logger("hupu_crawler")
        self.redis_client = Redis()

    def mongo_cache(self, func):
        @wraps(func)
        def mongo_cached(*args, **kwargs):
            key = kwargs.get("key")
            if key:
                collection_name = kwargs.get("collection_name", "default")
                try:
                    return self.cache.get(collection_name, key)
                except KeyError:
                    pass
            return func

        return mongo_cached

    def get_video_html_messages(self, page_nums=50):
        """
        get video_html_urls then parse get video urls
        example: https://bbs.hupu.com/4858-1
        :param page_nums:
        :return:
        """

        def parse_list_html(html):
            """
             <a class="truetit" href="/25595900.html" target="_blank">zt对会跳舞的小姐姐毫无抵抗力</a>
            :param html:
            :return:
            """
            soup = BeautifulSoup(html, "html.parser")
            videos = soup.find_all("div", {"class": "titlelink box"})

            for video in videos:
                yield (urljoin(base_url, video.a["href"]), video.a.text)

        collection_name = "video_html"
        page_begin_index = int(self.redis_client.get(HUPU_PAGE_INDEX_KEY))
        if not page_begin_index:
            page_begin_index = 1

        for page_index in range(page_begin_index, page_nums):
            url = base_video_url.format(page_index)
            try:
                html = self.cache.get(collection_name=collection_name, key=url)
                print(self.cache.length(collection_name), "length")
                self.logger.info(msg="get html from cache: {}".format(url))
            except KeyError:
                res = requests.get(url=url, timeout=10)
                html = res.text
                self.logger.warning(
                    msg="cached does not exist, go request url:{} status_code: {}".format(
                        url, res.status_code
                    )
                )
                self.cache.set(collection_name=collection_name, key=url, value=html)
            yield parse_list_html(html)
        #     更新Index值
        self.redis_client.set(HUPU_PAGE_INDEX_KEY, page_begin_index + page_nums)

    def get_video_messages(self, video_html_messages):
        """
        parse video_messages and download video
        :param video_html_messages: tuple
        :return:
        """
        collection_name = "video_html_urls"

        def get_video_url(video_html_url):
            res = requests.get(video_html_url, headers=self.headers)
            soup = BeautifulSoup(res.text, "html.parser")
            try:
                video_url = soup.find("video")["src"]
            except TypeError:
                self.logger.debug(
                    u"outlink can not be downloaded: video_html_url: {}".format(
                        video_html_url
                    )
                    .encode("utf-8")
                    .strip()
                )
                return
            self.logger.warning(
                "cached does not exist, get video url:{} status_code: {}".format(
                    video_url, res.status_code
                )
            )
            return video_url

        for page_messages in video_html_messages:
            for video_html_url, video_title in page_messages:
                try:
                    video_url = self.cache.get(collection_name, key=video_html_url)[
                        "video_url"
                    ]
                    self.logger.info(
                        msg="get video_url from cache: {} video_title: {}".format(
                            video_url, video_title
                        )
                    )
                except KeyError:
                    video_url = get_video_url(video_html_url)
                    if not video_url:
                        continue
                    self.cache.set(
                        collection_name,
                        video_html_url,
                        {"video_url": video_url, "video_title": video_title},
                    )
                yield video_url, video_title

    def download_videos(self, video_messages):
        """
        get video_urls from video_messages and save video to local path
        :param video_messages:
        :return:
        """
        collection_name = "video_urls"

        # save to local path

        def save(io_content, file_name):
            file_path = urljoin("/data/hupu_crawler/", file_name + ".mp4")
            with open(file_path, "wb") as opener:
                for chunk in io_content:
                    opener.write(chunk)
                    opener.flush()
            self.logger.warning("save video in local path {}".format(file_path))

        for video_url, video_title in video_messages:
            try:
                self.cache.get(collection_name, video_url)
                self.logger.info("video_url {} exist in cache !".format(video_url))
            except KeyError:
                video_messages = {"video_url": video_url, "video_title": video_title}
                self.cache.set(collection_name, video_url, video_messages)
                res = requests.get(video_url, headers=self.headers, stream=True)
                save(res.iter_content(chunk_size=1024), video_title)

    def main(self):
        # video_urls
        video_html_messages = self.get_video_html_messages()
        # get video_messages
        video_messages = self.get_video_messages(video_html_messages)
        # download videos and save to local path
        self.download_videos(video_messages)


if __name__ == "__main__":
    hupu_crawler = HupuVideoCrawler(
        cache=MongoCache("root", "newpass", host="127.0.0.1", db_name="hupu")
    )
    hupu_crawler.main()
