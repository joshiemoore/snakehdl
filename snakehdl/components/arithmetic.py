from snakehdl import (
  BOp,
  bit, join,
  xor, disj, conj,
)


def adder1(a: BOp, b: BOp, cin: BOp) -> tuple[BOp, BOp]:
  """
  1-bit full adder.
  Returns (sum, cout)
  """
  return (
    xor(xor(a, b), cin),
    disj(conj(a, b), conj(xor(a, b), cin)),
  )

def adderN(bits: int, a: BOp, b: BOp, cin: BOp) -> tuple[BOp, BOp]:
  """
  N-bit full adder.
  Returns (sum, cout)
  """
  assert 1 <= bits <= 64
  out = []
  _cin = cin
  for i in range(bits):
    bit_a = bit(a, i)
    bit_b = bit(b, i)
    res, cout = adder1(bit_a, bit_b, _cin)
    out.append(res)
    _cin = cout
  return join(*out), cout
