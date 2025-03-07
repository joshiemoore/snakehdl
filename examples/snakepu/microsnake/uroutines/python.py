# snakePU microcode implementations of Python bytecode ops

PY_UROUTINES = {
  'POP_TOP': '''
    sub sp, 1
    ret
  ''',

  'LOAD_CONST': '''
    mov addr, arg
    add tmp0, 3
    push ram
    geq ram, $PYOBJTYPE_FUNCTION
    add addr, 1
    push ram
    add addr, 1
    jz prim
    push addr
    ret
  prim:
    push ram
    ret
  ''',

  'MAKE_FUNCTION': '''
    ; we already have the function object on the stack through
    ; LOAD_CONST, so just move the stack to it
    ; TODO is there anything else we need to do here?
    sub sp, 4
    ret
  ''',

  'CALL_FUNCTION': '''
    ; TODO fix this, function object is already on the stack
    mov addr, sp
    push pc
    push fp
    mov fp, addr
    sub addr, arg
    mov addr, ram
    add addr, 1
    mov pc, ram
    add addr, 1
    mov tmp0, ram
    mul tmp0, 3
    add sp, tmp0
    ret
  ''',

  'RETURN_VALUE': '''
    pop tmp0
    ; TODO restore old frame pointer
    pop fp
    ; pop pc
    poke tmp0
    ret
  ''',
}
