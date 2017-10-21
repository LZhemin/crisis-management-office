$(function() {


    //load_posts()

    // Load all posts on page load
    function load_posts() {
        $.ajax({
            url : "/operator/", // the endpoint
            type : "GET", // http method
            // handle a successful response
            success : function(json) {
                for (var i = 0; i < json.length; i++) {
                    console.log(json[i])
                    $("#cmoapp").prepend("<li id='crisis-"+json[i].crisispk+"'><strong>"+json[i].analyst+
                        "</strong> - <em> "+json[i].crisispk+"</em> - <span> "+json[i].status+
                        "</span> - <a id='delete-post-"+json[i].id+"'>delete me</a></li>");
                }
               // console.log("load success"); // another sanity check
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

    // AJAX for posting
    function create_crisis() {
        console.log("create post is working! test") // sanity check
        $.ajax({
            url : "/operator/create_crisis/", // the endpoint
            type : "POST", // http method
            data : { getanalyst : $('#getanalyst').val(), getcrisis : $('#getcrisis').val()
             }, // data sent with the post request //, getstatus : $('#getstatus').val()
            // handle a successful response
            success : function(json) {
                $('#getanalyst').val(''); // remove the value from the input
                $('#getcrisis').val(''); // remove the value from the input
                //$('#getstatus').val(''); // remove the value from the input
                console.log(json); // log the returned json to the console

                $("#cmoapp").prepend("<li id='crisis-"+json.crisispk+"'><strong>"+'Crisis '+json.crisispk+"</strong> - <em> "+'analyst'+json.analyst+
                "</em>  - <a id='delete-post-"+json.crisispk+"'>delete me</a></li>"); //- <span> "+json.status+"</span>

                /*
                 $("#cmoapp").prepend("<td id='crisis-"+json.crisispk+
                                    "'><td class="">"+json.crisispk"</td>"
                                    "'><td class="">"+json.analyst"</td>"
                                    "'><td class="">"+json.crisistypes"</td>"
                                    "'><td class="">"+json.type"</td>" );
                 */
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

    function delete_post(post_primary_key){
        if (confirm('are you sure you want to remove this post?')==true){
            $.ajax({
                url : "/operator/delete_crisis/", // the endpoint
                type : "DELETE", // http method
                data : { crisispk : post_primary_key }, // data sent with the delete request
                success : function(json) {
                    // hide the post
                  $('#crisis-'+post_primary_key).hide(); // hide the post on success
                  console.log("Crisis deletion successful");
                },

                error : function(xhr,errmsg,err) {
                    // Show an error
                    $('#results').html("<div class='alert-box alert radius' data-alert>"+
                    "Oops! We have encountered an error. <a href='#' class='close'>&times;</a></div>"); // add error to the dom
                    console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
                }
            });
        } else {
            return false;
        }
    };


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