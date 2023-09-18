import unittest
from blake2b.blake2b import blake2b
from blake2b.const import BLAKE2B_OUTBYTES


class TestBlake2b(unittest.TestCase):

    def test_blake2b_empty_input(self):
        out = bytearray(BLAKE2B_OUTBYTES)
        in_data = b''
        expected_out = bytearray.fromhex('786a02f742015903c6c6fd852552d272912f4740e15847618a86e217f71f5419d25e1031afee585313896444934eb04b903a685b1448b755d56f701afe9be2ce')

        result = blake2b(out, BLAKE2B_OUTBYTES, in_data, 0)

        self.assertEqual(result, 0)
        self.assertEqual(out, expected_out)

    def test_blake2b_basic(self):
        out = bytearray(BLAKE2B_OUTBYTES)
        in_data = b'This is a test message.'
        expected_out = bytearray.fromhex('2ed5ebbd434e6ddbf05ecdd9bddc9737897bc413fb7b771634a39c6db9b78c3a89e973e63c51d2d9d944c986f6cb7e995af44bfb4d19325e28b93b737ce03e20')

        result = blake2b(out, 64, in_data, len(in_data))

        self.assertEqual(result, 0)
        self.assertEqual(out, expected_out)

    def test_blake2b_keyed(self):
        out = bytearray(BLAKE2B_OUTBYTES)
        in_data = b'This is a test message.'
        key = b'This is a test key.'
        expected_out = bytearray.fromhex('47fd77149f0d11b45eb3acb26b7ed5b1e8d3f422c16ed024ed4cf9e4830bb79aa4605d6fdccecd9052799127c2d344b7093ebace2ceeebc597135d6024dcf313')

        result = blake2b(out, BLAKE2B_OUTBYTES, in_data, len(in_data), key, len(key))

        self.assertEqual(result, 0)
        self.assertEqual(out, expected_out)
