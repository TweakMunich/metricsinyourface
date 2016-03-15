#! /usr/bin/python

# Simple program that retrieves the number of likes ona s epcific Facebook
# page (Az france in this example) and posts it to the metrics display 

import json
import sys
import urllib
import urllib2

def getLikes(page):
  query = "https://graph.facebook.com/fql?q=SELECT+like_count+FROM+link_stat+WHERE+url%3D%27{0}%27"
  url = query.format(urllib.quote_plus(page))
  response = urllib2.urlopen(url)
  data = json.loads(response.read().decode('utf-8'))

  if "data" in data:
    return int(data["data"][0]["like_count"])

def postData(host, id, value):
  """ Posts data into the shared data repository to be displayed by the Pi. """

  url = host + "/setValue"
  data = urllib.urlencode({"id": id, "value":value})
  response = urllib2.urlopen(url, data)
  if response.getcode() != 200:
    print "Error posting data %i %s" % (response.getcode(), response.read())

def main():
  args = sys.argv
  if len(args) < 2:
    print "usage %s facebook_page [host]" % args[0]
    sys.exit()

  page = args[1]
  if len(args) > 2:
    host = args[2]
  else:
    host = None

  likes = getLikes(page)
  if likes:
    value = "%.1f" % (likes / 1000.0)
    print value
    if host:
      postData(host, "testpi7", value)

if __name__ == "__main__":
  main()
