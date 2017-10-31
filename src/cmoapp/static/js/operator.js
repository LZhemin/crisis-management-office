$(function() {



    //Load 911 API Reports
    //Auto Refresh every 5 second
    setInterval(function() {
       // alert("happy");
        load_crisisreports();
        load_crisis();
        load_analyst();
      }, 5000);


    // convert ugly date to human readable date
    function convert_to_readable_date(date_time_string) {
        var newDate = moment(date_time_string).format('lll')
        return newDate
    }

    //---------CrisisReport Ajax API Func Calls
    // Load all posts on page load
    function load_crisisreports() {
        $.ajax({
            url : "api/crisisreports/", // the endpoint
            type : "GET", // http method
            // handle a successful response
            success : function(json) {
                var html = '';
                for (var i = 0; i < json.length; i++) {
                    console.log(json[i])
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

     // AJAX for posting
    function create_crisisreport() {
        console.log("create crisisrepor is working! test") // sanity check
        $.ajax({
            url : "api/crisisreports/", // the endpoint
            type : "POST", // http method
            data : { getcrisisreport : $('#getcrisisreport').val(),
                     getdescription : $('#getdescription').val(),
                     getdatetime : $('#getdatetime').val(),
                     getlatitude : $('#getlatitude').val(),
                     getlongitude : $('#getlongitude').val(),
                     getradius : $('#getradius').val(),
                     getcrisis : $('#getcrisis').val(),
                     getcrisisType : $('#getcrisisType').val()
             }, // data sent with the post request
            // handle a successful response
            success : function(json) {
                    $('#getcrisisreport').val(''); // remove the value from the input
                    $('#getdescription').val(''); // remove the value from the input
                    $('#getdatetime').val(''); // remove the value from the input
                    $('#getlatitude').val(''); // remove the value from the input
                    $('#getlongitude').val(''); // remove the value from the input
                    $('#getradius').val(''); // remove the value from the input
                    $('#getcrisis').val(''); // remove the value from the input
                    $('#getcrisisType').val(''); // remove the value from the input
                    //$('#getstatus').val(''); // remove the value from the input
                console.log(json); // log the returned json to the console

                $("#cmoapp").prepend("<li id='crisisreport-"+json[i].id+"'><strong>"
                                                                +json[i].description+"</strong> - <em> "
                                                                +json[i].datetime+"</em> - <em>"
                                                                +json[i].latitude+"</em> - <em>"
                                                                +json[i].longitude+"</em> - <em>"
                                                                +json[i].radius+"</em> - <em>"
                                                                +json[i].crisis+"</em> - <span>"
                                                                +json[i].crisisType+"</span> - <a id='delete-post-"
                                                                +json[i].id+"'>delete me</a></li>");

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

    function delete_crisisreport(crisisreport_primary_key){
        if (confirm('are you sure you want to remove this post?')==true){
            $.ajax({
                url : "api/crisisreports/"+crisisreport_primary_key, // the endpoint
                type : "DELETE", // http method
                data : { id : crisisreport_primary_key }, // data sent with the delete request
                success : function(json) {
                    // hide the post
                  $('#crisisreport-'+crisisreport_primary_key).hide(); // hide the post on success
                  console.log("Crisis Report deletion successful");
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

                for (var i = 0; i < json.length; i++) {
                    console.log(json[i])
                    $('#crisis-'+json[i].pk).remove();
                        //if(json[i].id != null){
                        var html = '<tr id ='+'crisis-'+json[i].pk+'>';
                        html += '<td></td>';
                        html += '<td><span class="label label-default">'+json[i].pk+'</span></td>';
                        html += '<td><span class="label label-danger">'+json[i].fields.crisis+'</span></td>';
                        html += '<td><span class="label label-warning">'+json[i].fields.crisisType+'</span></td>';
                        html += '<td>'+json[i].fields.description+'</td>';
                        dateString = convert_to_readable_date(json[i].fields.datetime);
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