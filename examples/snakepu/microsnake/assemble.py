#!/usr/bin/env python3
# assemble.py - assembler for snakePU microroutines
# TODO write tests!

from dataclasses import dataclass
from enum import Enum, auto
from typing import List
#from uroutines.python import PY_UROUTINES


class Register(Enum):
  NONE = 0
  IMM = auto()
  IR = auto()
  SP = auto()
  STACK = auto()
  FP = auto()
  ARG = auto()
  PC = auto()
  ADDR = auto()
  RAM = auto()
  ROM = auto()
  TMP0 = auto()
  TMP1 = auto()
  TMP2 = auto()
  TMP3 = auto()

class ALUOp(Enum):
  NONE = 0

  # arithmetic operations
  ADD = auto()
  SUB = auto()
  MUL = auto()
  DIV = auto()

  # logical operations
  NOT = auto()
  AND = auto()
  XOR = auto()
  OR = auto()
  SHL = auto()
  SHR = auto()

class CMPOp(Enum):
  NONE = 0
  EQ = auto()
  GT = auto()
  LT = auto()
  GEQ = auto()
  LEQ = auto()

class JMPOp(Enum):
  NONE = 0
  RET = auto()
  JMP = auto()
  JZ = auto()
  JNZ = auto()

@dataclass(frozen=True)
class UInst:
  op: str
  DST: Register
  SRC: Register | int
  ALU_OP: ALUOp = ALUOp.NONE
  JMP_OP: JMPOp = JMPOp.NONE
  CMP_OP: CMPOp = CMPOp.NONE
  INC_SP: bool = False
  DEC_SP: bool = False
  IMM: int = 0

def nargs_error(inst: str) -> None:
  raise RuntimeError('incorrect number of operands: ' + inst)

def dst_error(inst: str) -> None:
  raise RuntimeError('dst must be a register: ' + inst)

def validate_dst(inst: str, dst: Register | int) -> Register:
  if type(dst) is not Register or dst is Register.IMM: raise RuntimeError('dst must be a register: ' + inst)
  return dst

def resolve_loc(inst: str, loc: int | str, labels: dict[str, int]) -> int:
  if type(loc) is int: return loc
  if type(loc) is str:
    if loc not in labels: raise RuntimeError('label not found: ' + inst)
    return labels[loc]
  raise RuntimeError('invalid loc ' + inst)

