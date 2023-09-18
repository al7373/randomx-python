import unittest
from randomx.configuration import RANDOMX_ARGON_ITERATIONS, RANDOMX_ARGON_LANES, RANDOMX_ARGON_MEMORY, RANDOMX_ARGON_SALT
from randomx.initCache import initCache
from randomx.randomx_alloc_cache import randomx_alloc_cache
import json
import os

"""
runTest("Cache initialization", RANDOMX_ARGON_ITERATIONS == 3 && RANDOMX_ARGON_LANES == 1 && RANDOMX_ARGON_MEMORY == 262144 && stringsEqual(RANDOMX_ARGON_SALT, "RandomX\x03"),	[]() {
		initCache("test key 000");
		uint64_t* cacheMemory = (uint64_t*)cache->memory;
		assert(cacheMemory[0] == 0x191e0e1d23c02186);
		assert(cacheMemory[1568413] == 0xf1b62fe6210bf8b1);
		assert(cacheMemory[33554431] == 0x1f47f056d05cd99b);
	});
"""

class TestInitCache(unittest.TestCase):

    def test_initCache(self):
        self.assertEqual(RANDOMX_ARGON_ITERATIONS, 3)
        self.assertEqual(RANDOMX_ARGON_LANES, 1)
        self.assertEqual(RANDOMX_ARGON_MEMORY, 262144)
        self.assertEqual(RANDOMX_ARGON_SALT, "RandomX\x03")

        cache = randomx_alloc_cache()

        key = "test key 000"

        initCache(cache, key, len(key))

        cacheMemory = cache.memory

        self.assertEqual(cacheMemory[0].v[0], 0x191e0e1d23c02186)
        # (1568413, 0xf1b62fe6210bf8b1)
        self.assertEqual(cacheMemory[12253].v[29], 0xf1b62fe6210bf8b1)
        # (33554431, 0x1f47f056d05cd99b)
        self.assertEqual(cacheMemory[262143].v[127], 0x1f47f056d05cd99b)

        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'reciprocals.json'), 'r') as f:
            reciprocals = json.load(f)

        self.assertEqual(cache.reciprocalCache, reciprocals)


