<!-- markdownlint-disable -->

# API Overview

## Modules

- [`bops`](./bops.md#module-bops)
- [`compilers`](./compilers.md#module-compilers)
- [`compilers.compiler`](./compilers.compiler.md#module-compilerscompiler)
- [`compilers.python`](./compilers.python.md#module-compilerspython)
- [`compilers.verilog`](./compilers.verilog.md#module-compilersverilog)
- [`compilers.vhdl`](./compilers.vhdl.md#module-compilersvhdl)
- [`components`](./components.md#module-components)
- [`components.arithmetic`](./components.arithmetic.md#module-componentsarithmetic)
- [`components.logical`](./components.logical.md#module-componentslogical)

## Classes

- [`bops.BOp`](./bops.md#class-bop): Primitive binary operations that must be implemented in hardware.
- [`bops.BOpGroup`](./bops.md#class-bopgroup): Utility class for grouping related `BOps`.
- [`bops.BOps`](./bops.md#class-bops): Enum representing a specific type of primitive binary operation.
- [`compiler.Compiled`](./compilers.compiler.md#class-compiled): Compiled(data: bytes)
- [`compiler.Compiler`](./compilers.compiler.md#class-compiler): Compiler(tree: snakehdl.bops.BOp, name: Optional[str] = None, _shared: set[snakehdl.bops.BOp] = <factory>, _sorted: List[snakehdl.bops.BOp] = <factory>, _inputs: dict[str, snakehdl.bops.BOp] = <factory>, _outputs: dict[str, snakehdl.bops.BOp] = <factory>)
- [`python.PythonCompiler`](./compilers.python.md#class-pythoncompiler)
- [`verilog.VerilogCompiler`](./compilers.verilog.md#class-verilogcompiler)
- [`vhdl.VHDLCompiler`](./compilers.vhdl.md#class-vhdlcompiler)

## Functions

- [`bops.bit`](./bops.md#function-bit): BIT - select one bit from `src`
- [`bops.conj`](./bops.md#function-conj): `a` AND `b`
- [`bops.const_bits`](./bops.md#function-const_bits): CONST - constant value
- [`bops.disj`](./bops.md#function-disj): `a` OR `b`
- [`bops.input_bits`](./bops.md#function-input_bits): INPUT - named circuit input
- [`bops.join`](./bops.md#function-join): JOIN - combine `n` 1-bit signals into one `n`-bit signal
- [`bops.nand`](./bops.md#function-nand): `a` NAND `b`
- [`bops.neg`](./bops.md#function-neg): NOT `a`
- [`bops.nor`](./bops.md#function-nor): `a` NOR `b`
- [`bops.output`](./bops.md#function-output): OUTPUT - named circuit output
- [`bops.xnor`](./bops.md#function-xnor): `a` XNOR `b`
- [`bops.xor`](./bops.md#function-xor): `a` XOR `b`
- [`arithmetic.adder`](./components.arithmetic.md#function-adder): N-bit full adder.
- [`logical.multiway`](./components.logical.md#function-multiway)
- [`logical.mux`](./components.logical.md#function-mux)


---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
