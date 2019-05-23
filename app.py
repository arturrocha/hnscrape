import requests
import time
import newspaper
from newspaper import Article


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


def read_news(news_id, count, total):
    res = get_item(news_id)
    if res['type'] == 'story':
        try:
            print('*******************************************************')
            print('****', res['title'])
            print('*******************************************************')
            print('***', res['url'])
        except Exception as e:
            print(e)
        print('*** https://news.ycombinator.com/item?id={}'.format(news_id))
        request = input('{0}/{1} next? >'.format(count, total))
        if request == 'n':
            print('****************')
            article = Article(res['url'])
            article.download()
            article.parse()
            print(article.text)
            article.nlp()
            print('***', article.keywords)
            print('****************')
            comments = input('{0}/{1} read comments? Def N >'.format(count, total))
            if comments == 'y':
                try:
                    for reply in res['kids']:
                        print('*>')
                        kids(reply)
                except KeyError:
                    pass


def main():
    top = get_item('top_stories')
    count = 0
    total = len(top)
    for news_id in top:
        count += 1
        read_news(news_id, count, total)


main()
