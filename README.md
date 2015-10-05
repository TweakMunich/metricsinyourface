# metricsinyourface
An IoT project mixing RaspberryPI code and code for the Cloud.
This project will contain the overall documentation and the kanban board.

The client folder contains the code running in the pi to display data on the 7 segment digits after reading the value to display on the server. (Python 3 code)

The server folder is the code running somewhere on a public cloud. To make it run on your machine, execute : npm install, then node app.js. (NodeJS 0.12 code)

To make it run on AWS Beanstalk, create a zip from this the file contained in this folder and follow the instruction on AWS Beanstalk wizard.
