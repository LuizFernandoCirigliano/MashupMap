from flask import Blueprint, flash, redirect, url_for, request
from flask.ext.login import current_user, login_required
from flask import render_template
from MashupMap.models import Playlist, Mashup
from MashupMap import db

playlist_api = Blueprint('playlist_api', __name__)


@playlist_api.route("/<int:pid>", methods=["GET"])
@login_required
def playlist_index(pid):
    playlist = Playlist.query.get(pid)
    if playlist is not None and playlist.ownerprof.user_id == current_user.id:
        return render_template("playlist.html", playlist=playlist)
    else:
        flash("You don't have access to this playlist")
        return redirect(url_for("index"))


@playlist_api.route("/<int:pid>/<int:sid>", methods=["POST"])
@login_required
def edit_playlist(pid, sid):
    playlist = Playlist.query.get(pid)
    mashup = Mashup.query.get(sid)

    operation = request.form['_operation']

    if playlist.ownerprof.user_id == current_user.id:
        if operation == "DELETE":
            playlist.songs.remove(mashup)
        elif operation == "ADD":
            playlist.songs.append(mashup)
        db.session.commit()
    else:
        flash("You are not the owner of this playlist")
    return redirect(url_for('playlist_api.playlist_index'))
