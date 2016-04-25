var favorites_list = []

function get_favorites() {
    $returnmap.show();
    $mapinfo.hide();
    $.get("/playlist/favorites/").done( function (data) {
        $("#favorites").html(data);
        $("#favorites").show();
        $("#favorites_link").unbind('click');
        $("#favorites_link").click(clear_favorites);
        $("#mynetwork").hide();
        $(".navigation-arrow").hide();
    });
}


function clear_favorites() {
    $(".navigation-arrow").show();
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

function play_favorites() {
    set_playlist(favorites_list);
}

$(document).ready(function() {
    $("#tracks").on('click', '.favorite-button', function() {
        var arr = this.id.split("-");
        $.get("/playlist/favorites/" + arr[1] + "/add/").done( function() {
            get_favorites();
        });
    });
});
