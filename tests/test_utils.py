import numpy as np
import pytest
from snakehdl.utils import select_bits


class TestUtils:
  def test_select_bits(self):
    assert select_bits(np.uint(0b0101), [0, 2]) == np.uint(0b0011)
    assert select_bits(np.uint(0b0011), [0, 2]) == np.uint(0b0001)
    assert select_bits(np.uint(0b1100), [3, 1, 2]) == np.uint(0b0101)
    with pytest.raises(IndexError):
      tst = np.uint(0b1111)
      select_bits(tst, [tst.nbytes * 8])
    with pytest.raises(IndexError):
      select_bits(np.uint(0b1111), [-1])
