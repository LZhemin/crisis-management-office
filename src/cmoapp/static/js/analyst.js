//Variables to track number of each of the stats
var efCount=-1, commentCount=-1, crCount=-1;

//Used to Get the CSRF Token later on
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
//Passing the CSRF Token with every ajax call
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        var csrfToken = getCookie('csrftoken');
        xhr.setRequestHeader("X-CSRFToken", csrfToken);
    }
});

/*
function queryStatus()
{
    $.ajax({

    });
}
*/
document.getElementById('neuroNetwork').addEventListener('ended',myHandler,false);
function myHandler(e) {
    console.log("handler");
    $('#neuroNetwork').hide();
    $('#neutraloverlay').hide();
}
function generateAP(crisisId){
    console.log("here!");
    if($('#id_type').val()=='Combat')
    {
        console.log("Combat here!");
        $.ajax({
            type:"GET",
            url: "generateCombatAP/",
            dataType: 'json',
            success: function (data) {
                var newEfCount = data['count'];
                if(efCount==-1)
                    efCount = newEfCount;
                else if(efCount<newEfCount) {
                    reloadEfUpdate(efCount);
                    efCount = newEfCount
                }
            },
            error: function(data){
                console.log(data);
            }
        });

    }
    else if($('#id_type').val()=='Clean-up'){
        $.ajax({
            type:"GET",
            url: "generateCleanupAP/",
            dataType: 'json',
            success: function (data) {
                var newEfCount = data['count'];
                if(efCount==-1)
                    efCount = newEfCount;
                else if(efCount<newEfCount) {
                    reloadEfUpdate(efCount);
                    efCount = newEfCount
                }
            },
            error: function(data){
                console.log(data);
            }
        });
    }
    else{
        new PNotify({
            title: 'No Action Plan Type Selected!',
            text: 'Please select a Action Plan type before generating a Action Plan!',
            type: 'warning',
            styling: 'bootstrap3'
        });
        return
    }
    $("#neuroNetwork").show();
    document.getElementById("neuroNetwork").play();
    $('#neutraloverlay').show();
}

//Auto Update Notification After 3 Seconds
setInterval(function()
{
    reload_notifications()
}, 3000);


//Polling for Updates Sections
//Checking for New EFUpdates
function checkEfUpdate(){
    $.ajax({
        type:"GET",
        url: "get_efupdate_count/",
        dataType: 'json',
        success: function (data) {
            var newEfCount = data['count'];
            if(efCount==-1)
                efCount = newEfCount;
            else if(efCount<newEfCount) {
                reloadEfUpdate(efCount);
                efCount = newEfCount
            }
        },
        error: function(data){
            console.log(data);
        }
    });
}

//Append to EFList
function reloadEfUpdate(count){
    var array = [];
    var html = "";
    $.ajax({
        type:"POST",
        url: "get_efupdates/",
        data:{'startNum':count},
        dataType: 'json',
        success: function (data) {
            array = data;
            //Remove the  <span>No Reports Yet</span> first
            if($('#EFUpdateList li').length==0)
                $('#EFUpdateList').html("");
            for(num in array){
                html += "<li><div class='block'>" +
                            "<div class='block_content'> " +
                                "<h2 class='title'>"+array[num]['description']+"</h2> " +
                                "<div class='byline'>"+array[num]['datetime']+"</div> " +
                                "</div> " +
                            "</div> " +
                        "</li>";
            }
            $('#EFUpdateList').append(html);
            new PNotify({
                title: 'Update!',
                text: 'New EF Updates available for viewing!',
                type: 'info',
                styling: 'bootstrap3'
            });
        },
        error: function(data){

        }
    });
}

//Checking for New EFUpdates
function checkCommentUpdate(){
    $.ajax({
        type:"GET",
        url: "get_comment_count/",
        dataType: 'json',
        success: function (data) {
            var newcommentCount = data['count'];

            if(commentCount==-1)
                commentCount = newcommentCount;
            else if(commentCount<newcommentCount) {
                reloadComments(commentCount);
                commentCount = newcommentCount
            }
        },
        error: function(data){
            console.log(data);
        }
    });
}

