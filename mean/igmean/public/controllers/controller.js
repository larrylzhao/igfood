var myNgApp = angular.module('myNgApp', ['ngAnimate', 'ui.bootstrap', 'ngFileUpload']);

myNgApp.controller('AppCtrl', ['$scope', '$http', 'Upload', '$timeout',
	function($scope, $http, Upload, $timeout) {
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
	$scope.imgName = "";
	$scope.imgHeight = 300;
	$scope.imgWidth = 300;
	   var tmpstr = "BFE20Rpnx5X";
	// $scope.orig = "upload/orig/"+tmpstr;
 //    $scope.cb = "upload/cb/"+tmpstr;
	// $scope.rhisto = "upload/rhisto/"+tmpstr;
	// $scope.ghisto = "upload/ghisto/"+tmpstr;
	// $scope.bhisto = "upload/bhisto/"+tmpstr;
	$scope.uploadFiles = function(file, errFiles) {
        $scope.f = file;
        $scope.errFile = errFiles && errFiles[0];
        if (file) {
        	console.log("i got a file upload");
            file.upload = Upload.upload({
                url: '/upload',
                data: {file: file}
            });

            file.upload.then(function (response) {
            	var str = response.data;
            	str = str.replace(/\.jpg/i, "");
            	$scope.imgName = str;
            	$scope.orig = "upload/orig/"+str;
            	$scope.cb = "upload/cb/"+str;
            	$scope.rhisto = "upload/rhisto/"+str;
            	$scope.ghisto = "upload/ghisto/"+str;
            	$scope.bhisto = "upload/bhisto/"+str;
            	$scope.show = true;
            	$http.get('/upload/origSize/'+str).success(function(response) {
            		console.log(response);
            		$scope.imgWidth = response[0];
            		$scope.imgHeight = response[1];    
	            	var twoface = TwoFace('twoface-demo', $scope.imgWidth, $scope.imgHeight);
					twoface.add("upload/orig/"+str);
					twoface.add("upload/cb/"+str);
				});
                $timeout(function () {
                    file.result = response.data;
                });
            }, function (response) {
            	//console.log("upload response: " + response);
                if (response.status > 0)
                    $scope.errorMsg = response.status + ': ' + response.data;
            }, function (evt) {
                file.progress = Math.min(100, parseInt(100.0 * 
                                         evt.loaded / evt.total));
            });
        }   
    }

    function TwoFace(id, width, height) {
    if (!(this instanceof TwoFace)) {
        return new TwoFace(id, width, height);
    }

    var canvas = document.createElement('canvas'),
        container = document.getElementById(id),
        divide = 0.5;

    this.ctx = canvas.getContext('2d');
    this.images = [];

    // Event handlers
    canvas.addEventListener('mousemove', handler, false);
    canvas.addEventListener('mousedown', handler, false);
    canvas.addEventListener('mouseup', handler, false);

    var self = this;

    function handler(ev) {
        if (ev.layerX || ev.layerX == 0) { // Firefox
            ev._x = ev.layerX;
            ev._y = ev.layerY;
        } else if (ev.offsetX || ev.offsetX == 0) { // Opera
            ev._x = ev.offsetX;
            ev._y = ev.offsetY;
        }

        var eventHandler = self[ev.type];
        if (typeof eventHandler == 'function') {
            eventHandler.call(self, ev);
        }
    }

    // Draw canvas into its container
    canvas.setAttribute('width', $scope.imgWidth);
    canvas.setAttribute('height', $scope.imgHeight);
    if (container.childNodes[0]) {
    	container.removeChild(container.childNodes[0]);
	}
    container.appendChild(canvas);
    console.log(container.childNodes);

    Object.defineProperty(this, 'ready', {
        get: function() {
            return this.images.length >= 2;
        }
    });

    Object.defineProperty(this, 'width', {
        get: function() {
            return width;
        }
    });

    Object.defineProperty(this, 'height', {
        get: function() {
            return height;
        }
    });

    Object.defineProperty(this, 'divide', {
        get: function() {
            return divide;
        },
        set: function(value) {
            if (value > 1) {
                value = (value / 100);
            }

            divide = value;
            this.draw();
        }
    });
}




TwoFace.prototype = {
    add: function(src) {
        var img = createImage(src, onload.bind(this));

        function onload(event) {
            this.images.push(img);

            if (this.ready) {
                this.draw();
            }
        }
    },

    draw: function() {
        if (!this.ready) {
            return;
        }

        var lastIndex = this.images.length - 1,
            before = this.images[lastIndex - 1],
            after = this.images[lastIndex];

        this.drawImages(this.ctx, before, after);
        this.drawHandle(this.ctx);
    },

    drawImages: function(ctx, before, after) {
        var split = this.divide * this.width;

        ctx.drawImage(after, 0, 0);
        ctx.drawImage(before, 0, 0, split, this.height, 0, 0, split, this.height);
    },

    drawHandle: function(ctx) {
        var split = this.divide * this.width;
        
        ctx.fillStyle = "rgb(220, 50, 50)";
        ctx.fillRect(split - 1, 0, 2, this.height);
    },

    mousedown: function(event) {
        var divide = event._x / this.width;
        this.divide = divide;

        this.dragstart = true;
    },

    mousemove: function(event) {
        if (this.dragstart === true) {
            var divide = event._x / this.width;
            this.divide = divide;
        }
    },

    mouseup: function(event) {
        var divide = event._x / this.width;
        this.divide = divide;

        this.dragstart = false;
    }
};




function createImage(src, onload) {
    var img = document.createElement('img');
    img.src = src;

    if (typeof onload == 'function') {
        img.addEventListener('load', onload);
    }

    return img;
}






}]);








