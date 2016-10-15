#! /usr/bin/python

# Manages a set of i2c displays, offering global operations and 
# simultaneous update,

from sevenseg_i2c import SevenSegDisplay
from bargraph_i2c import BarGraphDisplay

import time

class Displays:

  @staticmethod
  def make_displays(config):
    """ Generates one display for each config.
        i2c displays must have i2c addresses in ascending order. """
    address = 0x70
    displays = []
    for d in config:
      if d[0] == 0:  ## FIXME (0 length means bargraph)
        disp = BarGraphDisplay(address=address)
      else:
        disp = SevenSegDisplay(d[0], address=address)
      disp.setup()
      displays += [disp]
      address = address + disp.addrs()
    return Displays(displays)

  def __init__(self, displays):
    """ Pass an array of display objects. """
    self.displays = displays
    self.data = [""] * len(displays)

  def set(self, index, data):
    """ Sets the data the nth display (integer or string)."""
    self.data[index] = data

  def display(self):
    """ Shows set data on the displays. """
    count = 0
    for d in self.displays:
      d.start() 
      d.output(self.data[count])
      count += 1
    for d in self.displays:
      d.latch()
   
  def blank(self, index=-1):
    """ Blanks all displays or only the specified one. Call display()
        to restore previous data to display. """
    if index < 0:
      for d in self.displays:
        d.start() 
        d.blank()
      for d in self.displays:
        d.latch()
    else:
      self.displays[index].blank()
      self.displays[index].latch()

  def loads_config_data(self):
    """ Indicates whether displaying data already loads config data.
        True only for serial display and config input. """
    return False


def main():
  displays = Displays.make_displays([(4, 10 ), (0, 10)])
  displays.set(0, 56.78)
  displays.set(1, 56.78)
  displays.display()
  time.sleep(0.5)
  displays.set(0, "56.78.")
  displays.set(1, "56.78.")
  displays.display()
  time.sleep(0.5)
  displays.blank()
  time.sleep(0.5)
  displays.display()

if __name__ == "__main__":
  main()


