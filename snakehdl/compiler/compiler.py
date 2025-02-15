from dataclasses import dataclass
from snakehdl import BOp, BOps


@dataclass
class Compiled:
  data: bytes

  def save(self, filename: str) -> bool:
    # TODO
    raise NotImplementedError()

class Compiler:
  def compile(self, tree: BOp) -> Compiled:
    # pre-compile validations, optimizations etc, not to be overriden
    assert tree.op is BOps.OUTPUT, 'tree root must be OUTPUT'
    tree.validate()
    # TODO optimizations
    return Compiled(self._compile(tree))

  def _compile(self, tree: BOp) -> bytes:
    # override with your compiler implementation
    # turn the validated BOp tree into compiled bytes for your target
    raise NotImplementedError()
