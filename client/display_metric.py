#! /usr/bin/python
#
# sudo python display_metric.py domain_name.com metric_id
#
# Fetches decimal numbers from simple webs service and displays 
# them on 7 segment diaplsys. Uses 74HCT595 shift registers connected
# to 74LS274 BCD-to-7-Segment decoders.

import bcd

import json
import time
import os
import sys
import urllib2

def main():

  args=sys.argv
  if len(args) < 3:
    print "usage %s url metric_id" % args[0]
    sys.exit()
 
  url = "http://" + os.getenv("metricsinyourfaceurl", args[1]) + "/getvalue?id=" + args[2]
  bcd.setup()

  while (True):
    # getting the value from the cloud
    response = urllib2.urlopen(url)
    data = json.loads(response.read().decode('utf-8'))
    # displaying the value
    bcd.output(int(data["value"]))
    time.sleep(2)

  # resetting GPIO messes up display
  bcd.cleanup()

main()
