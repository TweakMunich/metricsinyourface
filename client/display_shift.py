#! /usr/bin/python

# Manages a set of shift register displays,offering global operations and
# simultaneous update.

from sevenseg_shift import SevenSegDisplay

class Displays:

  def __init__(self, displays):
    """ Pass an array of display objects. """
    self.displays = displays
    self.data = [""] * len(displays)


  @staticmethod
  def make_displays(config):
    """ Generates one display for each config.
        Displays must must be chained on shift registers. """
    displays = []
    for d in config:
      disp = SevenSegDisplay(d[0])
      disp.setup()
      displays += [disp]
    return Displays(displays)

  def set(self, index, data):
    """ Sets the content for one display, either integer or string."""
    self.data[index] = data

  def display(self):
    """ Sends defined data to the displays. """
    count = 0
    self.displays[0].start() # call only once to support shift chain
    for d in self.displays:
      d.output(self.data[count])
      count += 1
    self.displays[0].latch() # call only once to support shift chain
   
  def blank(self, index=-1):
    """ Blanks all displays or only the specified one. Call display()
        to restore previous data to display. """
    self.displays[0].start() # call only once to support shift chain
    if index < 0:
      for d in self.displays:
        d.blank()
    else:
      self.displays[index].blank()
    self.displays[0].latch() # call only once to support shift chain

  def loads_config_data(self):
    """ Indicates whether displaying data already loads config data.
        True only for serial display and config input. """
    return True

