import unittest
from randomx.fillAes4Rx4 import fillAes4Rx4
import os

class TestFillAes4Rx4(unittest.TestCase):
    def test_fillAes4Rx4(self):
        program = bytearray(2176)
        seed = bytearray([
            0x84,	0x90,	0x6b,	0x48,	0xbd,	0x9f,	0x8c,	0xbf,
            0x62,	0xf5,	0xa0,	0x8a,	0xbc,	0xc4,	0x65,	0x82,
            0x76,	0x8c,	0x31,	0xde,	0x46,	0x1c,	0x9f,	0x08,
            0x93,	0x76,	0x0e,	0x8f,	0x71,	0xda,	0xf4,	0x5f,
            0xaa,	0x91,	0x45,	0x82,	0x96,	0x59,	0x6b,	0xfe,
            0x48,	0xef,	0x62,	0x6d,	0x20,	0xb0,	0x18,	0xac,
            0x95,	0xe7,	0x5e,	0xde,	0xdd,	0xba,	0xec,	0x29,
            0xcf,	0xdf,	0x56,	0x4b,	0x6e,	0x3d,	0xba,	0x58
        ])
        fillAes4Rx4(seed, len(program), program)
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'program_dump.bin'), 'rb') as f:
            expected = f.read()
        self.assertEqual(program, expected)

