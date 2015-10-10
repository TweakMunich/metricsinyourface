#! /usr/bin/python
#
# Reads configuration input from shift register.

import RPi.GPIO as GPIO
import time
import os
import sys

# IO Port definitions (not pins!)
GPIO_SER = 18 # serial data in (high bit first) - 
GPIO_SCLK = 24  # Serial clock (rising edge) - 
GPIO_RCLK = 25  # Register latch (rising edge) -

NUM_BITS = 8    # Bits in each digit

def setup():
  GPIO.setmode(GPIO.BCM)

  GPIO.setup(GPIO_SER, GPIO.IN)
  GPIO.setup(GPIO_SCLK, GPIO.OUT)
  GPIO.setup(GPIO_RCLK, GPIO.OUT)

  GPIO.output(GPIO_SCLK, GPIO.LOW)
  GPIO.output(GPIO_RCLK, GPIO.LOW)

def cleanup():
  GPIO.cleanup()

def load_data():
  """ Latches data into inputs with high strobe (SHIFT/LOAD) """
  GPIO.output(GPIO_RCLK, GPIO.LOW)
  GPIO.output(GPIO_SCLK, GPIO.LOW)
  GPIO.output(GPIO_SCLK, GPIO.HIGH)
  GPIO.output(GPIO_RCLK, GPIO.HIGH)

def readbyte():
  """ . """
  value = 0
  mask = 2**(NUM_BITS - 1)
  for i in range(NUM_BITS):
    if GPIO.input(GPIO_SER):
      value = value | mask
    GPIO.output(GPIO_SCLK, GPIO.LOW)
    GPIO.output(GPIO_SCLK, GPIO.HIGH)
    mask = mask >> 1
  return value

def main():
  setup()
  load_data()
  value1 = readbyte()
  value2 = readbyte()
  print "%x" % (value1 ^ 0xff) 
  print "%x" % (value2 ^ 0xff) 
  cleanup()

if __name__ == "__main__":
  main()
