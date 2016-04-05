from flask import render_template, jsonify, g
from MashupMap.graph_maker import get_mashup_graph, get_artist_mashups
from MashupMap import app
from MashupMap.analytics import count_stuff
from Users.views import user_api
from flask.ext.login import current_user
from MashupMap.music_api import get_artist


@app.before_request
def before_request():
    g.user = current_user


@app.route("/")
def index():
    return render_template(
        'index.html'
        )


@app.route("/full")
def mashup_map():
    return render_template(
        'mashupmap-full.html'
        )


@app.route("/graph")
def get_graph():
    nodes, edges, songs, song_for_edge = get_mashup_graph()
    return jsonify({
        "nodes": nodes,
        "edges": edges,
        "songs": songs,
        "song_for_edge": song_for_edge
    })


@app.route("/graph/artist/<artist_name>")
def get_artist_graph(artist_name):
    artist = get_artist(artist_name)
    print(artist)
    if artist:
        nodes, edges, songs, song_for_edge = get_artist_mashups(artist.name)
        return jsonify({
            "nodes": nodes,
            "edges": edges,
            "songs": songs,
            "song_for_edge": song_for_edge
        })
    else:
        print('No artist found!')
        # return get_graph()
        return 'No artist found', 404
        # raise InvalidUsage('No artist found', status_code=404)


@app.route("/count/<key>", methods=["POST"])
def count_route(key):
    count_stuff(key)
    return ""


app.register_blueprint(user_api, url_prefix='/user')