def parse_uinst(inst: str, labels: dict[str, int]={}) -> UInst:
  try:
    sp_idx: int = inst.index(' ')
    op: str = inst[:sp_idx]
    args: List[str] = inst[sp_idx + 1:].replace(' ', '').split(',')
  except ValueError:
    op = inst
    args = []
  args_enc: List[Register | int] = []
  for arg in args:
    if arg in Register.__members__: args_enc.append(Register[arg])
    else:
      try:
        args_enc.append(int(arg))
      except ValueError:
        if arg in labels: args_enc.append(labels[arg])
        elif arg[0] == '$': args_enc.append(0) # TODO resolve builtin variables
  # TODO DRY this up
  # we can DRY CMP and JMP ops at least
  # also ALU ops can be DRY'd up
  if op == 'MOV':
    if len(args_enc) != 2: nargs_error(inst)
    src = args_enc[1]
    dst = validate_dst(inst, args_enc[0])
    if type(src) is Register: return UInst(op, dst, src)
    elif type(src) is int: return UInst(op, dst, Register.IMM, IMM=src)
  elif op == 'PUSH':
    if len(args_enc) != 1: nargs_error(inst)
    src = args_enc[0]
    if type(src) is Register: return UInst(op, Register.STACK, src, INC_SP=True)
    elif type(src) is int: return UInst(op, Register.STACK, Register.IMM, INC_SP=True, IMM=src)
  elif op == 'POKE':
    if len(args_enc) != 1: nargs_error(inst)
    src = args_enc[0]
    if type(src) is Register: return UInst(op, Register.STACK, src)
    elif type(src) is int: return UInst(op, Register.STACK, Register.IMM, IMM=src)
  elif op == 'POP':
    if len(args_enc) != 1: nargs_error(inst)
    dst = validate_dst(inst, args_enc[0])
    return UInst(op, dst, Register.STACK, DEC_SP=True)
  elif op == 'PEEK':
    if len(args_enc) != 1: nargs_error(inst)
    dst = validate_dst(inst, args_enc[0])
    return UInst(op, dst, Register.STACK)
  elif op == 'RET':
    if len(args_enc) != 0: nargs_error(inst)
    return UInst(op, Register.NONE, Register.NONE, JMP_OP=JMPOp.RET)
  elif op == 'JMP':
    if len(args_enc) != 1: nargs_error(inst)
    if type(args_enc[0]) is not int: raise RuntimeError('jump loc must be immediate or label: ' + inst)
    loc = resolve_loc(inst, args_enc[0], labels)
    return UInst(op, Register.NONE, Register.IMM, IMM=loc, JMP_OP=JMPOp.JMP)
  elif op == 'JZ':
    if len(args_enc) != 1: nargs_error(inst)
    if type(args_enc[0]) is not int: raise RuntimeError('jump loc must be immediate or label: ' + inst)
    loc = resolve_loc(inst, args_enc[0], labels)
    return UInst(op, Register.NONE, Register.IMM, IMM=loc, JMP_OP=JMPOp.JZ)
  elif op == 'JNZ':
    if len(args_enc) != 1: nargs_error(inst)
    if type(args_enc[0]) is not int: raise RuntimeError('jump loc must be immediate or label: ' + inst)
    loc = resolve_loc(inst, args_enc[0], labels)
    return UInst(op, Register.NONE, Register.IMM, IMM=loc, JMP_OP=JMPOp.JNZ)
  elif op == 'EQ':
    if len(args_enc) != 2 : nargs_error(inst)
    src = args_enc[1]
    dst = validate_dst(inst, args_enc[0])
    if type(src) is Register: return UInst(op, dst, src, CMP_OP=CMPOp.EQ)
    elif type(src) is int: return UInst(op, dst, Register.IMM, IMM=src, CMP_OP=CMPOp.EQ)
  elif op == 'GT':
    if len(args_enc) != 2: nargs_error(inst)
    src = args_enc[1]
    dst = validate_dst(inst, args_enc[0])
    if type(src) is Register: return UInst(op, dst, src, CMP_OP=CMPOp.GT)
    elif type(src) is int: return UInst(op, dst, Register.IMM, IMM=src, CMP_OP=CMPOp.GT)
  elif op == 'LT':
    if len(args_enc) != 2: nargs_error(inst)
    src = args_enc[1]
    dst = validate_dst(inst, args_enc[0])
    if type(src) is Register: return UInst(op, dst, src, CMP_OP=CMPOp.LT)
    elif type(src) is int: return UInst(op, dst, Register.IMM, IMM=src, CMP_OP=CMPOp.LT)
  elif op == 'GEQ':
    if len(args_enc) != 2: nargs_error(inst)
    src = args_enc[1]
    dst = validate_dst(inst, args_enc[0])
    if type(src) is Register: return UInst(op, dst, src, CMP_OP=CMPOp.GEQ)
    elif type(src) is int: return UInst(op, dst, Register.IMM, IMM=src, CMP_OP=CMPOp.GEQ)
  elif op == 'LEQ':
    if len(args_enc) != 2: nargs_error(inst)
    src = args_enc[1]
    dst = validate_dst(inst, args_enc[0])
    if type(src) is Register: return UInst(op, dst, src, CMP_OP=CMPOp.LEQ)
    elif type(src) is int: return UInst(op, dst, Register.IMM, IMM=src, CMP_OP=CMPOp.LEQ)
  elif op == 'ADD':
    if len(args_enc) != 2: nargs_error(inst)
    src = args_enc[1]
    dst = validate_dst(inst, args_enc[0])
    if type(src) is Register: return UInst(op, dst, src, ALU_OP=ALUOp.ADD)
    elif type(src) is int: return UInst(op, dst, Register.IMM, IMM=src, ALU_OP=ALUOp.ADD)
  elif op == 'SUB':
    if len(args_enc) != 2: nargs_error(inst)
    src = args_enc[1]
    dst = validate_dst(inst, args_enc[0])
    if type(src) is Register: return UInst(op, dst, src, ALU_OP=ALUOp.SUB)
    elif type(src) is int: return UInst(op, dst, Register.IMM, IMM=src, ALU_OP=ALUOp.SUB)
  elif op == 'MUL':
    if len(args_enc) != 2: nargs_error(inst)
    src = args_enc[1]
    dst = validate_dst(inst, args_enc[0])
    if type(src) is Register: return UInst(op, dst, src, ALU_OP=ALUOp.MUL)
    elif type(src) is int: return UInst(op, dst, Register.IMM, IMM=src, ALU_OP=ALUOp.MUL)
  elif op == 'DIV':
    if len(args_enc) != 2: nargs_error(inst)
    src = args_enc[1]
    dst = validate_dst(inst, args_enc[0])
    if type(src) is Register: return UInst(op, dst, src, ALU_OP=ALUOp.DIV)
    elif type(src) is int: return UInst(op, dst, Register.IMM, IMM=src, ALU_OP=ALUOp.DIV)
  elif op == 'NOT':
    if len(args_enc) != 2: nargs_error(inst)
    src = args_enc[1]
    dst = validate_dst(inst, args_enc[0])
    if type(src) is Register: return UInst(op, dst, src, ALU_OP=ALUOp.NOT)
    elif type(src) is int: return UInst(op, dst, Register.IMM, IMM=src, ALU_OP=ALUOp.NOT)
  elif op == 'AND':
    if len(args_enc) != 2: nargs_error(inst)
    src = args_enc[1]
    dst = validate_dst(inst, args_enc[0])
    if type(src) is Register: return UInst(op, dst, src, ALU_OP=ALUOp.AND)
    elif type(src) is int: return UInst(op, dst, Register.IMM, IMM=src, ALU_OP=ALUOp.AND)
  elif op == 'XOR':
    if len(args_enc) != 2: nargs_error(inst)
    src = args_enc[1]
    dst = validate_dst(inst, args_enc[0])
    if type(src) is Register: return UInst(op, dst, src, ALU_OP=ALUOp.XOR)
    elif type(src) is int: return UInst(op, dst, Register.IMM, IMM=src, ALU_OP=ALUOp.XOR)
  elif op == 'OR':
    if len(args_enc) != 2: nargs_error(inst)
    src = args_enc[1]
    dst = validate_dst(inst, args_enc[0])
    if type(src) is Register: return UInst(op, dst, src, ALU_OP=ALUOp.OR)
    elif type(src) is int: return UInst(op, dst, Register.IMM, IMM=src, ALU_OP=ALUOp.OR)
  elif op == 'SHL':
    if len(args_enc) != 2: nargs_error(inst)
    src = args_enc[1]
    dst = validate_dst(inst, args_enc[0])
    if type(src) is Register: return UInst(op, dst, src, ALU_OP=ALUOp.SHL)
    elif type(src) is int: return UInst(op, dst, Register.IMM, IMM=src, ALU_OP=ALUOp.SHL)
  elif op == 'SHR':
    if len(args_enc) != 2: nargs_error(inst)
    src = args_enc[1]
    dst = validate_dst(inst, args_enc[0])
    if type(src) is Register: return UInst(op, dst, src, ALU_OP=ALUOp.SHR)
    elif type(src) is int: return UInst(op, dst, Register.IMM, IMM=src, ALU_OP=ALUOp.SHR)
  raise RuntimeError('invalid instruction: ' + inst)

def assemble_uroutine(routine: str) -> List[UInst]:
  # initial pass over uinsts to resolve labels and remove comments/empty lines
  labels = {}
  idx = 0
  uinsts: List[str] = []
  for uinst in routine.split('\n'):
    uinst_u = uinst.strip().upper()
    if not uinst_u or uinst_u[0] == ';': continue
    if uinst_u[-1] == ':':
      labels[uinst_u[:-1]] = idx
      continue
    uinsts.append(uinst_u)
    idx += 1
  res: List[UInst] = []
  for uinst in uinsts:
    if uinst[-1] == ':': continue
    res.append(parse_uinst(uinst, labels))
  return res

if __name__ == '__main__':
  #for uname in PY_UROUTINES:
  #  assemble_uroutine(PY_UROUTINES[uname])
  print(parse_uinst('SHR TMP0, TMP1'))
