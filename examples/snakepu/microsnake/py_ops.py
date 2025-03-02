# snakePU microcode implementations of Python bytecode ops


POP_TOP = '''
  sub sp, sp, 1
  ret
'''

LOAD_CONST = '''
  mov addr, arg
  add tmp0, tmp0, 3
  push ram
  geq ram, $PYOBJTYPE_FUNCTION
  add addr, addr, 1
  push ram
  add addr, addr, 1
  jz prim
  push addr
  ret
prim:
  push ram
  ret
'''

MAKE_FUNCTION = '''
  ; we already have the function object on the stack through
  ; LOAD_CONST, so just move the stack to it
  ; TODO is there anything else we need to do here?
  sub sp, sp, 4
  ret
'''

CALL_FUNCTION = '''
  ; TODO fix this, function object is on the stack
  mov addr, sp
  push pc
  push fp
  mov fp, addr
  sub addr, addr, arg
  mov addr, ram
  add addr, addr, 1
  mov pc, ram
  add addr, addr, 1
  mov tmp0, ram
  mul tmp0, tmp0, 3
  add sp, sp, tmp0
  ret
'''

RETURN_VALUE = '''
  pop tmp0
  ; TODO restore old frame pointer
  pop fp
  ; pop pc
  poke tmp0
  ret
'''
