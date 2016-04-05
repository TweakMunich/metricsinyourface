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
# Link from your current directory to the following driver files cloned from
# https://github.com/adafruit/Adafruit-Raspberry-Pi-Python-Code:
#   Adafruit_I2C.py
#   Adafruit_7Segment.py
#   Adafruit_LEDBackpack.py

import sevenseg

import sys
import time
import threading

from Adafruit_7Segment import SevenSegment

class SevenSegDisplay:

  def __init__(self, num_digits=4, address=0x70):
    self.num_digits = num_digits
    self.digit = 0
    self.seg = SevenSegment(address)
    self.lock = threading.Lock()
    self.scroller = threading.Thread(target=self.scroll)
    self.scroller.setDaemon(True)
    self.disp_data = [0, 0, 0, 0]
    self.scroller.start()

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
    self.lock.acquire()
    self.data = raw
    self.lock.release()

  def blank(self):
    """ Blanks the display (all LED off). """
    self.lock.acquire()
    self.data = [0, 0, 0, 0]
    self.lock.release()

  def scroll(self):
    """ Thread callback to scroll large strings. """
    old_data = self.data
    offset = 0
    for i in range(self.num_digits):
      self.send_raw(self.data[i])
    print("Entering loop")
    time0 = time.time()
    while (True):
      if (len(old_data) <= self.num_digits):
        self.lock.acquire()
        old_data = self.data
        self.lock.release()
        offset = 0
        self.start()
        for i in range(self.num_digits):
          self.send_raw(old_data[i])
      else:
        if (offset == len(old_data) + self.num_digits - 2):
          self.lock.acquire()
          old_data = self.data
          self.lock.release()
          offset = 0
        self.start()
        for i in range(self.num_digits):
          dd = old_data + [0] + old_data
          self.send_raw(dd[i + offset])
        offset += 1
      time1 = time.time()
      dt = time1 - time0
      time0 += 0.4
      if (dt < 0):
        dt = 0
      elif (dt > 0.4):
        dt = 0.4
      time.sleep(0.4 - dt)

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
