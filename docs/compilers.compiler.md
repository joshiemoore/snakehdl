<!-- markdownlint-disable -->

<a href="../snakehdl/compilers/compiler.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `compilers.compiler`






---

<a href="../snakehdl/compilers/compiler.py#L6"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `Compiled`
Compiled(data: bytes) 

<a href="../<string>"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(data: bytes) → None
```








---

<a href="../snakehdl/compilers/compiler.py#L10"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `save`

```python
save(filepath: str) → None
```






---

<a href="../snakehdl/compilers/compiler.py#L14"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `Compiler`
Compiler(tree: snakehdl.bops.BOp, name: Optional[str] = None, _shared: set[snakehdl.bops.BOp] = <factory>, _sorted: List[snakehdl.bops.BOp] = <factory>, _inputs: dict[str, snakehdl.bops.BOp] = <factory>, _outputs: dict[str, snakehdl.bops.BOp] = <factory>) 

<a href="../<string>"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(
    tree: BOp,
    name: Optional[str] = None,
    _shared: set[BOp] = <factory>,
    _sorted: List[BOp] = <factory>,
    _inputs: dict[str, BOp] = <factory>,
    _outputs: dict[str, BOp] = <factory>
) → None
```








---

<a href="../snakehdl/compilers/compiler.py#L23"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `compile`

```python
compile() → Compiled
```








---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
