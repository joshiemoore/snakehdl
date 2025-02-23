from snakehdl import (
  BOp,
  bit, join,
  xor, disj, conj,
)


def adder(bits: int, a: BOp, b: BOp, cin: BOp) -> tuple[BOp, BOp]:
  """
  N-bit full adder.
  Returns (sum, cout)
  """
  assert bits > 0
  out = []
  cout = cin
  for i in range(bits):
    bit_a = bit(a, i)
    bit_b = bit(b, i)
    res = xor(xor(bit_a, bit_b), cout)
    cout = disj(conj(bit_a, bit_b), conj(xor(bit_a, bit_b), cout))
    out.append(res)
  return join(*out), cout
