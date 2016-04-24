from flask import Blueprint, flash, redirect, url_for
from flask.ext.login import current_user, login_required
from flask import render_template
from MashupMap.models import Playlist, Mashup
from MashupMap import db
from werkzeug.exceptions import abort

playlist_api = Blueprint('playlist_api', __name__)


def favorites_for_user():
    u_playlists = current_user.profile.playlists
    favorite = next(filter(lambda x: x.favorites, u_playlists))
    return favorite


def playlist_for_pid(pid):
    playlist = favorites_for_user() if pid == "favorites" \
        else Playlist.query.get(int(pid))

    if playlist is not None:
        return playlist
    else:
        abort(404)


@playlist_api.route("/<pid>/", methods=["GET"])
@login_required
def playlist_index(pid):
    playlist = playlist_for_pid(pid)
    if playlist is not None and playlist.ownerprof.user_id == current_user.id:
        song_list = [song.to_JSON() for song in playlist.songs]
        return render_template("playlist.html", playlist=playlist, song_list=song_list)
    else:
        flash("You don't have access to this playlist")
        return redirect(url_for("index"))


@playlist_api.route("/<pid>/<int:sid>/<operation>/", methods=["GET", "POST"])
@login_required
def edit_playlist(pid, sid, operation):
    playlist = playlist_for_pid(pid)
    mashup = Mashup.query.get(sid)

    if playlist.ownerprof.user_id == current_user.id:
        if operation == "delete":
            playlist.songs.remove(mashup)
        elif operation == "add":
            if mashup not in playlist.songs:
                playlist.songs.append(mashup)
        db.session.commit()
    else:
        flash("You are not the owner of this playlist")
    return 'OK'
