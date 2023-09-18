import unittest
from randomx.rx_vec_i128 import rx_vec_i128
from randomx.soft_aesenc import soft_aesenc

class TestSoftAESEnc(unittest.TestCase):

    def test_soft_aesenc(self):
        in_val = rx_vec_i128(0xc74d069d, 0x7b23c384, 0x650a2157, 0x0cafd860)
        key = rx_vec_i128(0x0da1dc4e, 0x1725d378, 0x846a710d, 0x6d7caf07)
        expected_output = rx_vec_i128(0xab33c817, 0x7a309443, 0x43dbb6d4, 0x4a4c3240)

        output = soft_aesenc(in_val, key)

        self.assertEqual(output.u32(), expected_output.u32())

