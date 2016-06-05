#! /usr/bin/python
#
# Reads configuration input from shift registers. Multiple shift registers
# can be chained analog to the displays with 16 bits per display.
#
# For each display, a 16 bit shift register must report the config:
# bit 0-11  = display ID (0-4095), inverted (e.g. all bits high is ID 0)
# bit 12    = unused (use to switch common anode / cathode?)
# bit 13-15 = number digits - 1 (e.g. 0b011 = 4 digits)
#
# The serial input is pulled high, so the end of the shift chain is detected
# by the top 3 bits being 0b111, which is not allowed for the size bits

import RPi.GPIO as GPIO
import time
import os
import sys

# IO Port definitions (not pins!)
GPIO_MISO =  25  # serial data in / MISO (high bit first) - 
GPIO_SCLK = 24  # Serial clock  / CLK (rising edge) - 
GPIO_RCLK = 18  # Register latch  / RESET (rising edge) -

NUM_BITS = 8    # Bits in each digit

NUM_DIGITS = [2, 3, 4, 6]

def setup():
  """ sets up IO pins into proper mode. """
  GPIO.setmode(GPIO.BCM)

  GPIO.setup(GPIO_MISO, GPIO.IN, pull_up_down=GPIO.PUD_UP)
  GPIO.setup(GPIO_SCLK, GPIO.OUT)
  GPIO.setup(GPIO_RCLK, GPIO.OUT)

  GPIO.output(GPIO_SCLK, GPIO.LOW)
  GPIO.output(GPIO_RCLK, GPIO.LOW)

def load_data():
  """ Latches data into inputs with high strobe (SHIFT/LOAD) """
  GPIO.output(GPIO_RCLK, GPIO.LOW)
  GPIO.output(GPIO_SCLK, GPIO.LOW)
  GPIO.output(GPIO_SCLK, GPIO.HIGH)
  GPIO.output(GPIO_RCLK, GPIO.HIGH)

def read_byte():
  """ Reads a single byte serially, MSB first. """
  GPIO.output(GPIO_RCLK, GPIO.HIGH)  # shift mode
  value = 0
  mask = 2**(NUM_BITS - 1)
  for i in range(NUM_BITS):
    if GPIO.input(GPIO_MISO):
      value = value | mask
    GPIO.output(GPIO_SCLK, GPIO.LOW)
    GPIO.output(GPIO_SCLK, GPIO.HIGH)
    mask = mask >> 1
  return value

def read_config():
  """ returns a list of tupels indicating (num digits, ID) for each
      connected display. Configs are detected by at least one of the
      highest 3 bits (number of digits) being set to 0."""
  result = []
  while(True):
    hi = read_byte()
    lo = read_byte()
    # print "hi %i lo %i" % (hi, lo)
    digits = ((hi & 0xE0) >> 5) + 1
    id = ((hi & 0x0f) << 8 | lo) ^ 0xFFF
    if digits == 8:
      return result
    result += [(digits, id)]

def main():
  setup()
  load_data()
  config = read_config()
  print config

  #lo = read_byte()
  #hi = read_byte()
  #print "%x" % (lo ^ 0xff) 
  #print "%x" % (hi ^ 0xff) 
  # cleanup()

if __name__ == "__main__":
  main()
