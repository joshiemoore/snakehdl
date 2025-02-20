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
    op = join(const_bits(1), const_bits(0))
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

class TestValidations:
  def test_assign_bits(self):
    out = output(
      a=neg(input_bits('in_a', 3)),
      b=conj(
        input_bits('in_b', 4),
        input_bits('in_c', 4),
      ),
    )
    out.assign_bits()
    assert out.outputs['a'].bits == 3
    assert out.outputs['b'].bits == 4

  def test_assign_bits_invalid_src(self):
    # all of a node's src nodes must have the same bit width
    with pytest.raises(RuntimeError):
      output(
        a=conj(
          const_bits(0, 2),
          const_bits(0, 3),
        ),
      ).assign_bits()

  def test_validation_bit_index(self):
    with pytest.raises(IndexError):
      bit(const_bits(0, 2), 2).assign_bits()
    with pytest.raises(IndexError):
      bit(const_bits(0, 2), -1).assign_bits()

  def test_validation_join_1_bit(self):
    with pytest.raises(ValueError):
      join(const_bits(0, 2), const_bits(0, 2)).assign_bits()

  def test_validation_duplicate_input_labels_different_widths(self):
    # no duplicate input labels for inputs of differing widths
    with pytest.raises(RuntimeError):
      output(a=input_bits('in_a', 2), b=input_bits('in_a', 3)).validate()

  def test_validation_duplicate_input_labels_same_widths(self):
    # duplicate input labels with same widths allowed
    output(a=input_bits('in_a', 2), b=input_bits('in_a', 2)).validate()

  def test_validation_duplicate_input_output_labels(self):
    # input and output labels must be unique from each other
    with pytest.raises(RuntimeError):
      output(label_a=input_bits('label_a')).validate()

  def test_validation_multiple_output_nodes(self):
    with pytest.raises(RuntimeError):
      output(a=output(a=const_bits(0))).validate()

  def test_validation_input_missing_label(self):
    with pytest.raises(RuntimeError):
      output(a=input_bits(None)).validate()