//Append to Comments List
function reloadComments(count){
    var array = [];
    var html = "";
    $.ajax({
        type:"POST",
        url: "get_comments/",
        data:{'startNum':count},
        dataType: 'json',
        success: function (data) {
            array = data;
            for(num in array){
                html += "<div class=\"mail_list\">\n" +
                            "<div style=\"padding-left: 1em;\">\n" +
                                "<h3>"+array[num]['author']+"</h3>\n" +
                                "<div>\n" +
                                    "<p class=\"small\"><span style=\"float:left\">Plan Number: "+array[num]['actionPlan']['plan_number']+"</span style=\"font-style:italic; color:darkgrey;\"><br><span>"+array[num]['timeCreated']+"</span></p>\n" +
                                "</div>\n" +
                                "<p>"+array[num]['text']+"</p>\n" +
                            "</div>\n" +
                        "</div>";
            }
            $('#commentList').append(html);
            new PNotify({
                title: 'Update!',
                text: 'New comments available for viewing!',
                type: 'info',
                styling: 'bootstrap3'
            });
        },
        error: function(data){
            console.log(data);
        }
    });
}


//Checking for New EFUpdates
function checkCRUpdate(){
    $.ajax({
        type:"GET",
        url: "get_crisis_report_count/",
        dataType: 'json',
        success: function (data) {
            var newCRCount = data['count'];
            if(crCount==-1)
                crCount = newCRCount;
            else if(crCount<newCRCount) {
                reloadCr(crCount);
                crCount = newCRCount
            }
        },
        error: function(data){
            console.log(data);
        }
    });
}
//Reload Crisis Reports
function reloadCr(count){
    var array = [];
    var html = "";
    $.ajax({
        type:"POST",
        url: "get_crisis_reports/",
        data:{'startNum':count},
        dataType: 'json',
        success: function (data) {
            array = data;
            //Remove the  <span>No Reports Yet</span> first
            if($('#911ReportList li').length==0)
                $('#911ReportList').html("");
            for(num in array){
                html += "<li>\n" +
                            "<div id=\"{{ report.id }}\" class=\"block\">\n" +
                                "<div class=\"block_content\">\n" +
                                    "<h2 class=\"title\">"+array[num]['description']+"</h2>\n" +
                                    "<div class=\"byline\">\n" +
                                        "<span>"+array[num]['datetime']+"</span>\n" +
                                    "</div>\n" +
                                "</div>\n" +
                            "</div>\n" +
                        "</li>";
            }
            $('#911ReportList').append(html);
            new PNotify({
                title: 'Update!',
                text: 'New 911 Reports available for viewing!',
                type: 'info',
                styling: 'bootstrap3'
            });
        },
        error: function(data){
            console.log(data);
        }
    });
}


function reloadCurrentStat() {
    $.ajax({
        url :"reload_current_stat/",
        type : "GET", // http method
        // handle a successful response
        //var html;
        success : function(data) {
            $('#CurrentStatList').load(location.href +  ' #CurrentStatList');
        },
        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
}

//--------------------------------------------

/* Basic Templating JS */
function attachDataToTemplate(template, data)
{
    var len = data.length,
    fragment = '';

    function replace(obj) {
        var t, key, reg

        for (key in obj)
        {
            reg = new RegExp('<<' + key + '>>', 'ig')
            t = (t || template).replace(reg, obj[key])
        }
        return t;
    }
    for(var i = 0; i < len; i++)
    {
        fragment+= replace(data[i])
    }

    return fragment;
}


//reloads the all_crisis template
function reload_notifications() {
    $.ajax({
        url :"/analyst/reload_notification/",
        type : "GET", // http method
        success : function(data) {
            if(!$('#presentation1').hasClass('open')) {
                $('#analyst_notifications').text(data.length);
                $('#menu1').empty();
                var i;
                if (data.length != 0) {
                    for (i = 0; i < data.length; ++i) {
                        $('#menu1').append("<li><span><strong>" + data[i].title + "</strong></span>" +
                            "</span><br/><span class='message'>" + data[i].text + "</span>" +
                            "<span class='time text-right'>" + data[i].time_added + "</span></li>");
                    }
                }
                else{
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
        url :"/analyst/delete_notification/",
        type : "GET", // http method
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