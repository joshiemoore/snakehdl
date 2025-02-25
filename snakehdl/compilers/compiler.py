from dataclasses import dataclass, field
from typing import Optional, List
from snakehdl import BOp, BOps


@dataclass(frozen=True)
class Compiled:
  data: bytes

  def save(self, filepath: str) -> None:
    with open(filepath, 'wb') as f:
      f.write(self.data)

@dataclass(frozen=True)
class Compiler:
  tree: BOp
  name: Optional[str] = None
  _shared: set[BOp] = field(default_factory=set)
  _sorted: List[BOp] = field(default_factory=list)
  _inputs: dict[str, BOp] = field(default_factory=dict)
  _outputs: dict[str, BOp] = field(default_factory=dict)

  def compile(self) -> Compiled:
    # pre-compilation validations, optimizations etc
    # not to be overridden
    assert self.tree.op is BOps.OUTPUT, 'compilation tree root must be OUTPUT'
    # TODO optimizations
    self._toposort(self.tree, set())
    dupes = set(self._inputs.keys()).intersection(set(self._outputs.keys()))
    if dupes: raise RuntimeError(f'duplicate labels for inputs and outputs not allowed: {", ".join(dupes)}')
    for op in self._sorted: self._assign_bits(op)
    return Compiled(self._compile())

  def _compile(self) -> bytes:
    # override with your compiler implementation
    # turn the validated BOp tree into compiled bytes for your target
    raise NotImplementedError()

  def _toposort(self, op: BOp, seen: set[BOp]) -> None:
    if op.op is BOps.OUTPUT:
      if len(self._outputs) > 0: raise RuntimeError('only one OUTPUT node allowed in tree')
      if op.outputs is None: raise RuntimeError('outputs cannot be None')
      self._outputs.update(op.outputs)
      for out in self._outputs.values(): self._toposort(out, seen)
      return
    elif op.op is BOps.INPUT:
      if op.input_name is None: raise RuntimeError('input missing label:\n' + str(op))
      if op.input_name in self._inputs and self._inputs[op.input_name]._bits != op._bits:
        raise RuntimeError(f'duplicate labels for differing inputs not allowed: {op.input_name}')
      self._inputs[op.input_name] = op
      return
    if op in self._shared: return
    if op in seen:
      if op.op is not BOps.INPUT: self._shared.add(op)
      return
    seen.add(op)
    for v in op.src: self._toposort(v, seen)
    self._sorted.append(op)

  def _assign_bits(self, op: BOp) -> int:
    if op.op is BOps.INPUT or op.op is BOps.CONST:
      if op._bits is None: raise RuntimeError(f'{op.op} missing bits\n' + str(op))
      if op._bits < 1 or op._bits > 64: raise RuntimeError(f'{op.op} bits must be 1-64\n' + str(op))
      return op._bits
    elif op.op is BOps.BIT:
      res = self._assign_bits(op.src[0])
      if op.bit_index is None: raise RuntimeError('BIT missing index\n' + str(op))
      if op.bit_index < 0 or op.bit_index >= res: raise IndexError(f'bit index {op.bit_index} out of range\n' + str(op))
      object.__setattr__(op, '_bits', 1)
      return 1
    if op._bits is not None: return op._bits
    if op.op is BOps.JOIN:
      b = len(op.src)
      if b < 1: raise RuntimeError('JOIN must have at least one input\n' + str(op))
      for v in op.src:
        if self._assign_bits(v) != 1: raise ValueError('All JOIN inputs must be 1 bit wide\n' + str(op))
      object.__setattr__(op, '_bits', b)
      return b
    parent_bits = list([self._assign_bits(v) for v in op.src])
    if not all(v == parent_bits[0] for v in parent_bits): raise RuntimeError('parent bit width mismatch\n' + str(op))
    object.__setattr__(op, '_bits', parent_bits[0])
    return parent_bits[0]
