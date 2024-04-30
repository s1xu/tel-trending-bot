import datetime
from pyquery import PyQuery as pq
import requests
import os
import time

BOT_TOKEN = os.getenv('BOT_TOKEN')  # Get BOT_TOKEN from Secrets
CHAT_ID = os.getenv('CHAT_ID')  # Get Chat ID from Secrets
TRANSLATE_URL = os.getenv('TRANSLATE_URL')


def translate_text(text, source_lang, target_lang):
    translate_url = TRANSLATE_URL
    payload = {
        "text": text,
        "source_lang": source_lang,
        "target_lang": target_lang
    }
    response = requests.post(translate_url, json=payload)
    translated_text = response.json().get('data')
    return translated_text


def push2bot(title, language, description, url):
    language = language or 'all'
    URL = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
    translated_description = translate_text(description, 'en', 'zh')
    now = datetime.datetime.now().strftime('%Y%m%d')
    data = {
        'chat_id': CHAT_ID,
        'text': f'*{title}*\n{description}`\n{translated_description}\n`\n#日期{now}  #{language}   [Repo URL]({url}) ',
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
        items = d('div.Box article.Box-row')[:10]  # Get the first 10 pieces of data

        for item in items:
            i = pq(item)
            title = i(".lh-condensed a").text()
            # owner = i(".lh-condensed span.text-normal").text()
            description = i("p.col-9").text()
            url = i(".lh-condensed a").attr("href")
            url = "https://github.com" + url
            push2bot(title, language, description, url)
            time.sleep(2)


if __name__ == '__main__':
    languages = ['', 'java', 'javascript', 'python', 'go']
    scrape_top5(languages)
