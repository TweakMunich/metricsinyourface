#!/bin/bash
curl –o node.tar.gz https://nodejs.org/dist/v4.1.2/node-v4.1.2-linux-x64.tar.gz
tar –zxvf node.tar.gz
mkdir metricsinyourface
cd metricsinyourface
curl –o app.js https://raw.githubusercontent.com/TweakMunich/metricsinyourface/master/server/app.js
curl –o package.json https://raw.githubusercontent.com/TweakMunich/metricsinyourface/blob/master/server/package.json
../node-v4.1.2-linux-x64/bin/npm install
../node-v4.1.2-linux-x64/bin/npm install fovever
forever start app.js
