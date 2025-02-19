from __future__ import annotations
from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional
import numpy as np


class BOps(Enum):
  """
  Primitive binary operations that must be implemented in hardware.
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

@dataclass(frozen=True, kw_only=True)
class BOp:
  op: BOps
  src: tuple[BOp, ...] = tuple()
  bits: int = 0

  # only for INPUT
  input_name: Optional[str] = None

  # only for OUTPUT
  outputs: Optional[dict[str, BOp]] = None

  # only for CONST
  val: Optional[np.uint] = None

  # only for BIT
  bit_index: Optional[int] = None

  def pretty(self, indent: int=0, whitespace: bool=False) -> str:
    sep = '  ' if whitespace else ''
    nl = '\n' if whitespace else ''
    out = _BOP_FUNCS[self.op].__name__ + '('
    if self.op is BOps.INPUT or self.op is BOps.CONST:
      out += nl + indent*sep + f'bits={self.bits},'
      if self.op is BOps.INPUT: out += nl + indent*sep + f'name="{self.input_name}",'
      elif self.op is BOps.CONST: out += nl + indent*sep + f'val={self.val},'
    elif self.op is BOps.OUTPUT:
      if self.outputs is not None:
        for k,v in self.outputs.items(): out += nl + (indent+1)*sep + f'{k}={v.pretty(indent=indent + 2, whitespace=whitespace)},'
    else:
      for v in self.src: out += nl + indent*sep + f'{v.pretty(indent=indent + 1, whitespace=whitespace)},'
    if self.op is BOps.BIT: out += nl + indent*sep + f'index={self.bit_index},'
    out += nl + (indent-1)*sep + ')'
    return out

  def __repr__(self): return self.pretty()

  def __str__(self): return self.pretty(whitespace=True)

  def validate(self) -> None:
    # validate this BOp and all of its ancestors, throwing exceptions where errors are found
    # TODO
    if self.op is BOps.OUTPUT and self.outputs is not None:
      for k,v in self.outputs.items(): v.validate()
    else:
      for v in self.src: v.validate()

  def assign_bits(self) -> int:
    # recurse up a validated tree and infer bit widths based on inputs
    if self.op is BOps.INPUT or self.op is BOps.CONST:
      if self.bits < 1 or self.bits > 64: raise RuntimeError('INPUT/CONST bits must be 1-64')
      return self.bits
    elif self.op is BOps.OUTPUT:
      if self.outputs is not None:
        for k,v in self.outputs.items():
          v.assign_bits()
      return 0
    elif self.op is BOps.BIT:
      self.src[0].assign_bits()
      if self.bit_index is None: raise RuntimeError('BIT missing index\n' + str(self))
      if self.bit_index < 0 or self.bit_index >= self.src[0].bits: raise IndexError(f'bit index {self.bit_index} out of range\n' + str(self))
      object.__setattr__(self, 'bits', 1)
      return 1
    elif self.op is BOps.JOIN:
      for v in self.src:
        v.assign_bits()
        if v.bits != 1: raise RuntimeError('All JOIN inputs must be 1 bit wide\n' + str(self))
      b = len(self.src)
      object.__setattr__(self, 'bits', b)
      return b
    else:
      parent_bits = list([v.assign_bits() for v in self.src])
      if not all(v == parent_bits[0] for v in parent_bits): raise RuntimeError('parent bit width mismatch\n' + str(self))
      object.__setattr__(self, 'bits', parent_bits[0])
      return parent_bits[0]

# I/O operations
def const_bits(val: np.uint | int, bits: int=1) -> BOp: return BOp(op=BOps.CONST, val=np.uint(val), bits=bits)
def input_bits(name: str, bits: int=1) -> BOp: return BOp(op=BOps.INPUT, input_name=name, bits=bits)
def output(**kwargs: BOp) -> BOp: return BOp(op=BOps.OUTPUT, outputs=kwargs)
def bit(src: BOp, index: int) -> BOp: return BOp(op=BOps.BIT, src=(src,), bit_index=index)
def join(*args: BOp) -> BOp: return BOp(op=BOps.JOIN, src=tuple(args))

# combinational operations
def neg(a: BOp) -> BOp: return BOp(op=BOps.NOT, src=(a,))
def conj(a: BOp, b: BOp) -> BOp: return BOp(op=BOps.AND, src=(a,b))
def nand(a: BOp, b: BOp) -> BOp: return BOp(op=BOps.NAND, src=(a,b))
def disj(a: BOp, b: BOp) -> BOp: return BOp(op=BOps.OR, src=(a,b))
def nor(a: BOp, b: BOp) -> BOp: return BOp(op=BOps.NOR, src=(a,b))
def xor(a: BOp, b: BOp) -> BOp: return BOp(op=BOps.XOR, src=(a,b))
def xnor(a: BOp, b: BOp) -> BOp: return BOp(op=BOps.XNOR, src=(a,b))

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
