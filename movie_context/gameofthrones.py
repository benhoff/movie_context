import praw
from configparser import ConfigParser
import requests
import pprint
import code
import pickle

from lossy_count import LossyCount


def _recursive_reply_handle(replies: dict, lossy_count: LossyCount, total_count: int):
    children = replies['data']['children']
    for child in children:
        comment = child['data']

        total_count += 1
        # keys include `kind` and `data`. We want data
        body = comment.get('body')

        if body is None or body == '.':
            continue

        if comment.get('replies'):
            _recursive_reply_handle(comment['replies'], lossy_count, total_count)

        if len(body) > 60:
            continue
        print(body)
        lossy_count[body] = 1

def _loop(reddit: praw.Reddit, lossy_count: LossyCount, total_count: int):
    headers = {'user-agent': 'archive by /u/beohoff'}
    for post in reddit.subreddit('gameofthrones').submissions(end=1507098238, start=1351578237):
        json_url = 'https://reddit.com' + post.permalink + '.json'
        try:
            response = requests.get(json_url, headers=headers)
        except Exception as e:
            print(e)
            bread = input()
        try:
            data = response.json()
        except json.decoder.JSONDecodeError:
            # continue
            return
        # data[0] contains post information. data[1] contains comment info
        for comment in data[1]['data']['children']:
            total_count += 1
            # keys include `kind` and `data`. We want data
            comment = comment['data']
            body = comment.get('body')
            if body is None:
                continue
            if len(body) > 60:
                continue
            print(body)
            lossy_count[body] = 1
            """
            ups = comment['ups']
            downs = comment['downs']
            gilds = comment['gilded']
            parent_text = None
            """
            if comment.get('replies'):
                _recursive_reply_handle(comment['replies'], lossy_count, total_count)


def main():
    USER_AGENT = 'Ask Reddit Bot by /u/beohoff'

    parser = ConfigParser()
    parser.read('/home/hoff/.config/vexbot/movie_context.ini')
    parser = {s:dict(parser.items(s)) for s in parser.sections()}

    config = parser['default']

    reddit = praw.Reddit(client_id=config['client_id'],
                         client_secret=config['client_secret'],
                         password=config['password'],
                         username=config['username'],
                         user_agent=USER_AGENT)

    total_count = 0
    # will store 10,000 items
    lossy_count = LossyCount(.0001)
    try:
        _loop(reddit, lossy_count, total_count)
    except KeyboardInterrupt:
        pass

    print(lossy_count._count)
    with open('dict.pickle', 'wb') as f:
        pickle.dump(lossy_count._count, f)

    print(lossy_count._n)
    print(total_count)


if __name__ == '__main__':
    main()
