var myNgApp = angular.module('myNgApp', []);

myNgApp.controller('AppCtrl', ['$scope', '$http',
	function($scope, $http) {
		console.log("hello world controller");

	$scope.hello = "hello world binding";

	var refresh = function() {
		$http.get('/igfoodlist').success(function(response) {
			console.log("i got the data i requested");
			$scope.igfoodlist = response;
			$scope.post = "";
		});
	}

	refresh();

	$scope.addpost = function() {
		console.log($scope.post);
		$http.post('/igfoodlist', $scope.post).success(function(response) {
			console.log(response);
			refresh();
		});
	}

	$scope.remove = function(id) {
		console.log(id);
		$http.delete('/igfoodlist/' + id).success(function(response) {
			refresh();
		});
	}

	$scope.edit = function(id) {
		console.log(id);
		$http.get('/igfoodlist/' + id).success(function(response) {
			$scope.post = response;
		});
	}

	$scope.update = function() {
		console.log($scope.post._id);
		$http.put('/igfoodlist/' + $scope.post._id, $scope.post).success(function(response) {
			refresh();
		})

	};

	$scope.deselect = function() {
		$scope.post = "";
	}

}]);

