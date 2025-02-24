#!/usr/bin/env python3
import sys
import time
from snakehdl import BOp, BOps, input_bits, output, const_bits, neg, conj, bit
from snakehdl.components import adder, mux, multiway
from snakehdl.compilers import LogisimCompiler, VerilogCompiler


def hack_alu(DATA_BITS: int) -> BOp:
  ###### INPUTS ######

  # data inputs
  x = input_bits('x', DATA_BITS)
  y = input_bits('y', DATA_BITS)

  # preset the x input
  zx = input_bits('zx')
  nx = input_bits('nx')

  # preset the y input
  zy = input_bits('zy')
  ny = input_bits('ny')

  # function selector
  # 0 -> out = x & y
  # 1 -> out = x + y
  f = input_bits('f')

  # negate output
  no = input_bits('no')


  ###### ALU IMPLEMENTATION ######

  # preset x
  x_zero = mux(DATA_BITS, zx, x, const_bits(0, DATA_BITS))
  x_neg = mux(DATA_BITS, nx, x_zero, neg(x_zero))

  # preset y
  y_zero = mux(DATA_BITS, zy, y, const_bits(0, DATA_BITS))
  y_neg = mux(DATA_BITS, ny, y_zero, neg(y_zero))

  # x&y or x+y
  out = mux(DATA_BITS, f, conj(x_neg, y_neg), adder(DATA_BITS, x_neg, y_neg, const_bits(0))[0])

  # negate output
  out_neg = mux(DATA_BITS, no, out, neg(out))

  zr = multiway(BOps.NOR, *[bit(out_neg, i) for i in range(DATA_BITS)])

  # HACK ALU!
  return output(out=out_neg, ng=bit(out_neg, DATA_BITS-1), zr=zr)

if __name__ == '__main__':
  compiler_classes = {
    'logisim': LogisimCompiler,
    'verilog': VerilogCompiler,
  }
  alu_bits = {
    'logisim': 4,
    'verilog': 4,
  }

  if len(sys.argv) != 2 or sys.argv[1] not in compiler_classes:
    print('Usage: ./HACK_ALU.py <logisim/verilog>')
    print('e.g. ./HACK_ALU.py logisim')
    exit(1)

  alu = hack_alu(alu_bits[sys.argv[1]])
  print(f'compiling {alu_bits[sys.argv[1]]}-bit HACK ALU from BOp tree to {sys.argv[1]}...', end='', flush=True)
  stime = time.time()
  cres = compiler_classes[sys.argv[1]](alu).compile()
  print(f' done in {time.time() - stime} seconds')

  if sys.argv[1] == 'logisim':
    cres.save('HACK_ALU.circ')
    print('HACK ALU Logisim circuit saved to HACK_ALU.circ')
  elif sys.argv[1] == 'verilog':
    cres.save('HACK_ALU.v')
    print('HACK ALU Verilog saved to HACK_ALU.v')
