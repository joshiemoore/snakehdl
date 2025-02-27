#!/usr/bin/env python3

import dis
import sys


if __name__ == '__main__':
  if len(sys.argv) != 2:
    print('Usage: ./disas.py <romfile>')
    exit(1)

  source = sys.argv[1]
  with open(source, 'rb') as f: dis.dis(f.read())
