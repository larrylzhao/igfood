var ig = require('instagram-node').instagram();
var request = require('request');

var config = require('../../lztest/config.json');

//console.log(config);
config.access_token = "16384709.6ac06b4.49b97800d7fd4ac799a2c889f50f2587";
ig.use({ access_token: "config.access_token",
			//client_id: config.client_id,
         	//client_secret: config.client_secret 
});

var tagName = 'brzetto';
var count = '5';
var max_tag_id = "AQBqz7-AE1aB1OumD6_yUH0QgXjLNA6C_Q2IcOHc_Jk4h_4lFzDKnLvPuLO_00LqqPcjIuwhGqHXQQ0N-R2VjbMWqqQns17aFKm4ZhuFjz6WvDsB_TSFqQytsAxR58zMLPzA20iFbn3VSBFDqIn2V0l6trmWLfxgqGSjXkCGmWqkvw";
var min_tag_id;// = "AQAa6UgrOd579zIOu45H84zuK1bieyUXx1U6Yv9upiwT0akanyZV6hoD4YLHhDc3RjxKuiPFDBGJlXz5YCF6r5yo4fTPQXbmSdVx0LsaQbxKeSTqT5ZhpiHtRqkXtoEfnX9IiIzURiHU2ZOy3BpRBOi8aiOaEvBngr7Elp9HAX-qTA";
var queryString = 'https://api.instagram.com/v1/tags/' + tagName + '/media/recent?access_token='
+ config.access_token + '&count=' + count + '&max_tag_id=' + max_tag_id;

console.log(queryString);
var index = 0;

request(queryString, function (err, res, body) {
	//console.log(err);
	//console.log(res);
	//console.log(body);
	//var reqBody = body.toString();
	reqBody = JSON.parse(body);

	/*min_tag_id = reqBody.pagination.min_tag_id;
	var link = reqBody.data[index].link;
	var tags = reqBody.data[index].tags.length;
	var likes = reqBody.data[index].likes.count;
	var time = reqBody.data[index].created_time;
	var type = reqBody.data[index].type; //must be 'image'
	var filter = reqBody.data[index].filter;
	var thumbnail = reqBody.data[index].images.thumbnail.url;
	var lowres = reqBody.data[index].images.low_resolution.url;
	var user = reqBody.data[index].user.username;

	var imageInfo = '\n min_tag_id: ' + min_tag_id +
					'\n Time: ' + time +
					'\n type: ' + type +
					'\n tags: ' + tags +
					'\n user: ' + user + //need # of subs user has
					'\n likes: ' + likes +
					'\n thumbnail: ' + thumbnail +
					'\n lowres: ' + lowres +
					'\n';
	console.log(imageInfo);*/
	console.log(reqBody.data[4]);

	var fs = require('fs');
	fs.writeFile("igFetch.txt", body, function(err) {
	    if(err) {
	        return console.log(err);
	    }

    console.log("The file was saved!");
}); 
});


