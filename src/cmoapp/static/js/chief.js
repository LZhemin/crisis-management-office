
//Collapse to the right
var efCount = -1;
$(document).ready(function() {
    //Collapse to the right code
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

//Change Status of the Crisis
function changeStatus(id,status){
    $.ajax({
        type:"POST",
        url: "change_status/",
        data: { id: id, status: status},
        dataType: 'json',
        success: function (data) {
            console.log(data);
            new PNotify({
                title: "Crisis Status Changed!",
                text: "Crisis "+id+" Status Changed to "+status+"!",
                type: 'success',
                styling: 'bootstrap3'
            });
            $('#collapse'+id).addClass('collapse');
            console.log('Here!');
            window.setTimeout(function(){
                reload_table();
                reload_crisis();
            },150);
        },
        error: function(data){
            console.log(data);
        }
    });
    filterMapCrisis(id);
}

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
    sendNotificationPMO(id);
}

//Allow the user to send chat message by pressing the Enter Key
$("#msgBox").on('keyup', function (e) {
    if (e.keyCode == 13) {
        $("#msgSendBtn").trigger('click');
        $(this).val("");
    }
});

//Allow the user to send chat message by pressing the Enter Key
$("#efMsgBox").on('keyup', function (e) {
    if (e.keyCode == 13) {
        $("#efMsgSendBtn").trigger('click');
        $(this).val("");
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
    var text;
    //Dont Filter anything if no Crisis Selected
    if(!checkIfCrisisInactive()){
        for (i = 0; i < markers.length; i++) {
            markers[i][0].setVisible(true);
            circles[i].setVisible(true);
        }

        //Show all EFUpdates
        $('#efUpdateList').find('li').each(function(){
            $(this).show();
        });
        text = "Site no longer being filtered by Crisis ID!";
        changeChat('GeneralChat');
        changeEFChat('GeneralChat');
    }
    //Filter if Crisis is selected
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
        //Filter the EFUpdates based on the Crisis Selected
        $('#efUpdateList').find('li').each(function(){
            var div = $(this).find('div')[0];
            if(div.id==('efCrisis'+(id)))
                $(this).show();
            else
                $(this).hide();
        });
        text = "Showing Stats of Crisis ID: "+id+"!";
        changeChat(id);
        changeEFChat(id);
    }

    new PNotify({
        title: 'Stats Filtered by Crisis',
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
    checkEfUpdate();

}, 30000);

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

function reloadEfUpdate(count){
    var array = [];
    var html = "";
    $.ajax({
        type:"POST",
        url: "get_efupdates/",
        data:{'startNum':count},
        dataType: 'json',
        success: function (data) {
            array = JSON.parse(data);
            console.log(array[0]['fields']);
            for(update in array){
                html += "<li><div id='efCrisis"+array[update]['crisis']+"' class='block'>" +
                            "<div class='block_content'> " +
                                "<h2 class='title'>Crisis "+array[update]['crisisTitle']+"</h2> " +
                                "<div class='byline'>"+array[update]['datetime']+"</div> " +
                                    "<p class='excerpt'>"+array[update]['description']+"</p> " +
                                "</div> " +
                            "</div> " +
                        "</li>";
            }
            $('#efUpdateList').append(html);
        },
        error: function(data){
            console.log(data);
        }
    });
}


//reloads the action_plan_table template
function reload_table() {
    $.ajax({
        url :"reload_table/",
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
        url :"reload_crisis/",
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

}
