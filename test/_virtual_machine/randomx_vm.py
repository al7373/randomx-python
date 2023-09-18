import unittest
from virtual_machine.randomx_vm import randomx_vm
from blake2b.blake2b import blake2b
import os

class TestRandomXVM(unittest.TestCase):

    def test_initScratchpad(self):
        machine = randomx_vm()
        tempHash = bytearray(64)
        """
        l'initialisation ci-dessous de in_data n'a pas marché à cause du 0 à la fin des chaînes
        de caractères en C
        """
        # in_data = b'RandomX example input'
        in_data = bytes([
            0x52,	0x61,	0x6e,	0x64,	0x6f,	0x6d,	0x58,	0x20,
            0x65,	0x78,	0x61,	0x6d,	0x70,	0x6c,	0x65,	0x20,
            0x69,	0x6e,	0x70,	0x75,	0x74,	0x00
        ])
        blakeResult = blake2b(tempHash, len(tempHash), in_data, len(in_data), None, 0)
        self.assertEqual(blakeResult, 0)
        machine.initScratchpad(tempHash)
        # Charger le contenu de scratchpad_dump.bin
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'scratchpad_dump.bin'), 'rb') as f:
            expected = f.read()
        self.assertEqual(machine.getScratchpad(), expected)

    def test_initialize(self):
        machine = randomx_vm()
        tempHash = bytearray(64)
        in_data = bytes([
            0x52,	0x61,	0x6e,	0x64,	0x6f,	0x6d,	0x58,	0x20,
            0x65,	0x78,	0x61,	0x6d,	0x70,	0x6c,	0x65,	0x20,
            0x69,	0x6e,	0x70,	0x75,	0x74,	0x00
        ])
        blakeResult = blake2b(tempHash, len(tempHash), in_data, len(in_data), None, 0)
        machine.initScratchpad(tempHash)
        machine.generateProgram(tempHash)
        machine.initialize()

        self.assertEqual(machine.reg.a[0].lo, 2149835947.1810861)
        self.assertEqual(machine.reg.a[0].hi, 2638.4968321402316)
        self.assertEqual(machine.reg.a[1].lo, 917833.1847499148)
        self.assertEqual(machine.reg.a[1].hi, 15.755895524927684)
        self.assertEqual(machine.reg.a[2].lo, 1006.0685992408105)
        self.assertEqual(machine.reg.a[2].hi, 18993.25198922756)
        self.assertEqual(machine.reg.a[3].lo, 92365838.791484013)
        self.assertEqual(machine.reg.a[3].hi, 1738118321.5794246)

        self.assertEqual(machine.mem.ma, 1215362368)
        self.assertEqual(machine.mem.mx, 1860707480)

        self.assertEqual(machine.config.readReg0, 0)
        self.assertEqual(machine.config.readReg1, 3)
        self.assertEqual(machine.config.readReg2, 4)
        self.assertEqual(machine.config.readReg3, 7)

        self.assertEqual(machine.datasetOffset, 5031744)

        self.assertEqual(machine.config.eMask[0], 4035225266128095857)
        self.assertEqual(machine.config.eMask[1], 4467570830353087134)


