import unittest
from randomx.rx_vec_f128 import rx_vec_f128, rx_load_vec_f128, rx_set_vec_f128, rx_store_vec_f128 
import struct
from randomx.RegisterFile import RegisterFile

class TestRxVecF128(unittest.TestCase):

    def test_rx_load_vec_f128(self):
        test_bytes = struct.pack('<d', 1.23) + struct.pack('<d', 4.56)
        result = rx_load_vec_f128(test_bytes)

        # Check that the function correctly unpacks the bytes into the rx_vec_f128 object
        self.assertEqual(result.lo, 1.23)
        self.assertEqual(result.hi, 4.56)

    def test_rx_load_vec_f128_0x75(self):
        vec = rx_load_vec_f128(bytes([
            0x75,	0xcb,	0x65,	0x95,	0x7c,	0x04,	0xe0,	0x41,
            0xcb,	0x43,	0xc8,	0x60,	0xfe,	0x9c,	0xa4,	0x40
        ]))
        self.assertEqual(vec.lo, 2149835947.1810861)
        self.assertEqual(vec.hi, 2638.4968321402316)

    def test_rx_load_vec_f128_reg_a_0(self):
        reg = RegisterFile()
        reg.a[0].lo = 2149835947.1810861
        reg.a[0].hi = 2638.4968321402316
        vec = rx_load_vec_f128(struct.pack('<d', reg.a[0].lo) + struct.pack('<d', reg.a[0].hi))
        self.assertEqual(vec.lo, 2149835947.1810861)
        self.assertEqual(vec.hi, 2638.4968321402316)

    def test_rx_load_vec_f128_0x74(self):
        vec = rx_load_vec_f128(bytes([
            0x74,	0x8a,	0x97,	0x5e,	0x92,	0x02,	0x2c,	0x41,
            0xaa,	0x83,	0xfd,	0xbc,	0x04,	0x83,	0x2f,	0x40
        ]))
        self.assertEqual(vec.lo, 917833.1847499148)
        self.assertEqual(vec.hi, 15.755895524927684)

    def test_rx_load_vec_f128_0x7e(self):
        vec = rx_load_vec_f128(bytes([
            0x7e,	0x3e,	0xc2,	0x7d,	0x8c,	0x70,	0x8f,	0x40,
            0xd4,	0x6c,	0x97,	0x20,	0x50,	0x8c,	0xd2,	0x40
        ]))
        self.assertEqual(vec.lo, 1006.0685992408105)
        self.assertEqual(vec.hi, 18993.25198922756)

    def test_rx_load_vec_f128_0xc9(self):
        vec = rx_load_vec_f128(bytes([
            0xc9,	0x7a,	0x2a,	0x3b,	0x90,	0x05,	0x96,	0x41,
            0x4b,	0x15,	0x65,	0x2c,	0x65,	0xe6,	0xd9,	0x41
        ]))
        self.assertEqual(vec.lo, 92365838.791484013)
        self.assertEqual(vec.hi, 1738118321.5794246)

    def test_rx_load_vec_f128_0xa1(self):
        vec = rx_load_vec_f128(bytes([
            0xa1,	0x2e,	0x95,	0xe5,	0x18,	0xf4,	0x69,	0x3f,
            0xaa,	0x88,	0x6b,	0xb0,	0xdf,	0x03,	0x3b,	0x0d
        ]))
        self.assertEqual(vec.lo, 0.0031681524530194492)
        self.assertEqual(vec.hi, 6.1820232163239664e-245)

    def test_rx_set_vec_f128(self):
        result = rx_set_vec_f128(953360005391419562, 4569451684712230561)
        self.assertEqual(result.lo, 0.0031681524530194492)
        self.assertEqual(result.hi, 6.1820232163239664e-245)

    def test_rx_store_vec_f128_953360005391419562(self):
        dst = bytearray(16)
        vec = rx_set_vec_f128(953360005391419562, 4569451684712230561)
        rx_store_vec_f128(dst, 0, vec)
        expected = bytearray([
            0xa1,	0x2e,	0x95,	0xe5,	0x18,	0xf4,	0x69,	0x3f,
            0xaa,	0x88,	0x6b,	0xb0,	0xdf,	0x03,	0x3b,	0x0d
        ])
        self.assertEqual(dst.hex(), expected.hex())

