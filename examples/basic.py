# A simple 3-bit AND gate, 3-bit OR gate, and 3-bit negation

from snakehdl import *
from snakehdl.compiler import LogisimCompiler


out = output(  # compilation tree root must be an OUTPUT node
  and3=conj(   # conj == 'conjunction' (because 'and' is a reserved keyword in Python)
    conj(
      input_bits('a'),
      input_bits('b'),
    ),
    input_bits('c'),
  ),
  or3=disj(    # disj == 'disjunction' (because 'or' is a reserved keyword)
    disj(
      input_bits('a'),
      input_bits('b'),
    ),
    input_bits('c'),
  ),
  neg3=join(               # n 1-bit signals can be join()ed in one n-bit signal
    neg(input_bits('a')),  # neg == 'negation' (because 'not' is a reserved keyword)
    neg(input_bits('b')),
    neg(input_bits('c')),
  )
)

# BOp trees are printed as valid Python syntax, so they
# can be copy-pasted and recreated
print(out)

# Compile and save Logisim circuit file
# Open basic.circ in Logisim Evolution to see the result!
LogisimCompiler().compile(out).save('basic.circ')
