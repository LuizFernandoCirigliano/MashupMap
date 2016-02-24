import praw
import re
import music_api as m
import os

user_agent = os.environ.get('USER_AGENT')

r = praw.Reddit(user_agent=user_agent)
submissions = r.get_subreddit('mashups').get_hot(limit=10)

for submission in submissions:
    if not submission.is_self:
        # text_in_par is an array of strings found inside parenthesis
        text_in_par = re.findall('\(([^\)]+)\)', submission.title)
        if len(text_in_par) > 0:
            artists_try = text_in_par[0].split(',')
            for a in artists_try:
                print(m.get_artist(a))


