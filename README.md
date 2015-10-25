# metricsinyourface

An IoT project for a Raspberry PI that pulls data from the cloud and displays it in a seven-segment display. Each Pi can drive multiple displays that can be daisy-chained together. Each data display has a configurable ID and number of digits, both of which are read by the Pi.


## Client Code

The `client` folder contains the code running in the Pi. To execute: 

    sudo python domainname:port valueprefix

The Pi will retrieve values with the `valueprefix` concatenated with the display ID. For example if `valueprefix` is `foo` and a display with the ID 3 is connected to the Pi, it will look for the value of the parameter `foo3`.


## Server-side code

The `server` folder contains the code running on a public cloud. It starts a simple Web server available via HTTP.

To make it run on your machine, execute : `npm install`, then `node app.js`. A deployment script has been provided to more easily deploy on a Linux box. See the sub directory : deployment scripts. It has been tested on an EC2 instance AWS Linux AMI.

The server can easily run on AWS Beanstalk: create a zip from the file contained in the server folder after having done an 'npm install' and follow the instruction on AWS Beanstalk wizard.



