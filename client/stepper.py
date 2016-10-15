#! /usr/bin/python

import RPi.GPIO as GPIO
import time

# Variables

delay = 0.0012
steps = 200

GPIO_AIN1 = 17  # coil A pin 1
GPIO_AIN2 = 18  # coil A pin 2

GPIO_BIN1 = 22  # coil B pin 1
GPIO_BIN2 = 23  # coil B pin 2

step2coils = [ 	[1,0,1,0],
		[0,1,1,0],
		[0,1,0,1],
		[1,0,0,1] ]

def setup():
  GPIO.setmode(GPIO.BCM)
  GPIO.setwarnings(False)

  GPIO.setup(GPIO_AIN1, GPIO.OUT)
  GPIO.setup(GPIO_AIN2, GPIO.OUT)
  GPIO.setup(GPIO_BIN1, GPIO.OUT)
  GPIO.setup(GPIO_BIN2, GPIO.OUT)

def setCoils(w1, w2, w3, w4):
  GPIO.output(GPIO_AIN1, w1)
  GPIO.output(GPIO_AIN2, w2)
  GPIO.output(GPIO_BIN1, w3)
  GPIO.output(GPIO_BIN2, w4)

def single_step():
  """ loop through step sequence based on number of steps """
  for coils in step2coils:
    setCoils(coils[0],coils[1],coils[2],coils[3])
    time.sleep(delay)

def single_step_back():
  for i in range(len(step2coils)-1, -1, -1):
    coils = step2coils[i]
    setCoils(coils[0],coils[1],coils[2],coils[3])
    time.sleep(delay)

def open():
  """ Leaves the motor without power. """
  setCoils(1,1,1,1)

def main():
  setup()
  for i in range(0,150):
    single_step()
  time.sleep(0.5)

  for i in range(0,150):
    single_step_back()
  time.sleep(0.5)

  for i in range(0,10):
    single_step()
    time.sleep(0.3)
  time.sleep(0.5)

  for i in range(0,10):
    single_step_back()
    time.sleep(0.3)

  open()

if __name__ == "__main__":
  main()
