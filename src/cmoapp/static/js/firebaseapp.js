
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
var efApp = angular.module('EFChatApp', ['firebase1']);
var EFRef, EFCrisisChatID;
efApp.controller('EFChatController', function($scope, $firebaseArray) {
        //Crisis
        //crisisChatID = "1";
        EFCrisisChatID = 1;
        //$scope.crisis = ["1", "2", "3"];

        EFRef = firebase1.database().ref().child(EFCrisisChatID).child('CMO-EF');

        $scope.efMessages = $firebaseArray(EFRef);

        $scope.assignCrisis = function() {
            EFCrisisChatID = $scope.crisisID;
            EFRef = firebase1.database().ref().child(EFCrisisChatID).child('CMO-EF');
            $scope.efMessages = $firebaseArray(EFRef);

        }
        $scope.changeChat = function(){
            EFRef = firebase1.database().ref().child(EFCrisisChatID).child('CMO-EF');
            $scope.efMessages = $firebaseArray(EFRef);
        }

        $scope.send = function() {
            $scope.efMessages.$add({
                sender: "CMO",
                message: $scope.efMessageText,
                date: Date.now()
            })
        }
});

function changeEFChat(id){
    EFCrisisChatID = id;
    var scope1 = angular.element(document.getElementById('EFChatController')).scope();
    console.log("HI");
    console.log(scope1);
    scope1.$apply(function(){
        scope1.changeChat();
    });
}