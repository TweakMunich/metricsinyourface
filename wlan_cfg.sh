#!/bin/sh
#
# Enable i2c, set hostname and upgrades packages
# extracted from https://github.com/asb/raspi-config

WPA=/etc/wpa_supplicant/wpa_supplicant.conf

if [ -z "$2" ]; then
  echo "usage $0 bensl wlan_password"
  exit	
fi

if [ $(id -u) -ne 0 ]; then
  echo "Please run as root"
  exit
fi

echo "Adding WLAN configuration"
if ! grep -q -E "az_wpa2auth" $WPA; then
  printf "network={\n  ssid=\"az_wpa2auth\"\n  proto=RSN\n  key_mgmt=WPA-EAP\n  pairwise=CCMP\n  auth_alg=OPEN\n  eap=PEAP\n  identity=\"xxx@allianz\"\n  password=\"xxx\"\n}\n" >>$WPA
fi
sed $WPA -i -r -e "s/(^\s*identity=\")(\w+)(@allianz)/\1$1\3/"
sed $WPA -i -r -e "s/(^\s*password=\")(\w+)/\1$2/"

echo "Enabling automatic network reboot"
cp client/reset_wlan0 /etc/cron.hourly

