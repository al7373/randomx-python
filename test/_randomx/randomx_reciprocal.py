import unittest
from randomx.randomx_reciprocal import randomx_reciprocal
import os
import json

class TestRandomxReciprocal(unittest.TestCase):
    def test_basic_cases(self):
        self.assertEqual(randomx_reciprocal(1), 0)
        self.assertEqual(randomx_reciprocal(2), 0)
        self.assertEqual(randomx_reciprocal(4), 0)

    def test_non_power_of_two_cases(self):
        self.assertEqual(randomx_reciprocal(3), 12297829382473034410)
        self.assertEqual(randomx_reciprocal(5), 14757395258967641292)
        self.assertEqual(randomx_reciprocal(6), 12297829382473034410)

    def test_large_divisor(self):
        self.assertEqual(randomx_reciprocal(1 << 62), 0)

    def test_some_cases(self):
        test_cases = [
            (3515202012, 11269361226438717911),
            (3245996972, 12203979732218976572),
            (3491616210, 11345485550123554042),
            (630988878, 15695237522527365687)
        ]

        for divisor, expected_result in test_cases:
            with self.subTest(divisor=divisor):
                actual_result = randomx_reciprocal(divisor)
                self.assertEqual(actual_result, expected_result, f"Failed for divisor: {divisor}")

    def test_divisor_zero(self):
        with self.assertRaises(AssertionError):
            randomx_reciprocal(0)

    def test_divisor_quotient(self):
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'divisor_quotient.json'), 'r') as f:
            divisor_quotient = json.load(f)
        for d_q in divisor_quotient:
            divisor = d_q["divisor"]
            expected = d_q["quotient"]
            quotient = randomx_reciprocal(divisor)
            self.assertEqual(quotient, expected)


