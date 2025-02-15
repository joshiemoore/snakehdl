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

  def __str__(self) -> str: return super().__str__().split('.')[1]

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

  def pretty(self, indent: int=0) -> str:
    sep = '  '
    NO_PARENTS = {BOps.CONST, BOps.INPUT, BOps.NOOP}
    out = str(self.op)
    if self.input_id is not None: out += f' {self.input_id}'
    if self.bits is not None: out += f' {self.bits}'
    if self.val is not None: out += f' {self.val}'
    if self.op not in NO_PARENTS:
      out += ' (\n'
      if self.outputs is not None:
        for k,v in self.outputs.items(): out += sep * (indent + 1) + f'{k}={v.pretty(indent=indent + 1)}'
      elif self.src is not None:
        for v in self.src: out += sep * (indent + 1) + f'{v.pretty(indent=indent + 1)}'
      out += f'{sep * indent})\n'
    else: out += '\n'
    return out

  def __repr__(self): return self.pretty()

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
