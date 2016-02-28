import praw
import re
import MashupMap.music_api as m
import os
from MashupMap import cache, db
import random
import pickledb
import datetime
from MashupMap.models import Artist, Mashup

KEY_LAST_REDDIT = 'last_reddit_mashup'
pdb = pickledb.load('pickle.db', False)

user_agent = os.environ.get('USER_AGENT')
r = praw.Reddit(user_agent=user_agent)


def random_color():
    rc = lambda: random.randint(0, 255)
    return '#%02X%02X%02X' % (rc(), rc(), rc())


def insert_submission_in_db(submission):
    if submission.is_self:
        return None
    # text_in_par is an array of strings found inside parenthesis
    text_in_par = re.findall('\(([^\)]+)\)', submission.title)
    if len(text_in_par) == 0:
        return None

    artists_names = text_in_par[0].split(',')

    content = submission.media_embed.get('content')
    if content is None:
        return None

    author = submission.author.name
    reddit_url = submission.permalink
    date = datetime.datetime.utcfromtimestamp(
        submission.created_utc
    )

    check_mash = Mashup.query.filter_by(
        permalink=reddit_url
    ).first()
    if check_mash is not None:
        return check_mash

    mashup = Mashup(
        title=submission.title,
        author=author,
        permalink=reddit_url,
        date=date,
        content=content
    )

    for name in artists_names:
        # Check Music API to normalize name
        new_artist = m.get_artist(name)
        if new_artist is not None:
            # Add artist to the current mashup
            mashup.artists.append(new_artist)
    db.session.add(mashup)
    db.session.commit()

    last = pdb.get(KEY_LAST_REDDIT)
    if last is None or submission.id > last:
        pdb.set(KEY_LAST_REDDIT, last)

    return mashup


def download_new_submissions():
    last = pdb.get(KEY_LAST_REDDIT)
    submissions = r.get_subreddit('mashups').get_hot(
        after_field='after',
        params={
            "after": last
        }
    )
    for submission in submissions:
        insert_submission_in_db(submission)


@cache.cached(timeout=60*60*4, key_prefix='get_mashup_graph')
def get_mashup_graph():
    nodes = []
    edges = []
    songs = {}

    artists = Artist.query.all()
    mashups = Mashup.query.all()

    for artist in artists:
        nodes.append({
            "id": artist.id,
            "shape": "circularImage",
            "image": artist.imageURL,
            "label": artist.name
        })
    for mashup in mashups:
        mashup_color = random_color()
        for a1 in mashup.artists:
            for a2 in mashup.artists:
                if a1.id < a2.id:
                    eid = len(edges)
                    edges.append({
                        "from": a1.id,
                        "to": a2.id,
                        "id": eid,
                        "color": mashup_color
                        })
                    songs[eid] = {
                        "embed": mashup.content,
                        "author": mashup.author,
                        "redditurl": mashup.permalink
                    }

    return nodes, edges, songs
