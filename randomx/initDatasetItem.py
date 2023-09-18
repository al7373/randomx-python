from .const import superscalarMul0, superscalarAdd1, superscalarAdd2, superscalarAdd3, superscalarAdd4, superscalarAdd5, superscalarAdd6, superscalarAdd7, CacheLineSize
from .configuration import RANDOMX_CACHE_ACCESSES
from .getMixBlock import getMixBlock
from superscalar.SuperscalarProgram import SuperscalarProgram
from superscalar.executeSuperscalar import executeSuperscalar
from blake2b.load64 import load64
from .RandomxCache import RandomxCache 
from typing import List

def initDatasetItem(cache: RandomxCache, out: List[int], item_number: int):
    rl = [0] * 8
    register_value = item_number
    rl[0] = ((item_number + 1) * superscalarMul0) & 0xFFFFFFFFFFFFFFFF
    rl[1] = (rl[0] ^ superscalarAdd1) & 0xFFFFFFFFFFFFFFFF
    rl[2] = (rl[0] ^ superscalarAdd2) & 0xFFFFFFFFFFFFFFFF
    rl[3] = (rl[0] ^ superscalarAdd3) & 0xFFFFFFFFFFFFFFFF
    rl[4] = (rl[0] ^ superscalarAdd4) & 0xFFFFFFFFFFFFFFFF
    rl[5] = (rl[0] ^ superscalarAdd5) & 0xFFFFFFFFFFFFFFFF
    rl[6] = (rl[0] ^ superscalarAdd6) & 0xFFFFFFFFFFFFFFFF
    rl[7] = (rl[0] ^ superscalarAdd7) & 0xFFFFFFFFFFFFFFFF


    for i in range(RANDOMX_CACHE_ACCESSES):
        mix_block = getMixBlock(register_value, cache.memory)
        prog = cache.programs[i]

        executeSuperscalar(
            rl, 
            prog, 
            cache.reciprocalCache
        )

        for q in range(8):
            rl[q] ^= load64(mix_block[8 * q: 8 * (q + 1)])

        register_value = rl[prog.getAddressRegister()]

    # out[:CacheLineSize] = b''.join([r.to_bytes(8, 'little') for r in rl])
    for i in range(len(rl)):
        out[i] = rl[i]



