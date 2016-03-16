var nodes = null;
var edges = null;
var songs = null;
var song_for_edge = null;
var network = null;
var current_song = null;

var showingImages=false;
var nodeOptions = {
		shape: "icon",
		borderWidth:4,
		size:25,
		mass: 4,
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
		width: 1,
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
		navigationButtons: true
	}
};

function create_network(data) {
	songs = data.songs;
	song_for_edge = data.song_for_edge;
	set_playlist(songs.slice(0,4));
	if(network != null) {
		console.log('network != null');
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
}

function request_graph() {
	var artist_name = $('#artist_input').val();
	if (typeof(artist_name) != 'undefined' && artist_name.length > 0) {
		$.get("/graph/artist/" + artist_name).done(function(data) {
			create_network(data);
		})
		.fail(function() {
			$('#no_artist_error').show(0).delay(2000).hide(0);
		});
	}
	else {
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


function move_info_div(x, y) {
	var infodiv = $("#infocontainer");
	infodiv.show();
	infodiv.css("left", x + "px");
	infodiv.css("top", (y - 150) + "px");
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
	network.on("dragStart", function(params) {
	 $("#infocontainer").hide();
	});

	network.on("selectEdge", function (params) {
		current_song = song_for_edge[params.edges[0]];
		var selectedSong = songs[current_song];
		$('#redditlink').attr("href", selectedSong.redditurl);
		$('#author').html(selectedSong.author);
		move_info_div(params.pointer.DOM.x, params.pointer.DOM.y);
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
	$('#random_mashup_button').click(function(){
	play_random_song();
	});

}

function search_artist() {
	request_graph();
}

$(document).ready(function() {
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
