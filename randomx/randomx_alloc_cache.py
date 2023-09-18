from argon2.randomx_argon2_fill_segment import randomx_argon2_fill_segment 
from .configuration import RANDOMX_ARGON_LANES, RANDOMX_ARGON_MEMORY
from argon2.const import ARGON2_QWORDS_IN_BLOCK 
from argon2.Block import Block
from .RandomxCache import RandomxCache

def randomx_alloc_cache():
    cache = RandomxCache()

    cache.memory = [Block([0] * ARGON2_QWORDS_IN_BLOCK) for _ in range(RANDOMX_ARGON_MEMORY * RANDOMX_ARGON_LANES)]
    cache.argonImpl = randomx_argon2_fill_segment 

    return cache
