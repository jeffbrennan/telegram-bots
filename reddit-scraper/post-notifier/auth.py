import praw
import pandas as pd

REDDIT_AUTH = pd.read_csv('./auth/reddit.csv').squeeze()
reddit = praw.Reddit(client_id=REDDIT_AUTH[0],
                     client_secret=REDDIT_AUTH[1],
                     user_agent='my user agent',
                     username=REDDIT_AUTH[2],
                     password=REDDIT_AUTH[3])

TELEGRAM_AUTH = open('./auth/telegram.txt', 'r').read()
jeff = pd.read_csv('./auth/id.csv', header=None).squeeze()
