//Collapse to the right
$(document).ready(function() {
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

//Rejecting a ActionPlan function called
function rejectActionPlan(idval,commentId){

    var comment = document.getElementById(commentId).value;
    if(comment.length>0){
        $.ajax({
            type:"POST",
            url: "reject_action_plan/",
            data: { id: idval, comment: comment},
            dataType: 'json',
            success: function (data) {
                new PNotify({
                    title: "Action Plan "+idval+" Rejected Successfully!" ,
                    text: "Notifying Analyst!",
                    type: 'success',
                    styling: 'bootstrap3'
                });

                window.setTimeout(function(){
                    reload_table();
                    reload_crisis();
                },150);
            }
        });
    }
    else{
        new PNotify({
            title: "Rejecting Action Plan Failed!",
            text: "Please Ensure that your have keyed in a comment!",
            type: 'error',
            styling: 'bootstrap3'
        });
    }
}

//Accepting a ActionPlan (forward to PMO for Approval After this)
//Need to Add Connecting to PMO Notification API (within success field of the ajax call)
function acceptActionPlan(id){
    var url = '{% url "Approve_Action_Plan" %}';
    $.ajax({
        type:"POST",
        url: 'approve_action_plan/',
        data:{ id: id},
        dataType: 'json',
        success: function (data) {
            new PNotify({
                title: "Action Plan "+id+" Accepted Successfully!",
                text: "Sending Action Plan to PMO for Approval!",
                type: 'success',
                styling: 'bootstrap3'
            });
            window.setTimeout(function(){
                reload_table();
                reload_crisis();
            },150);
        },
        error : function(xhr,errmsg,err) {
            console.log(errmsg);
        }
    });
}

//Allow the user to send chat message by pressing the Enter Key
$("#msgBox").on('keyup', function (e) {
    if (e.keyCode == 13) {
        $("#msgSendBtn").trigger('click');
    }
});

//Reset the Comments TextArea in the modal if the user cancels
$(".modal").on("hidden.bs.modal", function(){
    var body = $(this).find(".modal-body");
    var textArea = body.find('textArea');
    textArea.val('');
});

//Check if any of the Crisis Tabs are Expanded
function checkIfCrisisInactive(){
    var $_PANELS = $('.panel-heading');
    var result = true;
    $_PANELS.each(function(){
        if(!$(this).hasClass('collapsed'))
            result = false;
    });

    return result;
}

function filterMapCrisis(id){
    if(!checkIfCrisisInactive()){
        for (i = 0; i < markers.length; i++) {
            markers[i][0].setVisible(true);
            circles[i].setVisible(true);
        }
    }
    else{
        for (i = 0; i < markers.length; i++) {
            if(markers[i][1]==id){
                markers[0].setVisible(true);
                circles[i].setVisible(true);
            }
            else{
                markers[0].setVisible(false);
                circles[i].setVisible(false);
            }
        }
    }
}

function filterMapCrisis(id){
    var text;
    if(!checkIfCrisisInactive()){
        for (i = 0; i < markers.length; i++) {
            markers[i][0].setVisible(true);
            circles[i].setVisible(true);
        }
        text = "Map is no longer being filtered by any Crisis ID!";
    }
    else{
        for (i = 0; i < markers.length; i++) {
            if(markers[i][1]==id){
                markers[i][0].setVisible(true);
                circles[i].setVisible(true);
            }
            else{
                markers[i][0].setVisible(false);
                circles[i].setVisible(false);
            }
        }
        text = "Map is being filtered by Crisis ID: "+id+"!";
    }

    new PNotify({
        title: 'Map Filtered by Crisis',
        text: text,
        type: 'info',
        styling: 'bootstrap3'
    });
}

//Auto Update After 30 Seconds
setInterval(function()
{

    console.log($('#allCrisis').hasClass('active'));
    //Reload the action_plan_template, and only reload
    // all_crisis template if none of the crisis are selected
    if($('#allCrisis').hasClass('active')){
        reload_table();
        if(checkIfCrisisInactive())
            reload_crisis();
    }
    //if the ActionPlans Awaiting Approval tab is on
    //reloads the all_crisis template, and only reload action_plan_template
    //if there are no modals active
    else{
        reload_crisis();
        if($('.modal:visible').size()==0)
            reload_table();
    }

}, 30000);

//reloads the action_plan_table template
function reload_table() {
    $.ajax({
        url :"/chief/reload_table/",
        type : "GET", // http method
        // handle a successful response
        //var html;
        success : function(data) {
            $('#actionPlanTable').html(data);
        },
        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
}
//reloads the all_crisis template
function reload_crisis() {
    $.ajax({
        url :"/chief/reload_crisis/",
        type : "GET", // http method
        // handle a successful response
        //var html;
        success : function(data) {
            $('#allCrisis').html(data);
        },
        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
}


function select_crisischat(id) {
    $.ajax({
        url : "/chief/select_crisischat/", // the endpoint
        type : "GET", // http method
        // handle a successful response
        success : function(json) {

            for (var i = 0; i < json.length; i++) {
                //console.log(json[i])
                //if(json[i].id == id)
            }
            //$('#updatechat').html(data);
            $('#updatechat').load(location.href +  ' #updatechat');
            /*
             var res1;

            for(var i = 0; i < data.length; i++)
            {
                // Parse through the JSON array which was returned.
                // A proper error handling should be added here (check if
                // everything went successful or not)

                res1 = data[i].res1;

                // Do something with the returned data
                $('#updatechat').html(res1);
            }
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
}
