import cocotb
from cocotb.triggers import Timer


@cocotb.test()
async def testbench(dut):
  await Timer(1, units='ns')
  assert dut.out.value == 0b10101110
