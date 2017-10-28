var app = angular.module('chatApp', ['firebase']);

//Only for PMO - CMO

app.controller('ChatController', function($scope, $firebaseArray) {

	//Crisis
	
	var crisis = "Crisis1";
	
	//Query
	
    var ref = firebase.database().ref().child(crisis).child('CMO-PMO');
	
    $scope.messages = $firebaseArray(ref);

    $scope.send = function() {
        $scope.messages.$add({
			sender: "CMO",
            message: $scope.messageText,
            date: Date.now()
        })
    }
})