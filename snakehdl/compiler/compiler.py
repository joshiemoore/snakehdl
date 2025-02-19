from dataclasses import dataclass
from snakehdl import BOp, BOps


@dataclass
class Compiled:
  data: bytes

  def save(self, filepath: str) -> None:
    with open(filepath, 'wb') as f:
      f.write(self.data)

class Compiler:
  def compile(self, tree: BOp) -> Compiled:
    # pre-compilation validations, optimizations etc
    # not to be overridden
    assert tree.op is BOps.OUTPUT, 'tree root must be OUTPUT'
    # TODO collapse internal IO (submodules)
    tree.validate()
    # TODO optimizations
    tree.assign_bits()
    return Compiled(self._compile(tree))

  def _compile(self, tree: BOp) -> bytes:
    # override with your compiler implementation
    # turn the validated BOp tree into compiled bytes for your target
    raise NotImplementedError()
