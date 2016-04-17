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


$(document).ready(function() {
    $("#tracks").on('click', '.favorite-button', function() {
        $.get("/playlist/favorites/" + this.id + "/add").done( function() {
            get_favorites();
        });
    });
});
