import praw
import re
import music_api as m

r = praw.Reddit(user_agent='my_mashup_mapper')
submissions = r.get_subreddit('mashups').get_hot(limit=10)

for submission in submissions:
    if not submission.is_self:
        # text_in_par is an array of strings found inside parenthesis
        text_in_par = re.findall('\(([^\)]+)\)', submission.title)
        if len(text_in_par) > 0:
            artists_try = text_in_par[0].split(',')
            for a in artists_try:
                print(m.get_artist(a))


