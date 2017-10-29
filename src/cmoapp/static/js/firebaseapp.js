var app = angular.module('chatApp', ['firebase']);

//Only for PMO - CMO
var crisisChatID;

app.controller('ChatController', function($scope, $firebaseArray) {

	//Crisis
	
	crisisChatID = "Crisis1";
    //$scope.crisis = ["1", "2", "3"];
    $scope.assignCrisis = function() {
        crisisChatID = $scope.messageText;

    }

	//Query
	
    var ref = firebase.database().ref().child(crisisChatID).child('CMO-PMO');
	
    $scope.messages = $firebaseArray(ref);

    $scope.send = function() {
        $scope.messages.$add({
			sender: "CMO",
            message: $scope.messageText,
            date: Date.now()
        })
    }
})