#!/usr/bin/env python3

from snakehdl import input_bits, output
from snakehdl.components import adder
from snakehdl.compilers import VHDLCompiler, VerilogCompiler


BITS = 4

res, cout = adder(BITS, input_bits('a', BITS), input_bits('b', BITS), input_bits('cin'))
out = output(res=res, cout=cout)

VerilogCompiler(out, name='ADD').compile().save('ADD.v')
VHDLCompiler(out, name='ADD').compile().save('ADD.vhdl')
