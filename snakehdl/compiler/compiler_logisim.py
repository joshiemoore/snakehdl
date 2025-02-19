from collections import defaultdict
from dataclasses import dataclass
import os.path
from typing import List, DefaultDict, Any
from xml.etree import ElementTree
from xml.etree.ElementTree import Element
from snakehdl import BOp, BOps
from snakehdl.compiler import Compiler


STEP = 10    # distance between grid units
STRIDE = 3   # grid units between output pins

# origin to begin component placement at
OG_X, OG_Y = STEP*10, STEP*10

# Map snakeHDL BOps to names of logisim components
_BOP_MAP = {
  BOps.CONST: 'Constant',
  BOps.BIT: 'Splitter',
  BOps.JOIN: 'Splitter',
  BOps.NOT: 'NOT Gate',
  BOps.AND: 'AND Gate',
  BOps.NAND: 'NAND Gate',
  BOps.OR: 'OR Gate',
  BOps.NOR: 'NOR Gate',
  BOps.XOR: 'XOR Gate',
  BOps.XNOR: 'XNOR Gate',
}

# layer % 2 gives gate orientation
_DIRECTION = {
  0: 'west',
  1: 'north',
}

class LogisimRender:
  def render(self, parent: Element) -> None:
    raise NotImplementedError()

@dataclass(frozen=True)
class LogisimGate(LogisimRender):
  op: BOp
  x: int
  y: int
  orientation: int

  def render(self, parent: Element) -> None:
    if self.op.op is BOps.INPUT:
      win = raycast(self.x, self.y, self.orientation, STEP*STRIDE)
      LogisimWire(self.x, self.y, win[0], win[1]).render(parent)
      return
    attrib = {
      'lib': '1',
      'loc': f'({self.x},{self.y})',
      'name': _BOP_MAP[self.op.op],
    }
    props = {
      'facing': _DIRECTION[self.orientation],
      'width': str(self.op.bits),
    }
    if self.op.op is not BOps.NOT:
      props['size'] = '30'
    if self.op.op is BOps.CONST:
      attrib['lib'] = '0'
      props['value'] = hex(self.op.val) if self.op.val else '0x0'
    elif self.op.op is BOps.BIT:
      attrib['lib'] = '0'
      new_pos = raycast(self.x, self.y, self.orientation, STEP*2)
      attrib['loc'] = f'({new_pos[0]},{new_pos[1]})'
      props['appear'] = 'center'
      props['incoming'] = str(self.op.src[0].bits)
      props['fanout'] = '1'
      for i in range(self.op.src[0].bits):
        bit_key = 'bit' + str(i)
        if i == self.op.bit_index: props[bit_key] = '0'
        else: props[bit_key] = 'none'
    elif self.op.op is BOps.JOIN:
      attrib['lib'] = '0'
      props['facing'] = 'east' if self.orientation == 0 else 'south'
      props['appear'] = 'right' if self.orientation == 0 else 'left'
      props['spacing'] = str(STRIDE)
      props['incoming'] = str(len(self.op.src))
      props['fanout'] = str(len(self.op.src))
      if self.orientation == 1:
        src_len = len(self.op.src)
        for i in range(src_len):
          bit_key = 'bit' + str(i)
          props[bit_key] = str(src_len - i - 1)
    el = Element('comp', attrib=attrib)
    LogisimProperties(props).render(el)
    parent.append(el)

  def get_inputs(self) -> tuple[tuple[BOp, int, int], ...]:
    if self.orientation not in {0, 1}: raise ValueError('invalid direction: ' + str(self.orientation))
    if self.op.op is BOps.CONST: return tuple()
    elif self.op.op is BOps.INPUT:
      inp = raycast(self.x, self.y, self.orientation, STEP*STRIDE)
      return ((self.op, inp[0], inp[1]),)
    elif self.op.op is BOps.NOT:
      inp = raycast(self.x, self.y, self.orientation, STEP*STRIDE)
      return ((self.op.src[0], inp[0], inp[1]),)
    elif self.op.op is BOps.BIT:
      inp = raycast(self.x, self.y, self.orientation, STEP*(STRIDE - 1))
      return ((self.op.src[0], inp[0], inp[1]),)
    elif self.op.op is BOps.JOIN:
      res = []
      for i in reversed(range(len(self.op.src))):
        pop = self.op.src[i]
        if self.orientation == 0: res.append((pop, self.x + STEP*(STRIDE-1), self.y + STEP  + i * STEP*STRIDE))
        else: res.append((pop, self.x + STEP + i * STEP*STRIDE, self.y + STEP*(STRIDE-1)))
      return tuple(res)
    if self.orientation == 0:
      return (
        (self.op.src[0], self.x + STEP*STRIDE, self.y - STEP),
        (self.op.src[1], self.x + STEP*STRIDE, self.y + STEP),
      )
    elif self.orientation == 1:
      return (
        (self.op.src[0], self.x - STEP, self.y + STEP*STRIDE),
        (self.op.src[1], self.x + STEP, self.y + STEP*STRIDE),
      )
    return tuple() # should never end up here

