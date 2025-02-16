from typing import Iterable
import numpy as np


def select_bits(val: np.uint, bits: Iterable[int]):
  # shift selected bit indices into the LSBs
  # so if val is 0babcdefgh and bits is [0, 4, 6], result is 0b00000bdh
  nbits = len(bits)
  out: np.uint = np.uint(0)
  for i in range(nbits):
    bidx = bits[i]
    if bidx < 0 or bidx >= val.nbytes * 8: raise IndexError(bidx)
    bmask = np.uint(1) << i
    if i <= bidx: out |= (val >> (bidx - i)) & bmask
    else: out |= (val << (i - bidx)) & bmask
  return out
