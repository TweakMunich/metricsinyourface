#! /usr/bin/python
#
# sudo python sevenseg_i2c.py <number> -- display number
# sudo python sevenseg_i2c.py <text>   -- display text(very limited)
# sudo python sevenseg_i2c.py          -- count to 200
#
# Outputs decimal numbers to AdaFruit LED Backback 7 Segment display

import sevenseg

import sys
import time

from Adafruit_7Segment import SevenSegment

class SevenSegDisplay:

  def __init__(self, num_digits=4, address=0x70):
    self.num_digits = num_digits
    self.digit = 0
    self.seg = SevenSegment(address)

  def setup(self):
    return None

  def cleanup(self):
    return None

  def start(self):
    self.digit = 0

  def latch(self):
    return None

  def send_raw(self, segments):
    self.seg.writeDigitRaw(self.digit, segments)
    self.digit += 1
    # digits 2 is the colon, skip 
    if self.digit == 2:
      self.digit += 1

  def output(self, value):
    """ Outputs a string or a integer number onto 7-segment display."""
    raw = sevenseg.text(value, self.num_digits)
    self.start()
    for c in raw:
      self.send_raw(c)

  def blank(self):
    """ Blanks the display (all LED off). """
    raw = sevenseg.blanks(self.num_digits)
    self.start()
    for c in raw:
      self.send_raw(c)

def main():
  """ Simple test: drive one or more displays """
  args=sys.argv

  if len(args) < 2:
    # count on the first display
    display = SevenSegDisplay()
    display.setup()
    for num in range(0,200):
      display.start()
      display.output(num)
      display.latch()
      time.sleep(0.1)
    display.cleanup()
  else:
    # show values across multipel displays
    address = 0x70
    displays = []
    for value in args[1:]:
      displays += [SevenSegDisplay(address = address)]
      address += 1
    count = 1
    displays[0].start()
    for d in displays: 
      d.output(args[count])
      count += 1
    displays[0].latch()


if __name__ == "__main__":
  main()
