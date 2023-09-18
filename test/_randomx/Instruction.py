import unittest
from randomx.Instruction import Instruction

class TestInstruction(unittest.TestCase):

    def test_imm32(self):
        instruction = Instruction()
        val = 12345
        instruction.setImm32(val)
        self.assertEqual(instruction.getImm32(), val)

    def test_mod_mem(self):
        instruction = Instruction()
        val = 3
        instruction.setMod(val)
        self.assertEqual(instruction.getModMem(), val % 4)

    def test_mod_shift(self):
        instruction = Instruction()
        val = 12
        instruction.setMod(val)
        self.assertEqual(instruction.getModShift(), (val >> 2) % 4)

    def test_mod_cond(self):
        instruction = Instruction()
        val = 48
        instruction.setMod(val)
        self.assertEqual(instruction.getModCond(), val >> 4)

