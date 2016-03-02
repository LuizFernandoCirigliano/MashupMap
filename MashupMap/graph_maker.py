import random
from MashupMap import cache
from MashupMap.models import Mashup


def random_color():
    rc = lambda: random.randint(0, 255)
    return '#%02X%02X%02X' % (rc(), rc(), rc())


@cache.cached(timeout=60*2, key_prefix='get_mashup_graph')
def get_mashup_graph():
    artistset = set()
    nodes = []
    edges = []
    songs = []

    mashups = random.sample(Mashup.query.all(), 300)

    for mashup in mashups:
        mashup_color = random_color()
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
                    songs.append({
                        "embed": mashup.content,
                        "author": mashup.author,
                        "redditurl": mashup.permalink,
                        "title": mashup.title
                    })

    for a in artistset:
        nodes.append({
            "id": a.id,
            "image": a.imageURL,
            "label": a.name
        })
    return nodes, edges, songs
