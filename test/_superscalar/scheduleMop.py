import unittest
from superscalar.MacroOp import MacroOp
from superscalar.ExecutionPort import ExecutionPort
from superscalar.scheduleUop import scheduleUop
from superscalar.scheduleMop import scheduleMop
from randomx.const import CYCLE_MAP_SIZE

class TestScheduleMop(unittest.TestCase):
    def setUp(self):
        self.portBusy = [[ExecutionPort.Null for _ in range(3)] for _ in range(CYCLE_MAP_SIZE)]

    def test_scheduleMop(self):
        cycle = 0
        depCycle = 0
        commit = False

        result = scheduleMop(commit, MacroOp.Add_rr, self.portBusy, cycle, depCycle)
        self.assertEqual(result, 0, "Expected cycle 0 for Add_rr")

        result = scheduleMop(commit, MacroOp.Mov_rr, self.portBusy, cycle, depCycle)
        self.assertEqual(result, 0, "Expected cycle 0 for Mov_rr (eliminated)")

        result = scheduleMop(commit, MacroOp.Lea_sib, self.portBusy, cycle, depCycle)
        self.assertEqual(result, 0, "Expected cycle 0 for Lea_sib")

        result = scheduleMop(commit, MacroOp.Imul_rr, self.portBusy, cycle, depCycle)
        self.assertEqual(result, 0, "Expected cycle 0 for Imul_rr")

        commit = True
        scheduleMop(commit, MacroOp.Add_rr, self.portBusy, cycle, depCycle)

        result = scheduleMop(commit, MacroOp.Lea_sib, self.portBusy, cycle + 1, depCycle)
        self.assertEqual(result, 1, "Expected cycle 1 for Lea_sib after Add_rr")

        result = scheduleMop(commit, MacroOp.Ror_rcl, self.portBusy, cycle, depCycle)
        self.assertEqual(result, 2, "Expected cycle 2 for Ror_rcl")

