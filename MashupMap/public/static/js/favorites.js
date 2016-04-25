var favorites_list = []

function get_favorites() {
    $.ajax({
        url: "/playlist/favorites/",
        statusCode: {
            401: function() {
                show_login_form();
            }
        },
        success: function(data, textStatus, jqXHR) {
            $returnmap.show();
            $mapinfo.hide();
            console.log(textStatus);
            $("#favorites").html(data);
            $("#favorites").show();
            $("#favorites_link").unbind('click');
            $("#favorites_link").click(clear_favorites);
            $("#mynetwork").hide();
            $(".navigation-arrow").hide();
        }
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
    play_song(0);
}

$(document).ready(function() {
    $("#tracks").on('click', '.favorite-button', function() {
        var arr = this.id.split("-");
        $.ajax({
            url:"/playlist/favorites/" + arr[1] + "/add/",
            statusCode: {
                401: function() {
                    show_login_form();
                }
            },
            success: function(data, textStatus, jqXHR) {
                console.log(textStatus);
                get_favorites();
            }
        });
    });
});
