# metricsinyourface
An IoT project mixing RaspberryPI code and code for the Cloud.
This project will contain the overall documentation and the kanban board.

The client folder contains the code running in the pi to display data on the 7 segment digits after reading the value to display on the server. To execute : sudo python domainname:port piid

The server folder is the code running somewhere on a public cloud. To make it run on your machine, execute : npm install, then node app.js. A deployment script has been provided to deploy on a linux box. See the sub directory : deployment scripts. It has been tested on an EC2 instance AWS Linux AMI.

The server can easily run on AWS Beanstalk, create a zip from the file contained in the server folder after havind done an 'npm install' and follow the instruction on AWS Beanstalk wizard.
