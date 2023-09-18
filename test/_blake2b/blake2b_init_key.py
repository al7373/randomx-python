import unittest
from blake2b.Blake2bParam import Blake2bParam
from blake2b.Blake2bState import Blake2bState
from blake2b.blake2b_init_key import blake2b_init_key
from blake2b.const import BLAKE2B_OUTBYTES, BLAKE2B_KEYBYTES

class TestBlake2bInitKey(unittest.TestCase):

    def test_init_key_valid(self):
        S = Blake2bState()
        outlen = 32
        key = b"test_key"
        keylen = len(key)

        result = blake2b_init_key(S, outlen, key, keylen)
        self.assertEqual(result, 0)

    def test_init_key_invalid_outlen(self):
        S = Blake2bState()
        outlen = 0
        key = b"test_key"
        keylen = len(key)

        result = blake2b_init_key(S, outlen, key, keylen)
        self.assertEqual(result, -1)

    def test_init_key_invalid_keylen(self):
        S = Blake2bState()
        outlen = 32
        key = b"test_key"
        keylen = BLAKE2B_KEYBYTES + 1

        result = blake2b_init_key(S, outlen, key, keylen)
        self.assertEqual(result, -1)

    def test_init_key_none_state(self):
        S = None
        outlen = 32
        key = b"test_key"
        keylen = len(key)

        result = blake2b_init_key(S, outlen, key, keylen)
        self.assertEqual(result, -1)

    def test_init_key_none_key(self):
        S = Blake2bState()
        outlen = 32
        key = None
        keylen = 0

        result = blake2b_init_key(S, outlen, key, keylen)
        self.assertEqual(result, -1)

    def test_init_key_max_keylen(self):
        S = Blake2bState()
        outlen = 32
        key = b'a' * BLAKE2B_KEYBYTES
        keylen = len(key)

        result = blake2b_init_key(S, outlen, key, keylen)
        self.assertEqual(result, 0)

