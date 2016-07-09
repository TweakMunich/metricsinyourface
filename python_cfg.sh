#!/bin/sh
#
# Install adafruit python packages

if [ $(id -u) -ne 0 ]; then
  echo "Please run as root: sudo" $0
  exit
fi
 
sudo apt-get -y install python-pip python-smbus
sudo pip -y install adafruit-led-backpack

