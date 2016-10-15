#! /usr/bin/python
#
# sudo python sevenseg_i2c.py <number> -- display number
# sudo python sevenseg_i2c.py <text>   -- display text(very limited)
# sudo python sevenseg_i2c.py          -- count to 200
#
# Outputs decimal numbers to AdaFruit LED Backback 7 Segment display
#
# i2c must be enabled on the raspberry pi. If you don't see /dev/i2c-1 this
# code can't work. 
#
# Requires Adafruit seven segment library:
# sudo pip install adafruit-led-backpack

import sevenseg

import sys
import time

from Adafruit_LED_Backpack import SevenSegment

class SevenSegDisplay:

  next_addr = 0x70  # next available i2c display address

  def __init__(self, num_digits=4, address=None):
    """ Sets up one physical display per 4 digits. 
        If no address is specified, auto-increments address from 0x70."""
    self.num_digits = num_digits
    if not address:
      address = SevenSegDisplay.next_addr
    self.seg = []
    for i in range(num_digits / 4):
      self.seg += [SevenSegment.SevenSegment(address = address)]
      address += 1
    SevenSegDisplay.next_addr = address
    self.start()

  def addrs(self):
    """ Returns the number of i2c addresses used by the display."""
    return self.num_digits / 4

  def setup(self):
    for seg in self.seg:
      try:
        seg.begin()
      except IOError:
         print("cannot connect to i2c device")

  def cleanup(self):
    return None

  def start(self):
    """ Prepares the display for setting data."""
    self.digit = 0

  def latch(self):
    """ Shows the set value on the display."""
    for seg in self.seg:
      try:
        seg.write_display()
      except IOError:
        pass

  def send_raw(self, segments):
    self.seg[(self.num_digits - self.digit - 1) / 4].set_digit_raw(self.digit % 4, segments)
    self.digit += 1

  def output(self, value):
    """ Outputs a string or a integer number onto 7-segment display.
        Value is shown after call to latch(). """
    raw = sevenseg.text(value, self.num_digits)
    self.start()
    for c in raw:
      self.send_raw(c)

  def blank(self):
    """ Blanks the display (all LED off). requires call to latch(). """
    raw = sevenseg.blanks(self.num_digits)
    self.start()
    for c in raw:
      self.send_raw(c)

def main():
  """ Simple test: drive one or more displays """
  args=sys.argv

  if len(args) < 2:
    # count on the first display
    display = SevenSegDisplay(address = 0x70)
    display.setup()
    for num in range(0,200):
      display.start()
      display.output(num)
      display.latch()
      time.sleep(0.1)
    display.cleanup()
  elif len(args[1]) > 4:
    # show large value across multipel displays
    display = SevenSegDisplay(num_digits = 8)
    display.setup()
    display.start()
    display.output(args[1])
    display.latch()
  else:
    # show values across multiple displays
    address = 0x70
    displays = []
    for value in args[1:]:
      display = SevenSegDisplay()
      display.setup()
      displays += [display]
      address += 1
    count = 1
    for d in displays: 
      d.start()
      d.output(args[count])
      count += 1
      d.latch()


if __name__ == "__main__":
  main()
