import math
from snakehdl import BOp, BOps, BOpGroup, conj, disj, neg, bit, join


def _multiway(*args: BOp) -> BOp:
  if len(args) == 2: return BOp(args[0].op, src=args)
  return BOp(args[0].op, src=(
    _multiway(*args[:len(args) // 2]),
    _multiway(*args[len(args) // 2:]),
  ))

def multiway(*args: BOp) -> BOp:
  assert len(args) >= 2, 'multiway component must have at least two inputs'
  assert args[0].op is not BOps.NOT, 'NOT cannot be made multiway'
  assert args[0].op in BOpGroup.COMBINATIONAL, 'only combinational BOps can be made multiway'
  for op in args: assert op.op is args[0].op, 'all multiway gate inputs must be the same op'
  num_layers = math.log2(len(args))
  assert num_layers.is_integer(), 'number of multiway gate inputs must be an even power of 2'
  return _multiway(*args)

def _mux(sel: BOp, sel_idx: int, *args: BOp) -> BOp:
  if sel_idx == 0:
    return disj(
      conj(args[0], neg(bit(sel, 0))),
      conj(args[1], bit(sel, 0)),
    )
  return disj(
    conj(_mux(sel, sel_idx - 1, *args[:len(args) // 2]), neg(bit(sel, sel_idx))),
    conj(_mux(sel, sel_idx - 1, *args[len(args) // 2:]), bit(sel, sel_idx)),
  )

def mux(bits: int, sel: BOp, *args: BOp) -> BOp:
  # TODO can we DRY this and its helper up with multiway()?
  assert bits > 0
  assert len(args) >= 2, 'mux must have at least two inputs'
  sel_bits = math.log2(len(args))
  assert sel_bits.is_integer(), 'number of mux inputs must be an even power of 2'
  return join(*[_mux(sel, int(sel_bits - 1), *[bit(v, i) for v in args]) for i in range(bits)])
