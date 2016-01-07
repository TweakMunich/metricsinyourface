# metricsinyourface

An IoT project for a Raspberry PI that pulls data from the cloud and displays it in a seven-segment display. Each Pi can drive multiple displays that can be daisy-chained together. Each data display has a configurable ID and number of digits, both of which are read by the Pi via shift register.


## Client Code

The `client` folder contains the code running in the Pi. To execute: 

    sudo python display_metric.py domainname:port valueprefix

The Pi will retrieve values from the server based on an ID that is the concatenation of `valueprefix` and  the display ID, which is read from the switch on the display. For example if `valueprefix` is `foo` and a display with the ID 3 is connected to the Pi, it will look for the value of the parameter `foo3`.


## Server-side code

The `server` folder contains the code running on a public cloud. It starts a simple Web server available via HTTP.

To make it run on your machine, execute : `npm install`, then `node app.js`. A deployment script has been provided to more easily deploy on a Linux box. See the sub directory : deployment scripts. It has been tested on an EC2 instance AWS Linux AMI.

The server can easily run on AWS Beanstalk: create a zip from the file contained in the server folder after having done an 'npm install' and follow the instruction on AWS Beanstalk wizard.

#### API version 1
Set value with HTTP POST (if domain is missing, it is defaulted to *undefined*):

```
curl -v -H "Content-Type: application/json" -X POST -d  '{"domain": "testdomain", "id":"testid", "value":"200"}' http://myhost:3000/setValue
```

Get Value with HTTP GET or directly from browser (if domain is missing, it is defaulted to *undefined*): 
    
```
curl -v http://myhost:3000/getValue?id=testpi&domain=testdomain
```

#### API version 2
Set value with HTTP POST:

```
curl -v -H "Content-Type: application/json" -X POST -d  '{"value":"200"}' http://myhost:3000/:domain/:id
```

Get Value with HTTP GET or directly from browser: 

```
curl http://myhost:3000/:doman/:id
```

#### Client identifier
We are currently using the header *hostname* to identify the client.

#### System domain
System domain provides administrative/monitoring/test functions.  Current ID supported are ID = 1 and ID = 2.

System ID = 1 returns the number of clients known

System ID = 2 returns the number of active clients in the last 60 seconds 

Trying to GET access to an ID different from the known one returns an error code 404 (not found)

System domain with ID = 1 and 2 can only be queried, a POST on with prefix = 'system' returns 403 (forbidden) 


