from .Blake2bState import Blake2bState
from .const import blake2b_IV, BLAKE2B_BLOCKBYTES

def blake2b_init0(S: Blake2bState):
    S.h = blake2b_IV.copy()
    S.t = [0, 0]
    S.f = [0, 0]
    S.buflen = 0
    S.buf = bytearray(BLAKE2B_BLOCKBYTES)

