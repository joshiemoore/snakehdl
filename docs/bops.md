<!-- markdownlint-disable -->

<a href="../snakehdl/bops.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `bops`





---

<a href="../snakehdl/bops.py#L97"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `const_bits`

```python
const_bits(val: 'uint | int', bits: 'int' = 1) → BOp
```






---

<a href="../snakehdl/bops.py#L98"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `input_bits`

```python
input_bits(name: 'str', bits: 'int' = 1) → BOp
```






---

<a href="../snakehdl/bops.py#L99"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `output`

```python
output(**kwargs: 'BOp') → BOp
```






---

<a href="../snakehdl/bops.py#L100"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `bit`

```python
bit(src: 'BOp', index: 'int') → BOp
```






---

<a href="../snakehdl/bops.py#L101"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `join`

```python
join(*args: 'BOp') → BOp
```






---

<a href="../snakehdl/bops.py#L104"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `neg`

```python
neg(a: 'BOp') → BOp
```






---

<a href="../snakehdl/bops.py#L105"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `conj`

```python
conj(a: 'BOp', b: 'BOp') → BOp
```






---

<a href="../snakehdl/bops.py#L106"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `nand`

```python
nand(a: 'BOp', b: 'BOp') → BOp
```






---

<a href="../snakehdl/bops.py#L107"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `disj`

```python
disj(a: 'BOp', b: 'BOp') → BOp
```






---

<a href="../snakehdl/bops.py#L108"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `nor`

```python
nor(a: 'BOp', b: 'BOp') → BOp
```






---

<a href="../snakehdl/bops.py#L109"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `xor`

```python
xor(a: 'BOp', b: 'BOp') → BOp
```






---

<a href="../snakehdl/bops.py#L110"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `xnor`

```python
xnor(a: 'BOp', b: 'BOp') → BOp
```






---

<a href="../snakehdl/bops.py#L8"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `BOps`
Enum representing a specific type of primitive binary operation.  







---

<a href="../snakehdl/bops.py#L30"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `BOpGroup`
Utility class for grouping related `BOps`.  







---

<a href="../snakehdl/bops.py#L36"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `BOp`
Primitive binary operations that must be implemented in hardware. 

Users should not instantiate `BOp` objects directly, but rather create them through the API functions available in this module. 

<a href="../<string>"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(
    op: 'BOps',
    src: 'tuple[BOp, ]' = (),
    _bits: 'Optional[int]' = None,
    _hash: 'int' = 0,
    input_name: 'Optional[str]' = None,
    outputs: 'Optional[dict[str, BOp]]' = None,
    val: 'Optional[uint]' = None,
    bit_index: 'Optional[int]' = None
) → None
```








---

<a href="../snakehdl/bops.py#L73"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `pretty`

```python
pretty(indent: 'int' = 0, whitespace: 'bool' = False) → str
```








---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
