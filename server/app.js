// A very simple key-value store. Keys and values can be any string.
// 
// Override default port 3000 with PORT=1234 environment variable
//
// Set value with HTTP POST:
// curl -v -H "Content-Type: application/json" -X POST -d  '{"id":"testpi", "value":"200"}' http://myhost:3000/setValue
// 
// Get Value with HTTP GET (or directly from browser): 
// curl http://myhost:3000/getValue?id=testpi
// 


var express = require('express');
var bodyParser = require('body-parser');
var port = process.env.PORT || 3000;
var app = express();
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

var array = [];
// Persist storage
var storage = require('node-persist');
// flag for logging storage actions for debug
var logging = true;
// storage folder 
var storageBaseDir = __dirname +'/storage';
//you must first call storage.init or storage.initSync 
var metrics = storage.create({logging: true, dir: storageBaseDir + '/metrics'});
metrics.initSync();
var monitor = storage.create({logging: true, dir: storageBaseDir + '/monitor'});
monitor.initSync();

// set value in metrics storage
function setValue(req, res){
	var id = req.body.id;
    var value = req.body.value;
    if (id && value) {
      //array[id] = value;
      metrics.setItem(id, value);
      res.send(id + ': ' + value);
    } else {
      res.status(400).send('must post "id" and "value"');
    }
};

// get a value from metrics storage
function getValue(req, res) {
    if(req.param("id")) {
        res.send({"id" : req.param("id"),
                "value" : metrics.getItem(req.param("id"))});
    }
}

// save in monitor storage last time (in UTC) a request was received by a client and the metric
// using a JSON like {"metric":"1","tStamp":"2016-01-02T19:30:20.234Z"}
function setMonitor(req, res, next) {
	hostname = req.headers['hostname'];
	id = req.param("id");
	if(id && hostname){
		monitor.setItem(hostname, {metric : id , tStamp: new Date() } );
	}
	next();
}

// retrieve all monitor data from monitor storage
function getMonitor(req, res){
	result = {};
	monitor.forEach(function(key,value){
		result[key] = value;
	});
	res.status(200).send(result);
}

app.post('/setValue', setValue);

app.get('/getValue', setMonitor, getValue);

app.get('/getMonitor', getMonitor );

app.use(express.static('static'));

var server = app.listen(port, function () {
    var host = server.address().address;
    var port = server.address().port;

    console.log('Metrics in your face listening at http://%s:%s', host, port);
});
