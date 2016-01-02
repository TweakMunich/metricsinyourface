// A very simple key-value store. Keys and values can be any string.
// 
// Override default port 3000 with PORT=1234 environment variable
//
// Set value with HTTP POST:
// curl -v -H "Content-Type: application/json" -X POST -d  '{"id":"testpi", "value":"200"}' http://myhost:3000/setValue
// 
// Get Value with HTTP GET (or directly from browser): 
// curl http://myhost:3000/:prefix/:id with prefix = 'system' being reserved and id equal to 1 and 2 respectively for the 
// display count and active display count (a display is active if made a request in last 60 seconds)
// 


var express = require('express');
var bodyParser = require('body-parser');
var port = process.env.PORT || 3000;
var app = express();
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

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

function parse(req){
  path = req.path.split("/");
  ctx = {"domain":path[2], "id":path[3]};
  return ctx;
}

function getId(path){
  domain = path.domain;
  id= path.id;
  return domain + "_" + id;
}


// old set value
// set value in metrics storage
function setValue(req, res){
	var id = req.body.domain + "_" + req.body.id;
    var value = req.body.value;
    if (id && value) {
      //array[id] = value;
      metrics.setItem(id, value);
      res.send(id + ': ' + value);
    } else {
      res.status(400).send('must post "id" and "value"');
    }
};
// set value in metrics storage
function write(req, res){
	path = parse(req);
	id = getId(path);
    var value = req.body.value;
    if (id && value) {
      metrics.setItem(id, value);
      res.send(id + ': ' + value);
    } else {
      res.status(400).send('must post "id" and "value"');
    }
};

// get a value from metrics storage
function read(req,res) {
	path = parse(req);
	if(path.prefix && path.id){
		id = getId(path);
        res.send({"id" : id, "value" : metrics.getItem(id)});
	}
	else
	{
		res.send("Malformed request!");
	}
}

// save in monitor storage last time (in UTC) a request was received by a client and the metric
// using a JSON like {"metric":"1","tStamp":"2016-01-02T19:30:20.234Z"}
function heartbeat(req, res, next) {
	hostname = req.headers['hostname'];
	path = parse(req);
	id = getId(path);
	if(hostname && id){
		monitor.setItem(hostname, {metric : id , tStamp: new Date() } );
	}
	next();
}

// check if prefix is 'system' and managed metrics for system channels 1 and 2 
function stats(req, res, next) {
	path = parse(req);
	if(path.domain == "system")
	{		
		if(path.id=="1")
		{
			id = getId(path);
			metrics.setItem(id,monitor.length());
		}
		else if (path.id == "2")
		{
			count = 0;
			now = new Date();
			monitor.forEach(function(key,value){
			  tstamp = value.tStamp;
			  if(now-tstamp<60000) 
				  count++;
			});
			id = getId(path);
			metrics.setItem(id,""+count);
		}
	}
	next();
}


app.post('/setValue', setValue);

app.post('/api/*', write);

app.get('/api/*', heartbeat, stats, read);

app.use(express.static('static'));

var server = app.listen(port, function () {
    var host = server.address().address;
    var port = server.address().port;

    console.log('Metrics in your face listening at http://%s:%s', host, port);
});
