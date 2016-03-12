from flask import render_template, jsonify, g
from MashupMap.graph_maker import get_mashup_graph
from MashupMap import app
from MashupMap.analytics import count_stuff
from Users.views import user_api
from flask.ext.login import current_user


@app.before_request
def before_request():
    g.user = current_user


@app.route("/")
@app.route("/full")
def index():
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


@app.route("/count/<key>", methods=["POST"])
def count_route(key):
    count_stuff(key)
    return ""


app.register_blueprint(user_api, url_prefix='/user')
