import random
from MashupMap import cache
from MashupMap.models import Mashup, Artist, Counters
from sqlalchemy import or_


def random_color():
    rc = lambda: random.randint(0, 255)
    return '#%02X%02X%02X' % (rc(), rc(), rc())


def graph_for_mashup_list(mashups):
    artistset = set()
    nodes = []
    edges = []
    songs = []
    song_for_edge = []
    for mashup in mashups:
        mashup_color = random_color()
        song_id = len(songs)
        songs.append({
            "embed": mashup.content,
            "author": mashup.author,
            "redditurl": mashup.permalink,
            "title": mashup.clean_title,
            "db_id" : mashup.id,
            "artists" : [a.name for a in mashup.artists]
        })
        artistset |= set(mashup.artists)
        art_len = len(mashup.artists)
        if art_len >= 4:
            for i in range(art_len):
                a1 = mashup.artists[i]
                a2 = mashup.artists[(i + 1) % art_len]
                eid = len(edges)
                edges.append({
                    "from": a1.id,
                    "to": a2.id,
                    "id": eid,
                    "color": mashup_color,
                    "title": mashup.clean_title
                })
                song_for_edge.append(song_id)
        else:
            for a1 in mashup.artists:
                for a2 in mashup.artists:
                    if a1.id < a2.id:
                        eid = len(edges)
                        edges.append({
                            "from": a1.id,
                            "to": a2.id,
                            "id": eid,
                            "color": mashup_color,
                            "title": mashup.clean_title
                        })
                        song_for_edge.append(song_id)

    for a in artistset:
        nodes.append({
            "id": a.id,
            "image": a.imageURL,
            "label": a.name
        })
    return nodes, edges, songs, song_for_edge

def get_default_mashup(default_id=None):
    if default_id is None:
        default_counter = Counters.query.filter_by(key='defmashup').first()
        default_id = default_counter.value
    if default_id is not None:
        default_mashup = Mashup.query.get(default_id)
        return None if default_mashup.isBroken else default_mashup

# @cache.cached(timeout=60 * 2, key_prefix='get_mashup_graph')
def get_mashup_graph(mashup_id=None):
    mashups = random.sample(list(Mashup.query.filter(
        or_(Mashup.isBroken == None, Mashup.isBroken == False))), 100)

    default_mashup = get_default_mashup(mashup_id)
    if default_mashup is not None:
        mashups.insert(0, default_mashup)
    return graph_for_mashup_list(mashups)


def get_artist_mashups(artist_name):
    try:
        artist = Artist.query.filter_by(name=artist_name).first()
    except:
        return get_mashup_graph()

    if artist:
        mashups = [m for m in artist.artist_mashups if not m.isBroken == True]
    else:
        return get_mashup_graph()

    return graph_for_mashup_list(mashups)
