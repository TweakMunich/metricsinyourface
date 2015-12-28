#!/bin/sh 

# copy into /etc/cron.hourly
ping -c1 www.google.com  > /dev/null
 
if [ $? != 0 ] 
then
  echo "No network connection, restarting wlan0"
  ifdown 'wlan0'
  sleep 5
  ifup --force 'wlan0'
fi
