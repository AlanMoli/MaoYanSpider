import requests
from requests import RequestException
from pyquery import PyQuery as pq
import time


# 抓取网页
def get_one_page(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/67.0.3396.99 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None


# pyquery提取
def parse_one_page(html):
    doc = pq(html)

    # 提取排名
    index = []
    for Index in doc('.board-index').items():
        index.append(Index.text())

    # 提取图片
    image = []
    for Image in doc('.board-img').items():
        image.append(Image.attr('data-src'))

    # 提取片名
    name = []
    for Name in doc('.name').items():
        name.append(Name.text())

    # 提取主演
    actor = []
    for Actor in doc('.star').items():
        actor.append(Actor.text())

    # 提取时间
    times = []
    for Times in doc('.releasetime').items():
        times.append(Times.text())

    # 提取评分
    integer = []
    for Integer in doc('.integer').items():
        integer.append(Integer.text())

    fraction = []
    for Fraction in doc('.fraction').items():
        fraction.append(Fraction.text())

    for j in range(10):
        yield {
            '排名': index[j],
            '图片': image[j],
            '片名': name[j],
            '主演': actor[j].strip()[3:],
            '时间': times[j].strip()[5:],
            '评分': integer[j] + fraction[j]
        }


def main(offset):
    url = "https://maoyan.com/board/4?offset=" + str(offset)
    html = get_one_page(url)
    for item in parse_one_page(html):
        print(item)


if __name__ == '__main__':
    for i in range(10):
        main(offset=i * 10)
        time.sleep(1)
