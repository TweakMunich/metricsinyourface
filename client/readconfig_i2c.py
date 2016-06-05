#! /usr/bin/python
#
# sudo python readconfig.py -- display input
#
# Reads diaply configuration information from an MCP23017 I2C port expander.
# The I2C devices are assumed to use address 0x20 - 0x27 in ascending order
#
# Bits are allocated as follows (bit 0-7 =A0-A7, 8-15=B0-B7);
# bit 0-11  = display ID (0-4095), inverted (e.g. all bits high is ID 0)
# bit 12    = unused (use to switch common anode / cathode?)
# bit 13-15 = number digits - 1 (e.g. 0b011 = 4 digits)
#
# Requires Adafruit GPIO library:
# sudo pip install adafruit_gpio

import Adafruit_GPIO as GPIO
from Adafruit_GPIO import MCP230xx

def setup():
 return None

def bits_to_int(bits, invert=False):
  """ Converts a list of bits to an integer number assuming lowest bit first."""
  result = 0
  n = 0
  for bit in bits:
    result = result + ((bit ^ invert) << n)
    n += 1
  return result

def setup_mcp(mcp):
  """ Configures all bins as input with pullup."""
  for pin in range(16):
    mcp.setup(pin, GPIO.IN)
    mcp.pullup(pin, 1)

def read_config_mcp(mcp):
  """ Reads config data tuple (digits, channel) from the MCP chip."""
  bits = mcp.input_pins(range(12))
  channel = bits_to_int(bits, True)
  bits = mcp.input_pins(range(13,16))
  digits = bits_to_int(bits) + 1
  return (digits, channel)

def read_config():
  result = []
  for address in range(0x20, 0x28):
    try:
      mcp = MCP230xx.MCP23017(address)
    except IOError:
      return result
    setup_mcp(mcp)
    result += [read_config_mcp(mcp)]
  return result

def main():
  print read_config()
  raw_input("Press Enter to continue...")
  mcp = MCP230xx.MCP23017(0x20)
  setup_mcp(mcp)
  while True:
    config = read_config_mcp(mcp)
    print config[0], config[1]

if __name__ == "__main__":
  main()

