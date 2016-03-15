import random
from MashupMap import cache
from MashupMap.models import Mashup, Artist


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
            "title": mashup.title
        })
        for a1 in mashup.artists:
            artistset.add(a1)
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


@cache.cached(timeout=60*2, key_prefix='get_mashup_graph')
def get_mashup_graph():
    mashups = random.sample(Mashup.query.all(), 50)

    return graph_for_mashup_list(mashups)


@cache.cached(timeout=60*60*4, key_prefix='get_artist_mashups')
def get_artist_mashups(artist_name):
    # mashups = random.sample(Mashup.query.all(), 300)
    try:
        # later on, I'll implement the query using ID.
        artist = Artist.query.filter_by(name=artist_name).first()
    except:
        return get_mashup_graph()

    if artist:
        mashups = artist.artist_mashups
    else:
        return get_mashup_graph()

    return graph_for_mashup_list(mashups)
