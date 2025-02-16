from dataclasses import dataclass
from snakehdl import BOp, BOps


@dataclass
class Compiled:
  data: bytes

  def save(self, filename: str) -> bool:
    # TODO
    raise NotImplementedError()

class Compiler:
  @classmethod
  def compile(klass, tree: BOp) -> Compiled:
    # pre-compile validations, optimizations etc, not to be overridden
    assert tree.op is BOps.OUTPUT, 'compilation root must be OUTPUT'
    tree.validate()
    # TODO optimizations
    tree.assign_bits()
    return Compiled(klass._compile(tree))

  @staticmethod
  def _compile(tree: BOp) -> bytes:
    # override with your compiler implementation
    # turn the validated BOp tree into compiled bytes for your target
    raise NotImplementedError()
