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

function rejectActionPlan(id){
    var commnet = document.getElementsById("commentAP"+id);

}

function acceptActionPlan(id){

}

$("#msgBox").on('keyup', function (e) {
    if (e.keyCode == 13) {
        $("#msgSendBtn").trigger('click');
    }
});


$(".modal").on("hidden.bs.modal", function(){
    var body = $(this).find(".modal-body");
    var textArea = body.find('textArea');
    textArea.val('');
});

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