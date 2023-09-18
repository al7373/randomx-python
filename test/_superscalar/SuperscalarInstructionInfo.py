import unittest
from superscalar.SuperscalarInstructionInfo import SuperscalarInstructionInfo 
from superscalar.SuperscalarInstructionType  import SuperscalarInstructionType 
from superscalar.MacroOp import MacroOp, IMUL_RCP_ops_array
from superscalar.ExecutionPort import ExecutionPort

class TestSuperscalarInstructionInfo(unittest.TestCase):
    def test_single_op(self):
        instr = SuperscalarInstructionInfo.single_op("ISUB_R", SuperscalarInstructionType.ISUB_R, MacroOp.Sub_rr, 0)
        self.assertEqual(instr.getName(), "ISUB_R")
        self.assertEqual(instr.getType(), SuperscalarInstructionType.ISUB_R)
        self.assertEqual(instr.getSize(), 1)
        self.assertTrue(instr.isSimple())
        self.assertEqual(instr.getLatency(), MacroOp.Sub_rr.getLatency())
        self.assertEqual(instr.getResultOp(), 0)
        self.assertEqual(instr.getDstOp(), 0)
        self.assertEqual(instr.getSrcOp(), 0)

    def test_multi_op(self):
        instr = SuperscalarInstructionInfo.multi_op("IMUL_RCP", SuperscalarInstructionType.IMUL_RCP, IMUL_RCP_ops_array, 1, 1, -1)
        self.assertEqual(instr.getName(), "IMUL_RCP")
        self.assertEqual(instr.getType(), SuperscalarInstructionType.IMUL_RCP)
        self.assertEqual(instr.getSize(), 2)
        self.assertFalse(instr.isSimple())
        latency = MacroOp.Mov_ri64.getLatency() + MacroOp("imul r,r", 4, 3, ExecutionPort.P1, dependent=True).getLatency()
        self.assertEqual(instr.getLatency(), latency)
        self.assertEqual(instr.getResultOp(), 1)
        self.assertEqual(instr.getDstOp(), 1)
        self.assertEqual(instr.getSrcOp(), -1)

    def test_nop(self):
        NOP = SuperscalarInstructionInfo("NOP")
        self.assertEqual(NOP.getName(), "NOP")
        self.assertEqual(NOP.getSize(), 0)
        self.assertEqual(NOP.getType(), SuperscalarInstructionType.INVALID)
        self.assertEqual(NOP.getLatency(), 0)

