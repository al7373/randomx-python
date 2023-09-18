"""
runTest("AesGenerator1R", true, []() {
		char state[64] = { 0 };
		hex2bin("6c19536eb2de31b6c0065f7f116e86f960d8af0c57210a6584c3237b9d064dc7", 64, state);
		fillAes1Rx4<true>(state, sizeof(state), state);
		assert(equalsHex(state, "fa89397dd6ca422513aeadba3f124b5540324c4ad4b6db434394307a17c833ab"));
	});
"""
import unittest
from randomx.fillAes1Rx4 import fillAes1Rx4

class TestFillAes1Rx4(unittest.TestCase):
    def test_fillAes1Rx4(self):
        state = bytearray(64)
        state_hex_string = '6c19536eb2de31b6c0065f7f116e86f960d8af0c57210a6584c3237b9d064dc7'
        state[:len(state_hex_string)//2] = bytearray.fromhex(state_hex_string)

        fillAes1Rx4(state, len(state), state)

        # Convert the state back to a hex string for comparison
        state_hex = state.hex()
        expected_hex = "fa89397dd6ca422513aeadba3f124b5540324c4ad4b6db434394307a17c833aba330406d942cc6cd1d2b92a617b1726c56e28c091f52d9d2eb2f527537f2752a"

        self.assertEqual(state_hex, expected_hex)

