from flask import render_template, jsonify, g
from MashupMap.graph_maker import get_mashup_graph, get_artist_mashups
from MashupMap import app
from MashupMap.analytics import count_stuff
from Users.views import user_api
from flask.ext.login import current_user
from MashupMap.music_api import get_artist
from Users.forms import LoginForm, SignupForm
from MashupMap.routes.playlist_views import playlist_api


@app.before_request
def before_request():
    g.user = current_user


@app.context_processor
def inject_forms():
    form = LoginForm()
    signup = SignupForm()
    return dict(login_form=form, signup_form=signup)


@app.route("/")
def index():
    return render_template(
        'index.html'
        )


@app.route("/full", methods=["GET", "POST"])
@app.route('/full/<mashup_id>')
def mashup_map(mashup_id=None):
    return render_template('mashupmap-full.html')


@app.route("/graph")
@app.route('/graph/mashup/<int:mashup_id>')
def get_graph(mashup_id=None):
    # print('get_graph: ' + str(mashup_id))
    nodes, edges, songs, song_for_edge = get_mashup_graph(mashup_id)
    response = {
        "nodes": nodes,
        "edges": edges,
        "songs": songs,
        "song_for_edge": song_for_edge
    }

    # if a specific mashup was requested, get the index
    # of this mashup in the songs array.
    if mashup_id:
        try:
            first_song = [x for x, y in enumerate(songs) if y['db_id'] == mashup_id][0]
        except IndexError as e:
            print('Mashup with id={} not found.'.format(mashup_id))
            # may happend because link is broken
        except Exception as e:
            print('Unknown exception.')
            print(e, e.args)
        else:
            response["first_song_index"] = first_song

    return jsonify(response)


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
        return 'No artist found', 404


@app.route("/count/<key>", methods=["POST"])
def count_route(key):
    count_stuff(key)
    return ""


@app.route("/mashup/<mashup_id>")
def play_mashup(mashup_id):
    return get_graph(mashup_id=int(mashup_id))

app.register_blueprint(user_api, url_prefix='/user')
app.register_blueprint(playlist_api, url_prefix='/playlist')
