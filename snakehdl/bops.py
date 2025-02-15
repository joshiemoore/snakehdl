from __future__ import annotations
from dataclasses import dataclass
from enum import Enum, auto
from typing import Iterable, Optional


class BOps(Enum):
  """
  Primitive binary operations that must be implemented in hardware.
  """

  # Combinational operations
  NOT = auto()
  AND = auto()
  NAND = auto()
  OR = auto()
  NOR = auto()
  XOR = auto()
  XNOR = auto()

  # Special operations
  INPUT = auto()
  OUTPUT = auto()
  CONST = auto()
  NOOP = auto()

@dataclass
class BOp:
  op: BOps
  src: Optional[tuple[BOp, ...]] = None

  # only for BOps.INPUT
  input_id: Optional[str] = None
  input_bits: Optional[Iterable[int]] = None

  # only for BOps.OUTPUT
  outputs: Optional[dict] = None

  # only for BOps.CONST
  const: Optional[str] = None

# combinational operations
def neg(a: BOp) -> BOp: return BOp(op=BOps.NOT, src=(a,))
def conj(a: BOp, b: BOp) -> BOp: return BOp(op=BOps.AND, src=(a, b))
def nand(a: BOp, b: BOp) -> BOp: return BOp(op=BOps.NAND, src=(a, b))
def disj(a: BOp, b: BOp) -> BOp: return BOp(op=BOps.OR, src=(a, b))
def nor(a: BOp, b: BOp) -> BOp: return BOp(op=BOps.NOR, src=(a, b))
def xor(a: BOp, b: BOp) -> BOp: return BOp(op=BOps.XOR, src=(a, b))
def xnor(a: BOp, b: BOp) -> BOp: return BOp(op=BOps.XNOR, src=(a, b))

# special operations
def input(id: str, bits: Optional[Iterable[int]]=None) -> BOp: return BOp(op=BOps.INPUT, input_id=id, input_bits=bits if bits else [0])
def output(**kwargs: BOp) -> BOp: return BOp(op=BOps.OUTPUT, outputs=kwargs)
def const(val: str) -> BOp: return BOp(op=BOps.CONST, const=val)
def noop() -> BOp: return BOp(op=BOps.NOOP)
