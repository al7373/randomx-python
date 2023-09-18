import unittest
from superscalar.MacroOp import MacroOp 
from superscalar.ExecutionPort import ExecutionPort

class TestMacroOp(unittest.TestCase):

    def test_getName(self):
        macro_op = MacroOp("add r,r", 3, 1, ExecutionPort.P015)
        self.assertEqual(macro_op.getName(), "add r,r")

    def test_getSize(self):
        macro_op = MacroOp("add r,r", 3, 1, ExecutionPort.P015)
        self.assertEqual(macro_op.getSize(), 3)

    def test_getLatency(self):
        macro_op = MacroOp("add r,r", 3, 1, ExecutionPort.P015)
        self.assertEqual(macro_op.getLatency(), 1)

    def test_getUop1(self):
        macro_op = MacroOp("add r,r", 3, 1, ExecutionPort.P015)
        self.assertEqual(macro_op.getUop1(), ExecutionPort.P015)

    def test_getUop2(self):
        macro_op = MacroOp("imul r", 3, 4, ExecutionPort.P1, ExecutionPort.P5)
        self.assertEqual(macro_op.getUop2(), ExecutionPort.P5)

    def test_isSimple(self):
        macro_op = MacroOp("add r,r", 3, 1, ExecutionPort.P015)
        self.assertTrue(macro_op.isSimple())

    def test_isEliminated(self):
        macro_op = MacroOp("xor rcx,rcx", 3)
        self.assertTrue(macro_op.isEliminated())

    def test_isDependent(self):
        macro_op = MacroOp("imul r,r", 4, 3, ExecutionPort.P1, dependent=True)
        self.assertTrue(macro_op.isDependent())

