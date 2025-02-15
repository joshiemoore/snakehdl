from __future__ import annotations
from dataclasses import dataclass
from enum import Enum, auto
from typing import Iterable, Optional


class BOps(Enum):
  """
  Primitive binary operations that must be implemented in hardware.
  """

  # Special operations
  INPUT = auto()
  OUTPUT = auto()
  CONST = auto()
  NOOP = auto()

  # Combinational operations
  NOT = auto()
  AND = auto()
  NAND = auto()
  OR = auto()
  NOR = auto()
  XOR = auto()
  XNOR = auto()

  def __repr__(self): return self.name

@dataclass
class BOp:
  op: BOps
  src: Optional[tuple[BOp, ...]] = None

  # only for BOps.INPUT
  input_id: Optional[str] = None
  bits: Optional[Iterable[int]] = None

  # only for BOps.OUTPUT
  outputs: Optional[dict] = None

  # only for BOps.CONST
  val: Optional[int] = None

# special operations
def input_bits(id: str, bits: Optional[Iterable[int]]=None) -> BOp: return BOp(BOps.INPUT, input_id=id, bits=bits if bits else [0])
def output(**kwargs: BOp) -> BOp: return BOp(BOps.OUTPUT, outputs=kwargs)
def const(val: str|int) -> BOp: return BOp(BOps.CONST, val=int(val, 2) if isinstance(val, str) else val)
def noop() -> BOp: return BOp(BOps.NOOP)

# combinational operations
def neg(a: BOp) -> BOp: return BOp(BOps.NOT, src=(a,))
def conj(a: BOp, b: BOp) -> BOp: return BOp(BOps.AND, src=(a, b))
def nand(a: BOp, b: BOp) -> BOp: return BOp(BOps.NAND, src=(a, b))
def disj(a: BOp, b: BOp) -> BOp: return BOp(BOps.OR, src=(a, b))
def nor(a: BOp, b: BOp) -> BOp: return BOp(BOps.NOR, src=(a, b))
def xor(a: BOp, b: BOp) -> BOp: return BOp(BOps.XOR, src=(a, b))
def xnor(a: BOp, b: BOp) -> BOp: return BOp(BOps.XNOR, src=(a, b))
