#! /usr/bin/python
#
# python stepper.py <pos> [<pos>...] - set stepper to relative postions 0-100
# python stepper.py  - do some movements as test
#
# Drives a small stepper as a display gauge

import RPi.GPIO as GPIO

import sys
import time

# IO port definitions (not pin numbers!)
GPIO_AIN1 = 17  # coil A pin 1
GPIO_AIN2 = 18  # coil A pin 2

GPIO_BIN1 = 22  # coil B pin 1
GPIO_BIN2 = 23  # coil B pin 2

step2coils = [ 	[1,0,1,0],
		[0,1,1,0],
		[0,1,0,1],
		[1,0,0,1] ]

class Gauge:
  """ Sets up a stepper motor to act as gauge.
      total_steps = number of steps the mototr can do
      total_angle = the angle in degrees the steps cover
      used_angle = specify if a smaller angle range is useful (e.g. 270),
                   the gauge will then centeron the smaller range.
      delay = pause between steps in seconds """
  def __init__(self, total_steps = 630, total_angle=310, 
               used_angle=310, delay = 0.0012):

    self.total_steps = total_steps
    self.total_angle = total_angle
    self.used_angle = used_angle
    self.delay = delay
    self.current_step = 0

  def setup(self):
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    GPIO.setup(GPIO_AIN1, GPIO.OUT)
    GPIO.setup(GPIO_AIN2, GPIO.OUT)
    GPIO.setup(GPIO_BIN1, GPIO.OUT)
    GPIO.setup(GPIO_BIN2, GPIO.OUT)

  def setCoils(self, w1, w2, w3, w4):
    GPIO.output(GPIO_AIN1, w1)
    GPIO.output(GPIO_AIN2, w2)
    GPIO.output(GPIO_BIN1, w3)
    GPIO.output(GPIO_BIN2, w4)

  def step(self, fwd = True):
    """ Make one step in the specified direction. """
    if fwd:
      if self.current_step < self.total_steps:
        self.current_step += 1
    else:
      if self.current_step > 0:
        self.current_step -= 1 
    coils = step2coils[self.current_step % len(step2coils)]
    self.setCoils(coils[0],coils[1],coils[2],coils[3])
    time.sleep(self.delay)

  def poweroff(self):
    """ Leaves the motor without power. """
    self.setCoils(1,1,1,1)
  
  def reset(self):
    """ Moves the stepper all the way back to reset to 0 position. """
    self.current_step = self.total_steps
    #for i in range(0,self.total_steps):
      #self.step(True)
    #time.sleep(0.3)
    for i in range(0, self.total_steps):
      self.step(False)

  def output(self, value):
    """ Sets gauge to relative value between 0 and 100. """
    if value < 0:
      value = 0
    if value > 100:
      value = 100
    # reduce to used angle
    factor = float(self.used_angle) / self.total_angle
    value = value * factor + (1 - factor) * 100 / 2.0 
    # convert to step number
    target_step = int(value / 100.0 * self.total_steps)
    print self.current_step, target_step
    for i in range(abs(target_step - self.current_step)):
      self.step(target_step > self.current_step)

def main():
  args = sys.argv

  #gauge = Gauge()
  gauge = Gauge(used_angle = 270) # easy to draw
  gauge.setup()
  gauge.reset()
  time.sleep(0.5)
  
  if len(args) < 2:
    for i in range (21): 
      gauge.output((i % 7) * 100.0 / 6)
      time.sleep(0.3)
  else:
    for a in args[1:]:
      gauge.output(float(a))
      time.sleep(0.3)

#  for i in range(0,10):
#    gauge.step()
#    time.sleep(0.3)
#  time.sleep(0.5)
#
#  for i in range(0,10):
#    gauge.step(False)
#    time.sleep(0.3)

  gauge.poweroff()

if __name__ == "__main__":
  main()
