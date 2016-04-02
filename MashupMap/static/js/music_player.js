var my_songs;

var $tracks = $('#tracks'),
    players = [],
    count = 0,
    isReady = false,
    multi;

var player_start = function() {
    var index = 0;

    multi = new $Player(players);

    // Set the callout.
    multi.on('active', function(index) {
        $('.track').removeClass('currentTrack').eq(index).addClass('currentTrack');
    });

    configure_panels();

    isReady = true;
};

function configure_panels() {
    // Go to a track by clicking on it.
    $('.track-div').unbind('click').click(function() {
        if (!isReady) {
            return false;
        }
        var index = $('.track-div').index(this);
        multi.play(index);
        return false;
    });

    $('.delete-track').unbind('click').click(function() {
        var index = $('.delete-track').index(this);
        console.log("delete " + index);
        multi.remove_player(index);
        remove_song_from_playlist(index);
    });
}

// We need to wait for all the players to be ready before we go.
var onReady = function() {
    count++;
    if (count === my_songs.length) {
        player_start();
    }
};

function html_for_song(obj) {
    return '<li class="track">' +
        '<div class="track-div">' +
        '<h5>' + obj.title + '</h5>' +
        '<p>' + obj.author + '</p>' +
        '<div class="iframe">' + obj.embed + '</div>' +
        '</div><a class="delete-track"><span class="glyphicon glyphicon-remove"' +
        '</span></a></li>'
}

function set_playlist(songs) {
    console.log($tracks);
    my_songs = songs;
    var new_songs = ''
    for (var i = 0; i < my_songs.length; i++) {
        var obj = my_songs[i];
        new_songs += html_for_song(obj);
    }

    var disp = $tracks.css("display");

    $tracks.append(new_songs);

    $tracks.css("display", 'none');

    setTimeout(function(){
        $tracks.css("display", disp);

        // grab the iframes and create players from them.
        $('.track iframe').each(function(i, e) {
            var player = new playerjs.Player(e);
            players.push(player);
            player.on('ready', function() {
                player.unmute();
                onReady();
            });
        });
    }, 20);

}

function add_song_to_playlist(song) {
    $tracks.append(html_for_song(song));
    var iframe_set = $('.track iframe');
    var count = iframe_set.length;
    iframe_set.each(function(i, e) {
        if (i == count - 1) {
            var player = new playerjs.Player(e);
            player.on('ready', function () {
                console.log("new guy ready");
                multi.add_player(player);
                configure_panels();
            });
        }
    });
}

function remove_song_from_playlist(index) {
    console.log(index);
    var trackitems = $('.track');
    trackitems[index].remove();
}
