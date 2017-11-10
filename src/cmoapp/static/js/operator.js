$(function() {
    //Load 911 API Reports
    //Auto Refresh every 5 second
    setInterval(function() {
       // alert("happy");
        load_crisisreports();
        load_crisis();
        load_analyst();
      }, 5000);

setInterval(function()
{
    reload_notifications()
}, 3000);


// convert ugly date to human readable date
function convert_to_readable_date(date_time_string) {
    var newDate = moment(date_time_string).format('lll')
    return newDate
}

//---------CrisisReport Ajax API Func Calls
// Load all posts on page load
function load_crisisreports() {
    $.ajax({
        url : "/operator/crisisreports/", // the endpoint
        type : "GET", // http method
        // handle a successful response
        success : function(json) {
            var html = '';
            console.log(json);
            for (var i = 0; i < json.length; i++) {
                 $('#crisisreport-'+json[i].id).remove();
                    //if(json[i].crisis == null)
                    // {
                        //html = '<tbody>';
                        html = '<tr id ='+'crisisreport-'+json[i].id+'>';
                        html += '<td></td>';
                        html += '<td><span class="label label-default">'+json[i].id+'</span></td>';
                        html += '<td><span class="label label-danger">'+'Not Assigned'+'</span></td>';
                        //html += '<td><span class="label label-warning">'+json[i].crisisType+'</span></td>';
                        html += '<td>'+json[i].description+'</td>';
                        dateString = convert_to_readable_date(json[i].datetime);
                        html += '<td>'+dateString+'</td>';
                        html += '<td>'+' <button type="button" class="btn btn-round btn-info" data-toggle="modal" data-target="#add_existing" data-id='+json[i].id+'>'+
                               '<span class="glyphicon glyphicon-plus-sign"></span></button></td>';
                        html += '<td>'+' <button type="button" class="btn btn-round btn-info" data-toggle="modal" data-target="#add_project" data-id='+json[i].id+'>'+
                               '<span class="glyphicon glyphicon-plus-sign"></span></button></td>';

                        html += '</tr>';
                       // html += '</tbody>';
                        $("#Unacrisrptlist").append(html);

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


// Load all crisis on page load
function load_crisis() {
    $.ajax({
       // url : "api/crisis/", // the endpoint
         url :"/operator/crisisdisplay/",
        type : "GET", // http method
        // handle a successful response
        //var html;
        success : function(json) {
        //alert(json[0].pk + " " + json[0].fields.crisisType);
        //alert(JSON.stringify(json[0]))
       // alert("" + obj);
        //$("#Unacrisrptlist2").load(location.href + " #Unacrisrptlist2");
            //console.log(json);
            for (var i = 0; i < json.length; i++) {
                $('#crisis-'+json[i].id).remove();
                    //if(json[i].id != null){
                    var html = '<tr id ='+'crisis-'+json[i].id+'>';
                    html += '<td></td>';
                    html += '<td><span class="label label-default">'+json[i].id+'</span></td>';
                    html += '<td><span class="label label-danger">'+json[i].crisis+'</span></td>';
                    html += '<td><span class="label label-warning">'+json[i].crisisType+'</span></td>';
                    html += '<td>'+json[i].description+'</td>';
                    dateString = convert_to_readable_date(json[i].datetime);
                    html += '<td>'+dateString+'</td>';
                    html += '</tr>';
                    $("#Unacrisislist").append(html);
                   // }
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


// Load all analyst on page load
function load_analyst() {
    $.ajax({
        url : "/operator/load_analyst/", // the endpoint
        type : "GET", // http method
        // handle a successful response
        //var html;
        //alert("test");
        success : function(json) {
            for (var i = 0; i < json.length; i++) {
                console.log(json[i])

                    $('#analysts-'+json[i].pk).remove();
                    if(json[i].pk != null){
                        var html = '<tr id ='+'analysts-'+json[i].pk+'>';
                        html += '<td></td>';
                        html += '<td><span class="label label-default">'+json[i].pk+'</span></td>';
                        html += '<td><span class="label label-warning">'+json[i].fields.login+'</span></td>';
                        html += '<td>'+'<button type='+"button"+'  class="btn btn-primary"'+' onclick='+"window.location='/operator/"+json[i].pk+"';"+'>'+
                                             '<span class=" glyphicon glyphicon-plus"' + ' ></span></button></td>';
                        html += '</tr>';
                        $("#Unaacclist").append(html);
                     //}
                    // alert(json[i].id);

            }
           // console.log("load success"); // another sanity check
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

$('#existingcrisis-form').on('submit', function(event){
    event.preventDefault();
    console.log("form submitted!")  // sanity check
    assign_existingcrisis();
});
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
        data : { getanalyst : $('#getanalyst').val(), getcrisistype : $('#getcrisistype').val(), crisisreportid: $('#crisisreportid').val()
         }, // data sent with the post request //, getstatus : $('#getstatus').val()
        // handle a successful response
        success : function(json) {
            $('#getanalyst').val(''); // remove the value from the input
            $('#getcrisistype').val(''); // remove the value from the input
            $('#crisisreportid').val('');
            //$('#getstatus').val(''); // remove the value from the input
            console.log(json); // log the returned json to the console

            $('#analysts-'+json.id).remove();
            //$('#crisisreport-'+json.id).remove();
            //alert(json.id+json.crisispk);
            /*
            html = '<tr id ='+'crisis-'+json.crisispk+'>';
            html += '<td></td>';
            html += '<td><span class="label label-default">'+json.crisispk+'</span></td>';
            html += '<td><span class="label label-warning">'+json.analyst+'</span></td>';
            html += '<td><span class="label label-success">'+json.status+'</span></td>';
            html += '</tr>';
            $("#Unacrisislist").append(html);
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
function assign_existingcrisis() {
    console.log("create post is working! test") // sanity check
    $.ajax({
        url : "/operator/assignexisting/", // the endpoint
        type : "POST", // http method
        data : { getExisting : $('#getExisting').val(),existingreportid: $('#existingreportid').val()
         }, // data sent with the post request //, getstatus : $('#getstatus').val()
        // handle a successful response
        success : function(json) {
            //$('#crisisreport-'+existingreportid).remove();
            $('#getExisting').val(''); // remove the value from the input
            $('#existingreportid').val(''); // remove the value from the input
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

//reloads the all_crisis template
function reload_notifications() {
    $.ajax({
        url :"/operator/reload_notification/",
        type : "GET", // http method
        success : function(data) {
            if(!$('#presentation1').hasClass('open')) {
                $('#operator_notifications').text(data.length);
                $('#menu1').empty();
                var i;
                if (data.length != 0) {
                    for (i = 0; i < data.length; ++i) {
                        $('#menu1').append("<li><span><strong>" + data[i].title + "</strong></span>" +
                            "</span><br/><span class='message'>" + data[i].text + "</span>" +
                            "<span class='time text-right'>" + data[i].time_added + "</span></li>");
                    }
                }else{
                    $('#menu1').append("<li><span><strong>'You have no notifications'</strong></span></li>");
                }
            }
        },
        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
}


$('#presentation1').on('click', function () {
    if(!$('#presentation1').hasClass('open')) {
        $.ajax({
        url :"/operator/delete_notification/",
        type : "GET", // http method
        // handle a successful response
        //var html;
        success : function(data) {
            console.log('Delete Notification Success')
        },
        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
    }else{
        reload_notifications();
    }
});