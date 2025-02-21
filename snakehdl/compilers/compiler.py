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
    # TODO optimizations
    assert tree.op is BOps.OUTPUT, 'compilation tree root must be OUTPUT'
    inputs = tree.validate()
    tree.assign_bits()
    return Compiled(self._compile(tree, inputs=inputs))

  def _compile(self, tree: BOp, inputs: tuple[BOp, ...]=tuple()) -> bytes:
    # override with your compiler implementation
    # turn the validated BOp tree into compiled bytes for your target
    raise NotImplementedError()
