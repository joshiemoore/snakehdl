import numpy as np
import dill
from .compiler import Compiler
from snakehdl import BOp, BOps


class PythonCompiler(Compiler):
  def _compile(self, inputs: tuple[BOp, ...]=tuple()) -> bytes:
    def _func(**kwargs) -> dict[str, int]:
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
          return op.val
        elif op.op is BOps.INPUT:
          if op.input_name not in kwargs: raise KeyError(op.input_name)
          if op._bits is None: raise RuntimeError(f'{op.op} missing bits\n' + str(op))
          return np.uint(kwargs[op.input_name]) & np.uint(2**op._bits - 1)
        elif op.op is BOps.BIT:
          if op.bit_index is None: raise RuntimeError('missing bit_index')
          return np.uint(_func_helper(op.src[0]) >> op.bit_index) & np.uint(1)
        elif op.op is BOps.JOIN:
          res = np.uint(0)
          for i in range(len(op.src)): res |= (np.uint(_func_helper(op.src[i]) << i) & np.uint(1 << i))
          return res
        else: raise NotImplementedError(op.op)
      if not self.tree.outputs: raise RuntimeError('missing outputs')
      res = { }
      for k in self.tree.outputs:
        op = self.tree.outputs[k]
        if op._bits is None: raise RuntimeError(f'missing bits for output {k}\n' + str(op))
        res[k] = int(_func_helper(op) & np.uint(2**op._bits - 1))
      return res
    return bytes(dill.dumps(_func))
