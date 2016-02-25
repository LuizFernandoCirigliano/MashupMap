from flask import render_template, jsonify
from MashupMap.reddit_bot import get_mashup_graph
from MashupMap import app


@app.route("/")
def hello():
    nodes, edges, songs = get_mashup_graph()
    return render_template(
        'mashupmap.html',
        nodes=nodes,
        edges=edges,
        songs=songs
        )
