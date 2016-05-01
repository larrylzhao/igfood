var express = require('express');
var app = express();
var mongojs = require('mongojs');
var db = mongojs('igfoodlist', ['igfoodlist']);
var bodyParser = require('body-parser');
var fs = require("fs");

app.use(express.static(__dirname + "/public"));
app.use(bodyParser.json());

app.get('/igfoodlist', function (req, res) {
  console.log("i received a get request");

  db.igfoodlist.find(function (err, docs) {
    console.log(docs);
    res.json(docs);

  });
});

app.post('/igfoodlist', function (req, res) {
  console.log("hellooooooo" + req.body);
  db.igfoodlist.insert(req.body, function(err, doc) {
    res.json(doc);
  });
});

app.delete('/igfoodlist/:id', function (req, res) {
  var id = req.params.id;
  //console.log("hellooooooo" + id);
  db.igfoodlist.remove({_id: mongojs.ObjectId(id)}, function (err, doc) {
    res.json(doc);
  });
});

app.get('/igfoodlist/:id', function (req, res) {
  var id = req.params.id;
  console.log(id);
  db.igfoodlist.findOne({_id: mongojs.ObjectId(id)}, function (err, doc) {
    res.json(doc);
  });
});

app.get('/igfoodlist/tn/:tn', function (req, res) {
  var tn = req.params.tn;
  //tn = "BDbi1JZPndm";
  /*db.igfoodlist.findOne({link: "https://www.instagram.com/p/"+tn+"/"}, function (err, doc) {
    res.json(doc);
  });*/
  var fs = require('fs');
  fs.readFile('../../lztest/thumbnails/'+tn+'.jpg', function(err, data) {
    //if (err) throw err; // Fail if the file can't be read.
    //http.createServer(function(req, res) {
      res.writeHead(200, {'Content-Type': 'image/jpeg'});
      res.end(data); // Send the file data to the browser.
    //}).listen(8124);*/
    console.log('file opened by controller!');
  });
});

app.put('/igfoodlist/:id', function (req, res) {
  var id = req.params.id;
  //console.log(req.body.name);
  db.igfoodlist.findAndModify({query: {_id: mongojs.ObjectId(id)},
    update: {$set: {name: req.body.name, email: req.body.email, number: req.body.number}},
    new: true}, function (err, doc) {
      res.json(doc);
  });

});



/*
//Populate DB with data from imageinfo.json
var data = fs.readFileSync('../../database/imageinfo.json');
dataJSON = JSON.parse(data);
console.log(dataJSON['data'].length);
for (i = 1; i < dataJSON['data'].length; i++) { 
  console.log(i);
  db.igfoodlist.insert(dataJSON['data'][i], function(err, doc) {

  });
}
*/

app.listen(3000);
console.log("server running on port 3000");