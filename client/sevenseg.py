#! /usr/bin/python
#
# Converts digits and letters into corresponding 7-Segment encoding,
# setting high bits for illuminated segments.
# Deals with max display size, suppressing leading zeroes etc. 

# 7 Segment coding a=bit0, b=bit1, ..., DP=bit7
# Lowercase o can be used as "Degree" symbol

SEGMENTS = [0b00111111, 0b00000110, 0b01011011, 0b01001111, 0b01100110,
            0b01101101, 0b01111101, 0b00000111, 0b01111111, 0b01101111]
SPECIAL = { 'u': 0b00011100, 'c': 0b01011000 , '_': 0b00001000 ,
            '-': 0b01000000, ' ': 0b00000000 , 'o': 0b01100011}

def blank():
  """ Returns 7-segment code for a blank. """
  return 0

def digit(value, dp=False):
  """ Returns 7-segment code for a digit with optional decimal point. """
  return (SEGMENTS[value] | (0x80 * dp))

def char(value, dp=False):
  """ Returns 7-segment code for a charter with optional decimal point """
  if value in ['0','1','2','3','4','5','6','7','8','9']:
    return digit(int(value), dp)
  elif value in SPECIAL:
    return (SPECIAL[value] | (0x80 * dp))

def charList(value, dp=False):
  """ Returns a list containing the raw code if there is one,
      or an empty list if not. """
  raw = char(value,dp)
  if raw is None:
    return []
  else:
    return [raw]

def text(value, digits):
  """ Returns an array of 7-segment codings corresponding to a string or an
      integer number.

      If the string is shorter than the specified digits, it is padded on 
      the left. If it is longer, only the rightmost characters are included.

      Nonprintable characters are omitted.

      Periods are not separate characters but add a decimal point to the
      preceding character. To just print a period, specify " .".  A decimal
      point at the beginning of value renders a space with dp."""
  value = str(value)
  result = []
  c1 = None
  for c in value:
    if c == '.':
      result += charList(c1 if c1 else ' ', True)
      c1 = None
    else:
      if c1:
        result += charList(c1)
      c1 = c
  if c1:
    result += charList(c1)
  result = result[-digits:]
  while len(result) < digits:
    result = [blank()] + result
  return result

def blanks(digits):
  """ Blanks the display (all LED off). """
  return [blank()] * digits

def main():
  """ Poor man's unit tests """
  print "{0:08b}".format(blank())
  print "{0:08b}".format(digit(1))
  print "{0:08b}".format(digit(1, True))
  print text('1', 4)
  print text('1.', 4)
  print text('.', 4)
  print text('1.1.1.1.', 4)
  print text('21111', 4)
  print text(111, 4)
  print text(11111, 4)
  print text('xx1', 4)

if __name__ == "__main__":
  main()

