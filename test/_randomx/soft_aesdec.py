import unittest
from randomx.rx_vec_i128 import rx_vec_i128
from randomx.soft_aesdec import soft_aesdec

class TestSoftAESDec(unittest.TestCase):

    def test_soft_aesdec_0xf9866e11(self):
        in_val = rx_vec_i128(0xf9866e11, 0x7f5f06c0, 0xb631deb2, 0x6e53196c)
        key = rx_vec_i128(0xb4f44917, 0xdbb5552b, 0x62716609, 0x6daca553)
        expected_output = rx_vec_i128(0x554b123f, 0xbaadae13, 0x2542cad6, 0x7d3989fa)

        output = soft_aesdec(in_val, key)

        self.assertEqual(output.u32(), expected_output.u32())

