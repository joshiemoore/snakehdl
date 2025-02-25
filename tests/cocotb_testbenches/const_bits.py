import cocotb
from cocotb.triggers import Timer


@cocotb.test()
async def testbench(dut):
  await Timer(1, units='ns')
  assert dut.out0.value == 0xdead
  assert dut.out1.value == 0xbeef
