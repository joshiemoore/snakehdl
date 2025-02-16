import pytest
import numpy as np
from snakehdl.bops import (
  BOps,
  input_bits, output, const, noop,
  neg, conj, nand, disj, nor, xor, xnor,
)


class TestCreateBOps:
  #### special operations ####
  def test_input_bits(self):
    op = input_bits('a')
    assert op.op is BOps.INPUT
    assert str(op.op) == 'INPUT'
    assert op.input_id == 'a'
    assert op.bits == [0]

    op = input_bits('b', range(2,6))
    assert len(op.bits) == 4
    for i in range(2, 6): assert i in op.bits

  def test_output(self):
    op = output()
    assert op.op is BOps.OUTPUT
    assert str(op.op) == 'OUTPUT'
    assert op.outputs == {}

    op = output(out_a=const('0'), out_b=const('1'))
    assert op.outputs == {'out_a': const('0'), 'out_b': const('1')}

  def test_const(self):
    op = const(0b1010)
    assert op.op is BOps.CONST
    assert str(op.op) == 'CONST'
    assert op.val == 0b1010

    op = const(np.uint(1337))
    assert op.val == 1337

    op = const(123)
    assert op.val == 123

    with pytest.raises(ValueError):
      const('asdf')

    assert const(13) == const(13)
    assert const(8) != const(14)

  def test_noop(self):
    op = noop()
    assert op.op is BOps.NOOP
    assert str(op.op) == 'NOOP'

  #### combinational operations ####
  def test_neg(self):
    op = neg(const(1))
    assert op.op is BOps.NOT
    assert str(op.op) == 'NOT'
    assert len(op.src) == 1
    assert op.src[0] == const('1')

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
      op = func(const(0), const(1))
      assert op.op is bop
      assert str(op.op) == f'{bop.name}'
      assert len(op.src) == 2
      assert op.src[0] == const(0)
      assert op.src[1] == const(1)

  def test_pretty_print(self):
    # BOp pretty-print should be valid python syntax
    and3 = output(
      and3=conj(
        conj(input_bits('a'), input_bits('b')),
        input_bits('c'),
      )
    )
    and3_repr = eval(str(and3))
    assert and3_repr == and3
