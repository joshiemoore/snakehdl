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

  def pretty(self, indent: int=0, whitespace: bool=False) -> str:
    sep = '  ' if whitespace else ''
    nl = '\n' if whitespace else ''
    out = _BOP_FUNCS[self.op].__name__ + '('
    if self.input_id is not None: out += f'{nl + sep * (indent + 1)}id="{self.input_id}",'
    if self.bits is not None: out += f'{nl + sep * (indent + 1)}bits={self.bits},'
    if self.val is not None: out += f'{nl + sep * (indent + 1)}val={self.val},'
    if self.outputs is not None:
      for k,v in self.outputs.items(): out += nl + sep * (indent + 1) + f'{k}={v.pretty(indent=indent + 1, whitespace=whitespace)},'
    elif self.src is not None:
      out += f'{nl + sep * (indent + 1)}src=(' + nl
      for v in self.src: out += sep * (indent + 2) + f'{v.pretty(indent=indent + 2, whitespace=whitespace)},' + nl
      out += sep * (indent + 1) + '),'
    out += nl + (sep * indent) + ')'
    return out

  def __repr__(self): return self.pretty()
  def __str__(self): return self.pretty(whitespace=True)

# special operations
def input_bits(id: str, bits: Optional[Iterable[int]]=None) -> BOp: return BOp(BOps.INPUT, input_id=id, bits=bits if bits else [0])
def output(**kwargs: BOp) -> BOp: return BOp(BOps.OUTPUT, outputs=kwargs)
def const(val: str|int) -> BOp: return BOp(BOps.CONST, val=int(val, 2) if isinstance(val, str) else val)
def noop() -> BOp: return BOp(BOps.NOOP)

# combinational operations
def neg(src: tuple[BOp]) -> BOp: return BOp(BOps.NOT, src=src)
def conj(src: tuple[BOp, BOp]) -> BOp: return BOp(BOps.AND, src=src)
def nand(src: tuple[BOp, BOp]) -> BOp: return BOp(BOps.NAND, src=src)
def disj(src: tuple[BOp, BOp]) -> BOp: return BOp(BOps.OR, src=src)
def nor(src: tuple[BOp, BOp]) -> BOp: return BOp(BOps.NOR, src=src)
def xor(src: tuple[BOp, BOp]) -> BOp: return BOp(BOps.XOR, src=src)
def xnor(src: tuple[BOp, BOp]) -> BOp: return BOp(BOps.XNOR, src=src)

_BOP_FUNCS = {
  BOps.INPUT: input_bits,
  BOps.OUTPUT: output,
  BOps.CONST: const,
  BOps.NOOP: noop,
  BOps.NOT: neg,
  BOps.AND: conj,
  BOps.NAND: nand,
  BOps.OR: disj,
  BOps.NOR: nor,
  BOps.XOR: xor,
  BOps.XNOR: xnor,
}
