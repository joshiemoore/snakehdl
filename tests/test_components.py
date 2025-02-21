import dill
from typing import Callable
import pytest
from snakehdl import (
  BOp,
  input_bits, output,
)
from snakehdl.compiler import PythonCompiler
from snakehdl.components import adder, mux


def _get_func(tree: BOp) -> Callable:
  func_s = PythonCompiler().compile(tree).data
  return dill.loads(func_s)

class TestArithmeticComponents:
  def test_adder(self):
    res, cout = adder(4, input_bits('a', 4), input_bits('b', 4), input_bits('cin'))
    tree = output(res=res, cout=cout)
    func = _get_func(tree)
    for i in range(7): assert func(a=i, b=i, cin=0) == {'res': i + i, 'cout': 0}
    assert func(a=0, b=0, cin=1) == {'res': 1, 'cout': 0}
    assert func(a=10, b=5, cin=1) == {'res': 0, 'cout': 1}

class TestLogicalComponents:
  def test_mux(self):
    # 16-bit 2-way mux
    res = mux(16, input_bits('sel'), input_bits('a', 16), input_bits('b', 16))
    func = _get_func(output(res=res))
    assert func(sel=0, a=0xdead, b=0xbeef) == {'res': 0xdead}
    assert func(sel=1, a=0xc0de, b=0xcafe) == {'res': 0xcafe}

    # 8-bit 4-way mux
    res = mux(8, input_bits('sel', 2), input_bits('a', 8), input_bits('b', 8), input_bits('c', 8), input_bits('d', 8))
    func = _get_func(output(res=res))
    assert func(sel=0, a=1, b=2, c=3, d=4) == {'res': 1}
    assert func(sel=1, a=1, b=2, c=3, d=4) == {'res': 2}
    assert func(sel=2, a=1, b=2, c=3, d=4) == {'res': 3}
    assert func(sel=3, a=1, b=2, c=3, d=4) == {'res': 4}

    # compilation error if there are not enough bits in sel
    res = mux(8, input_bits('sel', 1), input_bits('a', 8), input_bits('b', 8), input_bits('c', 8), input_bits('d', 8))
    with pytest.raises(IndexError):
      func = _get_func(output(res=res))
