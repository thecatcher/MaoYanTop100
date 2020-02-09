import json
import requests
from requests.exceptions import RequestException
import re
from multiprocessing import Pool


def get_one_page(url):
    # 注意这个headers,单纯写user-agent是不可以的,操蛋的反爬虫机制
    headers = {
        'Host': 'maoyan.com',
        'User-Agent': 'User-Agent  Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN'
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException as e:
        print("Bad request:" + e.info)


def parse_one_page(html):
    pattern = re.compile(
        '<dd>.*?board-index.*?">(\d+)</i>.*?data-src="(.*?)".*?</a>.*?name"><a.*?">(.*?)</a></p>.*?star">(.*?)</p>.*?releasetime">(.*?)</p>.*?integer">(.*?)</i>.*?fraction">(.*?)</i>.*?</dd>',
        re.S)
    items = re.findall(pattern, html)
    # print(items)
    for item in items:
        yield {
            'index': item[0],
            'image': item[1],
            'title': item[2],
            'actors': item[3].strip()[3:],
            'time': item[4].strip()[5:],
            'score': item[5] + item[6]
        }


def write_to_file(content):
    with open('result.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')
        f.close()


def main(offset):
    url = 'https://maoyan.com/board/4?offset=' + str(offset)
    html = get_one_page(url)
    parse_one_page(html)
    for item in parse_one_page(html):
        print(item)
        write_to_file(item)
    # print(html)


if __name__ == '__main__':
    # for i in range(10):
    #     main(i * 10)
    pool = Pool()
    pool.map(main, [i * 10 for i in range(10)])
