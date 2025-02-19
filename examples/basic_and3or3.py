# A simple 3-input AND gate and 3-input OR gate

from snakehdl import *
from snakehdl.compiler import LogisimCompiler


# compilation tree root must be an OUTPUT node
out = output(
  and3=conj(   # conj == 'conjunction' (because 'and' is a reserved keyword in Python)
    conj(
      input_bits('a'),
      input_bits('b'),
    ),
    input_bits('c'),
  ),
  or3=disj(    # disj == 'disjunction' (again because 'or' is a reserved keyword)
    disj(
      input_bits('a'),
      input_bits('b'),
    ),
    input_bits('c'),
  )
)

# BOps are printed as valid Python syntax, so they
# can be copy-pasted and recreated
print(out)

# Compile and save Logisim circuit file
# Open basic_and3or3.circ in Logisim Evolution to see the result!
LogisimCompiler().compile(out).save('basic_and3or3.circ')
