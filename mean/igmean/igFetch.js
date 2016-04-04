var ig = require('instagram-node').instagram();
var request = require('request');

var config = require('../../lztest/config.json');

//console.log(config);
config.access_token = "16384709.6ac06b4.49b97800d7fd4ac799a2c889f50f2587";
ig.use({ access_token: "config.access_token",
			//client_id: config.client_id,
         	//client_secret: config.client_secret 
});

var endTime = '1459048599';
var startTime = '1459656933';
var tagName = 'resourcemagazine';
var count = '10';
var max_tag_id = '';

var i = 0;
//while (startTime > endTime) {
while (i < 4) {
	i++;
	console.log(i + ': ' + max_tag_id);


	
	var queryString = 'https://api.instagram.com/v1/tags/' + tagName + '/media/recent?access_token='
	+ config.access_token + '&count=' + count + '&max_tag_id=' + max_tag_id;

	//console.log(queryString);
	var index = 0;

	request(queryString, function (err, res, body) {

		reqBody = JSON.parse(body);

		max_tag_id = reqBody.pagination.next_max_tag_id;
		var link = reqBody.data[index].link;
		var tags = reqBody.data[index].tags.length;
		var likes = reqBody.data[index].likes.count;
		var time = reqBody.data[index].created_time;
		var type = reqBody.data[index].type; //must be 'image'
		var filter = reqBody.data[index].filter;
		var thumbnail = reqBody.data[index].images.thumbnail.url;
		var lowres = reqBody.data[index].images.low_resolution.url;
		var user = reqBody.data[index].user.username;

		var imageInfo = '\n max_tag_id: ' + max_tag_id +
						'\n Time: ' + time +
						'\n type: ' + type +
						'\n tags: ' + tags +
						'\n user: ' + user + //need # of subs user has
						'\n likes: ' + likes +
						'\n thumbnail: ' + thumbnail +
						'\n lowres: ' + lowres +
						'\n';
		console.log(imageInfo);
		//console.log(reqBody.data[4]);

		startTime = time;

		
	});
	var timer = setTimeout(function () {
        var dataArray = [123, 456, 789, 012, 345, 678];
        callback(dataArray);
    }, 3000);
}


/*var fs = require('fs');
		fs.writeFile("igFetch.txt", body, function(err) {
		    if(err) {
		        return console.log(err);
		    }
		    console.log("The file was saved!");
		}); 
*/
