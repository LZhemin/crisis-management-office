//Variables to track number of each of the stats
var efCount=-1, commentCount=-1, crCount=-1;

//Auto Update After 30 Seconds
setInterval(function()
{
    checkEfUpdate();
    checkCommentUpdate();
    checkCRUpdate();
}, 10000);

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


//Polling for Updates Sections
//Checking for New EFUpdates
function checkEfUpdate(){
    console.log("Checking ef Update");
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
                                    "<p class=\"small\"><span style=\"float:left\">Plan Number: "+array[num]['actionPlan']['plan_number']+"</span>&nbsp<span style=\"float:right\">"+array[num]['timeCreated']+"</span></p>\n" +
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
            console.log(newCRCount)
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
//--------------------------------------------

$(document).ready(function() {
    //Collapse to right code
    $('.collapse-link-right').on('click', function () {
        var $BOX_PANEL = $(this).closest('.x_content'),
            $TOGGLE_PANEL = $($(this).attr('id')),
            $OWN_PANEL = $('#own'),
            $ICON = $(this).find('i');

        $ICON.toggleClass("fa-chevron-left fa-chevron-right");
        if($TOGGLE_PANEL.is(":visible")){
            $TOGGLE_PANEL.addClass('fadeOutRight animated').one('webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend', function(){
                $OWN_PANEL.toggleClass('col-sm-9 col-sm-12');
                $TOGGLE_PANEL.removeClass('fadeOutRight animated');
                $TOGGLE_PANEL.hide();
            });

        }
        else {
            $OWN_PANEL.toggleClass('col-sm-9 col-sm-12');
            $TOGGLE_PANEL.delay(500).show(0).addClass('fadeInRight animated').one('webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend', function(){
                $TOGGLE_PANEL.removeClass('fadeInRight animated');
            });
        }

        /*
        if(!$BOX_TITLE.find('h2:eq(1)').is(':visible')){
            console.log( $BOX_TITLE.find('h2:eq(1)').html());
            $BOX_TITLE.find('h2:eq(1)').show();
            $BOX_CONTENT.show();
        }
        else{
            console.log( $BOX_TITLE.find('h2:eq(1)').html());
            $BOX_TITLE.find('h2:eq(1)').hide();
            $BOX_CONTENT.hide();
        }
        if ($BOX_TITLE.find('h2').attr('style')) {
            $BOX_TITLE.find('h2').removeAttr('style');
            $BOX_TITLE.find('h2').toggleClass('.collapse-right')
        } else {
            $BOX_CONTENT.slideToggle(200);
            $BOX_PANEL.css('height', 'auto');
        }

        $ICON.toggleClass('fa-chevron-right fa-chevron-left');*/
    });
});

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