import unittest
from typing import List
from superscalar.scheduleUop import scheduleUop
from superscalar.ExecutionPort import ExecutionPort 
from randomx.const import CYCLE_MAP_SIZE


class TestScheduleUop(unittest.TestCase):

    def setUp(self):
        self.portBusy: List[List[ExecutionPort]] = [[ExecutionPort.Null for _ in range(3)] for _ in range(CYCLE_MAP_SIZE)]

    def test_scheduleUop(self):
        # Test pour le port P5
        cycle_assigned = scheduleUop(True, ExecutionPort.P5, self.portBusy, 0)
        self.assertEqual(cycle_assigned, 0)
        self.assertEqual(self.portBusy[0][2], ExecutionPort.P5)

        # Test pour le port P0
        cycle_assigned = scheduleUop(True, ExecutionPort.P0, self.portBusy, 0)
        self.assertEqual(cycle_assigned, 0)
        self.assertEqual(self.portBusy[0][0], ExecutionPort.P0)

        # Test pour le port P1
        cycle_assigned = scheduleUop(True, ExecutionPort.P1, self.portBusy, 0)
        self.assertEqual(cycle_assigned, 0)
        self.assertEqual(self.portBusy[0][1], ExecutionPort.P1)

        # Test avec un port déjà occupé
        cycle_assigned = scheduleUop(True, ExecutionPort.P5, self.portBusy, 0)
        self.assertEqual(cycle_assigned, 1)
        self.assertEqual(self.portBusy[1][2], ExecutionPort.P5)

        # Test avec un port invalide
        cycle_assigned = scheduleUop(True, ExecutionPort.Null, self.portBusy, 0)
        self.assertEqual(cycle_assigned, -1)

        # Test avec un cycle hors limites
        cycle_assigned = scheduleUop(True, ExecutionPort.P0, self.portBusy, CYCLE_MAP_SIZE)
        self.assertEqual(cycle_assigned, -1)

