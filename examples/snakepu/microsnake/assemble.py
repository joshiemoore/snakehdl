#!/usr/bin/env python3
# assemble.py - assembler for snakePU microroutines

from dataclasses import dataclass
from enum import Enum, auto
from typing import List


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
  DST: Register
  SRC: Register | int
  ALU_OP: ALUOp = ALUOp.NONE
  JMP_OP: JMPOp = JMPOp.NONE
  CMP_OP: CMPOp = CMPOp.NONE
  INC_SP: bool = False
  DEC_SP: bool = False
  IMM: int = 0

def parse_uinst(inst: str) -> UInst:
  inst_u = inst.strip().upper()
  sp_idx: int = inst_u.index(' ')
  op: str = inst_u[:sp_idx]
  args: List[str] = inst_u[sp_idx + 1:].replace(' ', '').split(',')
  args_enc: List[Register | int] = []
  for arg in args:
    if arg in Register.__members__: args_enc.append(Register[arg])
    else: args_enc.append(int(arg))
  print(op)
  print(args_enc)
  # TODO create and return UInst instance with populated fields
  return UInst(
    Register.IMM,
    Register.IMM,
  )

if __name__ == '__main__':
  parse_uinst('eq stack, 0')
