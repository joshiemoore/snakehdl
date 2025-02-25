<!-- markdownlint-disable -->

<a href="../snakehdl/bops.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `bops`





---

<a href="../snakehdl/bops.py#L97"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `const_bits`

```python
const_bits(val: 'uint | int', bits: 'int' = 1) → BOp
```

CONST - constant value 



**Args:**
 
 - <b>`val`</b>:  The value to assign to this constant. 
 - <b>`bits`</b>:  The bit width of the constant value. 



**Returns:**
 A `BOp` representing a constant value with a defined bit width. 


---

<a href="../snakehdl/bops.py#L109"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `input_bits`

```python
input_bits(name: 'str', bits: 'int' = 1) → BOp
```

INPUT - named circuit input 



**Args:**
 
 - <b>`name`</b>:  The name to assign to this input. Make sure not to use reserved  keywords from Verilog or VHDL. 
 - <b>`bits`</b>:  The bit width of the input. 



**Returns:**
 A `BOp` representing a named input 


---

<a href="../snakehdl/bops.py#L122"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `output`

```python
output(**kwargs: 'BOp') → BOp
```

OUTPUT - named circuit output 



**Args:**
 
 - <b>`**kwargs`</b>:  Each kwarg represents a named output in your circuit. Make sure  not to use reserved keywords from Verilog or VHDL. 



**Returns:**
 A `BOp` representing a collection of named outputs. 


---

<a href="../snakehdl/bops.py#L134"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `bit`

```python
bit(src: 'BOp', index: 'int') → BOp
```

BIT - select one bit from `src` 



**Args:**
 
 - <b>`src`</b>:  The `BOp` to select a bit from. 
 - <b>`index`</b>:  The index of the bit to select (indexed from LSB to MSB). 



**Returns:**
 A `BOp` representing a bit selected from `src`. 


---

<a href="../snakehdl/bops.py#L146"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `join`

```python
join(*args: 'BOp') → BOp
```

JOIN - combine `n` 1-bit signals into one `n`-bit signal 



**Args:**
 
 - <b>`*args`</b>:  The list of `BOp`s to join into one signal. Each  arg must have a bit width of 1. 



**Returns:**
 A `BOp` of bit width `n`, where `n` is the length of `args`. 


---

<a href="../snakehdl/bops.py#L159"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `neg`

```python
neg(a: 'BOp') → BOp
```






---

<a href="../snakehdl/bops.py#L160"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `conj`

```python
conj(a: 'BOp', b: 'BOp') → BOp
```






---

<a href="../snakehdl/bops.py#L161"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `nand`

```python
nand(a: 'BOp', b: 'BOp') → BOp
```






---

<a href="../snakehdl/bops.py#L162"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `disj`

```python
disj(a: 'BOp', b: 'BOp') → BOp
```






---

<a href="../snakehdl/bops.py#L163"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `nor`

```python
nor(a: 'BOp', b: 'BOp') → BOp
```






---

<a href="../snakehdl/bops.py#L164"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `xor`

```python
xor(a: 'BOp', b: 'BOp') → BOp
```






---

<a href="../snakehdl/bops.py#L165"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

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
