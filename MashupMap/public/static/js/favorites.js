var favorites_list = []

function get_favorites() {
    $returnmap.show();
    $mapinfo.hide();
    $.ajax({
        url: "/playlist/favorites/",
        status_code: {
            401: function() {
                show_signup_form();
            }
        },
        success: function(data, textStatus, jqXHR) {
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
}

$(document).ready(function() {
    $("#tracks").on('click', '.favorite-button', function() {
        var arr = this.id.split("-");
        $.ajax({
            url:"/playlist/favorites/" + arr[1] + "/add/",
            status_code: {
                401: function() {
                    show_signup_form();
                }
            },
            success: function() {
                get_favorites();
            }
        });
    });
});
