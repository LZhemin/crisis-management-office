//Collapse to the right
$(document).ready(function() {
    $('.collapse-link-right').on('click', function () {
        var $BOX_PANEL = $(this).closest('.x_content'),
            $TOGGLE_PANEL = $($(this).attr('id')),
            $OWN_PANEL = $('#own'),
            $ICON = $(this).find('i'),
            $PLACEHOLDER = $(this).find('h2');
        // fix for some div with hardcoded fix class

        $ICON.toggleClass("fa-chevron-left fa-chevron-right");
        if ($ICON.attr('class') == "fa-chevron-left")
            $PLACEHOLDER.html("View Comments<i class='fa fa-chevron-left'></i>");
        else
            $PLACEHOLDER.html("Close Comments<i class='fa fa-chevron-right'></i>");
        console.log($TOGGLE_PANEL.is(":visible"));
        if($TOGGLE_PANEL.is(":visible")){

            $TOGGLE_PANEL.addClass('fadeOutRight animated').one('webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend', function(){
                $TOGGLE_PANEL.removeClass('fadeOutRight animated');
                $OWN_PANEL.toggleClass('col-sm-9 col-sm-12');
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