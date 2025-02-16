from __future__ import annotations
from dataclasses import dataclass
from enum import Enum, auto
from typing import Iterable, Optional
import numpy as np


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

@dataclass(frozen=True, kw_only=True)
class BOp:
  op: BOps
  src: tuple[BOp, ...] = tuple()
  bits: Optional[Iterable[int]] = None

  validated: bool = False

  # only for BOps.INPUT
  input_id: Optional[str] = None

  # only for BOps.OUTPUT
  outputs: Optional[dict[str, BOp]] = None

  # only for BOps.CONST
  val: Optional[np.uint] = None

  def pretty(self, indent: int=0, whitespace: bool=False) -> str:
    sep = '  ' if whitespace else ''
    nl = '\n' if whitespace else ''
    out = _BOP_FUNCS[self.op].__name__ + '('
    if self.input_id is not None: out += f'{nl + sep * (indent + 1)}id="{self.input_id}",'
    if self.bits is not None: out += f'{nl + sep * (indent + 1)}bits={self.bits},'
    if self.val is not None: out += f'{nl + sep * (indent + 1)}val={self.val},'
    if self.outputs is not None:
      for k,v in self.outputs.items(): out += nl + sep * (indent + 1) + f'{k}={v.pretty(indent=indent + 1, whitespace=whitespace)},'
    elif len(self.src) > 0:
      out += f'{nl + sep * (indent + 1)}src=(' + nl
      for v in self.src: out += sep * (indent + 2) + f'{v.pretty(indent=indent + 2, whitespace=whitespace)},' + nl
      out += sep * (indent + 1) + '),'
    out += nl + (sep * indent) + ')'
    return out

  def __repr__(self): return self.pretty()

  def __str__(self): return self.pretty(whitespace=True)

  def validate(self) -> None:
    # validate this BOp and all of its ancestors, throwing exceptions where errors are found
    # TODO
    object.__setattr__(self, 'validated', True)

  def assign_bits(self) -> None:
    # recurse up a validated tree and infer bit widths based on inputs
    # TODO
    assert self.validated
    raise NotImplementedError()

  def compile(self, compiler: str) -> bytes:
    from snakehdl.compiler import _COMPILERS
    kompiler_klass = _COMPILERS.get(compiler)
    if not kompiler_klass: raise KeyError(compiler)
    return kompiler_klass.compile(self).data

# special operations
def const(val: np.uint | int, bits: Optional[Iterable[int]]=None) -> BOp:
  return BOp(op=BOps.CONST, val=np.uint(val), bits=bits if bits else [0])
def input_bits(id: str, bits: Optional[Iterable[int]]=None) -> BOp: return BOp(op=BOps.INPUT, input_id=id, bits=bits if bits else [0])
def output(**kwargs: BOp) -> BOp: return BOp(op=BOps.OUTPUT, outputs=kwargs)
def noop() -> BOp: return BOp(op=BOps.NOOP)

# combinational operations
def neg(src: tuple[BOp]) -> BOp: return BOp(op=BOps.NOT, src=src)
def conj(src: tuple[BOp, BOp]) -> BOp: return BOp(op=BOps.AND, src=src)
def nand(src: tuple[BOp, BOp]) -> BOp: return BOp(op=BOps.NAND, src=src)
def disj(src: tuple[BOp, BOp]) -> BOp: return BOp(op=BOps.OR, src=src)
def nor(src: tuple[BOp, BOp]) -> BOp: return BOp(op=BOps.NOR, src=src)
def xor(src: tuple[BOp, BOp]) -> BOp: return BOp(op=BOps.XOR, src=src)
def xnor(src: tuple[BOp, BOp]) -> BOp: return BOp(op=BOps.XNOR, src=src)

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
