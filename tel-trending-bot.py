import datetime
from pyquery import PyQuery as pq
import requests

BOT_TOKEN = os.getenv('BOT_TOKEN')  # 从 Secrets获取 Bot Token
CHAT_ID = os.getenv('CHAT_ID')  # 从 Secrets获取 Chat ID

def push2Bot(title, owner, description, url):
    URL = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
    now = datetime.datetime.now().strftime('%Y%m%d')
    data = {
        'chat_id': CHAT_ID,
        'text': f'#日期{now}\n*{title}*\n*{owner}*\n{description}\n{url}',
        'parse_mode': 'markdown'
    }
    requests.get(URL, params=data)


def scrape_top5(languages):
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:11.0) Gecko/20100101 Firefox/11.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip,deflate,sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8'
    }

    for language in languages:
        url = f'https://github.com/trending/{language}?since=daily'
        r = requests.get(url, headers=HEADERS)
        assert r.status_code == 200

        d = pq(r.content)
        items = d('div.Box article.Box-row')[:5]  # 只获取前5条数据

        for item in items:
            i = pq(item)
            title = i(".lh-condensed a").text()
            owner = i(".lh-condensed span.text-normal").text()
            description = i("p.col-9").text()
            url = i(".lh-condensed a").attr("href")
            url = "https://github.com" + url
            push2Bot(title, owner, description, url)


if __name__ == '__main__':
    languages = ['java']
    scrape_top5(languages)
