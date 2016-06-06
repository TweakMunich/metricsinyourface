# metricsinyourface

A simple IoT project that pulls data from the cloud (the "server") and displays it on a seven-segment display (the "client"). Seven-segment displays are a bit retro but very easy to read and more attention-getting than a tablet or small screen. Also, you can connect very large displays up to 10cm.

One or more displays, each with a configurable ID or "Channel", are connected to a Raspberry Pi, which updates the display(s) every few seconds with data fetched from the cloud. Integer or floating point numbers plus a few special characters can be displayed.

## Hardware
To preserve the number of GPIO ports used, input and output occurs either via shift registers ('595 for output, '166 for input) or I2C bus (Adafruit LED backpacks based on HT16K33 for output, MCP23017 for input) . 

* Serial input: Each display's configurable ID and number of digits can be read from chained shift registers, 16 bits per display. Bits 0-11 are the display ID (aka "channel"), Bits 13-15 specify the number of digits (000 = 1, 110 = 7, 111 not allowed), Bit 12 is not used. 
* I2C input: The same bit assigment, but read from a 16 bit I2C port expander, which saves a lot of wiring. Multiple expanders can be connected (one for each display), addresses in ascending order of tehir I2C address (0x20 - 0x27).
* Serial Display: Large displays can be driven via chained shift registers, 8 bits per digit. The Pi shifts the correct number of digits for each display so that they can be chained together without addressing.
* I2C Display: To simplify soldering you can connect 4-digit I2C displays from Adafruit. The displays are addressed in ascending order of their I2C address (0x80 - 0x87).

## Client Code

The `client` folder contains the code running in the Pi. To execute: 

    sudo python display_metric.py url domain

The Pi retrieves values to be displayed from the server based on the display ID and the `domain` string. For example if `valueprefix` is `foo` and a display with the ID 3 is connected to the Pi, it will look for the value of the parameter `foo3`.


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
curl http://myhost:3000/api/:domain/:id
```

#### Client identifier
The server is using the header *remote_host* to identify the client.

#### System domain
The `system` domain provides administrative/monitoring/test functions.  The following ID's are currently supported:

* 1 returns the number of clients known
* 2 returns the number of clients that were active in the last 60 seconds 

Trying to GET access to an ID different from the known one returns an error code 404 (not found)

System domain with ID = 1 and 2 can only be queried, a POST on with prefix = 'system' returns 403 (forbidden) 


