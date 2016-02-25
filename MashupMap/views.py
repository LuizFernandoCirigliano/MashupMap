from flask import render_template, jsonify
from MashupMap.reddit_bot import get_mashup_graph
from MashupMap import app


@app.route("/")
def hello():
    return render_template(
        'mashupmap.html'
        )


@app.route("/graph")
def get_graph():
    nodes, edges, songs = get_mashup_graph()
    return jsonify({
        "nodes": nodes,
        "edges": edges,
        "songs": songs
    })
