#!/usr/bin/env python3

import dis
import sys


if __name__ == '__main__':
  if len(sys.argv) != 3:
    print('Usage: ./build_rom.py <source> <dest>')
    exit(1)

  source = sys.argv[1]
  dest = sys.argv[2]
  # TODO add microroutine list to ROM
  # TODO add constant table to ROM
  # TODO add initial global table to ROM
  with open(source, 'rb') as f: co = compile(f.read(), source, 'exec')
  with open(dest, 'wb') as f: f.write(co.co_code)
