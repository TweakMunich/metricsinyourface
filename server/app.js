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

app.post('/setValue', function (req, res) {
    var data = req.body;
    array[data.id] = data.value;
    res.send(data);
});

app.get('/getValue', function (req, res) {
    if(req.param("id"))
    {
        res.send({"id" : req.param("id"),
                "value" : array[req.param("id")]});
    }
});

var server = app.listen(port, function () {
    var host = server.address().address;
    var port = server.address().port;

    console.log('Metrics in your face listening at http://%s:%s', host, port);
});
