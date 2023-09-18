from .const import CacheSize, CacheLineSize
from argon2.Block import Block
from argon2.const import ARGON2_BLOCK_SIZE 
from typing import List

def getMixBlock(registerValue: int, memory: List[Block]) -> bytearray:
    mask = CacheSize // CacheLineSize - 1
    offset = (registerValue & mask) * CacheLineSize
    i = offset // ARGON2_BLOCK_SIZE 
    j = offset % ARGON2_BLOCK_SIZE 
    k = j // 8
    r = bytearray()
    for l in range(8):
        r.extend(memory[i].v[k + l].to_bytes(8, 'little'))
    return r

