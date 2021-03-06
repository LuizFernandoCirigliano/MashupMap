import praw
import re
import MashupMap.music_api as m
import os
from MashupMap import db
from populate_urls import get_url_from_embed
import link_checker

import datetime
from MashupMap.models import Mashup

KEY_LAST_REDDIT = 'last_reddit_mashup'

user_agent = os.environ.get('USER_AGENT', 'Default_User_Agent_For_Mashups')
r = praw.Reddit(user_agent=user_agent)


# gets clean title (without artists and duration of the mashup)
def get_clean_title(full_title):
    text_in_par = re.findall('\(([^\)]+)\) | \[([^\]]+)\]', full_title)
    if len(text_in_par) == 0 or len(text_in_par[0]) == 0:
        return full_title

    text_from_match = text_in_par[0][0] if text_in_par[
        0][0] != '' else text_in_par[0][1]
    index = full_title.find(text_from_match)
    title = full_title[:index - 1]
    return title


def save_clean_titles():
    mashups = Mashup.query.all()
    try:
        for m in mashups:
            m.clean_title = get_clean_title(m.title)
    except Exception as e:
        print('Unknown error')
        print(e, e.args)
    except:
        print('User interruption.')
    finally:
        db.session.commit()


def save_new_artist_list():
    mashups = Mashup.query.all()
    try:
        for i, mashup in enumerate(mashups):
            artist_list = artist_list_from_title(mashup.title)
            if not artist_list:
                continue
            print(i)
            # print(str(i), mashup.title, str(artist_list))
            mashup.artists = []
            for name in artist_list:
                # Check Music API to normalize name
                new_artist = m.get_artist(name)
                if new_artist is not None:
                    # Add artist to the current mashup
                    mashup.artists.append(new_artist)
    except Exception as e:
        print('Unknown error')
        print(e, e.args)
    except:
        print('User interruption.')
    finally:
        db.session.commit()


def strip_artist_name(match):
    print(match)
    # ft_pat = '\s+[fF](ea)?[tT]\.?\s+'
    # names_pat = '[\w\s]+'
    comma_pat = '\s*,\s*'
    vs_pat = '\s+[vV][sS]?\.?\s+'
    x_pat = '\s+[xX]\s+'

    divider = re.findall(comma_pat + '|' + vs_pat + '|' + x_pat, match)
    # print(divider)
    try:
        strip_string = divider[0]
    except IndexError as e:
        print('Index error!!')
        print(e, e.args)
        return None

    artist_list = match.split(strip_string)
    # print(artist_list)
    return artist_list


def artist_list_from_title(title):
    # text_in_par is an array of tuples. Each tuple contains a match for at
    # least one of the cases in the regex. If the first case is found, the
    # match is stored on the position 0 of the tuple,
    # if the second case if found, its stored in the position 1 of the tuple.
    text_in_par = re.findall('\(([^\)]+)\) | \[([^\]]+)\]', title)
    if len(text_in_par) == 0 or len(text_in_par[0]) == 0:
        return None

    text_from_match = text_in_par[0][0] if text_in_par[
        0][0] != '' else text_in_par[0][1]
    # print(text_from_match)
    # artists_names = [x.strip() for x in text_from_match.split(',')]
    # return artists_names
    return strip_artist_name(text_from_match)


def insert_submission_in_db(submission):
    if submission.is_self:
        return None

    artists_names = artist_list_from_title(submission.title)
    if artists_names is None:
        return None
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
    # print(content)
    url = get_url_from_embed(content)
    # print(url)
    clean_title = get_clean_title(submission.title)

    # isBroken = link_checker.check_link(url)
    # checking for broken links takes longer and new links are rarely broken.
    isBroken = False
    check_mash = Mashup.query.filter_by(
        permalink=reddit_url
    ).first()
    if check_mash is not None:
        return check_mash

    print(clean_title)
    mashup = Mashup(
        title=submission.title,
        author=author,
        permalink=reddit_url,
        date=date,
        content=content,
        url=url,
        isBroken=isBroken,
        clean_title=clean_title
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

        # last = pdb.get(KEY_LAST_REDDIT)
        # if last is None or submission.id > last:
        #     pdb.set(KEY_LAST_REDDIT, last)
    except:
        db.session.rollback()
    return mashup


def download_new_submissions():
    # last = pdb.get(KEY_LAST_REDDIT)
    # submissions = r.get_subreddit('mashups').get_hot(
    #     after_field='after',
    #     params={
    #         "after": last
    #     },
    #     limit=None
    # )
    submissions = r.get_subreddit('mashups').get_hot(
        limit=200
    )
    for submission in submissions:
        insert_submission_in_db(submission)


def download_top_submissions():
    submissions = r.get_subreddit('mashups').get_top_from_all(
        limit=None
    )
    for submission in submissions:
        insert_submission_in_db(submission)
