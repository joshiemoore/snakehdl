<!-- markdownlint-disable -->

<a href="../snakehdl/bops.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `bops`
Binary operations 

The `BOp` is the core data structure of snakeHDL. Each `BOp` represents a low-level primitive binary operation that must be implemented in hardware. 

`BOp` objects are immutable. They should not be modified by the user after initialization. 


---

<a href="../snakehdl/bops.py#L104"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

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

<a href="../snakehdl/bops.py#L116"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `input_bits`

```python
input_bits(name: 'str', bits: 'int' = 1) → BOp
```

INPUT - named circuit input 



**Args:**
 
 - <b>`name`</b>:  The name to assign to this input. Make sure not to use reserved  keywords from Verilog or VHDL. 
 - <b>`bits`</b>:  The bit width of the input. 



**Returns:**
 A `BOp` representing a named input. 


---

<a href="../snakehdl/bops.py#L129"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

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

<a href="../snakehdl/bops.py#L141"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

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

<a href="../snakehdl/bops.py#L153"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `join`

```python
join(*args: 'BOp') → BOp
```

JOIN - combine `n` 1-bit signals into one `n`-bit signal 



**Args:**
 
 - <b>`*args`</b>:  The `BOp` list to join into one signal. Each  arg must have a bit width of 1. 



**Returns:**
 A `BOp` of bit width `n`, where `n` is the length of `args`. 


---

<a href="../snakehdl/bops.py#L165"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `neg`

```python
neg(a: 'BOp') → BOp
```

NOT - negation 



**Args:**
 
 - <b>`a`</b>:  The `BOp` to negate. 



**Returns:**
 A `BOp` representing the unary operation `NOT a`. 


---

<a href="../snakehdl/bops.py#L176"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `conj`

```python
conj(a: 'BOp', b: 'BOp') → BOp
```

AND - conjunction 



**Args:**
 
 - <b>`a`</b>:  The first operand. 
 - <b>`b`</b>:  The second operand. 



**Returns:**
 A `BOp` representing the binary operation `a AND b`. 


---

<a href="../snakehdl/bops.py#L188"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `nand`

```python
nand(a: 'BOp', b: 'BOp') → BOp
```

NAND - non-conjunction 



**Args:**
 
 - <b>`a`</b>:  The first operand. 
 - <b>`b`</b>:  The second operand. 



**Returns:**
 A `BOp` representing the binary operation `a NAND b`. 


---

<a href="../snakehdl/bops.py#L200"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `disj`

```python
disj(a: 'BOp', b: 'BOp') → BOp
```

OR - disjunction 



**Args:**
 
 - <b>`a`</b>:  The first operand. 
 - <b>`b`</b>:  The second operand. 



**Returns:**
 A `BOp` representing the binary operation `a OR b`. 


---

<a href="../snakehdl/bops.py#L212"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `nor`

```python
nor(a: 'BOp', b: 'BOp') → BOp
```

NOR - non-disjunction 



**Args:**
 
 - <b>`a`</b>:  The first operand. 
 - <b>`b`</b>:  The second operand. 



**Returns:**
 A `BOp` representing the binary operation `a NOR b`. 


---

<a href="../snakehdl/bops.py#L224"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `xor`

```python
xor(a: 'BOp', b: 'BOp') → BOp
```

XOR - exclusive disjunction 



**Args:**
 
 - <b>`a`</b>:  The first operand. 
 - <b>`b`</b>:  The second operand. 



**Returns:**
 A `BOp` representing the binary operation `a XOR b`. 


---

<a href="../snakehdl/bops.py#L236"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `xnor`

```python
xnor(a: 'BOp', b: 'BOp') → BOp
```

XNOR - biconditional 



**Args:**
 
 - <b>`a`</b>:  The first operand. 
 - <b>`b`</b>:  The second operand. 



**Returns:**
 A `BOp` representing the binary operation `a XNOR b`. 


---

<a href="../snakehdl/bops.py#L16"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `BOps`
Enum representing specific types of primitive binary operations.  







---

<a href="../snakehdl/bops.py#L38"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `BOpGroup`
Utility class for grouping related `BOps`.  







---

<a href="../snakehdl/bops.py#L44"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

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

<a href="../snakehdl/bops.py#L81"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `pretty`

```python
pretty(indent: 'int' = 0, whitespace: 'bool' = False) → str
```








---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
