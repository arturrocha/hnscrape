import requests
import time


def get_item(news_id):
    if news_id == 'top_stories':
        url = 'https://hacker-news.firebaseio.com/v0/topstories.json?print=pretty'
    else:
        url = 'https://hacker-news.firebaseio.com/v0/item/{0}.json'.format(news_id)
    return requests.get(url).json()


def kids(news_id):
    kid = get_item(news_id)
    print(kid['text'])
    try:
        for reply in kid['kids']:
            kids(reply)
    except KeyError:
        pass


def read_news(news_id):
    res = get_item(news_id)
    if res['type'] == 'story':
        print('****', res['title'])
        print('***', res['url'])
        print('https://news.ycombinator.com/item?id={}'.format(news_id))
        end = input('read?')
        if end == 'y':
            try:
                for reply in res['kids']:
                    kids(reply)
            except KeyError:
                pass
        else:
            pass


def main():
    for news_id in get_item('top_stories'):
        read_news(news_id)


main()
