
var my_songs;

var $tracks = $('#tracks'),
players = [],
count = 0,
isReady = false;

var player_start = function(){
var index = 0;

var multi = new $Player(players);

// Set the callout.
multi.on('active', function(index){
  $('.panel').removeClass('callout').eq(index).addClass('callout');
});

// Go to a track by clicking on it.
$('.panel').on('click', function(){
  if (!isReady){
    return false;
  }
  var index = $('.panel').index(this);
  multi.play(index);
  return false;
});

isReady = true;
};

// We need to wait for all the players to be ready before we go.
var onReady = function(){
count++;
if (count === my_songs.length){
  player_start();
}
};

function set_playlist(songs) {
  my_songs = songs;
  var new_songs = ''
  for (var i = 0; i < my_songs.length; i++) {
      var obj = my_songs[i];
      new_songs += ['<li class="track">',
        '<div class="panel">',
          '<div class="row">',
            '<div class="large-12 medium-12 small-12 columns">',
              '<h4>'+obj.title+'</h4>',
              '<p>'+obj.author+'</p>',
            '</div>',
          '</div>',
          '<div class="iframe">'+obj.embed+'</div>',
        '</div>',
      '</li>'].join(' ');
  }
  $tracks.append(new_songs);
  // grab the iframes and create players from them.
  $('.track iframe').each(function(i, e){
    var player = new playerjs.Player(e);
    players.push(player);
    player.on('ready', function(){
      player.unmute();
      onReady();
    });
  });
}
