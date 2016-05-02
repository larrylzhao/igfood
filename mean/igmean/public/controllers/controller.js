var myNgApp = angular.module('myNgApp', ['ngAnimate', 'ui.bootstrap']);

myNgApp.controller('AppCtrl', ['$scope', '$http',
	function($scope, $http) {
		console.log("hello world controller");

	//$scope.hello = "hello world binding";
	var igfoodlist = [];
	var refresh = function() {
		$http.get('/igfoodlist').success(function(response) {
			console.log("i got the data i requested");
			igfoodlist = response;
			$scope.thumbnails = [];
			for (i = 0; i < igfoodlist.length; i++) {
			//for (i = 0; i < 2; i++) {
				var fname = igfoodlist[i].link;
				var patt = /p\/(.+)\/$/;
				var match = patt.exec(fname);
				$scope.thumbnails[i] = "igfoodlist/tn/"+match[1];
			}
			//$scope.post = "";
		});
	}

	refresh();

	$scope.addpost = function() {
		//console.log($scope.post);
		$http.post('/igfoodlist', $scope.post).success(function(response) {
			//console.log(response);
			refresh();
		});
	}

	$scope.remove = function(id) {
		//console.log(id);
		$http.delete('/igfoodlist/' + id).success(function(response) {
			refresh();
		});
	}

	$scope.edit = function(id) {
		//console.log(id);
		$http.get('/igfoodlist/' + id).success(function(response) {
			$scope.post = response;
		});
	}

	$scope.update = function() {
		//console.log($scope.post._id);
		$http.put('/igfoodlist/' + $scope.post._id, $scope.post).success(function(response) {
			refresh();
		})

	};

	$scope.deselect = function() {
		$scope.post = "";
	}



	$scope.colorGroups = ["pink","purple","red","orange","yellow","green","cyan","blue","brown","white","grey"];
	$scope.colors = [];
	$scope.colors['pink'] = ["pink","lightpink","hotpink","deeppink","palevioletpred","mediumvioletred"];
	$scope.colors['purple'] = ["Lavender","Thistle","Plum"];
	$scope.isCollapsed = true;

	$scope.oneAtATime = true;
	$scope.status = {
	    isFirstOpen: true,
	    isFirstDisabled: false
	};
	$scope.show = false;

}]);









