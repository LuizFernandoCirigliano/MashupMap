import random
from MashupMap import cache
from MashupMap.models import Mashup, Artist
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
            "title": mashup.title,
            "db_id" : mashup.id
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
                    "title": mashup.title
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
                            "title": mashup.title
                        })
                        song_for_edge.append(song_id)

    for a in artistset:
        nodes.append({
            "id": a.id,
            "image": a.imageURL,
            "label": a.name
        })
    return nodes, edges, songs, song_for_edge


@cache.cached(timeout=60 * 2, key_prefix='get_mashup_graph')
def get_mashup_graph(mashup_id=None):
    mashups = random.sample(list(Mashup.query.filter(
        or_(Mashup.isBroken == None, Mashup.isBroken == False))), 100)

        #if a specific mashup was requested (from sharing maybe)
    if mashup_id:
        try: #get mashup from DB
            m = Mashup.query.filter_by(id=mashup_id).first()
        except Exception as e:
            print(e, e.args)
        else:
            # if mashup not already in list, add it.
            print('Mashup with id={} found!'.format(mashup_id))
            if m not in mashups:
                mashups.append(m)


    return graph_for_mashup_list(mashups)


def get_artist_mashups(artist_name):
    try:
        # later on, I'll implement the query using ID.
        artist = Artist.query.filter_by(name=artist_name).first()
    except:
        return get_mashup_graph()

    if artist:
        mashups = []
        # to use filter method on collection object, we would need to configure
        # the lazy attribute to dynamic.
        for m in artist.artist_mashups:
            if not m.isBroken:
                mashups.append(m)
        # print(mashups)

    else:
        return get_mashup_graph()

    return graph_for_mashup_list(mashups)
