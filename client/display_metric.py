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
#
# The code can work with 2 different display types, shift register or i2c.
# You can combine shift registers for configuration with i2c displays.
# - import sevenseg_i2c or sevenseg_shift
# - change the calls to make_displays_xxx accordingly
# - if not using shift register for config, import readconfig_fake instead
# - If using shift register displays, comment out the call to load_data in the loop

#from sevenseg_i2c import SevenSegDisplay
from sevenseg_shift import SevenSegDisplay

#import readconfig_fake as readconfig
import readconfig as readconfig

from display import Displays

import json
import os
import socket
import sys
import time
import urllib2

def get_value(url, hostname):
  """ Fetches a single string value from host. 
       Returns None if value is undefined.
       Throws urllib2.URLError on connection problems."""
  try:
    req = urllib2.Request(url) 
    req.add_header("REMOTE_HOST", hostname)
    response = urllib2.urlopen(req, timeout=5)
    data = json.loads(response.read().decode('utf-8'))
    if "value" in data:
      return data["value"]
  except (urllib2.HTTPError, urllib2.URLError) as e:
    raise
  except socket.timeout:
    # undocumented exception thrown by urlopen
    print "socket.timeout"
    return None
  except ValueError:
    return None

def get_values(url, hostname, config):
  """ Gets values for all defined displays as a list. Unknown values 
      are indicated by 'u'. Returns None on connection problems. """
  data = []
  for display in config:
    digits = display[0]
    id = display[1]
    try:
      # get the value from the cloud
      value = get_value(url.format(id), hostname)
      if value or value == 0:
        text = str(value)
      else:
        text = "_" * digits
      data += [text]
    except urllib2.HTTPError as e:
      data += ["_" * digits]
    except urllib2.URLError as e:
      # if there is a connection problem, don't try again
      print "Connection error: " + str(e.reason)
      return None
  return data

def display_config(disp, config):
  """ Shows config info on the displays during start-up. """

  # Show number of digits for each display to confirm config is read
  index = 0
  for c in config: 
    disp.set(index, (str(c[0]) + '.') * c[0])
    index += 1
  disp.display()
  time.sleep(2)

  # Show ID of each display
  index = 0
  for c in config: 
    disp.set(index, str(c[1]).rjust(c[0], '.')[-c[0]:] + '.')
    index += 1
  disp.display()
  time.sleep(2)
  return config

def make_displays(config):
  """ Generates one display for each listed in config. 
      i2c displays must have i2c addresses in ascending order. """
  displays = []
  for d in config:
    disp = SevenSegDisplay(d[0])
    disp.setup()
    displays += [disp]
  return Displays(displays)

def main():
  args=sys.argv
  if len(args) < 3:
    print "usage %s url metric_id" % args[0]
    sys.exit()
 
  url = "http://%s/getValue?id=%s{0}" % ( 
        os.getenv("metricsinyourfaceurl", args[1]), 
        args[2])
#  url = "http://%s/%s/{0}" % ( 
#        os.getenv("metricsinyourfaceurl", args[1]), 
#        args[2])

  hostname = socket.gethostname()

  # Note: if config circuit is not present, import readconfig_fake instead
  readconfig.setup()
  readconfig.load_data()
  config = readconfig.read_config()
  print config

  disp = make_displays(config)
  display_config(disp, config)

  # Blink last decimal point to indicate data is fresh
  blink = False

  while (True):
    data = get_values(url, hostname, config)
    if data:
      for i in range(len(data)):
        disp.set(i, data[i] + ('.' * blink))
      disp.display()
      blink = not blink
    else: 
      # Blink if cannot connect
      print("could not reach server")
      disp.blank()
      time.sleep(.2)
      disp.display()

    # check whether configuration changed (new display, different ID) 
    # readconfig.load_data() # remove with shift register displays, display clock loads
    c = readconfig.read_config()
    if c and not c == config:
      config = c
      disp = make_displays(c)
      print "new config: %i digits, ID = %i" % (config[0][0], config[0][1])
    else:
      time.sleep(2)

  sevenseg.cleanup()

main()
