#! /usr/bin/python

# Manages a set of displays, accommodating scenarios like multiple
# displays connected on a single shift register chain. Hardware control
# (i2c, shift regs) is handled inside the passed-in display objects.

class Displays:

  def __init__(self, displays):
    """ Pass an array of display objects. """
    self.displays = displays
    self.data = [""] * len(displays)

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

