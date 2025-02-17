from __future__ import annotations
import numpy as np
import dill
from snakehdl.compiler import Compiler
from snakehdl.utils import select_bits
from snakehdl import BOp


class PythonCompiler(Compiler):
  def _compile(self, tree: BOp) -> bytes:
    # recurse up the validated tree generating python lambdas for BOps
    assert tree.validated

    def _func(**kwargs) -> dict[str, np.uint]:
      from snakehdl import BOps  # noqa: E401
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
        elif op.op is BOps.CONST:
          if op.val is None: raise RuntimeError('missing val')
          if op.bits is None: raise RuntimeError('missing bits')
          return select_bits(op.val, op.bits)
        elif op.op is BOps.INPUT:
          if op.input_id not in kwargs: raise KeyError(op.input_id)
          if op.bits is None: raise RuntimeError('missing bits')
          return select_bits(np.uint(kwargs[op.input_id]), op.bits)
        else: raise NotImplementedError(op.op)
      if not tree.outputs: raise RuntimeError('missing outputs')
      res = { }
      for k in tree.outputs:
        if tree.bits is None: raise RuntimeError('missing OUTPUT bits\n' + str(tree))
        res[k] = _func_helper(tree.outputs[k]) & np.uint(2**len(tree.bits) - 1)
      return res
    return bytes(dill.dumps(_func))
