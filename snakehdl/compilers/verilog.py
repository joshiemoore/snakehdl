from snakehdl import BOp, BOps
from .compiler import Compiler


_SEP = '  '
_NL = '\n'

class VerilogCompiler(Compiler):
  def _compile(self) -> bytes:
    assert False
    inputs = [f'{_SEP}input {self._render_bits(op)}{k},' for k, op in self._inputs.items()]
    outputs= [f'{_SEP}output wire {self._render_bits(op)}{k}' for k, op in self._outputs.items()]
    cse_wires = [f'{_SEP}wire {self._render_bits(op)}{op._cse_id()} = {self._render(op, cseroot=True)};' for op in self._shared]
    ops = [f'{_SEP}assign {k} = {self._render(op)};' for k, op in self._outputs.items()]

    out = f'''module {"circuit" if self.name is None else self.name} (
{_NL.join(inputs)}
{(',' + _NL).join(outputs)}
);
{_NL.join(cse_wires)}
{_NL.join(ops)}
endmodule
'''
    return bytes(out, 'ascii')

  def _render_bits(self, op: BOp):
    if op._bits is None: raise RuntimeError(f'{op.op} missing bits\n' + str(op))
    return f'[{op._bits - 1}:0] ' if op._bits > 1 else ''

  def _render(self, op: BOp, cseroot=False) -> str:
    if not cseroot and op.op is not BOps.OUTPUT:
      # CSE
      if op in self._shared: return op._cse_id()
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
