import praw
import re
import MashupMap.music_api as m
import os
from MashupMap import cache
import random

user_agent = os.environ.get('USER_AGENT')
r = praw.Reddit(user_agent=user_agent)


def random_color():
    rc = lambda: random.randint(0, 255)
    return '#%02X%02X%02X' % (rc(), rc(), rc())


@cache.cached(timeout=60*60*4, key_prefix='get_mashup_graph')
def get_mashup_graph():
    submissions = r.get_subreddit('mashups').get_hot(limit=50)
    nodes = []
    edges = []
    songs = {}

    already_inserted = {}

    for submission in submissions:
        if not submission.is_self:
            # text_in_par is an array of strings found inside parenthesis
            text_in_par = re.findall('\(([^\)]+)\)', submission.title)
            # print(submission.media_embed)
            this_mashup_artists = []
            mashup_color = random_color()
            if len(text_in_par) > 0:
                artists_names = text_in_par[0].split(',')
                for name in artists_names:
                    # Check Music API to normalize name
                    new_artist = m.get_artist(name)
                    if new_artist is None:
                        continue
                    # Add artist to the current mashup list
                    this_mashup_artists.append(new_artist.artistID)
                    # If it's the first time we see this artist, create
                    # a new node
                    if new_artist.artistID not in already_inserted:
                        # Mark as inserted
                        already_inserted[new_artist.artistID] = True
                        # Insert in node list
                        nodes.append({
                            "id": new_artist.artistID,
                            "shape": "circularImage",
                            "image": new_artist.imageURL,
                            "label": new_artist.name
                            })

                    # Create Edges
                    for a1 in this_mashup_artists:
                        for a2 in this_mashup_artists:
                            # Don't repeat edges
                            if a1 < a2:
                                eid = len(edges)
                                edges.append({
                                    "from": a1,
                                    "to": a2,
                                    "id": eid,
                                    "color": mashup_color
                                    })
                                content = submission.media_embed.get('content')
                                author = submission.author.name
                                rurl = submission.permalink
                                if content is not None:
                                    songs[eid] = {
                                        "embed": content,
                                        "author": author,
                                        "redditurl": rurl
                                    }

    return nodes, edges, songs
