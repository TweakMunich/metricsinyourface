#! /usr/bin/python
#
# sudo python display_metric.py domain_name.com metric_id
#
# Fetches decimal numbers from simple web service and displays 
# them on 7 segment displays via shift registers. For each value,
# the parameter name is the <metric_id> concatenated with the display ID.
#
# Multiple displays can be connected as long as they report their ID and
# the number of digits they use. After each time the values are displayed 
# the config is read and checked whether it changed. Therefore, new displays
# can be added anytime or IDs can be changed.

import sevenseg
import readconfig

import json
import time
import os
import sys
import urllib2

def get_value(url):
  """ Fetches a single value from host. Returns None if value is undefined
      or not numeric. Throws urllib2.URLError on connection problems."""
  try:
    response = urllib2.urlopen(url)
    data = json.loads(response.read().decode('utf-8'))
    if "value" in data:
      return int(data["value"])
  except(ValueError):
    print("invalid value %s" %data["value"])

def get_values(url, config):
  """ Gets values for all defined displays contatenated into a single
      string that can be shifted through the displays. Unknown values 
      are indicated by 'u'. Returns None on connection problems. """
  text = ""
  for display in config:
    digits = display[0]
    id = display[1]
    # get the value from the cloud
    try:
      value = get_value(url.format(id))
      if value:
        text = "{0: {width}}".format(value, width=digits)[-3:] + text
      else:
        text = "_" * digits
    except(urllib2.URLError):
      return None
  return text

def init():
  """ Reads initial configuration and shows it on the displays. Call
      only on start-up."""
  # Reading config latches data, so fill it with something before
  sevenseg.output_str("-" * 100)
  config = readconfig.read_config()
  # Show number of digits for each display to confirm config is read
  sevenseg.start_shift()
  for c in config: 
    sevenseg.send_str(str(c[0]) * c[0])
  sevenseg.latch()
  time.sleep(3)
  # Show ID of each display
  sevenseg.start_shift()
  for c in config: 
    sevenseg.send_number(c[1], c[0])
  sevenseg.latch()
  time.sleep(3)
  return config

def main():
  args=sys.argv
  if len(args) < 3:
    print "usage %s url metric_id" % args[0]
    sys.exit()
 
  url = "http://%s/getvalue?id=%s{0}" % ( 
        os.getenv("metricsinyourfaceurl", args[1]), 
        args[2])
  sevenseg.setup()
  readconfig.setup()
  config = init()
  if not config:
    config = [(3, 0)]  # Default: 1 display, 3 digits, ID 0
  text = "uuu"

  while (True):
    t = get_values(url, config)
    if t:
      text = t
      sevenseg.output_str(text)
    else: 
      print("could not reach server")
      sevenseg.output_str(" " * 100) # TODO; compute total num digits
      time.sleep(.2)
      sevenseg.output_str(text)

    c = readconfig.read_config()
    if c and not c == config:
      config = c
      print "new config: %i digits, ID = %i" % (config[0][0], config[0][1])
    else:
      time.sleep(2)

  sevenseg.cleanup()

main()
