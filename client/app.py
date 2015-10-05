#! /usr/bin/python3

# Outputs decimal numbers to 74HCT595 shift registers connected
# to 74LS274 BCD-to-7-Segment decoders.

import RPi.GPIO as GPIO
import urllib.request
import json
import time


# IO Port definitions (not pins!)
GPIO_SER = 17 # serial data (high bit first) - to 595 SER (14)
GPIO_SCLK = 27  # Serial clock (rising edge) - to 595 SRCLK (11)
GPIO_RCLK = 22  # Register latch (rising edge) - to 595 RCLK (12)

NUM_DIGITS = 3  # Number of 7-segment displays
NUM_BITS = 4    # Bits in each digit

def setup():
  GPIO.setmode(GPIO.BCM)

  GPIO.setup(GPIO_SER, GPIO.OUT)
  GPIO.setup(GPIO_SCLK, GPIO.OUT)
  GPIO.setup(GPIO_RCLK, GPIO.OUT)

  GPIO.output(GPIO_SER, GPIO.LOW)
  GPIO.output(GPIO_SCLK, GPIO.LOW)
  GPIO.output(GPIO_RCLK, GPIO.LOW)

def output_digit(num):
  mask = 2**(NUM_BITS - 1)

  # shift BCD data into register high bit first
  for i in range(NUM_BITS):
    # set bit (SER input)
    GPIO.output(GPIO_SER, int(num) & int(mask) != 0)
    # shift with high strobe (SCLK)
    GPIO.output(GPIO_SCLK, GPIO.HIGH)
    GPIO.output(GPIO_SCLK, GPIO.LOW)
    mask = mask >> 1

def output(num):
  """ Outputs an integer number onto BCD display.
      Leading digits will be ignored if fewer than needed 7-segment 
      displays are in place as data simply shifts through.  """

  mask = 10 ** (NUM_DIGITS - 1)
  for digit in range(NUM_DIGITS):
    output_digit((num / mask) % 10)  
    mask = mask / 10
  # latch data into outputs with high strobe (RCLK)
  GPIO.output(GPIO_RCLK, GPIO.HIGH)
  GPIO.output(GPIO_RCLK, GPIO.LOW)

def main():
  setup()

  while (True):
    # getting the value from the cloud
    url = "http://metricsinyourfacecl-env.elasticbeanstalk.com/getValue?id=testpi"
    response = urllib.request.urlopen(url)
    data = json.loads(response.read().decode('utf-8'))
    #displaying the value
    output(int(data["value"]))
    time.sleep(2)

  # resetting GPIO messes up display
  GPIO.cleanup()

main()
