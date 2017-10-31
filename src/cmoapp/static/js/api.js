$(function() {



    //Load 911 API Reports
    //Auto Refresh every 5 second
    setInterval(function() {

      }, 5000);


    // convert ugly date to human readable date
    function convert_to_readable_date(date_time_string) {
        var newDate = moment(date_time_string).format('lll')
        return newDate
    }

    //---------CrisisReport Ajax API Func Calls
    // Load all posts on page load
    function load_auth() {
        $.ajax({
            url : "api/auth/", // the endpoint
            type : "GET", // http method
            // handle a successful response
            success : function(json) {
                var html = '';
                for (var i = 0; i < json.length; i++) {
                //for (var i = json.length-1; i >= 0; i--) {
                    console.log(json[i])

                }

            },
            // handle a non-successful response
            error : function(xhr,errmsg,err) {
                $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                    " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
        });
    };

     // AJAX for posting
    function create_auth() {
        console.log("create auth is working! test") // sanity check
        $.ajax({
            url : "api/auth/", // the endpoint
            type : "POST", // http method
            data : { getactionplan : $('#getactionplan').val(),
                     getApproval : $('#getApproval').val(),
                     getCOComments : $('#getCOComments').val(),
                     getPMOComments : $('#getPMOComments').val()
             }, // data sent with the post request

            // handle a successful response
            success : function(json) {
                    $('#getactionplan').val(''); // remove the value from the input
                    $('#getApproval').val(''); // remove the value from the input
                    $('#getCOComments').val(''); // remove the value from the input
                    $('#getPMOComments').val(''); // remove the value from the input
                    //$('#getstatus').val(''); // remove the value from the input
                console.log(json); // log the returned json to the console



                console.log("success"); // another sanity check
            },
            // handle a non-successful response
            error : function(xhr,errmsg,err) {
                $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                    " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
        });
    };



    // Submit post on submit
    $('#crisis-form').on('submit', function(event){
        event.preventDefault();
        console.log("form submitted!")  // sanity check
        create_crisis();
    });

    // Delete post on click
    $("#cmoapp").on('click', 'a[id^=delete-post-]', function(){
        var post_primary_key = $(this).attr('id').split('-')[2];
        console.log(post_primary_key) // sanity check
        delete_post(post_primary_key);
    });

    // This function gets cookie with a given name
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');

    /*
    The functions below will create a header with csrftoken
    */

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    function sameOrigin(url) {
        // test that a given url is a same-origin URL
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                // Send the token to same-origin, relative URLs only.
                // Send the token only if the method warrants CSRF protection
                // Using the CSRFToken value acquired earlier
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

});