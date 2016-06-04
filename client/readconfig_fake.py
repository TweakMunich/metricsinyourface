#! /usr/bin/python
#
# Returns a fake config consisting of 2 4 digits displays
# pegged to ID 5 and 6. Import this instead of readconfig.py for testing.

def setup():
  return None

def load_data():
  return None

def read_config():
  """ returns a list of tupels indicating (num digits, ID) for each
      connected display. Hard coded to 4-digit displays pegged to 
      ID 5 and 6. Useful when using i2c displays without any serial."""
  return [(4, 8)]

