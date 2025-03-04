#!/usr/bin/env python3
# assemble.py - assembler for snakePU microroutines

from dataclasses import dataclass
from enum import Enum, auto
from typing import List


class Register(Enum):
  IMM = auto()
  IR = auto()
  SP = auto()
  STACK_TOP = auto()
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

@dataclass(frozen=True)
class UInst:
  ALU_OP: ALUOp
  DST: Register
  SRC: Register | int
  # TODO rest of instruction fields

def parse_uinst(inst: str) -> UInst:
  inst = inst.strip().upper()
  sp_idx: int = inst.index(' ')
  op: str = inst[:sp_idx]
  args: List[str] = inst[sp_idx + 1:].replace(' ', '').split(',')
  args_enc: List[Register | int] = []
  for arg in args:
    if arg in Register.__members__: args_enc.append(Register[arg])
    else: args_enc.append(int(arg))
  print(op)
  print(args_enc)
  # TODO create and return UInst instance with populated fields
  return UInst(
    ALUOp.NONE,
    Register.IMM,
    Register.IMM,
  )

if __name__ == '__main__':
  parse_uinst('mov sp, arg')
