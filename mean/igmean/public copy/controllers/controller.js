var myNgApp = angular.module('myNgApp', []);

myNgApp.controller('AppCtrl', ['$scope', '$http',
	function($scope, $http) {
		console.log("hello world controller");

	var refresh = function() {
		$http.get('/contactlist').success(function(response) {
			console.log("i got the data i requested");
			$scope.contactlist = response;
			$scope.contact = "";
		});
	}

	refresh();

	$scope.addContact = function() {
		console.log($scope.contact);
		$http.post('/contactlist', $scope.contact).success(function(response) {
			console.log(response);
			refresh();
		});
	}

	$scope.remove = function(id) {
		console.log(id);
		$http.delete('/contactlist/' + id).success(function(response) {
			refresh();
		});
	}

	$scope.edit = function(id) {
		console.log(id);
		$http.get('/contactlist/' + id).success(function(response) {
			$scope.contact = response;
		});
	}

	$scope.update = function() {
		console.log($scope.contact._id);
		$http.put('/contactlist/' + $scope.contact._id, $scope.contact).success(function(response) {
			refresh();
		})

	};

	$scope.deselect = function() {
		$scope.contact = "";
	}

}]);

