import numpy as np
import dill
from snakehdl import BOp, BOps
from snakehdl.compiler import Compiler
from snakehdl.utils import select_bits


class PythonCompiler(Compiler):
  @staticmethod
  def _compile(op: BOp) -> bytes:
    # recurse up the validated tree generating python lambdas for BOps
    assert op.validated

    def _func(**kwargs) -> dict[str, np.uint]:
      def _func_helper(op: BOp) -> np.uint:
        if op.op is BOps.NOT:
          return ~_func_helper(op.src[0])
        elif op.op is BOps.AND:
          return _func_helper(op.src[0]) & _func_helper(op.src[1])
        elif op.op is BOps.NAND:
          return ~(_func_helper(op.src[0]) & _func_helper(op.src[1]))
        elif op.op is BOps.OR:
          return _func_helper(op.src[0]) | _func_helper(op.src[1])
        elif op.op is BOps.NOR:
          return ~(_func_helper(op.src[0]) | _func_helper(op.src[1]))
        elif op.op is BOps.XOR:
          return _func_helper(op.src[0]) ^ _func_helper(op.src[1])
        elif op.op is BOps.XNOR:
          return ~(_func_helper(op.src[0]) ^ _func_helper(op.src[1]))
        elif op.op is BOps.NOOP:
          return np.uint(0) # TODO is this right?
        elif op.op is BOps.CONST:
          if op.val is None: raise RuntimeError('missing val')
          if op.bits is None: raise RuntimeError('missing bits')
          return select_bits(op.val, op.bits)
        elif op.op is BOps.INPUT:
          if op.input_id not in kwargs: raise KeyError(op.input_id)
          if op.bits is None: raise RuntimeError('missing bits')
          return select_bits(kwargs[op.input_id], op.bits)
        else: raise NotImplementedError(op.op)
      if not op.outputs: raise RuntimeError('missing outputs')
      return {k: _func_helper(op.outputs[k]) for k in op.outputs}
    return bytes(dill.dumps(_func))
