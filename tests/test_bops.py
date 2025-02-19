import pytest
import numpy as np
from snakehdl.bops import (
  BOps,
  const_bits, input_bits, output, bit, join,
  neg, conj, nand, disj, nor, xor, xnor,
)


class TestCreateBOps:
  #### I/O operations ####
  def test_input_bits(self):
    op = input_bits('a')
    assert op.op is BOps.INPUT
    assert str(op.op) == 'INPUT'
    assert op.input_name == 'a'
    assert op.bits == 1

    op = input_bits('b', range(2,6))
    assert len(op.bits) == 4
    for i in range(2, 6): assert i in op.bits

  def test_output(self):
    op = output()
    assert op.op is BOps.OUTPUT
    assert str(op.op) == 'OUTPUT'
    assert op.outputs == {}

    op = output(out_a=const_bits('0'), out_b=const_bits('1'))
    assert op.outputs == {'out_a': const_bits('0'), 'out_b': const_bits('1')}

  def test_const_bits(self):
    op = const_bits(0b1010)
    assert op.op is BOps.CONST
    assert str(op.op) == 'CONST'
    assert op.val == 0b1010

    op = const_bits(np.uint(1337))
    assert op.val == 1337

    op = const_bits(123)
    assert op.val == 123

    with pytest.raises(ValueError):
      const_bits('asdf')

    assert const_bits(13) == const_bits(13)
    assert const_bits(8) != const_bits(14)

  def test_bit(self):
    inp = input_bits('a', bits=16)
    op = bit(src=inp, index=0)
    assert op.op is BOps.BIT
    assert str(op.op) == 'BIT'
    assert op.bit_index == 0
    assert len(op.src) == 1
    assert op.src[0] == inp

  def test_join(self):
    op = join(src=(const_bits(1), const_bits(0)))
    assert op.op is BOps.JOIN
    assert str(op.op) == 'JOIN'
    assert len(op.src) == 2
    assert op.src[0] == const_bits(1)
    assert op.src[1] == const_bits(0)

  #### combinational operations ####
  def test_neg(self):
    op = neg(const_bits(1))
    assert op.op is BOps.NOT
    assert str(op.op) == 'NOT'
    assert len(op.src) == 1
    assert op.src[0] == const_bits('1')

  def test_binary_combinational_ops(self):
    ops = {
      BOps.AND: conj,
      BOps.NAND: nand,
      BOps.OR: disj,
      BOps.NOR: nor,
      BOps.XOR: xor,
      BOps.XNOR: xnor,
    }

    for bop, func in ops.items():
      op = func(const_bits(0), const_bits(1))
      assert op.op is bop
      assert str(op.op) == f'{bop.name}'
      assert len(op.src) == 2
      assert op.src[0] == const_bits(0)
      assert op.src[1] == const_bits(1)

  def test_pretty_print(self):
    # BOp pretty-print should be valid python syntax
    gate = output(
      and3=conj(
        conj(input_bits('a'), input_bits('b')),
        input_bits('c'),
      ),
      xor4=xor(
        xor(input_bits('d'), input_bits('e')),
        xor(const_bits(1), const_bits(0)),
      ),
    )
    gate_repr = eval(str(gate))
    assert gate_repr == gate
