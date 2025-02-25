#!/usr/bin/env python3

import dill
from snakehdl import input_bits, output, conj
from snakehdl.compilers import PythonCompiler


# basic AND gate
out = output(out=conj(input_bits('a'), input_bits('b')))

func_s = PythonCompiler(out).compile().data
func = dill.loads(func_s)

print('0 AND 0', func(a=0, b=0))
print('0 AND 1', func(a=0, b=1))
print('1 AND 1', func(a=1, b=1))
