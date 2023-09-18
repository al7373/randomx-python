import unittest
from blake2b.Blake2Generator import Blake2Generator

class TestBlake2Generator(unittest.TestCase):

    def test_blake2_generator(self):
        seed = b'This is a test seed for Blake2Generator.'
        seed_size = len(seed)
        nonce = 42

        blake_gen = Blake2Generator(seed, seed_size, nonce)

        # Test get_byte
        expected_byte_sequence = [14, 155, 34, 33, 220, 109, 169, 235, 10, 8]
        for expected_byte in expected_byte_sequence:
            self.assertEqual(blake_gen.get_byte(), expected_byte)

        # Test get_uint32
        expected_uint32_sequence = [2144065571, 3357413368, 3515593017, 2918571204, 325010461]
        for expected_uint32 in expected_uint32_sequence:
            self.assertEqual(blake_gen.get_uint32(), expected_uint32)

