from flask import Blueprint
from flask.ext.login import current_user, login_required
from flask import render_template

playlist_api = Blueprint('playlist_api', __name__)


@playlist_api.route("/", methods=["GET"])
@login_required
def playlist_index():
    playlists = current_user.profile.playlists
    return render_template("playlists.html", playlists=playlists)
