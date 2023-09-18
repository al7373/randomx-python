import unittest
from randomx.RegisterFile import RegisterFile
import struct

class TestRegisterFile(unittest.TestCase):

    def test_RegisterFile(self):
        reg = RegisterFile()

        reg.a[0].lo = struct.unpack('<d', struct.pack('<Q', 4746798940377434997))[0]
        self.assertEqual(reg.a[0].lo, 2149835947.1810861)

        reg.a[0].hi = struct.unpack('<d', struct.pack('<Q', 4658020530967299019))[0]
        self.assertEqual(reg.a[0].hi, 2638.4968321402316)
        
        reg.a[1].lo = struct.unpack('<d', struct.pack('<Q', 4696131339116055156))[0]
        self.assertEqual(reg.a[1].lo, 917833.1847499148)

        reg.a[1].hi = struct.unpack('<d', struct.pack('<Q', 4625059398706627498))[0]
        self.assertEqual(reg.a[1].hi, 15.755895524927684)

        reg.a[2].lo = struct.unpack('<d', struct.pack('<Q', 4652060688804626046))[0]
        self.assertEqual(reg.a[2].lo, 1006.0685992408105)

        reg.a[2].hi = struct.unpack('<d', struct.pack('<Q', 4670950039308692692))[0]
        self.assertEqual(reg.a[2].hi, 18993.25198922756)

        reg.a[3].lo = struct.unpack('<d', struct.pack('<Q', 4725970975997983433))[0]
        self.assertEqual(reg.a[3].lo, 92365838.791484013)

        reg.a[3].hi = struct.unpack('<d', struct.pack('<Q', 4745077004622435659))[0]
        self.assertEqual(reg.a[3].hi, 1738118321.5794246)

    def test_to_bytes(self):
        reg = RegisterFile()

        reg.r[:] = [
            15970445789787658950, 
            387315867719836589, 
            7767175896920704527, 
            7830140613705146425, 
            12320995378444337624, 
            17847759843158513508,
            17574223984151438125, 
            1053521245896736675
        ]

        reg.f[0].lo = 1.3954059160026739e-276
        reg.f[0].hi = 6.5288003821403134e-286 
        reg.f[1].lo = 4.7721398494389051e-306
        reg.f[1].hi = -1.4317116503916547e-275
        reg.f[2].lo = -1.0325317109785627e-265
        reg.f[2].hi = 6.4134350076402885e-236 
        reg.f[3].lo = 3.3992630577371405e-215
        reg.f[3].hi = 9.457570368990943e-229

        reg.e[0].lo = 1.3549013227859855e+35 
        reg.e[0].hi = 5.2687509235988228e+24
        reg.e[1].lo = 26616207.636194989 
        reg.e[1].hi = 6.9192523426632858e+35
        reg.e[2].lo = 2.4979073579527272e+44 
        reg.e[2].hi = 2.6611706743296336e+71
        reg.e[3].lo = 1.4807679379738859e+91 
        reg.e[3].hi = 2.7259528520774899e+83

        reg.a[0].lo = -7.1341064835401954e+26 
        reg.a[0].hi = -1.1277523294621121e+68
        reg.a[1].lo = 3.2640737338707528e-43 
        reg.a[1].hi = -2.4732742482529698e-249
        reg.a[2].lo = -1.1687149635454896e-68 
        reg.a[2].hi = -6.0122178224846464e+23
        reg.a[3].lo = 6.429726185560622e+34 
        reg.a[3].hi = 6.234337957418377e-201

        expected = bytearray([
            0xc6,	0x1a,	0xed,	0xac,	0xd4,	0x6b,	0xa2,	0xdd,
            0xad,	0x23,	0x50,	0xc7,	0xba,	0x05,	0x60,	0x05,
            0x0f,	0x46,	0xef,	0x73,	0x53,	0x8d,	0xca,	0x6b,
            0x39,	0x20,	0x41,	0xfd,	0x66,	0x3f,	0xaa,	0x6c,
            0xd8,	0x81,	0x67,	0x6b,	0x04,	0xf8,	0xfc,	0xaa,
            0x64,	0xd7,	0xf1,	0x0f,	0x04,	0xfb,	0xaf,	0xf7,
            0x2d,	0x23,	0x7f,	0xf2,	0x99,	0x2f,	0xe4,	0xf3,
            0xa3,	0x7f,	0x00,	0xc9,	0xfd,	0xdb,	0x9e,	0x0e,
            0x9e,	0xd6,	0x41,	0xa6,	0x5f,	0xbc,	0xa8,	0x06,
            0x51,	0xf6,	0x37,	0x5f,	0x85,	0xda,	0xb8,	0x04,
            0xbb,	0x74,	0x49,	0x0e,	0x13,	0xcf,	0x8a,	0x00,
            0x06,	0x9c,	0x0c,	0x7a,	0x69,	0xb9,	0xdf,	0x86,
            0xe7,	0x56,	0x58,	0xbd,	0x82,	0xa2,	0xea,	0x88,
            0x0e,	0xcd,	0x7a,	0x16,	0x03,	0x1a,	0x1a,	0x0f,
            0x5d,	0x6f,	0xa5,	0x9c,	0xba,	0x6f,	0x67,	0x13,
            0x62,	0x23,	0x83,	0x3a,	0x38,	0xf1,	0x96,	0x10,
            0x16,	0x1a,	0xf5,	0xe4,	0x2d,	0x18,	0x3a,	0x47,
            0x68,	0xd9,	0x51,	0x3d,	0xce,	0x6e,	0x11,	0x45,
            0xcc,	0xda,	0x2d,	0xfa,	0x18,	0x62,	0x79,	0x41,
            0x34,	0x2a,	0x86,	0x88,	0x51,	0xa8,	0x60,	0x47,
            0x2e,	0xba,	0x7b,	0xfe,	0xe9,	0x66,	0x26,	0x49,
            0x2a,	0xbf,	0x30,	0x52,	0x6a,	0x47,	0xc3,	0x4e,
            0x49,	0xe1,	0x30,	0x8f,	0xb0,	0x13,	0xdd,	0x52,
            0xe8,	0xd4,	0x49,	0x6a,	0x01,	0xf6,	0x41,	0x51,
            0x13,	0x8a,	0xed,	0xa5,	0xf4,	0x70,	0x82,	0xc5,
            0x29,	0x13,	0x09,	0x9f,	0x75,	0xbb,	0x10,	0xce,
            0x2a,	0x5c,	0x7f,	0xa4,	0xd3,	0x1d,	0x1d,	0x37,
            0x7e,	0xf8,	0xa7,	0x40,	0x3d,	0xb5,	0x51,	0x8c,
            0x76,	0x2e,	0x61,	0xfc,	0x59,	0x2a,	0xd4,	0xb1,
            0x2b,	0x5d,	0x72,	0x14,	0x13,	0xd4,	0xdf,	0xc4,
            0xd2,	0x67,	0xfe,	0x13,	0x33,	0xc4,	0x28,	0x47,
            0x03,	0xcf,	0x40,	0x41,	0x92,	0x8a,	0x5e,	0x16
        ])

        self.assertEqual(reg.to_bytes().hex(), expected.hex())
