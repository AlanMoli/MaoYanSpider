import requests
from requests.exceptions import RequestException
from lxml import etree
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


# XPath提取
def parse_one_page(html):
    html = etree.HTML(html)
    index = html.xpath('//i[contains(@class, "board-index")]//text()')
    image = html.xpath('//img/@data-src')
    name = html.xpath('//p[@class="name"]//text()')
    actor = html.xpath('//p[@class="star"]//text()')
    times = html.xpath('//p[@class="releasetime"]//text()')
    integer = html.xpath('//i[@class="integer"]/text()')
    fraction = html.xpath('//i[@class="fraction"]/text()')
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
