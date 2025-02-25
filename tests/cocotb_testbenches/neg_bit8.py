import cocotb
from cocotb.triggers import Timer


@cocotb.test()
async def testbench(dut):
  dut.ina.value = 0b00000010
  await Timer(1, units='ns')
  assert dut.res.value == 0

  dut.ina.value = 0b11111101
  await Timer(1, units='ns')
  assert dut.res.value == 1
