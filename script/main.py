import json
import common
import requests
from bs4 import BeautifulSoup

def desc_encode(str):
    words = str.split()

    cleaned_words = []
    for word in words:
        cleaned_word = "".join(char for char in word if not char.isascii() or char.isalnum())
        cleaned_words.append(cleaned_word)

    return " ".join(cleaned_words)

def write_markdown(data, description):
    title = data['title']
    author = data['author']
    date = data['time']
    content = data['content']
    description = desc_encode(description)

    if title[0] == '[':
        title = '![]' + title

    print(f'Writing article: "{title}" by {author}...')

    markdown = f'''---
title: {title}
date: {date}
description: {description}
author: {author}
---

{content}
'''

    file_path = f'./articles/{data["author"]}-{data["lid"]}.md'

    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(markdown)

    return file_path

def fetch_article(lid, description=''):
    url = f'https://www.luogu.com/article/{lid}'

    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html5lib')
    script_tag = soup.find('script', id='lentille-context')

    data = json.loads(script_tag.string)

    data = data['data']['article']
    data['author'] = data['author']['uid']
    data['content'] = write_markdown(data, description)

    return data

def fetch_user_articles(uid):
    article_list = []
    for i in range(1, 999):
        print(f'Fetching page {i} for user {uid}...')
        data = common.fetch_json(f'https://www.luogu.com/api/article/find?user={uid}&page={i}')
        if len(data['articles']['result']) == 0:
            break
        article_list += data['articles']['result']
    print(f'Found {len(article_list)} articles for user {uid}.')
    return [fetch_article(article['lid'], description=article['content']) for article in article_list]

if __name__ == "__main__":
    uid_list = common.load_json('uid.json')['uid_list']
    all_articles = []
    for uid in uid_list:
        print(f'Fetching articles for user {uid}...')
        user_articles = fetch_user_articles(uid)
        all_articles += user_articles
        common.write_json(f'./data/articles.{uid}.json', user_articles)
        print(f'Finished fetching articles for user {uid}.')
    common.write_json(f'./data/articles.json', all_articles)
    print('All articles fetched and saved.')
