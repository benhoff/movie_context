import praw
from configparser import ConfigParser

from Levenshtein import ratio


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

quotes = config['quotes']
quotes = quotes[1:-1]
quotes = quotes.split(',')
quotes = [x.lstrip() for x in quotes]
quotes = tuple(quotes)
greatest_length = 0
least_length = 100

for quote in quotes:
    quote_len = len(quote)
    if quote_len > greatest_length:
        greatest_length = quote_len
    if quote_len < least_length:
        least_length = quote_len


for comment in reddit.subreddit('AskReddit+movies+funny+pics').stream.comments():
    text = comment.body.lower()
    len_text = len(text)
    if len_text + 7 > greatest_length or len_text - 4 < least_length:
        continue

    greatest = 0
    best_quote = ''
    print(text)

    for quote in quotes:
        value = ratio(text, quote)
        if value > .75:
            print(text, quote)
        """
        if value > greatest:
            greatest = value
            best_quote = quote
        """

    # print(greatest, text, best_quote)
