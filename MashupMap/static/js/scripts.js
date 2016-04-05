var nodes = null;
var edges = null;
var songs = null;
var song_for_edge = null;
var network = null;
var current_song = null;
var artists_displayed = [];

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
			iterations:400
		},
		repulsion: {
			nodeDistance: 50,
			springLength: 1000,
			springConstant: 0.01,
			damping : 0.01
		}
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

function create_network(data) {
	songs = data.songs;
	song_for_edge = data.song_for_edge;
	if(network != null) {
		var newData = {
			nodes: data.nodes,
			edges: data.edges
		};
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

}

function request_graph(artist_name) {
	if (artist_name == undefined) {
		var artist_name = $('#artist_input').val();
	}
	console.log(artist_name);
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

function cv_resize() {
	var w = $(window).width();
	var h = $(window).height();
	var network = $("#mynetwork");
	network.css("width", w + "px");
	network.css("height", h + "px");
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
		var edgeIndex = params.edges[0];
		var selectedSong = songs[song_for_edge[edgeIndex]];
		add_song_to_playlist(selectedSong);
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
	player_start();
	$("#artist_input").keydown(function (e) {
		if (e.keyCode == 13) {
			request_graph();
		}
	});
	$('#search_artist_button').click(request_graph);
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
});
