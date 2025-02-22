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
    tree.assign_bits()
    return Compiled(self._compile(tree, inputs=inputs))

  def _compile(self, tree: BOp, inputs: tuple[BOp, ...]=tuple()) -> bytes:
    # override with your compiler implementation
    # turn the validated BOp tree into compiled bytes for your target
    raise NotImplementedError()

  def validate(self, tree) -> tuple[BOp, ...]:
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
