import unittest
from randomx.rx_vec_i128 import rx_vec_i128, rx_set_int_vec_i128, rx_load_vec_i128, rx_vec_i128_x, rx_vec_i128_y, rx_vec_i128_z, rx_vec_i128_w, rx_xor_vec_i128, rx_store_vec_i128
from randomx.const import AES_GEN_1R_KEY0, AES_GEN_1R_KEY1, AES_GEN_1R_KEY2, AES_GEN_1R_KEY3

class TestRxVecI128(unittest.TestCase):
    def test_init(self):
        vec = rx_vec_i128(1, 2, 3, 4)
        self.assertEqual(vec.u32(), (1, 2, 3, 4))

    def test_set_int(self):
        vec = rx_set_int_vec_i128(1, 2, 3, 4)
        self.assertEqual(vec.u32(), (1, 2, 3, 4))

    def test_load_vec_0x6c(self):
        vec = rx_load_vec_i128(bytearray([
            0x6c,	0x19,	0x53,	0x6e,	0xb2,	0xde,	0x31,	0xb6,
            0xc0,	0x06,	0x5f,	0x7f,	0x11,	0x6e,	0x86,	0xf9
        ]))
        self.assertEqual(vec.i64(), (-466564489955834176, -5318224827011360404))

    def test_load_vec_0x60(self):
        vec = rx_load_vec_i128(bytearray([
            0x60,	0xd8,	0xaf,	0x0c,	0x57,	0x21,	0x0a,	0x65,
            0x84,	0xc3,	0x23,	0x7b,	0x9d,	0x06,	0x4d,	0xc7
        ]))
        self.assertEqual(vec.i64(), (-4085602013509598332, 7280668405356550240))

    def test_rx_set_int_vec_i128_AES_GEN_1R_KEY0(self):
        vec = rx_set_int_vec_i128(*AES_GEN_1R_KEY0)
        self.assertEqual(vec.i64(), (-5407616885745953493, 7093563078766011731))

    def test_rx_set_int_vec_i128_AES_GEN_1R_KEY1(self):
        vec = rx_set_int_vec_i128(*AES_GEN_1R_KEY1)
        self.assertEqual(vec.i64(), (982308421697393528, -8905181010686333177))

    def test_rx_set_int_vec_i128_AES_GEN_1R_KEY2(self):
        vec = rx_set_int_vec_i128(*AES_GEN_1R_KEY2)
        self.assertEqual(vec.i64(), (4476827919204776271, -6947788935199038735))

    def test_rx_set_int_vec_i128_AES_GEN_1R_KEY3(self):
        vec = rx_set_int_vec_i128(*AES_GEN_1R_KEY3)
        self.assertEqual(vec.i64(), (5266556604591983752, -5640141172888338123))

    def test_rx_vec_i128_x(self):
        vec = rx_vec_i128(0xf9866e11, 0x7f5f06c0, 0xb631deb2, 0x6e53196c)
        expected = 0x6e53196c
        self.assertEqual(rx_vec_i128_x(vec), expected)

    def test_rx_vec_i128_y(self):
        vec = rx_vec_i128(0xf9866e11, 0x7f5f06c0, 0xb631deb2, 0x6e53196c)
        expected = 0xb631deb2
        self.assertEqual(rx_vec_i128_y(vec), expected)

    def test_rx_vec_i128_z(self):
        vec = rx_vec_i128(0xf9866e11, 0x7f5f06c0, 0xb631deb2, 0x6e53196c)
        expected = 0x7f5f06c0
        self.assertEqual(rx_vec_i128_z(vec), expected)

    def test_rx_vec_i128_w(self):
        vec = rx_vec_i128(0xf9866e11, 0x7f5f06c0, 0xb631deb2, 0x6e53196c)
        expected = 0xf9866e11
        self.assertEqual(rx_vec_i128_w(vec), expected)

    def test_rx_xor_vec_i128(self):
        a = rx_vec_i128(0xe1bf5b28, 0x6118fb38, 0x4733acdf, 0x10952ca9)
        b = rx_vec_i128(0xb4f44917, 0xdbb5552b , 0x62716609, 0x6daca553)
        expected = (0x554b123fbaadae13, 0x2542cad67d3989fa)
        xor_result = rx_xor_vec_i128(a, b)
        self.assertEqual(xor_result.i64(), expected)

    def test_rx_xor_vec_i128_0xa6921459(self):
        a = rx_vec_i128(0xa6921459, 0x6d15473b, 0xc7b1c7d9, 0x27309d47)
        b = rx_vec_i128(0x0da1dc4e, 0x1725d378, 0x846a710d, 0x6d7caf07)
        expected = (-6110320266251824061, 4889702843336634944)
        xor_result = rx_xor_vec_i128(a, b)
        self.assertEqual(xor_result.i64(), expected)

    def test_rx_store_vec_i128(self):
        dst = bytearray(16)
        vec = rx_vec_i128(0x554b123f, 0xbaadae13, 0x2542cad6, 0x7d3989fa)
        rx_store_vec_i128(dst, 0, vec)
        expected = bytearray([
            0xfa,	0x89,	0x39,	0x7d,	0xd6,	0xca,	0x42,	0x25,
            0x13,	0xae,	0xad,	0xba,	0x3f,	0x12,	0x4b,	0x55
        ])
        self.assertEqual(dst.hex(), expected.hex())



