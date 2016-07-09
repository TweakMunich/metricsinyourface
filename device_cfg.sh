#!/bin/sh
#
# Enable i2c, set hostname and upgrades packages
# extracted from https://github.com/asb/raspi-config

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
sed $CONFIG -i -r -e "s/^((device_tree_param|dtparam)=([^,]*,)*i2c(_arm)?)(=[^,]*)?/\1=on/"
if ! grep -q -E "^(device_tree_param|dtparam)=([^,]*,)*i2c(_arm)?=[^,]*" $CONFIG; then
  printf "dtparam=i2c_arm=on\n" >> $CONFIG
fi

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
