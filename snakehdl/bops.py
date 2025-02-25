from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Optional
import numpy as np


class BOps(Enum):
  """Enum representing a specific type of primitive binary operation.
  """

  # I/O operations
  INPUT = auto()
  OUTPUT = auto()
  CONST = auto()
  BIT = auto()
  JOIN = auto()

  # Combinational operations
  NOT = auto()
  AND = auto()
  NAND = auto()
  OR = auto()
  NOR = auto()
  XOR = auto()
  XNOR = auto()

  def __str__(self) -> str: return super().__str__().split('.')[1]

class BOpGroup:
  """Utility class for grouping related `BOps`.
  """
  IO = {BOps.INPUT, BOps.OUTPUT, BOps.CONST, BOps.BIT, BOps.JOIN}
  COMBINATIONAL = {BOps.NOT, BOps.AND, BOps.NAND, BOps.OR, BOps.NOR, BOps.XOR, BOps.XNOR}

@dataclass(frozen=True)
class BOp:
  """Primitive binary operations that must be implemented in hardware.

  Users should not instantiate `BOp` objects directly, but rather create
  them through the API functions available in this module.
  """

  op: BOps
  src: tuple[BOp, ...] = tuple()
  _bits: Optional[int] = field(default=None)
  _hash: int = 0

  # only for INPUT
  input_name: Optional[str] = None

  # only for OUTPUT
  outputs: Optional[dict[str, BOp]] = None

  # only for CONST
  val: Optional[np.uint] = None

  # only for BIT
  bit_index: Optional[int] = None

  def __post_init__(self):
    object.__setattr__(self, '_hash', hash((
      self.op,
      tuple(id(v) for v in self.src),
      self._bits,
      self.input_name,
      self.val,
      self.bit_index,
    )))

  def __hash__(self) -> int: return self._hash

  def pretty(self, indent: int=0, whitespace: bool=False) -> str:
    sep = '  ' if whitespace else ''
    nl = '\n' if whitespace else ''
    out = indent*sep + _BOP_FUNCS[self.op].__name__ + '('
    if self.op is BOps.INPUT or self.op is BOps.CONST:
      out += nl + (indent+1)*sep + f'bits={self._bits},'
      if self.op is BOps.INPUT: out += nl + (indent+1)*sep + f'name="{self.input_name}",'
      elif self.op is BOps.CONST: out += nl + (indent+1)*sep + f'val={self.val},'
    elif self.op is BOps.OUTPUT:
      if self.outputs is not None:
        for k,v in self.outputs.items(): out += nl + (indent+1)*sep + f'{k}={v.pretty(indent=indent + 2, whitespace=whitespace)},'
    else:
      for v in self.src: out += nl + f'{v.pretty(indent=indent + 1, whitespace=whitespace)},'
    if self.op is BOps.BIT: out += nl + (indent+1)*sep + f'index={self.bit_index},'
    out += nl + indent*sep + ')'
    return out

  def __repr__(self): return self.pretty()

  def __str__(self): return self.pretty(whitespace=True)

  def _cse_id(self) -> str: return 'shared_' + str(self._hash).replace('-', 'n')

# I/O operations
def const_bits(val: np.uint | int, bits: int=1) -> BOp: return BOp(BOps.CONST, val=np.uint(val), _bits=bits)
def input_bits(name: str, bits: int=1) -> BOp: return BOp(BOps.INPUT, input_name=name, _bits=bits)
def output(**kwargs: BOp) -> BOp: return BOp(BOps.OUTPUT, outputs=kwargs)
def bit(src: BOp, index: int) -> BOp: return BOp(BOps.BIT, src=(src,), bit_index=index)
def join(*args: BOp) -> BOp: return BOp(BOps.JOIN, src=tuple(args))

# combinational operations
def neg(a: BOp) -> BOp: return BOp(BOps.NOT, src=(a,))
def conj(a: BOp, b: BOp) -> BOp: return BOp(BOps.AND, src=(a,b))
def nand(a: BOp, b: BOp) -> BOp: return BOp(BOps.NAND, src=(a,b))
def disj(a: BOp, b: BOp) -> BOp: return BOp(BOps.OR, src=(a,b))
def nor(a: BOp, b: BOp) -> BOp: return BOp(BOps.NOR, src=(a,b))
def xor(a: BOp, b: BOp) -> BOp: return BOp(BOps.XOR, src=(a,b))
def xnor(a: BOp, b: BOp) -> BOp: return BOp(BOps.XNOR, src=(a,b))

_BOP_FUNCS = {
  BOps.CONST: const_bits,
  BOps.INPUT: input_bits,
  BOps.OUTPUT: output,
  BOps.BIT: bit,
  BOps.JOIN: join,
  BOps.NOT: neg,
  BOps.AND: conj,
  BOps.NAND: nand,
  BOps.OR: disj,
  BOps.NOR: nor,
  BOps.XOR: xor,
  BOps.XNOR: xnor,
}
