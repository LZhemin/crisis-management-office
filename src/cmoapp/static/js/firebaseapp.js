
//PMO SECTION
var app = angular.module('chatApp', ['firebase']);
var ref, crisisChatID;
app.controller('ChatController', function($scope, $firebaseArray) {
        //Crisis
        //crisisChatID = "1";
        crisisChatID = 1;
        //$scope.crisis = ["1", "2", "3"];
        ref = firebase.database().ref().child(crisisChatID).child('CMO-PMO');
        scope = $scope;
        $scope.messages = $firebaseArray(ref);


        $scope.assignCrisis = function() {
            crisisChatID = $scope.crisisID;
            ref = firebase.database().ref().child(crisisChatID).child('CMO-PMO');
            $scope.messages = $firebaseArray(ref);

        }
        $scope.changeChat = function(){
            ref = firebase.database().ref().child(crisisChatID).child('CMO-PMO');
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
