
//PMO SECTION
var app = angular.module('chatApp', ['firebase']);
var ref, crisisChatID, destination
app.controller('ChatController', function($scope, $firebaseArray) {
        //Crisis
        //crisisChatID = "1";
        crisisChatID = 1;
        destination = 'CMO-PMO';
        //$scope.crisis = ["1", "2", "3"];
        ref = firebase.database().ref().child(crisisChatID).child(destination);
        scope = $scope;
        $scope.messages = $firebaseArray(ref);


        $scope.assignCrisis = function() {
            crisisChatID = $scope.crisisID;
            ref = firebase.database().ref().child(crisisChatID).child(destination);
            $scope.messages = $firebaseArray(ref);

        }

        $scope.changeChat = function(){
            ref = firebase.database().ref().child(crisisChatID).child(destination);
            $scope.messages = $firebaseArray(ref);
        }

        $scope.send = function() {
            $scope.messages.$add({
                sender: "CMO",
                message: $scope.messageText,
                date: Date.now()
            })
        }
});
function changeChat(id){
    crisisChatID = id;
    console.log(crisisChatID)
    var scope = angular.element(document.getElementById('ChatController')).scope();
    scope.$apply(function(){
        scope.changeChat();
    });
}


function changeDest(id){
    console.log(document.getElementById('chatTitle'));
    if(id=='CMO'){
        destination='CMO-PMO';
        document.getElementById('chatTitle').innerHTML = "<i class=\"fa fa-comments\"></i> PMO Chat";
    }
    else{
       destination='CMO-EF';
       document.getElementById('chatTitle').innerHTML = "<i class=\"fa fa-comments\"></i> EF Chat";
    }
    var scope = angular.element(document.getElementById('ChatController')).scope();
    scope.$apply(function(){
        scope.changeChat();
    });
}