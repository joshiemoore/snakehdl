
# snakeHDL: A simple, purely-functional HDL for Python

snakeHDL is a tool for creating digital logic circuits with a focus on simplicity and accessibility.
This project is intended to be a fun and easy way for anyone to design real hardware with a few lines of Python.
Compile your circuit to Verilog, VHDL, or a dill-pickled Python function!

snakeHDL is Free Software licensed under the terms of the MIT License. The project is still early in development,
so bugs and general instability may occur.

Join us on [Discord](https://discord.gg/Vc6BrkTW)!

<p align="center">
  <img src="https://github.com/joshiemoore/snakehdl/blob/master/HACK_ALU.png" />

</p>
<p align="center">
  <i>The 16-bit HACK ALU from</i> "The Elements of Computing Systems" by Nisan and Schocken <i>implemented in snakeHDL, compiled to VHDL,
  and imported to Logisim. See</i> <a href="https://github.com/joshiemoore/snakehdl/blob/master/examples/HACK_ALU.py">examples/HACK_ALU.py</a>
</p>

## Introduction
snakeHDL has two main components: an API for expressing abstract trees of boolean logic, and an optimizing compiler that translates
these abstract logic trees into logic circuits. The compiler handles hardware-specific concerns, so you can focus purely on your
circuit's logic.

In short, snakeHDL lets you express **what** your circuit should do, instead of **how** it should do it.

```
  $ pip install snakehdl
  $ python3
  >>> from snakehdl import input_bits, output, xor
  >>> out = output(res=xor(input_bits('a'), input_bits('b')))
```

This creates a simple BOp tree representing a circuit with one output named `res` that is the XOR of two 1-bit inputs named `a` and `b`.

BOps are naturally composable into larger circuits because they are lazily evaluated. When you create a tree of BOps, nothing actually happens until you compile it:

```
  >>> from snakehdl.compilers import VerilogCompiler
  >>> VerilogCompiler(out, name='xor_ab').compile().save('xor_ab.v')
```

We can build composite logical structures like adders, multiplexers,
and even full ALUs starting from these fundamental BOps. Output bit widths
are automatically inferred based on the tree structure at compile time.

Since only twelve primitive BOps are specified by snakeHDL, it is straightforward to
create new compiler backends.

We will use snakeHDL to implement the ALU and control logic for the [Snake Processing Unit](https://github.com/joshiemoore/snakehdl/blob/master/examples/snakepu/design.txt), and then combine
this with the necessary sequential elements (registers, stack, RAM) to make the snakePU a mega-fast Python coprocessor chip.

## Binary Operations (BOps)
The following binary operations are specified by the snakeHDL API and must be implemented in hardware (or simulated hardware) by the compiler backends:

### Combinational Operations
* AND
* NAND
* OR
* NOR
* XOR
* XNOR
* NOT (unary)

### I/O Operations
* CONST
* INPUT
* OUTPUT
* BIT
* JOIN

...and that's it!
Check out the [BOp documentation](https://github.com/joshiemoore/snakehdl/blob/master/docs/bops.md) to learn more or look at the [examples](https://github.com/joshiemoore/snakehdl/tree/master/examples) to see BOps in action.

## Compiler Targets
- [x] Verilog
- [x] VHDL
- [x] Python - compile your circuit to a pickled Python function that accepts your named inputs
    as kwargs and returns the result as a dict of your named outputs. Useful for automated logic testing.
- [ ] Arduino
- [ ] Minecraft Redstone
- [ ] ...

## Optimizations
The following is a list of current and planned compiler optimizations:
- [x] Cached BOp hashing
- [x] Common Subexpression Elimination
- [ ] Constant folding (i.e. `A & 0 -> 0`)
- [ ] Gate pruning (i.e. `AND(A, AND(A, B)) -> AND(A, B)`)
- [ ] ...

## TODO
* Improve documentation
* Add more components to component library
* Add useful examples demonstrating snakeHDL functionality
* Optimize compiler output (constant folding, gate pruning, etc.)
* ***MAKE THE snakePU REAL***
