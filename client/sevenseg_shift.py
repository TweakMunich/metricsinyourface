#! /usr/bin/python
#
# sudo python sevenseg.py <number> -- display number
# sudo python sevenseg.py <text>   -- display text(very limited)
# sudo python sevenseg.py          -- count to 200
#
# Outputs decimal numbers to 74HCT595 shift registers connected
# to 7-Segment display vis 2803 darlington (Hi = on).

import sevenseg

import sys
import time

import RPi.GPIO as GPIO

# IO Port definitions (not pins!)
GPIO_SER  = 23 # serial data / MOSI (high bit first) - to 595 SER (14)
GPIO_CLK = 24  # Serial clock / CLK (rising edge) - to 595 SRCLK (11)
GPIO_RCLK = 18  # Register latch  / RESET (rising edge) - to 595 RCLK (12)

class SevenSegDisplay:

  NUM_BITS = 8    # Number of bits per digit

  def __init__(self, num_digits, 
               gpio_ser=GPIO_SER, gpio_clk=GPIO_CLK, gpio_rclk=GPIO_RCLK):
    self.num_digits = num_digits
    self.gpio_ser = gpio_ser
    self.gpio_clk = gpio_clk
    self.gpio_rclk = gpio_rclk

  def setup(self):
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(self.gpio_ser, GPIO.OUT)
    GPIO.setup(self.gpio_clk, GPIO.OUT)
    GPIO.setup(self.gpio_rclk, GPIO.OUT)

    GPIO.output(self.gpio_ser, GPIO.LOW)
    GPIO.output(self.gpio_clk, GPIO.LOW)
    GPIO.output(self.gpio_rclk, GPIO.LOW)

  def cleanup(self):
    GPIO.cleanup()

  def start(self):
    GPIO.output(self.gpio_rclk, GPIO.LOW)

  def latch(self):
    """ Latches data into outputs with high strobe (RCLK) """
    GPIO.output(self.gpio_rclk, GPIO.LOW)
    GPIO.output(self.gpio_rclk, GPIO.HIGH)
    GPIO.output(self.gpio_rclk, GPIO.LOW)

  # The following methods shift sindgle bits, bytes or strings to the
  # Shift registers. Call start_shift() before and latch() after.

  def shift_bit(self, bit):
    """ Shifts a single bit (true/false) to the serial buffer with
        rising edge of CLK signal. """
    GPIO.output(self.gpio_ser, bit)
    GPIO.output(self.gpio_clk, GPIO.LOW)
    GPIO.output(self.gpio_clk, GPIO.HIGH)

  def send_raw(self, segments):
    mask = 2**(self.NUM_BITS - 1)
    for i in range(self.NUM_BITS):
      self.shift_bit(int(segments) & int(mask) != 0)
      mask = mask >> 1

  def output(self, value):
    """ Outputs a string consisting of digits or blanks onto 7-segment display.
        Can be used for single display or multiple displays if the string 
        contains the correct number of characters for each display."""
    raw = sevenseg.text(value, self.num_digits)
    for c in raw:
      self.send_raw(c)

  def blank(self):
    """ Blanks the display (all LED off). """
    raw = sevenseg.blanks(self.num_digits)
    for c in raw:
       self.send_raw(c)

def main():
  args=sys.argv

  display = SevenSegDisplay(3) # hard coded to 3 digits for testing
  display.setup()

  if len(args) < 2:
    for num in range(0,200):
      display.start()
      display.output(num)
      display.latch()
      time.sleep(0.1)
  else:
    display.start()
    display.output(args[1])
    display.latch()

  # resetting GPIO messes up display
  display.cleanup()

if __name__ == "__main__":
  main()