@dataclass(frozen=True)
class LogisimIO(LogisimRender):
  op: BOp
  name: str
  output: bool
  x: int
  y: int

  def render(self, parent: Element) -> None:
    attrib = {
      'lib': '0',
      'name': 'Pin',
      'loc': f'({self.x},{self.y})',
    }
    el = Element('comp', attrib=attrib)
    props = {
      'appearance': 'classic',
      'facing': 'east',
      'label': self.name,
      'output': 'true' if self.output else 'false',
      'width': str(self.op.bits),
      'radix': '16',
    }
    propel = LogisimProperties(props)
    propel.render(el)
    parent.append(el)

@dataclass(frozen=True)
class LogisimWire(LogisimRender):
  # from - (xa,ya)
  # to - (xb,yb)
  xa: int
  ya: int
  xb: int
  yb: int

  def render(self, parent: Element) -> None:
    parent.append(Element('wire', attrib={
      'from': str((self.xa, self.ya)),
      'to': str((self.xb, self.yb)),
    }))

@dataclass(frozen=True)
class LogisimProperties(LogisimRender):
  props: dict[str, str]
  def render(self, parent: Element) -> None:
    for prop in self.props:
      el = Element('a', {
        'name': prop,
        'val': self.props[prop],
      })
      parent.append(el)

def raycast(xa: int, ya: int, direction: int, distance: int) -> tuple[int, int]:
  # given "from" (xa,ya), direction, and distance, return "to" (xb,yb)
  if direction == 1: return (xa, ya + distance)
  elif direction == 0: return (xa + distance, ya)
  raise ValueError('invalid direction: ' + str(direction))

