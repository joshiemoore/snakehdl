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
  assert bits > 0
  out = []
  cout = cin
  for i in range(bits):
    res, cout = adder1(bit(a, i), bit(b, i), cout)
    out.append(res)
  return join(*out), cout
