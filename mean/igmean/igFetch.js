var ig = require('instagram-node').instagram();
var request = require('request');

var config = require('../../lztest/config.json');

//console.log(config);
config.access_token = "16384709.6ac06b4.49b97800d7fd4ac799a2c889f50f2587";
ig.use({ access_token: "config.access_token",
			//client_id: config.client_id,
         	//client_secret: config.client_secret 
});

var tagName = 'coding';
var count = '2';
var queryString = 'https://api.instagram.com/v1/tags/' + tagName + '/media/recent?access_token='
+ config.access_token + '&count=' + count;

console.log(queryString);

request(queryString, function (err, res, body) {
	//console.log(err);
	//console.log(res);
	//console.log(body);
	var reqBody = body.toString();
	reqBody = JSON.parse(reqBody);
	//console.log(reqBody);
	console.log(reqBody.data)
});


