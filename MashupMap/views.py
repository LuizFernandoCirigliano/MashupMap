from flask import render_template, jsonify
from MashupMap.graph_maker import get_mashup_graph
from MashupMap import app


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
