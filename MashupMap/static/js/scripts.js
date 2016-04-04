var nodes = null;
var edges = null;
var songs = null;
var song_for_edge = null;
var network = null;
var current_song = null;
var artists_displayed = [];
var first_song = null;


var showingImages=false;
var nodeOptions = {
		shape: "icon",
		borderWidth:4,
		size:25,
		mass: 1,
		color: {
		  border: '#222222',
		},
		font:{color:'#eeeeee'},
		icon: {
		  code: '\u2022'
		}
};

var options = {
	layout: {
		improvedLayout:false
	},
	width: '100%',
	nodes: nodeOptions,
	edges: {
		width: 2,
		color: 'lightgray',
		// smooth: true,
		hoverWidth: 5
	},
	physics: {
	  // enabled: false,
		stabilization: {
			enabled:true,
			iterations:100
		},
		repulsion: {
			nodeDistance: 100,
			springLength: 1000,
			springConstant: 0.01,
			damping : 0.01
		}
	  // stabilization.iterations: 200,
	},
	interaction: {
		hover:true,
		tooltipDelay: 100,
		hideEdgesOnDrag: true,
		navigationButtons: true,
		selectConnectedEdges: false, //false, otherwise selecting a node will select adjacent edges.
		keyboard: {
			enabled: true
		}
	}
};

function start() {
	if (window.location.pathname.slice(6) !== "") {
		console.log('Storing first_song!');
		first_song = window.location.pathname.slice(6);
	}
	request_graph();
	$.fn.extend({
		animateCss: function (animationName) {
		var animationEnd = 'webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend';
		$(this).addClass('animated ' + animationName).one(animationEnd, function() {
		$(this).removeClass('animated ' + animationName);
		});
		}
	});
	var icon = $('.play');
	icon.click(function() {
		icon.toggleClass('active');
		return false;
	});
	$(window).bind("resize", function(){
		cv_resize();
	});
}


function play_random_song() {
	var random = Math.floor(Math.random()*songs.length);
	while (random == current_song) {
		random = Math.floor(Math.random()*songs.length);
	}
	current_song = random;
	var selectedSong = songs[current_song];
	play_song(selectedSong.embed, true);
}

function play_selected_song() {
	var selectedSong = songs[current_song];
	$('#song_title').html(selectedSong.title);
	$('#redditlink').attr("href", selectedSong.redditurl);
	$('#author').html(selectedSong.author);
	move_info_div();
	play_song(selectedSong.embed, false);
}

function play_song(song_embed, continuous) {
	$.post("/count/playcount");
	$("#playsong").html(song_embed);
	var iframe = $("#playsong iframe").get(0);
	// initialize the player.
	var player = new playerjs.Player(iframe);

  	// Wait for the player to be ready.
	player.on('ready', function(){
		if (continuous) {
	  // Listen to the play event.
			player.on('ended', function(){
		// Tell Google analytics that a video was played.
				play_random_song();
			});

	  // Listen to the play event.
			player.on('error', function(){
			// Tell Google analytics that a video was played.
				console.log("Iframe Error");
				play_random_song();
			});
		}
	//autoplay the video.
		player.play();
	});
	$("#infocontainer").hide();
}

function create_network(data, new_artist) {
	if(network != null && new_artist != undefined) {
			songs = data.songs;
			song_for_edge = data.song_for_edge;
			console.log('Artist selected!');
			var newData = {
				nodes: data.nodes,
				edges: data.edges
			}
			console.log(newData);

		artists_displayed.push(new_artist);
		network.setData(newData);
	}

	else {
		artists_displayed = [];
		songs = data.songs;
		song_for_edge = data.song_for_edge;
		nodes = data.nodes;
		edges = data.edges;
		draw();
		$(".myloader").hide();
		$(".myheader").css("background-color", "transparent");
	}
	if(data.first_song != undefined) {
		console.log('First songs was defined!');
		current_song = data.first_song;
		play_selected_song();
	}
}

function request_graph(artist_name) {
	if(first_song) {
		test_play_mashup(first_song);
	}

	if (artist_name == undefined) {
		var artist_name = $('#artist_input').val();
	}
	//if the user inputs an artist name, create graph for this artist.
	if (typeof artist_name != 'undefined' && artist_name.length > 0) {
		$.get("/graph/artist/" + artist_name).done(function(data) {
			create_network(data, artist_name);
		})
		.fail(function() { //display error if artist is not found.
			console.log('Failed to find artist!');
			$('#no_artist_error').show(0).delay(2000).hide(0);
		});
	}

	else {//if there is no artist name input, request full graph.
		$.get("/graph").done(function(data) {
			create_network(data);
		});
	}

}

function test_play_mashup(mashup_id) {
	console.log('Mashup id = ' + mashup_id);
	$.get("/mashup/" + mashup_id).done(function(data) {
		console.log(data);
		create_network(data);
	})
	.fail(function() { //display error if artist is not found.
		console.log('Failed to find mashup!!');
		request_graph();
		// $('#no_artist_error').show(0).delay(2000).hide(0);
	});
}

function cv_resize() {
	var w = $(window).width();
	var h = $(window).height();
	var network = $("#mynetwork");
	network.css("width", w + "px");
	network.css("height", h + "px");
}


function move_info_div(x, y) {
	var infodiv = $("#infocontainer");
	infodiv.show();
	// infodiv.css("left", x + "px");
	// infodiv.css("top", (y - 150) + "px");
	$('#infocontainer').animateCss('bounceIn');
	$('#mysubheader').hide();
}
// Called when the Visualization API is loaded.
function draw() {
  // create a network
	var container = document.getElementById('mynetwork');
	var data = {
		nodes: nodes,
		edges: edges
	};

	network = new vis.Network(container, data, options);

	network.on("selectEdge", function (params) {
		current_song = song_for_edge[params.edges[0]];
		play_selected_song();
	});

	network.on("selectNode", function (params) {
		// console.log(params);
		var node_id = params.nodes[0];
		// console.log(node_id);
		var obj = network.body.nodes[node_id];
		artist_name = obj.labelModule.lines[0];
		console.log(artist_name);
		request_graph(artist_name);

	});

	network.on("zoom", function(params) {
		if (showingImages == true && params.scale < 0.7) {
			showingImages = false;
			nodeOptions.shape = "icon";
			network.setOptions({nodes:nodeOptions});
		}
		else if (showingImages == false && params.scale > 0.7) {
			showingImages = true;
			nodeOptions.shape = "circularImage";
			network.setOptions({nodes:nodeOptions});
		}
	});


	cv_resize();
	$("#mynetwork").show();
}

function search_artist() {
	request_graph();
}

$(document).ready(function() {
	start();
	$("#artist_input").keydown(function (e) {
		if (e.keyCode == 13) {
			request_graph();
		}
	});
	$('#search_artist_button').click(function() {
		request_graph();
	});
	$('#random_mashup_button').click(play_random_song);


});
