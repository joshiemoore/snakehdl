from __future__ import annotations
from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional, Sequence
import numpy as np


class BOps(Enum):
  """
  Primitive binary operations that must be implemented in hardware.
  """

  # Special operations
  INPUT = auto()
  OUTPUT = auto()
  WIRE_OUT = auto()
  WIRE_IN = auto()
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

@dataclass(frozen=True, kw_only=True)
class BOp:
  op: BOps
  src: tuple[BOp, ...] = tuple()
  bits: Optional[Sequence[int]] = None

  validated: bool = False

  # only for INPUT and WIRE_IN
  input_id: Optional[str] = None

  # only for OUTPUT and WIRE_OUT
  outputs: Optional[dict[str, BOp]] = None

  # only for CONST
  val: Optional[np.uint] = None

  def pretty(self, indent: int=0, whitespace: bool=False) -> str:
    sep = '  ' if whitespace else ''
    nl = '\n' if whitespace else ''
    out = _BOP_FUNCS[self.op].__name__ + '('
    if self.input_id is not None: out += nl + indent*sep + f'id="{self.input_id}",'
    if self.bits is not None: out += nl + indent*sep + f'bits={self.bits},'
    if self.val is not None: out += nl + indent*sep + f'val={self.val},'
    if self.outputs is not None:
      for k,v in self.outputs.items(): out += nl + (indent+1)*sep + f'{k}={v.pretty(indent=indent + 2, whitespace=whitespace)},'
    elif len(self.src) > 0:
      for v in self.src: out += nl + indent*sep + f'{v.pretty(indent=indent + 1, whitespace=whitespace)},'
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
    object.__setattr__(self, 'validated', True)

  def assign_bits(self) -> Sequence:
    # recurse up a validated tree and infer bit widths based on inputs
    assert self.validated
    if self.bits is not None: return self.bits
    if self.op is BOps.OUTPUT and self.outputs is not None: parents_bits = list([v.assign_bits() for k,v in self.outputs.items()])
    else: parents_bits = list([v.assign_bits() for v in self.src])
    object.__setattr__(self, 'bits', parents_bits[0])
    return parents_bits[0]

  def compile(self, kompiler_klass): return kompiler_klass.compile(self)

# special operations
def const(val: np.uint | int, bits: Optional[Sequence[int]]=None) -> BOp:
  return BOp(op=BOps.CONST, val=np.uint(val), bits=bits if bits else [0])
def input_bits(id: str, bits: Optional[Sequence[int]]=None) -> BOp: return BOp(op=BOps.INPUT, input_id=id, bits=bits if bits else [0])
def output(**kwargs: BOp) -> BOp: return BOp(op=BOps.OUTPUT, outputs=kwargs)
#def wire_in(src: BOp, id: str) -> BOp: return BOp(op=BOps.WIRE_IN, input_id=id)
#def wire_out(**kwargs: BOp) -> BOp: return BOp(op=BOps.WIRE_OUT, outputs=kwargs)
def noop() -> BOp: return BOp(op=BOps.NOOP)

# combinational operations
def neg(a: BOp) -> BOp: return BOp(op=BOps.NOT, src=(a,))
def conj(a: BOp, b: BOp) -> BOp: return BOp(op=BOps.AND, src=(a,b))
def nand(a: BOp, b: BOp) -> BOp: return BOp(op=BOps.NAND, src=(a,b))
def disj(a: BOp, b: BOp) -> BOp: return BOp(op=BOps.OR, src=(a,b))
def nor(a: BOp, b: BOp) -> BOp: return BOp(op=BOps.NOR, src=(a,b))
def xor(a: BOp, b: BOp) -> BOp: return BOp(op=BOps.XOR, src=(a,b))
def xnor(a: BOp, b: BOp) -> BOp: return BOp(op=BOps.XNOR, src=(a,b))

_BOP_FUNCS = {
  BOps.INPUT: input_bits,
  BOps.OUTPUT: output,
#  BOps.WIRE_IN: wire_in,
#  BOps.WIRE_OUT: wire_out,
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
