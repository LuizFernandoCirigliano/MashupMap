/*global jQuery:true, playerjs:true */

(function($, document, window) {
    //Wraps the player with jQuery and a playerjs player to create controls.
    var $Player = function(players) {
        // Object.defineProperty(this, "index", {
        //     get: function () {
        //         console.log("Index - GET: " + this.value);
        //         return this.value;
        //     },
        //     set: function (x) {
        //         console.log("Index - SET: " + x);
        //         this.value = x;
        //     }
        // });
        this.init(players);
    };

    var prev_time = 0;

    $Player.prototype.init = function(players) {
        this.index = 0;
        // We always process as there are multiple players.
        this.players = $.isArray(players) ? players : [players];

        // Events.
        this.events = {
            'active': [],
            'mute': [],
            'unmute': []
        };

        // All the elements.
        var $controls = $('.controls'),
            $play = $('.controls .play'),
            $volume = $('.controls .volume'),
            $bars = $volume.find('span'),
            $mute = $('.controls .mute'),
            $progress = $('.controls .progress'),
            $meter = $('.controls .meter'),
            $next = $('.controls .next'),
            $previous = $('.controls .previous');

        // Reset. just in case.
        $progress.off('click');
        $play.off('click');
        $mute.off('click');
        $bars.off('mouseenter').off('click');
        $volume.off('mouseleave');

        // Set up the volume bars
        $bars.on('mouseenter', function() {
            var $this = $(this);
            var index = $bars.index($this);

            $bars.each(function(i) {
                var $this = $(this);
                if (i <= index) {
                    $this.removeClass('inactive').addClass('active');
                } else {
                    $this.removeClass('active').addClass('inactive');
                }
            });
        });

        $volume.on('mouseleave', function() {
            $bars.removeClass('active').removeClass('inactive');
        });

        // Loop through all the providers and set up events.
        $.each(this.players, $.proxy(function(i, player) {
            this.configure_player(i, player);
        }, this));

        // Index dependant actions.
        // Seek.
        $progress.on('click', $.proxy(function(e) {
            var percent = e.offsetX / $progress.width();

            this.player().getDuration(function(duration) {
                this.player().setCurrentTime(percent * duration);
            }, this);
        }, this));

        $play.on('click', $.proxy(function() {
            if ($play.hasClass('paused')) {
                this.player().play();
            } else {
                this.player().pause();
            }
        }, this));

        $mute.on('click', $.proxy(function() {
            if ($mute.hasClass('muted')) {
                this.unmute();
            } else {
                this.mute();
            }
        }, this));

        // Set Volume
        $bars.on('click', $.proxy(function(e) {
            var $this = $(e.target);
            var index = $bars.index($this);
            var volume = ((index + 1) / $bars.length) * 100;

            $.each(this.players, function(i, player) {
                player.setVolume(volume);
            });

            $bars.each(function(i) {
                var $this = $(this);
                if (i <= index) {
                    $this.addClass('set');
                } else {
                    $this.removeClass('set');
                }
            });

        }, this));

        // Next/Prev
        $next.on('click', $.proxy(function() {
            this.next();
            return false;
        }, this));

        $previous.on('click', $.proxy(function() {
            this.previous();
            return false;
        }, this));

        $bars.addClass('active');
        $previous.addClass('disable');

        this.$mute = $mute;
        this.$next = $next;
        this.$previous = $previous;
    };

    // Get the current player.
    $Player.prototype.player = function() {
        // return this.players[this.index];
        return this.players[0];
    };

    // Go to the next player
    $Player.prototype.next = function() {
        console.log("Move to next song");
        if (this.index === this.players.length - 1) {
            return false;
        }

        // this.player().setCurrentTime(0);
        this.player().pause();
        // Maybe this should change
        this.index++;
        this.emit('active', this.index);
        // this.player().play();

        // this.$previous.removeClass('disable');
        //
        // if (this.index === this.players.length - 1) {
        //     this.$next.addClass('disable');
        // }
    };

    // Go to the previous player
    $Player.prototype.previous = function() {
        if (this.index === 0) {
            return false;
        }
        // this.player().setCurrentTime(0);
        this.player().pause();
        this.index--;
        this.emit('active', this.index);
        // this.player().play();

        // this.$next.removeClass('disable');
        // if (this.index === 0) {
        //     this.$prev.addClass('disable');
        // }

        return true;
    };

    // Play.
    $Player.prototype.play = function(index) {
        //
        // if (index !== 0 && !index) {
        //     this.player().play();
        //     return true;
        // }

        if (index >= 0 && index < this.players.length) {
            if (this.index >= 0 && this.index < this.players.length){
                this.player().setCurrentTime(0);
                this.player().pause();
            }
            this.index = index;
            this.player().play();
        }
    };

    $Player.prototype.mute = function(index) {
        this.player().mute();
        this.emit('mute');
        this.$mute.addClass('muted');
    };

    $Player.prototype.unmute = function(index) {
        this.emit('unmute');
        this.player().unmute();
        this.$mute.removeClass('muted');
    };

    // Send an event to a listener.
    $Player.prototype.emit = function(event, value) {
        if (this.events.hasOwnProperty(event)) {
            $.each(this.events[event], $.proxy(function(i, func) {
                func.call(this, value);
            }, this));
        }
    };

    // Attach a listener.
    $Player.prototype.on = function(event, cb) {
        this.events[event].push(cb);
    };

    $Player.prototype.add_player = function(player) {
        // var i = this.players.length;
        // this.players.push(player);
        // this.configure_player(i, player);
    };

    $Player.prototype.remove_player = function(index) {
        // var i = this.players.length;
        // if (index < i) {
        //     this.players.splice(index, 1);
        // }
    };

    $Player.prototype.configure_player = function(i, player) {
        var $play = $('.controls .play'),
            $meter = $('.controls .meter');
        // Update meter
        player.on('timeupdate', function(data) {
            data.seconds = Math.round(data.seconds);
            var new_width = (data.seconds / data.duration) * 100 + '%';
            $meter.width(new_width);
            prev_time = data.seconds;
        });

        // Play events
        player.on('play', function() {
            this.emit('active', i);
            $play.removeClass('paused');
        }, this);

        player.on('pause', function() {
            $play.addClass('paused');
        });

        player.on('ended', function() {
            console.log("Player Ended");
            this.next();
        }, this);

        player.on('error', function() {
            console.log("Player Error");
            this.remove_player(this.index);
            remove_song_from_playlist(this.index);
        }, this);
    };

    $Player.prototype.play_iframe = function(iframe) {
        $('#div-track-iframe').html(iframe);

        setTimeout(function(){
            $tracks.css("display", disp);

            var iframe = $('#div-track-iframe iframe').get(0);

            console.log(iframe);
            var player = new playerjs.Player(iframe);
            // console.log(player);
            this.players[0] = player;

            player.on('ready', function() {
                player.play();
            });

        }, 20);

        // var player = new playerjs.Player(iframe);
        // this.players[0] = player;
        // player.on('ready', function() {
        //     player.play();
        // });
    }

    window.$Player = $Player;

})(jQuery, document, window);
