from flask import render_template, jsonify
from MashupMap.graph_maker import get_mashup_graph, get_artist_mashups
from MashupMap import app
from MashupMap.analytics import count_stuff
from MashupMap.music_api import get_artist


@app.route("/")
@app.route("/full")
def hello_full():

    return render_template(
        'mashupmap-full.html'
        )


@app.route("/graph")
def get_graph():
    nodes, edges, songs = get_mashup_graph()
    return jsonify({
        "nodes": nodes,
        "edges": edges,
        "songs": songs
    })


@app.route("/graph/artist/<artist_name>")
def get_artist_graph(artist_name):
    artist = get_artist(artist_name)
    print(artist.name)
    if artist:
        nodes, edges, songs = get_artist_mashups(artist.name)
        return jsonify({
            "nodes": nodes,
            "edges": edges,
            "songs": songs
        })
    else:
        return get_graph()


@app.route("/count/<key>", methods=["POST"])
def count_route(key):
    count_stuff(key)
    return ""
