from snakehdl import (
  BOp,
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
