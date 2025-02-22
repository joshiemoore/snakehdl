from snakehdl import BOp, BOps
from .compiler import Compiler


_SEP = '  '
_NL = '\n'

class VerilogCompiler(Compiler):
  def _render(self, op: BOp) -> str:
    if op.op is BOps.OUTPUT:
      res = ''
      if op.outputs is None: raise RuntimeError('OUTPUT missing outputs:\n' + str(op))
      for output_name, output_op in op.outputs.items():
        res += _SEP + f'assign {output_name} = {self._render(output_op)};' + _NL
      return res
    elif op.op is BOps.INPUT:
      if op.input_name is None: raise RuntimeError('INPUT missing name:\n' + str(op))
      return op.input_name
    elif op.op is BOps.CONST:
      if op.val is None: raise RuntimeError('CONST missing val:\n' + str(op))
      return str(op._bits) + '\'' + bin(op.val)[1:]
    elif op.op is BOps.BIT: return f'1\'({self._render(op.src[0])} >> {op.bit_index})'
    elif op.op is BOps.JOIN: return '{' + ', '.join([self._render(v) for v in reversed(op.src)]) + '}'
    elif op.op is BOps.NOT: return f'~({self._render(op.src[0])})'
    elif op.op is BOps.AND: return f'({self._render(op.src[0])} & {self._render(op.src[1])})'
    elif op.op is BOps.NAND: return f'~({self._render(op.src[0])} & {self._render(op.src[1])})'
    elif op.op is BOps.OR: return f'({self._render(op.src[0])} | {self._render(op.src[1])})'
    elif op.op is BOps.NOR: return f'~({self._render(op.src[0])} | {self._render(op.src[1])})'
    elif op.op is BOps.XOR: return f'({self._render(op.src[0])} ^ {self._render(op.src[1])})'
    elif op.op is BOps.XNOR: return f'~({self._render(op.src[0])} ^ {self._render(op.src[1])})'
    else: raise NotImplementedError()

  def _compile(self, tree: BOp, inputs: tuple[BOp, ...]=tuple()) -> bytes:
    if self.name is None: module_name = 'circuit'
    else: module_name = self.name

    # module header
    out = f'module {module_name} (' + _NL

    # inputs
    for op in inputs:
      if op.input_name is None: raise RuntimeError('INPUT missing name:\n' + str(op))
      out += _SEP + 'input ' + (f'[{op._bits - 1}:0] ' if op._bits > 1 else '') + op.input_name + f',{_NL}'

    # outputs
    if tree.outputs is None: raise RuntimeError('OUTPUT missing outputs:\n' + str(op))
    out += (',' + _NL).join([_SEP + 'output wire ' + (f'[{op._bits - 1}:0] ' if op._bits > 1 else '') + on for on, op in tree.outputs.items()])
    out += _NL + ');' + _NL

    # render tree
    out += self._render(tree)

    # module footer
    out += 'endmodule' + _NL

    return bytes(out, 'ascii')
