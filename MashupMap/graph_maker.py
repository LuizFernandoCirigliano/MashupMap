import random
from MashupMap import cache
from MashupMap.models import Artist, Mashup


def random_color():
    rc = lambda: random.randint(0, 255)
    return '#%02X%02X%02X' % (rc(), rc(), rc())


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
                        "color": mashup_color,
                        "title": mashup.title
                        })
                    songs[eid] = {
                        "embed": mashup.content,
                        "author": mashup.author,
                        "redditurl": mashup.permalink
                    }

    return nodes, edges, songs
