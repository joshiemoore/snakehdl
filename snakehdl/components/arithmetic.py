from snakehdl import (
  BOp,
  bit, join,
  xor, disj, conj,
)


def adder(bits: int, a: BOp, b: BOp, cin: BOp) -> tuple[BOp, BOp]:
  """
  N-bit full adder.
  Returns (sum, carry)
  """
  assert bits > 0
  out = []
  for i in range(bits):
    bit_a = bit(a, i)
    bit_b = bit(b, i)
    res = xor(xor(bit_a, bit_b), cin)
    cin = disj(conj(bit_a, bit_b), conj(xor(bit_a, bit_b), cin))
    out.append(res)
  return join(*out), cin
