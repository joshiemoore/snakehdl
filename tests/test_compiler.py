import dill
from typing import Callable
from snakehdl import (
  BOp,
  output, const_bits, input_bits, bit, join,
  neg, conj, nand, disj, nor, xor, xnor
)
from snakehdl.compilers import PythonCompiler


class TestPythonCompiler:
  inputs = (
    input_bits('ina', bits=8),
    input_bits('inb', bits=8),
  )

  def _get_func(self, tree: BOp) -> Callable:
    # compile the optree to a pickled python function,
    # then unpickle it and return the function
    func_s = PythonCompiler().compile(tree)
    return dill.loads(func_s.data)

  def test_const_bits(self):
    tree = output(out0=const_bits(0), out1=const_bits(1))
    func = self._get_func(tree)
    assert func() == {'out0': 0, 'out1': 1}

  def test_basic_relay8(self):
    tree = output(out=self.inputs[0])
    func = self._get_func(tree)
    assert func(ina=0) == {'out': 0}
    assert func(ina=0b10101111) == {'out': 0b10101111}

  def test_bit(self):
    tree = output(out=bit(self.inputs[0], 1))
    func = self._get_func(tree)
    assert func(ina=0b00000010) == {'out': 1}
    assert func(ina=0b11111101) == {'out': 0}

  def test_join(self):
    tree = output(out=join(
      const_bits(0),
      const_bits(1),
      const_bits(1),
      const_bits(1),
      const_bits(0),
      const_bits(1),
    ))
    func = self._get_func(tree)
    assert func() == {'out': 0b101110}

  def test_not8(self):
    tree = output(out=neg(self.inputs[0]))
    func = self._get_func(tree)
    assert func(ina=0) == {'out': 0b11111111}
    assert func(ina=0b11111111) == {'out': 0}
    assert func(ina=0b10101010) == {'out': 0b01010101}

  def test_and8(self):
    tree = output(out=conj(*self.inputs))
    func = self._get_func(tree)
    assert func(ina=0, inb=0) == {'out': 0}
    assert func(ina=0b11110000, inb=0b10101111) == {'out': 0b10100000}
    assert func(ina=0b11111111, inb=0b11111111) == {'out': 0b11111111}
    assert func(ina=0b100000000, inb=0b100000000) == {'out': 0}

  def test_nand8(self):
    tree = output(out=nand(*self.inputs))
    func = self._get_func(tree)
    assert func(ina=0, inb=0) == {'out': 0b11111111}
    assert func(ina=0b11111111, inb=0b11111111) == {'out': 0}
    assert func(ina=0b00000000, inb=0b11111111) == {'out': 0b11111111}
    assert func(ina=0b10101010, inb=0b11001111) == {'out': 0b01110101}

  def test_or8(self):
    tree = output(out=disj(*self.inputs))
    func = self._get_func(tree)
    assert func(ina=0, inb=0) == {'out': 0}
    assert func(ina=0b11111111, inb=0b11111111) == {'out': 0b11111111}
    assert func(ina=0b00110011, inb=0b10101010) == {'out': 0b10111011}

  def test_nor8(self):
    tree = output(out=nor(*self.inputs))
    func = self._get_func(tree)
    assert func(ina=0, inb=0) == {'out': 0b11111111}
    assert func(ina=0b11111111, inb=0b11111111) == {'out': 0}
    assert func(ina=0b10101010, inb=0b11001100) == {'out': 0b00010001}

  def test_xor8(self):
    tree = output(out=xor(*self.inputs))
    func = self._get_func(tree)
    assert func(ina=0, inb=0) == {'out': 0}
    assert func(ina=0b11111111, inb=0) == {'out': 0b11111111}
    assert func(ina=0b11111111, inb=0b11111111) == {'out': 0}
    assert func(ina=0b10100101, inb=0b11111111) == {'out': 0b01011010}

  def test_xnor8(self):
    tree = output(out=xnor(*self.inputs))
    func = self._get_func(tree)
    assert func(ina=0, inb=0) == {'out': 0b11111111}
    assert func(ina=0b11111111, inb=0b11111111) == {'out': 0b11111111}
    assert func(ina=0b11111111, inb=0) == {'out': 0}
    assert func(ina=0b11000110, inb=0b10101010) == {'out': 0b10010011}

  # TODO test composite gates
