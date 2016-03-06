from flask import render_template, jsonify
from MashupMap.graph_maker import get_mashup_graph, get_artist_mashups
from MashupMap import app
from MashupMap.analytics import count_stuff
from MashupMap.music_api import get_artist
from MashupMap.models import Artist


@app.route("/")
@app.route("/full")
def hello_full():

    return render_template(
        'mashupmap-full.html'
        )

@app.route("/artist/<artist_name>")
def artist_mashups(artist_name):
    name = artist_name.replace('+', ' ')
    artist = get_artist(name)
    if artist:
        print(artist.name)
        return render_template('mashupmap-artist.html', artist_name=artist.name, artist_id=artist.id)
    else:
        return render_template('mashupmap-full.html')



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
    nodes, edges, songs = get_artist_mashups(artist_name)
    return jsonify({
        "nodes": nodes,
        "edges": edges,
        "songs": songs
})

@app.route("/count/<key>", methods=["POST"])
def count_route(key):
    count_stuff(key)
    return ""
