
# snakeHDL: a simple and lazy HDL for Python

snakeHDL is a tool for creating logic circuits with a focus on simplicity and accessibility. The goal is not to compete with the industry heavyweights, but to give hackers, makers, and educators a fun and easy way to build hardware with a few lines of Python.

## Introduction
snakeHDL compiles trees of primitive binary operations into logic circuits with named inputs and outputs:

```
  $ pip install snakehdl
  $ python3
  >>> from snakehdl import *
  >>> in_a, in_b = input_bits('a'), input_bits('b')
  >>> outputs = output(out_xor=xor(in_a, in_b), out_and=conj(in_a, in_b))
```
BOps are naturally composable into larger circuits because they are lazily evaluated. When you create a tree of BOps, nothing actually happens until you compile it:

```
  >>> from snakehdl.compiler import PythonCompiler
  >>> pickled_func = outputs.compile(PythonCompiler()).data
  >>> import dill
  >>> func = dill.loads(pickled_func)
  >>> func(a=1, b=1)
  {'out_xor': np.uint64(0), 'out_and': np.uint64(1)}
```

We can build composite logical structures like adders, multiplexers,
and even full ALUs starting from these fundamental BOps. Bit widths throughout
the tree are automatically inferred from input widths at compile time.

snakeHDL abstracts hardware-specific concerns away into the compiler backends,
leaving you to focus on implementing the pure logic of your circuit.

Since only ten primitive BOps are specified by snakeHDL, it is straightforward to
create compiler backends for new target platforms.

Wanna use this to implement a Python bytecode interpreter as a real processor core and then make [Snakeware 2](https://github.com/joshiemoore/snakeware) without Linux? Let's build the SNAKE PROCESSOR!!!

## Compiler Targets
- [x] Python - compile your circuit to a pickled Python function that accepts your named inputs
    as kwargs and returns the result as a dict of your named outputs. Useful for automated logic testing.
- [ ] Logisim .circ files
- [ ] Verilog
- [ ] Arduino
- [ ] OpenCL kernels
- [ ] FPGAs+ASICs
- [ ] Minecraft Redstone
- [ ] ...

## Binary Operations (BOps)
The following binary operations are specified by the snakeHDL API and must be implemented in hardware (or simulated hardware) by the compiler backends:

### I/O Operations
* CONST - `const(val: np.uint | int, bits: Sequence[int]=[0]) -> BOp`
* INPUT - `input_bits(input_id: str, bits: Sequence[int]=[0]) -> BOp`
* OUTPUT - `output(**kwargs: BOp)`

At compile time, the root of the tree must be an OUTPUT node, and this node's named outputs
will be your circuit's outputs. Any INPUT leaf nodes will be treated as your circuit's
named inputs.

The `bits` argument to CONST and INPUT allows you to select a range of bits from the input signal by
providing a sequence of bit indices. For example, for an 8-bit input signal `0Babcdefgh`, passing `[2, 4]` as
the `bits` argument will result in the 2-bit signal `0Bdf` being emitted by the INPUT node.
You could also say `range(2, 8)` to select the six most significant bits from the 8-bit input signal.
The default argument `[0]` results in a 1-bit signal being emitted from the LSB of the input signal.

### Combinational Operations
* NOT - `neg(a: BOp) -> BOp`
* AND - `conj(a: BOp, b: BOp) -> BOp`
* NAND - `nand(a: BOp, b: BOp) -> BOp`
* OR - `disj(a: BOp, b: BOp) -> BOp`
* NOR - `nor(a: BOp, b: BOp) -> BOp`
* XOR - `xor(a: BOp, b: BOp) -> BOp`
* XNOR - `xnor(a: BOp, b: BOp) -> BOp`

...and that's it! See `examples/` for demonstrations of these operations. Sequential logic is not supported by snakeHDL, but sequential elements are in consideration for a future expansion.
