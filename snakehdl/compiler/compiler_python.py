from __future__ import annotations
import numpy as np
import dill
from snakehdl.compiler import Compiler
from snakehdl.utils import select_bits
from snakehdl import BOp


class PythonCompiler(Compiler):
  @staticmethod
  def _compile(op: BOp) -> bytes:
    # recurse up the validated tree generating python lambdas for BOps
    assert op.validated

    def _func(**kwargs) -> dict[str, np.uint]:
      from snakehdl import BOps  # noqa: E401
      def _func_helper(_op: BOp) -> np.uint:
        if _op.op is BOps.NOT:
          return ~_func_helper(_op.src[0])
        elif _op.op is BOps.AND:
          return _func_helper(_op.src[0]) & _func_helper(_op.src[1])
        elif _op.op is BOps.NAND:
          return ~(_func_helper(_op.src[0]) & _func_helper(_op.src[1]))
        elif _op.op is BOps.OR:
          return _func_helper(_op.src[0]) | _func_helper(_op.src[1])
        elif _op.op is BOps.NOR:
          return ~(_func_helper(_op.src[0]) | _func_helper(_op.src[1]))
        elif _op.op is BOps.XOR:
          return _func_helper(_op.src[0]) ^ _func_helper(_op.src[1])
        elif _op.op is BOps.XNOR:
          return ~(_func_helper(_op.src[0]) ^ _func_helper(_op.src[1]))
        elif _op.op is BOps.NOOP:
          return np.uint(0) # TODO is this right?
        elif _op.op is BOps.CONST:
          if _op.val is None: raise RuntimeError('missing val')
          if _op.bits is None: raise RuntimeError('missing bits')
          return select_bits(_op.val, _op.bits)
        elif _op.op is BOps.INPUT:
          if _op.input_id not in kwargs: raise KeyError(_op.input_id)
          if _op.bits is None: raise RuntimeError('missing bits')
          return select_bits(np.uint(kwargs[_op.input_id]), _op.bits)
        # python compiler does not support sequential ops
        # we would have to write some kind of runtime to make that work I think
        # not right now
        else: raise NotImplementedError(_op.op)
      if not op.outputs: raise RuntimeError('missing outputs')
      res = { }
      for k in op.outputs:
        if op.bits is None: raise RuntimeError('missing output bits\n' + str(op))
        res[k] = _func_helper(op.outputs[k]) & np.uint(2**len(op.bits) - 1)
      return res
    return bytes(dill.dumps(_func))
