function sendDeployment(id){
    //Code to send Notification to PMO to retrieve the Data to send
    $$.ajax({
        type:"POST",
        url: 'get_deployment_plan/',
        data:{id:id}
        ,
        dataType: 'json',
        success: function (data){

            //Call to Ef API to Send Data
            $.ajax({
                type:"POST",
                url: '',
                data:data,
                dataType: 'json',
                success: function (data) {

                },
                error : function(xhr,errmsg,err) {
                    console.log(errmsg);
                }
            });
        }
        ,
        error : function(xhr,errmsg,err) {
            console.log(errmsg);
        }
    });



}

function sendNotificationPMO(id){
    //Code to send Notification to PMO to retrieve the ActionPlan
    $.ajax({
        type:"POST",
        url: '',
        data:{ id: id},
        dataType: 'json',
        success: function (data) {
            /*
            new PNotify({
                title: "Action Plan",
                text: "Sending Action Plan to PMO for Approval!",
                type: 'success',
                styling: 'bootstrap3'
            });*/
        },
        error : function(xhr,errmsg,err) {
            console.log(errmsg);
        }
    });
}