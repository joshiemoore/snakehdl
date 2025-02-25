import cocotb
from cocotb.triggers import Timer


@cocotb.test()
async def testbench(dut):
  dut.ina.value = 0x00
  await Timer(1, units='ns')
  assert dut.res.value == 0x00

  dut.ina.value = 0xff
  await Timer(1, units='ns')
  assert dut.res.value == 0xff

  dut.ina.value = 0b10101010
  await Timer(1, units='ns')
  assert dut.res.value == 0b10101010
