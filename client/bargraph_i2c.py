#! /usr/bin/python
#
# sudo python bargraph_i2c.py <number> -- display number
#
# Outputs decimal numbers to AdaFruit LED Backback 7 Segment display
#
# i2c must be enabled on the raspberry pi. If you don't see /dev/i2c-1 this
# code can't work. 
#
# Requires Adafruit seven segment library:
# sudo pip install adafruit-led-backpack

from Adafruit_LED_Backpack import BicolorBargraph24

import sys
import time

class BarGraph:

  def __init__(self, yellow=70, red=85, address=None):
    """ Sets up one physical display. yellow and red define percentage of value 
        where color changes. """
    self.bar = BicolorBargraph24.BicolorBargraph24(address = address)
    self.yellow = yellow
    self.red = red

  def setup(self):
    self.bar.begin()

  def cleanup(self):
    return None
 
  def calcbar(self, value):
    """ Converts from 0 to 100 range into bar index, i.e. 0 / 23 """
    return (value + 4) * 24 / 100

  def output(self, value):
    """ Outputs an integer between 0 and 99 to bar graph display."""
    self.bar.clear()
    for num in range(0, self.calcbar(value)):
      if num >= self.calcbar(self.red):
        color = BicolorBargraph24.RED
      elif num >= self.calcbar(self.yellow):
        color = BicolorBargraph24.YELLOW
      else:
        color = BicolorBargraph24.GREEN
      self.bar.set_bar(num, color)
    self.bar.write_display()

  def blank(self):
    self.bar.clear()
    for num in range (0,24):
      self.bar.set_bar(num, BicolorBargraph24.OFF)
    self.bar.write_display()

def main():
  """ Simple test: drive one or more displays """
  args=sys.argv

  if len(args) < 2:
    # count on the first display
    display = BarGraph(50, 75, address = 0x70)
    display.setup()
    display.blank()
    for num in range(0,101):
      display.output(num)
      time.sleep(0.05)
    display.cleanup()
  else:
    value = int(args[1])
    display = BarGraph(address = 0x70)
    display.setup()
    display.blank()
    display.output(value)

if __name__ == "__main__":
  main()
