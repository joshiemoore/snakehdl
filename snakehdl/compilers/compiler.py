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
    self._assign_bits()
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
      self._shared.add(op)
      return
    seen.add(op)
    for v in op.src: self._toposort(v, seen)
    self._sorted.append(op)

  def _assign_bits(self, tree: Optional[BOp]=None) -> int:
    # recurse up the tree and infer bit widths based on inputs
    if tree is None: tree = self.tree
    if tree.op is BOps.INPUT or tree.op is BOps.CONST:
      if tree._bits < 1 or tree._bits > 64: raise RuntimeError('INPUT/CONST bits must be 1-64')
      return tree._bits
    elif tree.op is BOps.OUTPUT:
      if tree.outputs is not None:
        for k,v in tree.outputs.items():
          self._assign_bits(v)
      return 0
    elif tree.op is BOps.BIT:
      self._assign_bits(tree.src[0])
      if tree.bit_index is None: raise RuntimeError('BIT missing index\n' + str(tree))
      if tree.bit_index < 0 or tree.bit_index >= tree.src[0]._bits: raise IndexError(f'bit index {tree.bit_index} out of range\n' + str(tree))
      object.__setattr__(tree, '_bits', 1)
      return 1
    elif tree.op is BOps.JOIN:
      for v in tree.src:
        self._assign_bits(v)
        if v._bits != 1: raise ValueError('All JOIN inputs must be 1 bit wide\n' + str(tree))
      b = len(tree.src)
      object.__setattr__(tree, '_bits', b)
      return b
    else:
      parent_bits = list([self._assign_bits(v) for v in tree.src])
      if not all(v == parent_bits[0] for v in parent_bits): raise RuntimeError('parent bit width mismatch\n' + str(tree))
      object.__setattr__(tree, '_bits', parent_bits[0])
      return parent_bits[0]
