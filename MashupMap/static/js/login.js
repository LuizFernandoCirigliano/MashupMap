// ---------------------------------SmallForms------------------------------
$(document).ready(function() {
    $( "#loginform" ).hide();
    $( "#signupform" ).hide();

    $( "#login_cancel" ).click(function() {
       var position = $( "#Login" ).offset();
       $("#loginform").css({top: (position.top+54), left: position.left, position:'absolute'});
       $( "#loginform" ).hide( "slow" );
    });
    $( "#Login" ).click(function() {
       $( "#signupform" ).hide();
       var position = $( "#Login" ).offset();
       var docWidth = $( document ).width();
       $("#loginform").css({top: (position.top+54), left: Math.min(position.left, docWidth - 200), position:'absolute'});
       $( "#loginform" ).show( "slow" );
    });

    $( "#singup_cancel" ).click(function() {
       var position = $( "#Signup" ).offset();
       $("#signupform").css({top: (position.top+54), left: position.left, position:'absolute'});
       $( "#signupform" ).hide( "slow" );
    });
    $( "#Signup" ).click(function() {
       $( "#loginform" ).hide();
       var position = $( "#Signup" ).offset();
       var docWidth = $( document ).width();
       $("#signupform").css({top: (position.top+54), left: Math.min(position.left, docWidth - 200), position:'absolute'});
       $( "#signupform" ).show( "slow" );
    });

    $(document).scroll(function() {
        $( "#loginform" ).hide();
        $( "#signupform" ).hide();
    });
});

function resizeIframe(obj) {
    obj.style.height = obj.contentWindow.document.body.scrollHeight + 'px';
}
