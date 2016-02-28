import praw
import re
import MashupMap.music_api as m
import os
from MashupMap import db
import pickledb
import datetime
from MashupMap.models import Mashup

KEY_LAST_REDDIT = 'last_reddit_mashup'
pdb = pickledb.load('pickle.db', False)

user_agent = os.environ.get('USER_AGENT')
r = praw.Reddit(user_agent=user_agent)


def artist_list_from_title(title):
    # text_in_par is an array of tuples. Each tuple contains a match for at
    # least one of the cases in the regex. If the first case is found, the
    # match is stored on the position 0 of the tuple,
    # if the second case if found, its stored in the position 1 of the tuple.
    text_in_par = re.findall('\(([^\)]+)\) | \[([^\]]+)\]', title)
    if len(text_in_par) == 0 or len(text_in_par[0]) == 0:
        return None

    text_from_match = text_in_par[0][0] if text_in_par[0][0] != '' else text_in_par[0][1]

    artists_names = [x.strip() for x in text_from_match.split(',')]
    return artists_names


def insert_submission_in_db(submission):
    if submission.is_self:
        return None

    artists_names = artist_list_from_title(submission.title)
    content = submission.media_embed.get('content')
    if content is None:
        return None

    author = None
    if submission.author:
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
    try:
        db.session.add(mashup)
        db.session.commit()

        last = pdb.get(KEY_LAST_REDDIT)
        if last is None or submission.id > last:
            pdb.set(KEY_LAST_REDDIT, last)
    except:
        db.session.rollback()
    return mashup


def download_new_submissions():
    last = pdb.get(KEY_LAST_REDDIT)
    submissions = r.get_subreddit('mashups').get_hot(
        after_field='after',
        params={
            "after": last
        },
        limit=None
    )
    for submission in submissions:
        insert_submission_in_db(submission)


def download_top_submissions():
    submissions = r.get_subreddit('mashups').get_top_from_all(
        limit=None
    )
    for submission in submissions:
        insert_submission_in_db(submission)
