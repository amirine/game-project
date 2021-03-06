/* Handling must button: sending AJAX request and changing color and text on click */

$(document).ready(function () {
    $("button.must-button").click(function () {
        let game_id = $(this).data("game_id");
        let page_url = $(this).data("url_root");
        let current_button = $(this);
        $.ajax({
            method: "POST",
            url: page_url,
            data: {
                'game_id': game_id,
            },
            success: function () {
                if (current_button.hasClass('active')) {
                    current_button.removeClass('active').text('Must').button("refresh");
                } else {
                    current_button.addClass("active").text('Unmust').button("refresh");
                }
            },
        });
    });
});

/* Handling AJAX CSRF */

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        let cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            let cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

$(function () {
    $.ajaxSetup({
        headers: {"X-CSRFToken": getCookie("csrftoken")}
    });
});
