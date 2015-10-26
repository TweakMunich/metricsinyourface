#! /usr/bin/python
#
# sudo python bcd.py <number>  -- display number
# sudo python bcd.py           -- count to 200
#
# Outputs decimal numbers to 74HCT595 shift registers connected
# to 74LS274 BCD-to-7-Segment decoders.

import RPi.GPIO as GPIO
import time
import os
import sys

# IO Port definitions (not pins!)
GPIO_SER = 17 # serial data (high bit first) - to 595 SER (14)
GPIO_SCLK = 27  # Serial clock (rising edge) - to 595 SRCLK (11)
GPIO_RCLK = 22  # Register latch (rising edge) - to 595 RCLK (12)

NUM_DIGITS = 3  # Number of 7-segment displays
NUM_BITS = 4    # Bits in each digit
BCD_BLANK = 15  # 74247 decodes 15 to blank

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

  mask = 2**(NUM_BITS - 1)
  for i in range(NUM_BITS):
    shift_bit(int(num) & int(mask) != 0)
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
  for digit in range(NUM_DIGITS):
    output_digit(BCD_BLANK)
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
