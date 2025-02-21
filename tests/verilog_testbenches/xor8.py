import cocotb
from cocotb.triggers import Timer


@cocotb.test()
async def testbench(dut):
  dut.ina.value = 0x00
  dut.inb.value = 0x00
  await Timer(1, units='ns')
  assert dut.out.value == 0x00

  dut.ina.value = 0xff
  dut.inb.value = 0x00
  await Timer(1, units='ns')
  assert dut.out.value == 0xff

  dut.ina.value = 0xff
  dut.inb.value = 0xff
  await Timer(1, units='ns')
  assert dut.out.value == 0x00

  dut.ina.value = 0b10100101
  dut.inb.value = 0b11111111
  await Timer(1, units='ns')
  assert dut.out.value == 0b01011010
