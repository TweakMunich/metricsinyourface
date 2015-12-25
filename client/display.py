#! /usr/bin/python

# Manages a set of displays, accommodating scenarios like multiple
# displays connected on a single shift register chain. Hardware control
# is handled inside the display objects.

import time
 
class Displays:

  def __init__(self, displays):
    """ pass an array defining the width for each display """
    self.displays = displays
    self.data = [""] * len(displays)

  def set(self, index, data):
    self.data[index] = data

  def display(self):
    count = 0
    self.displays[0].start()
    for d in self.displays:
      d.output(self.data[count])
      count += 1
    self.displays[0].latch()
   
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