class LogisimCompiler(Compiler):
  def _compile(self, tree: BOp) -> bytes:
    # init compilation state
    layers: DefaultDict[int, List[BOp]] = defaultdict(list)
    layer_gates: DefaultDict[int, List[LogisimGate]] = defaultdict(list)
    outputs: List[LogisimIO] = []
    inputs: dict[BOp, LogisimIO] = {}

    if tree.outputs is None: raise RuntimeError('circuit has no outputs!')

    # init XML tree from template
    template_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data/logisim/template.circ')
    with open(template_path, 'r') as f:
      xmltree = ElementTree.parse(f)
    circuit: Element | Any | None = xmltree.getroot().find('circuit')
    if circuit is None or type(circuit) is not Element: raise RuntimeError('circuit root not found in template.circ')

    # cursor for placing gates and IO pins
    cursor = {
      'x': OG_X,
      'y': OG_Y,
    }

    # populate and render output pins
    init_q = []
    for out_id in tree.outputs:
      op = tree.outputs[out_id]
      init_q.append(op)
      out = LogisimIO(op, out_id, True, cursor['x'], cursor['y'])
      outputs.append(out)
      out.render(circuit)
      cursor['y'] += STEP*STRIDE
    cursor['x'] += STEP*STRIDE

    # breadth-first traversal to populate layer structure with ops
    def _populate(q: List[BOp], layer: int) -> None:
      if len(q) == 0: return
      next_q: List[BOp] = []
      while len(q) > 0:
        op = q.pop(0)
        next_q.extend(op.src)
        layers[layer].append(op)
      return _populate(next_q, layer + 1)
    _populate(init_q, 1)

    # collapse duplicates
    for layer in layers: layers[layer] = list(dict.fromkeys(layers[layer]))

    # run through layers 1 -> n
    # propagate leaf INPUTs to the next layer up so they can "snake through"
    # and so everything in the top layer should be INPUT or CONST
    # also render the gates and draw gate output wires
    row_x = cursor['x']
    row_y = cursor['y']
    for layer_num in layers:
      orientation = layer_num % 2
      for op in layers[layer_num]:
        # propagate inputs
        if op.op is BOps.INPUT and layer_num < len(layers) and len(op.src) == 0 and op not in layers[layer_num + 1]:
          layers[layer_num + 1].append(op)
        # render gate
        gate = LogisimGate(op, cursor['x'], cursor['y'], orientation)
        layer_gates[layer_num].append(gate)
        gate.render(circuit)
        # render gate output wire
        if layer_num > 1:
          if orientation == 1: LogisimWire(gate.x, gate.y, gate.x, row_y - STEP*STRIDE).render(circuit)
          else: LogisimWire(gate.x, gate.y, row_x - STEP*STRIDE, gate.y).render(circuit)
        if op.op is BOps.JOIN:
          if orientation == 1: cursor['x'] += STEP*STRIDE * len(op.src)
          else: cursor['y'] += STEP*STRIDE * len(op.src)
        else:
          if orientation == 1: cursor['x'] += STEP*STRIDE
          else: cursor['y'] += STEP*STRIDE
      if orientation == 1:
        cursor['y'] += STEP*STRIDE * 2
        row_y = cursor['y']
      else:
        cursor['x'] += STEP*STRIDE * 2
        row_x = cursor['x']

    # render gate input wires
    for layer_num in range(len(layer_gates)):
      for gate in layer_gates[layer_num]:
        for inp in gate.get_inputs():
          pgate = next(v for v in layer_gates[layer_num + 1] if v.op == inp[0])
          if gate.orientation == 0: LogisimWire(pgate.x, inp[2], inp[1], inp[2]).render(circuit)
          else: LogisimWire(inp[1], pgate.y, inp[1], inp[2]).render(circuit)

    # render input pins
    for op in layers[len(layers)]:
      if op.op is not BOps.INPUT: continue
      if op in inputs: continue
      if op.input_name is None: continue
      # input pin
      input_pin = LogisimIO(op, op.input_name, False, OG_X, cursor['y'] + len(inputs) * STEP*STRIDE)
      input_pin.render(circuit)
      inputs[op] = input_pin

    # connect output gates to output pins
    gate_x = OG_X + STEP*STRIDE
    for i, output in enumerate(outputs):
      output = outputs[i]
      LogisimWire(OG_X, output.y, gate_x, output.y).render(circuit)
      LogisimWire(gate_x, output.y, gate_x, OG_X + len(outputs) * STEP*STRIDE).render(circuit)
      if output.op.op is BOps.JOIN: gate_x += len(output.op.src) * STEP*STRIDE
      else: gate_x += STEP*STRIDE

    # connect top layer inputs to input pins
    top_len = len(layers[len(layers)])
    for input_op in inputs:
      input_pin = inputs[input_op]
      for in_idx in range(top_len):
        if layers[len(layers)][in_idx] != input_pin.op: continue
        if len(layers) % 2 == 0:
          ix = cursor['x'] + (top_len - in_idx) * STEP*STRIDE
          LogisimWire(input_pin.x, input_pin.y, ix, input_pin.y).render(circuit)
          iy = cursor['y'] - (top_len - in_idx) * STEP*STRIDE
          LogisimWire(ix, input_pin.y, ix, iy).render(circuit)
          LogisimWire(ix, iy, cursor['x'] - STEP*STRIDE, iy).render(circuit)
        else:
          ix = cursor['x'] - (top_len - in_idx) * STEP*STRIDE
          LogisimWire(input_pin.x, input_pin.y, ix, input_pin.y).render(circuit)
          LogisimWire(ix, input_pin.y, ix, cursor['y'] - STEP*STRIDE).render(circuit)

    # convert XML tree to bytes and return it
    return bytes(ElementTree.tostring(xmltree.getroot(), encoding='ascii'))
