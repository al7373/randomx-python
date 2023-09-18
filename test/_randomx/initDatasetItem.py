import unittest
from randomx.configuration import RANDOMX_ARGON_ITERATIONS, RANDOMX_ARGON_LANES, RANDOMX_ARGON_MEMORY, RANDOMX_ARGON_SALT
from randomx.initCache import initCache
from randomx.randomx_alloc_cache import randomx_alloc_cache
from randomx.initDatasetItem import initDatasetItem

class TestInitDatasetItem(unittest.TestCase):

    def test_initDatasetItem(self):
        self.assertEqual(RANDOMX_ARGON_ITERATIONS, 3)
        self.assertEqual(RANDOMX_ARGON_LANES, 1)
        self.assertEqual(RANDOMX_ARGON_MEMORY, 262144)
        self.assertEqual(RANDOMX_ARGON_SALT, "RandomX\x03")

        cache = randomx_alloc_cache()

        key = "test key 000"

        initCache(cache, key, len(key))

        out = [0] * 8

        initDatasetItem(cache, out, 0)

        self.assertEqual(out[0], 0x680588a85ae222db)

        initDatasetItem(cache, out, 10000000)

        self.assertEqual(out[0], 0x7943a1f6186ffb72)

        initDatasetItem(cache, out, 20000000)

        self.assertEqual(out[0], 0x9035244d718095e1)

        initDatasetItem(cache, out, 30000000)

        self.assertEqual(out[0], 0x145a5091f7853099)



