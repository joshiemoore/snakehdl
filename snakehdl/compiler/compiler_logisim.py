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
OG_X, OG_Y = STEP*20, STEP*20

# Map snakeHDL BOps to names of logisim components
_BOP_MAP = {
  BOps.CONST: 'Constant',
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
    el = Element('comp', attrib=attrib)
    LogisimProperties(props).render(el)
    parent.append(el)

  def get_inputs(self) -> dict[BOp, tuple[int, int]]:
    if self.op.op is BOps.CONST: return {}
    if self.op.op is BOps.INPUT: return {self.op: raycast(self.x, self.y, self.orientation, STEP*STRIDE)}
    elif self.op.op is BOps.NOT: return {self.op.src[0]: raycast(self.x, self.y, self.orientation, STEP*STRIDE)}
    if self.orientation not in {0, 1}: raise ValueError('invalid direction: ' + str(self.orientation))
    if self.orientation == 0:
      inputs = {
        self.op.src[0]: (self.x + STEP*STRIDE, self.y - STEP),
        self.op.src[1]: (self.x + STEP*STRIDE, self.y + STEP),
      }
    elif self.orientation == 1:
      inputs = {
        self.op.src[0]: (self.x - STEP, self.y + STEP*STRIDE),
        self.op.src[1]: (self.x + STEP, self.y + STEP*STRIDE),
      }
    return inputs

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
  if direction not in {0, 1}: raise ValueError('invalid direction: ' + str(direction))
  if direction == 1: return (xa, ya + distance)
  elif direction == 0: return (xa + distance, ya)
  return (-1, -1) # should never hit this

class LogisimCompiler(Compiler):
  def _compile(self, tree: BOp) -> bytes:
    # init compilation state
    layers: DefaultDict[int, List[BOp]] = defaultdict(list)
    outputs: List[LogisimIO] = []
    inputs: List[LogisimIO] = []

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
      #orientation = layer % 2
      while len(q) > 0:
        op = q.pop(0)
        next_q.extend(op.src)
        layers[layer].append(op)
      return _populate(next_q, layer + 1)
    _populate(init_q, 1)

    # collapse duplicate ops in layers
    for layer in layers:
      layers[layer] = list(dict.fromkeys(layers[layer]))

    # run through layers 1 -> n
    # propagate leaf INPUTs to the next layer up so they can "snake through"
    # and so everything in the top layer should be INPUT or CONST
    # also render the gates and draw gate output wires
    for layer_num in layers:
      orientation = layer_num % 2
      for op in layers[layer_num]:
        # propagate inputs
        if op.op is BOps.INPUT and layer_num < len(layers) and len(op.src) == 0 and op not in layers[layer_num + 1]:
          layers[layer_num + 1].append(op)
        # render gate
        gate = LogisimGate(op, cursor['x'], cursor['y'], orientation)
        gate.render(circuit)
        # render gate output wire
        if layer_num > 1:
          out_pos = raycast(gate.x, gate.y, orientation, (len(layers[layer_num - 1]) + 1) * -STEP*STRIDE)
          LogisimWire(gate.x, gate.y, out_pos[0], out_pos[1]).render(circuit)
        # render gate input wires
        if op.op is not BOps.CONST and layer_num < len(layers):
          gate_inputs = gate.get_inputs()
          for input in gate_inputs:
            in_to = gate_inputs[input]
            in_idx = layers[layer_num + 1].index(input)
            in_from = raycast(in_to[0], in_to[1], orientation, (in_idx + 1) * STEP*STRIDE)
            LogisimWire(in_to[0], in_to[1], in_from[0], in_from[1]).render(circuit)
        if orientation == 1: cursor['x'] += STEP*STRIDE
        else: cursor['y'] += STEP*STRIDE
      if orientation == 1: cursor['y'] += STEP*STRIDE * 2
      else: cursor['x'] += STEP*STRIDE * 2

    # render input pins and rails
    for op in layers[len(layers)]:
      if op.op is not BOps.INPUT: continue
      if op.input_id is None: continue
      # input pin
      input_pin = LogisimIO(op, op.input_id, False, OG_X, cursor['y'] + len(inputs) * STEP*STRIDE)
      input_pin.render(circuit)
      inputs.append(input_pin)

    # connect output gates to output pins
    for i, output in enumerate(outputs):
      output = outputs[i]
      gate_x = output.x + (i + 1) * STEP*STRIDE
      LogisimWire(output.x, output.y, output.x + (i + 1) * STEP*STRIDE, output.y).render(circuit)
      LogisimWire(gate_x, output.y, gate_x, OG_X + len(outputs) * STEP*STRIDE).render(circuit)

    # connect top layer inputs to input pins
    for i, input_pin in enumerate(inputs):
      ix = cursor['x'] - (i + 1) * STEP*STRIDE
      LogisimWire(input_pin.x, input_pin.y, ix, input_pin.y).render(circuit)
      if len(layers) % 2 == 0:
        LogisimWire(ix, input_pin.y, ix, cursor['y'] - (i + 1) * STEP*STRIDE).render(circuit)
      else:
        LogisimWire(ix, input_pin.y, ix, cursor['y'] - STEP*STRIDE).render(circuit)

    # convert XML tree to bytes and return it
    return bytes(ElementTree.tostring(xmltree.getroot(), encoding='ascii'))
