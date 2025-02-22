# A simple 3-bit AND gate, 3-bit OR gate, and 3-bit negation

import dill
from snakehdl import output, input_bits, join, conj, disj, neg
from snakehdl.compilers import PythonCompiler


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

# The PythonCompiler compiles your circuit to a pickled Python function
# that accepts your named inputs as kwargs and returns a dict of your named outputs
out_compiled = PythonCompiler(out).compile()

out_func = dill.loads(out_compiled.data)

print('\na=0, b=0, c=0')
print(out_func(a=0, b=0, c=0))
print('\na=1, b=1, c=1')
print(out_func(a=1, b=1, c=1))
