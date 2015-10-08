var express = require('express');
var bodyParser = require('body-parser');
var port = process.env.PORT || 3000;
var app = express();
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

var array = [];

app.post('/setValue', function (req, res) {
    var id = req.body.id;
    var value = req.body.value;
    if (id && value) {
      array[id] = value;
      res.send(id + ': ' + value);
    } else {
      res.status(400).send('must post "id" and "value"');
    }
});

app.get('/getValue', function (req, res) {
    if(req.param("id")) {
        res.send({"id" : req.param("id"),
                "value" : array[req.param("id")]});
    }
});

app.get('/', function (req, res) {
    res.send('<html><form action="/setValue" method="post">' + 
            'id: ' + 
            '<input type="text" name="id"><br>' +
            'value: ' + 
            '<input type="text" name="value"><br>' +
            '<input type="submit" value="Submit">' +
            '<form/></html>');
});

var server = app.listen(port, function () {
    var host = server.address().address;
    var port = server.address().port;

    console.log('Metrics in your face listening at http://%s:%s', host, port);
});
