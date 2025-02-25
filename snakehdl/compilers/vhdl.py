from snakehdl import BOp, BOps
from .compiler import Compiler


_SEP = '  '
_NL = '\n'

class VHDLCompiler(Compiler):
  def _compile(self) -> bytes:
    module_name = "circuit" if self.name is None else self.name
    inputs = [f'{_SEP*2}{k} :aasdasddds in {self._render_bits(op)};' for k, op in self._inputs.items()]
    outputs = []
    cse_signals = []
    ops = []
    for op in self._shared:
      cse_id = op._cse_id()
      cse_signals.append(f'{_SEP}signal {cse_id} : {self._render_bits(op)};')
      ops.append(f'{_SEP}{cse_id} <= {self._render(op, True)};')
    for k, op in self._outputs.items():
      outputs.append(f'{_SEP*2}{k} : out {self._render_bits(op)}')
      ops.append(f'{_SEP}{k} <= {self._render(op)};')

    out = f'''library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity {module_name} is
  port(
{_NL.join(inputs)}
{(';' + _NL).join(outputs)}
  );
end entity {module_name};

architecture rtl of {module_name} is
{_NL.join(cse_signals)}
begin
{_NL.join(ops)}
end architecture rtl;
'''
    return bytes(out, 'ascii')

  def _render_bits(self, op: BOp):
    if op._bits is None: raise RuntimeError(f'{op.op} missing bits\n' + str(op))
    return f'std_logic_vector({op._bits-1} downto 0)' if op._bits > 1 else 'std_logic'

  def _render(self, op: BOp, cseroot=False) -> str:
    if not cseroot and op.op is not BOps.OUTPUT:
      # CSE
      if op in self._shared: return op._cse_id()
    if op.op is BOps.INPUT:
      if op.input_name is None: raise RuntimeError('INPUT missing name:\n' + str(op))
      return op.input_name
    elif op.op is BOps.CONST:
      if op._bits is None: raise RuntimeError('CONST missing bits\n' + str(op))
      if op.val is None: raise RuntimeError('CONST missing val:\n' + str(op))
      if op._bits > 1: return f'std_logic_vector(to_unsigned({op.val}, {op._bits}))'
      else: return f'\'{op.val}\''
    elif op.op is BOps.BIT:
      if op.bit_index is None: raise RuntimeError('BIT missing index\n' + str(op))
      pop = op.src[0]
      if pop._bits is None: raise RuntimeError('BIT src missing bits\n' + str(op))
      return f'({self._render(pop)}({op.bit_index}))' if pop._bits > 1 else f'{self._render(pop)}'
    elif op.op is BOps.JOIN: return '(' + ' & '.join([self._render(v) for v in reversed(op.src)]) + ')'
    elif op.op is BOps.NOT: return f'not {self._render(op.src[0])}'
    elif op.op is BOps.AND: return f'({self._render(op.src[0])} and {self._render(op.src[1])})'
    elif op.op is BOps.NAND: return f'({self._render(op.src[0])} nand {self._render(op.src[1])})'
    elif op.op is BOps.OR: return f'({self._render(op.src[0])} or {self._render(op.src[1])})'
    elif op.op is BOps.NOR: return f'({self._render(op.src[0])} nor {self._render(op.src[1])})'
    elif op.op is BOps.XOR: return f'({self._render(op.src[0])} xor {self._render(op.src[1])})'
    elif op.op is BOps.XNOR: return f'({self._render(op.src[0])} xnor {self._render(op.src[1])})'
    else: raise NotImplementedError()
