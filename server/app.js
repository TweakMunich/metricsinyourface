// A very simple key-value store. Keys and values can be any string except "0".
//
// Override default port 3000 with PORT=1234 environment variable or 
// command line argument
//
// Set value with HTTP POST:
// curl -v -H "Content-Type: application/json" -X POST -d  '{"id":"testpi", "value":"200"}' http://myhost:3000/setValue
//
// Get Value with HTTP GET (or directly from browser):
// curl http://myhost:3000/:prefix/:id 
// curl http://myhost:3000/getValue?domain=:prefix&id=:id 
// curl http://myhost:3000/getValue?id=:id (deprecated)
//
// prefix = 'system' is reserved (no updates possible):
//   id 1 - number devices known
//   id 2 - number of active devices (made a request in last 60 seconds)


var express = require('express');
var bodyParser = require('body-parser');
var port = process.argv[2] || process.env.PORT || 3000;
var app = express();
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

// Persist storage
var storage = require('node-persist');
// flag for logging storage actions for debug
var logging = false;
// storage folder
var storageBaseDir = __dirname +'/storage';
//you must first call storage.init or storage.initSync
var metrics = storage.create({"logging": logging, "dir": storageBaseDir + '/metrics'});
metrics.initSync();
var monitor = storage.create({"logging": logging, "dir": storageBaseDir + '/monitor'});
monitor.initSync();

// identifier of the reserved system domain
var SYSTEM_DOMAIN = "system";

//*****************************************
//      UTILITY FUNCTIONS
//*****************************************

// Parse the request path and break it down into version, domain, id
function _parse(req){
  path = req.path.split("/");
  version = "na";
  domain = "";
  id = "";
  if (path.length == 4 && path[1] == "api") {
    version = "2";
    domain = path[2];
    id = path[3];
  }
  else if (path.length == 2 && path[1] == "setValue"){
    version = "1";
    domain = req.body.domain ? req.body.domain : "";
    id = req.body.id;
  }
  else if (path.length == 2 && path[1].toLowerCase() == "getvalue"){
    version = "1";
    domain = req.query.domain ? req.query.domain : "";
    id = req.query.id;
  }
  return {"version": version, "domain": domain, "id": id};
}

// the key is generated as concatenation of <domain> + '_' + <id>
function _createKey( domain, id){
  return domain ? "" + domain + "_" + id : "" + id;
}

// build the response JSON as {"domain":domain, "id":id, "value":value}
function _format(path, value){
    return {"domain":path.domain,"id":path.id, "value":value};
}


//*****************************************
//      Request Handler Callbacks
//*****************************************

// set value in metrics storage
function write(req, res){
  path = _parse(req);

  if (path.version == "1" && !req.body.domain)
    path.domain = req.body.domain;

  var value = req.body.value;

  console.log(path);
  console.log(value);

  // do not allow client to post on system domain
  if( path.domain == SYSTEM_DOMAIN )
    res.status(403).send();
  else {
    if (path.id && value) {
      key = _createKey(path.domain, path.id);
      metrics.setItem(key, {"value":value, "lastUpdateDt": new Date()});
      res.send(_format(path, value));
    } else {
      res.status(400).send('must post "id" and "value"');
    }
  }
};

// get a value from metrics storage only if ID is not empty
function read(req, res) {
  path = _parse(req);
  // console.log(path);
  if (path.id) {
    key = _createKey(path.domain, path.id);
    value = metrics.getItem(key);
    if (value)
      res.send(_format(path,value.value));
    else
      res.status(404).send("not found");
  }
  else {
    res.send("Malformed request!");
  }
}


// save the last time (in UTC) a request was received by a client identified
// by the REMOTE_HOST HTTP header in a using a JSON like 
// {version: "1", "metric": "domain_id","lastUpdateDt":"2016-01-02T19:30:20.234Z"}
function heartbeat(req, res, next) {
  hostname = req.headers['remote_host'];
  path = _parse(req);
  if (hostname && path.id) {
    monitor.setItem(hostname, {"version": path.version, 
                               "metric" : _createKey(path.domain, path.id),
                               "lastUpdateDt": new Date() } );
  }
  next();
}

// if prefix is 'system' store system metrics to be retrieved by _read
function stats(req, res, next) {
  path = _parse(req);
  if (path.domain == SYSTEM_DOMAIN) {
    if (path.id == "1") {
        metrics.setItem(_createKey(path.domain, path.id), {"value":monitor.length(),"lastUpdateDt":new Date()});
    }
    else if (path.id == "2") {
      count = 0;
      now = new Date();
      monitor.forEach(function(key,value){
        tstamp = value.lastUpdateDt;
        if (now-tstamp <= 60000)
          count++;
        });
      metrics.setItem(_createKey(path.domain, path.id),{"value":count,"lastUpdateDt":new Date()});
    }
  }
  next();
}


//*****************************************
//      VERSION 1
//*****************************************
app.post('/setValue', write);
app.get('/getValue', heartbeat, stats, read);

//*****************************************
//      VERSION 2
//*****************************************
app.post('/api/*', write);
app.get('/api/*', heartbeat, stats, read);


app.use(express.static('static'));

var server = app.listen(port, function () {
    var host = server.address().address;
    var port = server.address().port;

    console.log('Metrics in your face listening at http://%s:%s', host, port);
});
