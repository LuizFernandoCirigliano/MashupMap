var current_playlist = [];

var $tracks = $('#tracks'),
    player,
    current_index = 0;

var $play = $('.controls .play'),
    $meter = $('.controls .meter'),
    $progress = $('.controls .progress');

$progress.unbind('click');
$play.unbind('click');

$play.click(function() {
    if ($play.hasClass('paused')) {
        if (!player && current_playlist.length > 0) {
            play_song(0);
        } else if (player){
            player.play();
        }
    } else {
        player.pause();
    }
});

$progress.click(function(e) {
    var percent = e.offsetX / $progress.width();

    player.getDuration(function(duration) {
        player.setCurrentTime(percent * duration);
    }, this);
});

var configure_player = function(player, song_index) {
    // Wait for the player to be ready.
    player.on('ready', function(){
        player.on('ended', function(){
            play_song(song_index + 1);
        });

        player.on('error', function(){
            console.error("Player Error");
        });

        // Update meter
        player.on('timeupdate', function(data) {
            data.seconds = Math.round(data.seconds);
            var new_width = (data.seconds / data.duration) * 100 + '%';
            $meter.width(new_width);
        });

        // Play events
        player.on('play', function() {
            $play.removeClass('paused');
        }, this);

        player.on('pause', function() {
            $play.addClass('paused');
        });

        //autoplay the video.
        player.play();
    });
}
var play_song = function(song_index) {
    if (player) {
        player.pause();
    }
    current_index = song_index;
    var song = current_playlist[song_index];
    $('.track').removeClass('currentTrack').eq(current_index).addClass('currentTrack');
    $('#iframe-div').html(song.embed);

    var iframe = $("#iframe-div iframe").get(0);
    player = new playerjs.Player(iframe);
    configure_player(player, song_index);
}

var play_next = function() {
    if (current_index < current_playlist.length - 1) {
        play_song(current_index + 1);
    }
}

var play_previous = function() {
    if (current_index > 0) {
        play_song(current_index - 1);
    } else {
        play_song(0);
    }
}

function configure_all_panels() {
    // Go to a track by clicking on it.
    $('.track-div').unbind('click').click(function() {
        var index = $('.track-div').index(this);
        play_song(index);
    });

    $('.delete-track').unbind('click').click(function() {
        var index = $('.delete-track').index(this);
        remove_song_from_playlist(index);
    });

    $('.share_link').unbind('click').click(function() {
        console.log('Clicked a share_link!');
        var index = $('.share_link').index(this);
        share_id = current_playlist[index].db_id;
        final_link = 'mashupmap.me/full/' + share_id;
        console.log(final_link);
        var share_window = $("#share_window");
        $('#share_window input').val(final_link);

        var position = $(this).parent().offset();
        share_window.css({top: (position.top), right: (0) , position:'absolute'});
        share_window.show( "slow" );

    });
    $( "#close_share_window" ).click(function() {
        console.log('Hide share window!');
        var share_window = $("#share_window");
        var position = $(this).parent().offset();
        share_window.css({top: (position.top), right: (0) , position:'absolute'});
        share_window.hide( "slow" );
    });

}

function html_for_song(obj) {
    var output = '<li class="track">' + '<div class="track-div">';
    output += '<h5><b> ' + obj.title + '</b></h5>';
    output += '<marquee scrollamount="3">';
    for (i in obj.artists) {
        output += ' ' + obj.artists[i] + ',';
    };
    output = output.substring(0, output.length - 1);
    output += '</marquee>';;
    output += '<p><b>Reddit author: </b>' + obj.author + '</p></div>';
    output +='<a class="delete-track"><span class="glyphicon glyphicon-remove"' + '</span></a>';
    output += '<a class="share_link" title="share this mashup!"><span class="glyphicon glyphicon-share"></span></a></li>'

    return output;

}

function set_playlist(songs) {
    current_playlist = songs;
    var new_songs_html = ''
    for (var i = 0; i < current_playlist.length; i++) {
        var obj = current_playlist[i];
        new_songs_html += html_for_song(obj);
    }

    $tracks.append(new_songs_html);

    //Hacky force redraw
    var disp = $tracks.css("display");
    $tracks.css("display", 'none');
    setTimeout(function(){
        $tracks.css("display", disp);
        configure_all_panels();
    }, 20);
}

function add_song_to_playlist(song) {
    current_playlist.push(song);
    $tracks.append(html_for_song(song));
    if (current_playlist.length == 1) {
        play_song(0);
    }
    //Make this more efficient later
    configure_all_panels();
}

function remove_song_from_playlist(index) {
    if (index == current_index) {
        player.pause();
        player = null;
    }
    if (current_index > index) {
        current_index--;
    }
    current_playlist.splice(index, 1);
    var trackitems = $('.track');
    trackitems[index].remove();
}

var player_start = function(songs) {
    if (typeof songs != 'undefined') {
        set_playlist(songs);
    }
};
