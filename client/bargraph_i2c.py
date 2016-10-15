#! /usr/bin/python
#
# sudo python bargraph_i2c.py  -- bar graph test
# sudo python bargraph_i2c.py <number> -- display number between 0 and 100 on bar graph
#
# Outputs decimal numbers to AdaFruit LED Backback bicolor bar graph display
#
# i2c must be enabled on the raspberry pi. If you don't see /dev/i2c-1 this
# code can't work. 
#
# Requires Adafruit seven segment library:
# sudo pip install adafruit-led-backpack

from Adafruit_LED_Backpack import BicolorBargraph24

import sys
import time

class BarGraphDisplay:

  def __init__(self, yellow=50, red=75, address=None):
    """ Sets up one physical display. yellow and red define percentage of value 
        where color changes. """
    self.bar = BicolorBargraph24.BicolorBargraph24(address = address)
    self.yellow = yellow
    self.red = red
    self.address = address

  def addrs(self):
    """ Returns the number of i2c addresses used by the display."""
    return 1

  def setup(self):
    try:
      self.bar.begin()
    except IOError:
      print("cannot connect to i2c device %s" % hex(self.address))

  def cleanup(self):
    return None
 
  def start(self):
    """ Prepares the display for setting data."""
    try:
      self.bar.clear()
    except IOError:
      pass
 
  def latch(self):
    """ Shows the set value on the display."""
    try:
      self.bar.write_display()
    except IOError:
      pass
 
  def calcbar(self, value):
    """ Converts from 0 to 100 range into bar index, i.e. 0 - 23 """
    return (value + 4) * 24 / 100

  def output(self, value):
    """ Outputs an integer between 0 and 99 to bar graph display.
        Value is shown after call to latch(). """
    try:
      value = int(float(str(value).strip('.')))
    except ValueError:
      value = 0

    if value < 0:
      value = 0
    if value > 99:
      value = 99
    
    self.start()
    for num in range(0, self.calcbar(value)):
      if num >= self.calcbar(self.red):
        color = BicolorBargraph24.RED
      elif num >= self.calcbar(self.yellow):
        color = BicolorBargraph24.YELLOW
      else:
        color = BicolorBargraph24.GREEN
      self.bar.set_bar(num, color)

  def blank(self):
    """ Blanks display. Requires call to latch(). """
    self.bar.clear()
    for num in range (0,24):
      self.bar.set_bar(num, BicolorBargraph24.OFF)

def main():
  """ Simple test: drive one display """
  args=sys.argv

  if len(args) < 2:
    # count on the display
    display = BarGraphDisplay(50, 75, address = 0x71)
    display.setup()
    for num in range(0,101):
      display.start()
      display.output(num)
      display.latch()
      time.sleep(0.05)
    display.cleanup()
  else:
    # displayu the number from command line
    value = int(args[1])
    display = BarGraphDisplay(address = 0x71)
    display.setup()
    display.start()
    display.output(value)
    display.latch()

if __name__ == "__main__":
  main()
