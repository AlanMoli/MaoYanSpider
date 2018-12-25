import requests
from requests import RequestException
from bs4 import BeautifulSoup
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


# Beautiful Soup提取
def parse_one_page(html):
    soup = BeautifulSoup(html, 'lxml')

    # 提取排名
    index = []
    for Index in soup.find_all(class_="board-index"):
        index.append(Index.string)

    # 提取图片
    image = []
    for Image in soup.find_all(class_="board-img"):
        image.append(Image['data-src'])

    # 提取片名
    name = []
    for Name in soup.find_all(class_="name"):
        name.append(Name.string)

    # 提取主演
    actor = []
    for Actor in soup.find_all(class_="star"):
        actor.append(Actor.string)

    # 提取时间
    times = []
    for Times in soup.find_all(class_="releasetime"):
        times.append(Times.string)

    # 提取评分
    integer = []
    for Integer in soup.find_all(class_="integer"):
        integer.append(Integer.string)

    fraction = []
    for Fraction in soup.find_all(class_="fraction"):
        fraction.append(Fraction.string)

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
