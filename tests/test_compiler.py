import pytest
from cocotb.runner import get_runner
import dill
from typing import Callable
from pathlib import Path
from snakehdl import (
  BOp,
  output, const_bits, input_bits, bit, join,
  neg, conj, nand, disj, nor, xor, xnor
)
from snakehdl.compilers import Compiler, PythonCompiler, VerilogCompiler


inputs = (
  input_bits('ina', bits=8),
  input_bits('inb', bits=8),
)

class TestPythonCompiler:
  def _get_func(self, tree: BOp) -> Callable:
    # compile the optree to a pickled python function,
    # then unpickle it and return the function
    func_s = PythonCompiler().compile(tree)
    return dill.loads(func_s.data)

  def test_const_bits(self):
    tree = output(out0=const_bits(0xdead, 16), out1=const_bits(0xbeef, 16))
    func = self._get_func(tree)
    assert func() == {'out0': 0xdead, 'out1': 0xbeef}

  def test_basic_relay8(self):
    tree = output(out=inputs[0])
    func = self._get_func(tree)
    assert func(ina=0) == {'out': 0}
    assert func(ina=0b10101111) == {'out': 0b10101111}

  def test_bit(self):
    tree = output(out=bit(inputs[0], 1))
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
    tree = output(out=neg(inputs[0]))
    func = self._get_func(tree)
    assert func(ina=0) == {'out': 0b11111111}
    assert func(ina=0b11111111) == {'out': 0}
    assert func(ina=0b10101010) == {'out': 0b01010101}

  def test_and8(self):
    tree = output(out=conj(*inputs))
    func = self._get_func(tree)
    assert func(ina=0, inb=0) == {'out': 0}
    assert func(ina=0b11110000, inb=0b10101111) == {'out': 0b10100000}
    assert func(ina=0b11111111, inb=0b11111111) == {'out': 0b11111111}
    assert func(ina=0b100000000, inb=0b100000000) == {'out': 0}

  def test_nand8(self):
    tree = output(out=nand(*inputs))
    func = self._get_func(tree)
    assert func(ina=0, inb=0) == {'out': 0b11111111}
    assert func(ina=0b11111111, inb=0b11111111) == {'out': 0}
    assert func(ina=0b00000000, inb=0b11111111) == {'out': 0b11111111}
    assert func(ina=0b10101010, inb=0b11001111) == {'out': 0b01110101}

  def test_or8(self):
    tree = output(out=disj(*inputs))
    func = self._get_func(tree)
    assert func(ina=0, inb=0) == {'out': 0}
    assert func(ina=0b11111111, inb=0b11111111) == {'out': 0b11111111}
    assert func(ina=0b00110011, inb=0b10101010) == {'out': 0b10111011}

  def test_nor8(self):
    tree = output(out=nor(*inputs))
    func = self._get_func(tree)
    assert func(ina=0, inb=0) == {'out': 0b11111111}
    assert func(ina=0b11111111, inb=0b11111111) == {'out': 0}
    assert func(ina=0b10101010, inb=0b11001100) == {'out': 0b00010001}

  def test_xor8(self):
    tree = output(out=xor(*inputs))
    func = self._get_func(tree)
    assert func(ina=0, inb=0) == {'out': 0}
    assert func(ina=0b11111111, inb=0) == {'out': 0b11111111}
    assert func(ina=0b11111111, inb=0b11111111) == {'out': 0}
    assert func(ina=0b10100101, inb=0b11111111) == {'out': 0b01011010}

  def test_xnor8(self):
    tree = output(out=xnor(*inputs))
    func = self._get_func(tree)
    assert func(ina=0, inb=0) == {'out': 0b11111111}
    assert func(ina=0b11111111, inb=0b11111111) == {'out': 0b11111111}
    assert func(ina=0b11111111, inb=0) == {'out': 0}
    assert func(ina=0b11000110, inb=0b10101010) == {'out': 0b10010011}

  # TODO test components


# TODO test LogisimCompiler


