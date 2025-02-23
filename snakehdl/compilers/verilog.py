from snakehdl import BOp, BOps
from .compiler import Compiler


_SEP = '  '
_NL = '\n'

class VerilogCompiler(Compiler):
  def _compile(self) -> bytes:
    # module header
    out = f'module {"circuit" if self.name is None else self.name} (' + _NL

    # inputs
    for on in self._inputs:
      out += _SEP + 'input ' + self._render_bits(self._inputs[on]) + on + f',{_NL}'

    # outputs
    out += (',' + _NL).join([_SEP + 'output wire ' + self._render_bits(self._outputs[on]) + on for on in self._outputs])
    out += _NL + ');' + _NL

    # CSE - intermediate wires
    for op in self._shared:
      out += _NL+ _SEP + 'wire ' + self._render_bits(op) + self._cse_id(hash(op)) + ' = ' + self._render(op, cseroot=True) + ';'

    for on, op in self._outputs.items(): out += _NL + _SEP + f'assign {on} = {self._render(op)};'

    out += _NL + 'endmodule' + _NL

    return bytes(out, 'ascii')

  def _render_bits(self, op: BOp): return f'[{op._bits - 1}:0] ' if op._bits > 1 else ''

  def _cse_id(self, op_hash: int) -> str: return 'shared_' + str(op_hash).replace('-', '_')

  def _render(self, op: BOp, cseroot=False) -> str:
    if not cseroot and op.op is not BOps.OUTPUT:
      # CSE
      if op in self._shared: return self._cse_id(hash(op))
    if op.op is BOps.INPUT:
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
