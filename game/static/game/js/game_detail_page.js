/* Handling must button: changing color and text on click */

$("#must-button").click(function(){
    if ( $('#must-button').hasClass('active') ) {
            $('#must-button').removeClass('active').text('MUST').button("refresh");;
    }else{
            $("#must-button").addClass("active").text('UNMUST').button("refresh");
    }
});