class TestVerilogCompiler:
  def run(self, tree: BOp, tdir: Path, name: str):
    # compile verilog and save to tmp directory
    VerilogCompiler(name).compile(tree).save(tdir / (name + '.v'))

    # build and run the cocotb test
    runner = get_runner('verilator')
    runner.build(
      sources=[tdir / (name + '.v')],
      hdl_toplevel=name,
    )
    runner.test(hdl_toplevel=name, test_module='tests.verilog_testbenches.' + name)

  def test_const_bits(self, tmp_path):
    tree = output(out0=const_bits(0xdead, 16), out1=const_bits(0xbeef, 16))
    self.run(tree, tmp_path, 'const_bits')

  def test_basic_relay8(self, tmp_path):
    tree = output(out=inputs[0])
    self.run(tree, tmp_path, 'basic_relay8')

  def test_bit8(self, tmp_path):
    # select bit from input
    tree = output(out=bit(inputs[0], 1))
    self.run(tree, tmp_path, 'bit8')

  def test_neg_bit8(self, tmp_path):
    # select bit from BOp
    tree = output(out=bit(neg(inputs[0]), 1))
    self.run(tree, tmp_path, 'neg_bit8')

  def test_join8(self, tmp_path):
    tree = output(out=join(
      const_bits(0),
      const_bits(1),
      const_bits(1),
      const_bits(1),
      const_bits(0),
      const_bits(1),
      const_bits(0),
      const_bits(1),
    ))
    self.run(tree, tmp_path, 'join8')

  def test_not8(self, tmp_path):
    tree = output(out=neg(inputs[0]))
    self.run(tree, tmp_path, 'not8')

  def test_and8(self, tmp_path):
    tree = output(out=conj(*inputs))
    self.run(tree, tmp_path, 'and8')

  def test_nand8(self, tmp_path):
    tree = output(out=nand(*inputs))
    self.run(tree, tmp_path, 'nand8')

  def test_or8(self, tmp_path):
    tree = output(out=disj(*inputs))
    self.run(tree, tmp_path, 'or8')

  def test_nor8(self, tmp_path):
    tree = output(out=nor(*inputs))
    self.run(tree, tmp_path, 'nor8')

  def test_xor8(self, tmp_path):
    tree = output(out=xor(*inputs))
    self.run(tree, tmp_path, 'xor8')

  def test_xnor8(self, tmp_path):
    tree = output(out=xnor(*inputs))
    self.run(tree, tmp_path, 'xnor8')

  # TODO test components


class TestValidations:
  def test_assign_bits(self):
    c = Compiler()
    out = output(
      a=neg(input_bits('in_a', 3)),
      b=conj(
        input_bits('in_b', 4),
        input_bits('in_c', 4),
      ),
    )
    c.assign_bits(out)
    assert out.outputs['a']._bits == 3
    assert out.outputs['b']._bits == 4

  def test_assign_bits_invalid_src(self):
    # all of a node's src nodes must have the same bit width
    c = Compiler()
    with pytest.raises(RuntimeError):
      c.assign_bits(output(
        a=conj(
          const_bits(0, 2),
          const_bits(0, 3),
        ),
      ))

  def test_validation_bit_index(self):
    c = Compiler()
    with pytest.raises(IndexError):
      c.assign_bits(bit(const_bits(0, 2), 2))
    with pytest.raises(IndexError):
      c.assign_bits(bit(const_bits(0, 2), -1))

  def test_validation_join_1_bit(self):
    c = Compiler()
    with pytest.raises(ValueError):
      c.assign_bits(join(const_bits(0, 2), const_bits(0, 2)))

  def test_validation_duplicate_input_labels_different_widths(self):
    # no duplicate input labels for inputs of differing widths
    c = Compiler()
    with pytest.raises(RuntimeError):
      c.validate(output(a=input_bits('in_a', 2), b=input_bits('in_a', 3)))

  def test_validation_duplicate_input_labels_same_widths(self):
    # duplicate input labels with same widths allowed
    c = Compiler()
    c.validate(output(a=input_bits('in_a', 2), b=input_bits('in_a', 2)))

  def test_validation_duplicate_input_output_labels(self):
    # input and output labels must be unique from each other
    c = Compiler()
    with pytest.raises(RuntimeError):
      c.validate(output(label_a=input_bits('label_a')))

  def test_validation_multiple_output_nodes(self):
    c = Compiler()
    with pytest.raises(RuntimeError):
      c.validate(output(a=output(a=const_bits(0))))

  def test_validation_input_missing_label(self):
    c = Compiler()
    with pytest.raises(RuntimeError):
      c.validate(output(a=input_bits(None)))
