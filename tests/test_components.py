import dill
from typing import Callable
from snakehdl import (
  BOp,
  input_bits, output,
)
from snakehdl.compiler import PythonCompiler
from snakehdl.components import adder1, adderN


def _get_func(tree: BOp) -> Callable:
  func_s = PythonCompiler().compile(tree).data
  return dill.loads(func_s)

class TestComponents:
  def test_adder1(self):
    res, cout = adder1(input_bits('a'), input_bits('b'), input_bits('cin'))
    tree = output(res=res, cout=cout)
    func = _get_func(tree)
    assert func(a=0, b=0, cin=0) == {'res': 0, 'cout': 0}
    assert func(a=0, b=0, cin=1) == {'res': 1, 'cout': 0}
    assert func(a=0, b=1, cin=0) == {'res': 1, 'cout': 0}
    assert func(a=0, b=1, cin=1) == {'res': 0, 'cout': 1}
    assert func(a=1, b=0, cin=0) == {'res': 1, 'cout': 0}
    assert func(a=1, b=0, cin=1) == {'res': 0, 'cout': 1}
    assert func(a=1, b=1, cin=0) == {'res': 0, 'cout': 1}
    assert func(a=1, b=1, cin=1) == {'res': 1, 'cout': 1}

  def test_adderN(self):
    res, cout = adderN(4, input_bits('a', 4), input_bits('b', 4), input_bits('cin'))
    tree = output(res=res, cout=cout)
    func = _get_func(tree)
    for i in range(7): assert func(a=i, b=i, cin=0) == {'res': i + i, 'cout': 0}
    assert func(a=0, b=0, cin=1) == {'res': 1, 'cout': 0}
    assert func(a=10, b=5, cin=1) == {'res': 0, 'cout': 1}
