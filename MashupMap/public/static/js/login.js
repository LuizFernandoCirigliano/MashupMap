// ---------------------------------SmallForms------------------------------

function show_login_form() {
   $( "#signupform" ).hide();
   var position = $( "#Login" ).offset();
   var docWidth = $( document ).width();
   $("#loginform").css({top: (position.top+54), right: (docWidth - position.left - 70), position:'absolute'});
   $( "#loginform" ).show( "slow" );
}

function show_signup_form() {
   $( "#loginform" ).hide();
   var position = $( "#Signup" ).offset();
   var docWidth = $( document ).width();
   $("#signupform").css({top: (position.top+54), right:(docWidth - position.left - 120), position:'absolute'});
   $( "#signupform" ).show( "slow" );
}

$(document).ready(function() {
    error_login = document.getElementById("login_error");
    error_register = document.getElementById("register_error");

    if(error_login){
       var position = $( "#Login" ).offset();
       var docWidth = $( document ).width();
       $("#loginform").css({top: (position.top+54), right: (docWidth - position.left - 70), position:'absolute'});
       $( "#loginform" ).show( "slow" );
    }else{
       $( "#loginform" ).hide();
    }

    if(error_register){
       var position = $( "#Signup" ).offset();
       var docWidth = $( document ).width();
       $("#signupform").css({top: (position.top+54), right:(docWidth - position.left - 120), position:'absolute'});
       $( "#signupform" ).show( "slow" );
    }else{
       $( "#signupform" ).hide();
    }

    $( "#login_cancel" ).click(function() {
       var position = $( "#Login" ).offset();
       var docWidth = $( document ).width();
       $("#loginform").css({top: (position.top+54), right: (docWidth - position.left - 70), position:'absolute'});
       $( "#loginform" ).hide( "slow" );
    });
    $( "#Login" ).click(show_login_form);

    $( "#singup_cancel" ).click(function() {
       var position = $( "#Signup" ).offset();
       var docWidth = $( document ).width();
       $("#signupform").css({top: (position.top+54), right:(docWidth - position.left - 120), position:'absolute'});
       $( "#signupform" ).hide( "slow" );
    });
    $( "#Signup" ).click(show_signup_form);

    $(document).scroll(function() {
        $( "#loginform" ).hide();
        $( "#signupform" ).hide();
    });
});

function resizeIframe(obj) {
    obj.style.height = obj.contentWindow.document.body.scrollHeight + 'px';
}

$(document).ready(function() {
  error = document.getElementById("login_error");
  if(error){
    $('#loginform').trigger('click');
  }
});
