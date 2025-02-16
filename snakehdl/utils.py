from typing import Sequence
import numpy as np


def select_bits(val: np.uint, bits: Sequence) -> np.uint:
  # shift selected bit indices into the LSBs
  # so if val is 0babcdefgh and bits is [0, 4, 6], result is 0b00000bdh
  out: np.uint = np.uint(0)
  i: int= 0
  for bidx in bits:
    if bidx < 0 or bidx >= val.nbytes * 8: raise IndexError(bidx)
    bmask = np.uint(1) << i
    if i <= bidx: out |= np.uint((val >> (bidx - i)) & bmask)
    else: out |= np.uint((val << (i - bidx)) & bmask)
    i += 1
  return out
