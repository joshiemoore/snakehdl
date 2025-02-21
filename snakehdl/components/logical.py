import math
from snakehdl import BOp, conj, disj, neg, bit, join


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
  assert bits > 0
  assert len(args) >= 2, 'mux must have at least two inputs'
  sel_bits = math.log2(len(args))
  assert sel_bits.is_integer(), 'number of mux inputs must be an even power of 2'
  return join(*[_mux(sel, int(sel_bits - 1), *[bit(v, i) for v in args]) for i in range(bits)])
