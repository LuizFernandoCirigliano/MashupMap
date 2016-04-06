var nodes = null;
var edges = null;
var songs = null;
var song_for_edge = null;
var network = null;
var current_song = null;
var first_song_id = null;

var errors = {
	'artist_not_found' : 'Sorry, no mashups from this artist.',
	'mashup_not_found' : 'Sorry, mashup not found.',
}

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
		improvedLayout:false,
		randomSeed: 1,
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
			iterations:200,
			fit:true
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
		nodes = data.nodes;
		edges = data.edges;
		draw();
		$(".myloader").hide();
		$(".myheader").css("background-color", "transparent");
	}
	if(data.first_song_index != undefined) {
		console.log('First songs was defined!');
		add_song_to_playlist(songs[data.first_song_index]);
		play_song(0);
	}
}

function request_graph(artist_name) {
	if(first_song_id) {
		request_with_one_mashup(first_song_id);
	}

	//if the user inputs an artist name, create graph for this artist.
	if (typeof artist_name != 'undefined' && artist_name.length > 0) {
		$.get("/graph/artist/" + artist_name).done(function(data) {
			create_network(data, artist_name);
		})
		.fail(function() { //display error if artist is not found.
			console.log('Failed to find artist!');
			$('#error_display').html(errors['artist_not_found']);
			$('#error_display').show(0).delay(2000).hide(0);
		});
	}
	else {//if there is no artist name input, request full graph.
		$.get("/graph").done(function(data) {
			create_network(data);
		});
	}

}


function request_with_one_mashup(mashup_id) {
	console.log('Mashup id = ' + mashup_id);
	$.get("/graph/mashup/" + mashup_id).done(function(data) {
		console.log('Data: ', data);
		if(data.first_song_index == undefined) {
			$('#error_display').html(errors['mashup_not_found']);
			$('#error_display').show(0).delay(2000).hide(0);
		}
		create_network(data);
	})
	.fail(function() { //display error if artist is not found.
		console.log('Failed to find mashup!!');
		request_full_graph();
		$('#error_display').html(errors['mashup_not_found']);
		$('#error_display').show(0).delay(2000).hide(0);
	});
}

// function request_artist_graph() {
//
// }

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
		var node_id = params.nodes[0];
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

	// var focusPoint = Object.keys(network.getPositions())[0];
	// console.log(focusPoint);
	// setTimeout(function() {
	// 	network.focus(
	// 		focusPoint,
	// 		{scale:1.5, animation:true}
	// 	);
	// }, 200);

	cv_resize();
	$("#mynetwork").show();
}



$(document).ready(function() {
	if (window.location.pathname.slice(6) !== "" && first_song_id == null) { //get mashup_id, if specified in URL
		console.log('Storing first_song!');
		first_song_id = window.location.pathname.slice(6);
	}
	player_start();
	$("#artist_input").keydown(function (e) {
		if (e.keyCode == 13) {
			var artist_name = $('#artist_input').val();
			request_graph(artist_name);
		}
	});
	$('#search_artist_button').click(function() {
		var artist_name = $('#artist_input').val();
		request_graph(artist_name);
	});
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

 // ---------------------------------SmallForms------------------------------
$( "#loginform" ).hide();
$( "#signupform" ).hide();

$( "#login_cancel" ).click(function() {
	var position = $( "#Login" ).offset();
	$("#loginform").css({top: (position.top+54), left: position.left, position:'absolute'});
	$( "#loginform" ).hide( "slow" );
});
$( "#Login" ).click(function() {
	$( "#signupform" ).hide();
	var position = $( "#Login" ).offset();
	$("#loginform").css({top: (position.top+54), left: position.left, position:'absolute'});
	$( "#loginform" ).show( "slow" );
});

$( "#singup_cancel" ).click(function() {
	var position = $( "#Signup" ).offset();
	$("#signupform").css({top: (position.top+54), left: position.left, position:'absolute'});
	$( "#signupform" ).hide( "slow" );
});
$( "#Signup" ).click(function() {
	$( "#loginform" ).hide();
	var position = $( "#Signup" ).offset();
	$("#signupform").css({top: (position.top+54), left: position.left, position:'absolute'});
	$( "#signupform" ).show( "slow" );
});
