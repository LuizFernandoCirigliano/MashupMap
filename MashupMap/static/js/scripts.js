 var nodes = null;
    var edges = null;
    var songs = null;
    var network = null;
    var current_song = null;

    var showingImages=false;
    var nodeOptions = {
            shape: "icon",
            borderWidth:4,
            size:25,
            mass: 2,
            color: {
              border: '#222222',
            },
            font:{color:'#eeeeee'},
            icon: {
              code: '\u2022'
            }
          };

    function start() {
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

    function choose_random() {
      var random = Math.floor(Math.random()*songs.length);
      while (random == current_song) {
        random = Math.floor(Math.random()*songs.length);
      }
      current_song = random;
      play_song();
    }
    function play_song() {
      $("#playsong").html(songs[current_song].embed);
      $("#infocontainer").hide();
    }

    function request_graph() {
      $.get("/graph").done(function(data) {
        console.log("terminou");
        nodes = data.nodes;
        edges = data.edges;
        songs = data.songs;
        draw();
        $(".myloader").hide();
        $(".myheader").css("background-color", "transparent");
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
      var options = {
        layout: {
          improvedLayout:false
        },
        width: '100%',
        nodes: nodeOptions,
        edges: {
          width: 1,
          color: 'lightgray',
          smooth: false,
          hoverWidth: 5
        },
        physics: {
          // enabled: false,
          stabilization: {
            enabled:true,
            iterations:200
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
          navigationButtons: true
        }
      };
      network = new vis.Network(container, data, options);
      network.on("selectEdge", function (params) {
        console.log(params)
        current_song = params.edges[0]
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
        choose_random();
      });

    }
