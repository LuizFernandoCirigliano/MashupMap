function get_favorites() {
    $.get("/playlist/favorites").done( function (data) {
        $("#favorites").html(data);
        $("#favorites").show();
        $("#favorites_link").unbind('click');
        $("#favorites_link").click(clear_favorites);
        $("#mynetwork").hide();
    });
}


function clear_favorites() {
    $("#favorites").hide();
    $("#mynetwork").show();
    $("#favorites_link").unbind('click');
    $("#favorites_link").click(get_favorites);
}

function delete_favorite(e) {
    var arr = e.id.split("-");
    $.get("/playlist/" + arr[1] + "/"+ arr[2] + "/delete").done( function() {
        get_favorites();
    });
}

$(document).ready(function() {
    $("#tracks").on('click', '.favorite-button', function() {
        var arr = this.id.split("-");
        $.get("/playlist/favorites/" + arr[1] + "/add").done( function() {
            get_favorites();
        });
    });

    // $("#playlist-div").on('click', '.delete-favorite', function() {
    //     var arr = this.id.split("-");
    //     $.get("/playlist/" + arr[1] + "/"+ arr[2] + "/delete").done( function() {
    //         get_favorites();
    //     });
    // });
});
