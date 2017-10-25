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