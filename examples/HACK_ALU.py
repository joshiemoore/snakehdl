from snakehdl import input_bits, output, const_bits, neg, conj, bit
from snakehdl.components import adder, mux
from snakehdl.compilers import LogisimCompiler


DATA_BITS = 4


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

print('building tree...')
# preset x
x_zero = mux(DATA_BITS, zx, x, const_bits(0, DATA_BITS))
x_neg = mux(DATA_BITS, nx, x_zero, neg(x_zero))

#preset y
y_zero = mux(DATA_BITS, zy, y, const_bits(0, DATA_BITS))
y_neg = mux(DATA_BITS, ny, y_zero, neg(y_zero))

# x&y or x+y
out = mux(DATA_BITS, f, conj(x_neg, y_neg), adder(DATA_BITS, x_neg, y_neg, const_bits(0))[0])
# negate output
out_neg = mux(DATA_BITS, no, out, neg(out))

# HACK ALU!
hack_alu = output(out=out_neg, ng=bit(out_neg, DATA_BITS-1))

print('compiling HACK ALU...')
LogisimCompiler('HACK_ALU').compile(hack_alu).save('HACK_ALU.circ')

print('HACK ALU circuit written to HACK_ALU.circ!')
