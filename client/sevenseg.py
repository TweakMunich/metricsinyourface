#! /usr/bin/python
#
# sudo python sevenseg.py <number> -- display number
# sudo python sevenseg.py <text>   -- display text(very limited)
# sudo python sevenseg.py          -- count to 200
#
# Outputs decimal numbers to 74HCT595 shift registers connected
# to 7-Segment display vis 2803 darlington (Hi = on).

import RPi.GPIO as GPIO
import time
import sys

# IO Port definitions (not pins!)
GPIO_SER  = 23 # serial data / MOSI (high bit first) - to 595 SER (14)
GPIO_CLK = 24  # Serial clock / CLK (rising edge) - to 595 SRCLK (11)
GPIO_RCLK = 18  # Register latch  / RESET (rising edge) - to 595 RCLK (12)

NUM_BITS = 8    # Number of bits per digit

# 7 Segment coding a=bit0, b=bit1, ..., DP=bit7
SEGMENTS = [0b00111111, 0b00000110, 0b01011011, 0b01001111, 0b01100110,
            0b01101101, 0b01111101, 0b00000111, 0b01111111, 0b01101111]
SPECIAL = { 'u': 0b00011100, 'c': 0b01011000 , '_': 0b00001000 }

def setup():
  GPIO.setmode(GPIO.BCM)

  GPIO.setup(GPIO_SER, GPIO.OUT)
  GPIO.setup(GPIO_CLK, GPIO.OUT)
  GPIO.setup(GPIO_RCLK, GPIO.OUT)

  GPIO.output(GPIO_SER, GPIO.LOW)
  GPIO.output(GPIO_CLK, GPIO.LOW)
  GPIO.output(GPIO_RCLK, GPIO.LOW)

def cleanup():
  GPIO.cleanup()

def rclk_low():
  GPIO.output(GPIO_RCLK, GPIO.LOW)

def latch():
  """ Latches data into outputs with high strobe (RCLK) """
  GPIO.output(GPIO_RCLK, GPIO.LOW)
  GPIO.output(GPIO_RCLK, GPIO.HIGH)
  GPIO.output(GPIO_RCLK, GPIO.LOW)

# The following methods shift sindgle bits, bytes or strings to the
# Shift registers. Call rclk_low() before and latch() after.

def shift_bit(bit):
  """ Shifts a single bit (true/false) to the serial buffer with
      rising edge of CLK signal. """
  GPIO.output(GPIO_SER, bit)
  GPIO.output(GPIO_CLK, GPIO.LOW)
  GPIO.output(GPIO_CLK, GPIO.HIGH)

def send_raw(segments):
  mask = 2**(NUM_BITS - 1)
  for i in range(NUM_BITS):
    shift_bit(int(segments) & int(mask) != 0)
    mask = mask >> 1

def send_digit(value):
  """ Outputs a single digit via serial shift out. High bit first. """
  send_raw(SEGMENTS[value])

def send_blank():
  """ Sets a single digit display to blank (all LED off). """
  for digit in range(NUM_BITS):
    shift_bit(False)

def send_char(value):
  if value in ['0','1','2','3','4','5','6','7','8','9']:
    send_digit(int(value))
  elif value == ' ':
    send_blank()
  elif value in SPECIAL:
    send_raw(SPECIAL[value])

def send_str(value):
  """ Outputs a string consisting of digits or blanks onto 7-segment display. """
  rclk_low()
  for c in value:
    send_char(c)
  latch()

def send_number(value, digits):
  """ Outputs an integer number onto 7-segment display. 
      Supresses leading zeros. If width is insufficient,
      displays last (least significant) digits."""
  text = "{0: {width}}".format(value, width=digits)[-3:]
  output_str(text)

def send_blanks(digits):
  """ Blanks the display (all LED off). """
  for digit in range(digits):
    send_blank()

# The following methods send data and latch it to the display. 
# Each call must specify all values for all displays.
# Mostly provided for convenience if only one display is connected.

def output_str(text):
  """ Outputs a string consisting of digits or blanks onto 7-segment display.
      Can be used for single display or multiple displays if the string 
      contains the correct number of characters for each display."""
  rclk_low()
  send_str(text)
  latch()

def output_number(value, digits):
  """ Outputs an integer value onto a 7-segment display of the specified width. 
      Supresses leading zeros. If width is insufficient, displays the last 
      (least significant) digits."""
  rclk_low()
  send_number(value,digits)
  latch()

def blank(digits):
  """ Blanks the display. """
  rclk_low()
  send_blank(digits)
  latch()

def main():
  setup()
  args=sys.argv
  digits = 3 # should be read from config

  if len(args) < 2:
    for num in range(0,200):
      output_number(num, digits)
      time.sleep(0.1)
  elif args[1].isdigit():	
    output_number(int(args[1]), digits)
  else:
    output_str(args[1])

  # resetting GPIO messes up display
  cleanup()

if __name__ == "__main__":
  main()
