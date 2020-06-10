jQuery.validator.setDefaults({
    debug: true,
    success:  function(label){
      label.attr('id', 'valid');
      },
});
$( "#myform" ).validate({
    rules: {
      password: "required",
      comfirm_password: {
            equalTo: "#password"
      }
    },
    messages: {
        first_name: {
            required: "Please enter a firstname"
        },
        last_name: {
            required: "Please enter a lastname"
        },
        your_email: {
            required: "Please provide an email"
        },
        password: {
            required: "Please enter a password"
        },
        comfirm_password: {
            required: "Please enter a password",
            equalTo: "Wrong Password"
      }
    }
});