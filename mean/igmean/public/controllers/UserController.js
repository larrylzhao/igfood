UserController = function() {};

UserController.prototype.uploadFile = function(req, res) {
    // We are able to access req.files.file thanks to 
    // the multiparty middleware
    var file = req.files.file;
    //console.log(file.name);
    //console.log(file.type);
    //console.log(file);
    var fs = require('fs');
	fs.createReadStream(file.path).pipe(fs.createWriteStream('./public/test/' + file.name));
	var python = require('child_process').spawn(
	    'python',
	    // second argument is array of parameters, e.g.:
	    ["hello.py"]
	    //, req.files.myUpload.path
	    //, req.files.myUpload.type]
	  );
	  var output = "";
	  python.stdout.on('data', function(data){ output += data });
	  python.on('close', function(code){ 
	    console.log("python output:" + output);
	    if (code !== 0) {  
	        return res.send(500, code); 
	    }
	    return res.status(200).send(file.name);
	  });
}

module.exports = new UserController();