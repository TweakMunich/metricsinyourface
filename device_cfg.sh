#!/bin/sh
#
# Enable i2c, set hostname and upgrades packages
# Relies on raspi-config noninteractive mode. tested with Jessie 2016-05-27

CONFIG=/boot/config.txt

if [ -z "$1" ]; then
  echo "usage $0 hostname"
  exit	
fi

if [ $(id -u) -ne 0 ]; then
  echo "Please run as root"
  exit
fi

echo "enabling I2C interface"
# 0 enables the interface as it's the "yes" response from whiptail
sudo raspi-config nonint do_i2c 0

echo "Setting hostname to " $1
CURRENT_HOSTNAME=`cat /etc/hostname | tr -d " \t\n\r"`
NEW_HOSTNAME=$1
echo $NEW_HOSTNAME > /etc/hostname
sed -i "s/127.0.1.1.*$CURRENT_HOSTNAME/127.0.1.1\t$NEW_HOSTNAME/g" /etc/hosts

echo "Upgrading packages..."
apt-get -y update
apt-get -y upgrade

read -p "Hit ENTER to reboot (CTRL-C to abort)" foo

echo "Rebooting..."
sync
reboot
