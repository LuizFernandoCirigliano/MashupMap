var favorites_list = []

function get_favorites() {
    $.get("/playlist/favorites/").done( function (data) {
        $("#favorites").html(data);
        $("#favorites").show();
        $("#favorites_link").unbind('click');
        $("#favorites_link").click(clear_favorites);
        $("#mynetwork").hide();
    });
}


function clear_favorites() {
    $("#favorites").hide();
    $("#mynetwork").show();
    $("#favorites_link").unbind('click');
    $("#favorites_link").click(get_favorites);
}

function delete_favorite(e) {
    var arr = e.id.split("-");
    $.get("/playlist/" + arr[1] + "/"+ arr[2] + "/delete/").done( function() {
        get_favorites();
    });
}


function favorite_li_for_song(song, playlist) {
    var artists_string = '';
    var art_count = song.artists.length;
    for (var i = 0; i < art_count ; i++) {
        artists_string += song.artists[i].name + ', ';
    }

    '<li class="media">\
        <a class="pull-left" href="#"><img class="media-object" src="'
        + song.artists[0].imageURL + '" height="64" width="64"></a>\
        <div class="media-body">\
            <h4 class="media-heading">' + song.clean_title +'</h4>\
            <p>' +artists_string+ '</p>\
            <p><a href="' + song.redditurl +'" target="_blank">View Source.</a></p>\
            <div class="row">\
                <div class="col-md-1">\
                    <button class="btn btn-sm btn-success" type="submit" form="'
                    + playlist.id + '-' + song.id + '">\
                        <i class="glyphicon glyphicon-play"></i>\
                    </button>\
                </div>\
                <div class="col-md-1">\
                    <button class="btn btn-sm btn-danger delete-favorite" id="del-' +
                    playlist.id + '-' + song.id + '" onclick="delete_favorite(this)">\
                        <i class="glyphicon glyphicon-remove"></i>\
                    </button>\
                </div>\
            </div>\
        </div>\
    </li>'
}

$(document).ready(function() {
    $("#tracks").on('click', '.favorite-button', function() {
        var arr = this.id.split("-");
        $.get("/playlist/favorites/" + arr[1] + "/add/").done( function() {
            get_favorites();
        });
    });
});
