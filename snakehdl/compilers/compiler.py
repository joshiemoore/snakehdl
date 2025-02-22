from dataclasses import dataclass
from typing import Optional
from snakehdl import BOp, BOps


@dataclass(frozen=True)
class Compiled:
  data: bytes

  def save(self, filepath: str) -> None:
    with open(filepath, 'wb') as f:
      f.write(self.data)

@dataclass(frozen=True)
class Compiler:
  name: Optional[str] = None

  def compile(self, tree: BOp) -> Compiled:
    # pre-compilation validations, optimizations etc
    # not to be overridden
    assert tree.op is BOps.OUTPUT, 'compilation tree root must be OUTPUT'
    # TODO optimizations
    inputs = self.validate(tree)
    self.assign_bits(tree)
    return Compiled(self._compile(tree, inputs=inputs))

  def _compile(self, tree: BOp, inputs: tuple[BOp, ...]=tuple()) -> bytes:
    # override with your compiler implementation
    # turn the validated BOp tree into compiled bytes for your target
    raise NotImplementedError()

  def validate(self, tree: BOp) -> tuple[BOp, ...]:
    # validate this BOp and all of its ancestors, throwing exceptions where errors are found
    inputs: dict[str, BOp] = {}
    outputs: dict[str, BOp] = {}
    q = [tree]
    while len(q) > 0:
      op = q.pop(0)
      if op.op is BOps.OUTPUT:
        if len(outputs) > 0: raise RuntimeError('only one OUTPUT node allowed in tree')
        if op.outputs is None: raise RuntimeError('compilation outputs cannot be None')
        outputs = op.outputs
        q.extend(op.outputs.values())
      else: q.extend(op.src)
      if op.op is BOps.INPUT:
        if op.input_name is None: raise RuntimeError('input missing label:\n' + str(op))
        if op.input_name in inputs and inputs[op.input_name]._bits != op._bits:
          raise RuntimeError(f'duplicate labels for differing inputs not allowed: {op.input_name}')
        inputs[op.input_name] = op
    dupes = set(inputs).intersection(set(outputs))
    if dupes: raise RuntimeError(f'duplicate labels for inputs and outputs not allowed: {", ".join(dupes)}')
    return tuple(inputs.values())

  def assign_bits(self, tree: BOp) -> int:
    # recurse up the tree and infer bit widths based on inputs
    if tree.op is BOps.INPUT or tree.op is BOps.CONST:
      if tree._bits < 1 or tree._bits > 64: raise RuntimeError('INPUT/CONST bits must be 1-64')
      return tree._bits
    elif tree.op is BOps.OUTPUT:
      if tree.outputs is not None:
        for k,v in tree.outputs.items():
          self.assign_bits(v)
      return 0
    elif tree.op is BOps.BIT:
      self.assign_bits(tree.src[0])
      if tree.bit_index is None: raise RuntimeError('BIT missing index\n' + str(tree))
      if tree.bit_index < 0 or tree.bit_index >= tree.src[0]._bits: raise IndexError(f'bit index {tree.bit_index} out of range\n' + str(tree))
      object.__setattr__(tree, '_bits', 1)
      return 1
    elif tree.op is BOps.JOIN:
      for v in tree.src:
        self.assign_bits(v)
        if v._bits != 1: raise ValueError('All JOIN inputs must be 1 bit wide\n' + str(tree))
      b = len(tree.src)
      object.__setattr__(tree, '_bits', b)
      return b
    else:
      parent_bits = list([self.assign_bits(v) for v in tree.src])
      if not all(v == parent_bits[0] for v in parent_bits): raise RuntimeError('parent bit width mismatch\n' + str(tree))
      object.__setattr__(tree, '_bits', parent_bits[0])
      return parent_bits[0]
