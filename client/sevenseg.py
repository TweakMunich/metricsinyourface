#! /usr/bin/python
#
# sudo python sevenseg.py <number>  -- display number
# sudo python sevenseg.py           -- count to 200
#
# Outputs decimal numbers to 74HCT595 shift registers connected
# to 7-Segment display vis 2803 darlington (Hi = on).

import RPi.GPIO as GPIO
import time
import os
import sys

# IO Port definitions (not pins!)
GPIO_SER = 23 # serial data (high bit first) - to 595 SER (14)
GPIO_SCLK = 24  # Serial clock (rising edge) - to 595 SRCLK (11)
GPIO_RCLK = 25  # Register latch (rising edge) - to 595 RCLK (12)

NUM_DIGITS = 3  # Number of 7-segment displays
NUM_BITS = 8    # Number of bits per digit

# 7 Segment coding a=bit0, b=bit1, ..., DP=bit7
SEGMENTS = [0b00111111, 0b00000110, 0b01011011, 0b01001111, 0b01100110,
            0b01101101, 0b01111101, 0b00000111, 0b01111111, 0b01101111]

def setup():
  GPIO.setmode(GPIO.BCM)

  GPIO.setup(GPIO_SER, GPIO.OUT)
  GPIO.setup(GPIO_SCLK, GPIO.OUT)
  GPIO.setup(GPIO_RCLK, GPIO.OUT)

  GPIO.output(GPIO_SER, GPIO.LOW)
  GPIO.output(GPIO_SCLK, GPIO.LOW)
  GPIO.output(GPIO_RCLK, GPIO.LOW)

def cleanup():
  GPIO.cleanup()

def latch():
  """ Latches data into outputs with high strobe (RCLK) """
  GPIO.output(GPIO_RCLK, GPIO.HIGH)
  GPIO.output(GPIO_RCLK, GPIO.LOW)

def shift_bit(bit):
  """ Shifts a single bit (true/false) to the serial buffer. """

  GPIO.output(GPIO_SER, bit)
  # shift with high strobe (SCLK)
  GPIO.output(GPIO_SCLK, GPIO.HIGH)
  GPIO.output(GPIO_SCLK, GPIO.LOW)

def output_digit(num):
  """ Outputs a single digit via serial shift out. High bit first. """

  seg = SEGMENTS[num]
  mask = 2**(NUM_BITS - 1)
  for i in range(NUM_BITS):
    shift_bit(int(seg) & int(mask) != 0)
    mask = mask >> 1

def output(num):
  """ Outputs an integer number onto BCD display.
      Leading digits will be ignored if fewer than needed 7-segment 
      displays are in place as data simply shifts through.  """

  mask = 10 ** (NUM_DIGITS - 1)
  for digit in range(NUM_DIGITS):
    output_digit((num / mask) % 10)  
    mask = mask / 10
  latch()

def blank():
  for digit in range(NUM_DIGITS * NUM_BITS):
    shift_bit(False)
  latch() 

def main():
  setup()
  args=sys.argv
  if len(args) < 2:
    for num in range(0,200):
      output(num)
      time.sleep(0.1)
  else:	
    output(int(args[1]))

  # resetting GPIO messes up display
  cleanup()

if __name__ == "__main__":
  main()
