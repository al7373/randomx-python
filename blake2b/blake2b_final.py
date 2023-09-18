from .Blake2bState import Blake2bState
from .const import BLAKE2B_OUTBYTES, BLAKE2B_BLOCKBYTES
from .blake2b_increment_counter import blake2b_increment_counter 
from .blake2b_compress import blake2b_compress
from .blake2b_set_lastblock import blake2b_set_lastblock 
from .store64 import store64 

def blake2b_final(S: Blake2bState, out: bytearray, outlen: int) -> int:
    buffer = bytearray(BLAKE2B_OUTBYTES)

    # Sanity checks
    if S is None or out is None or outlen < S.outlen:
        return -1

    # Is this a reused state?
    if S.f[0] != 0:
        return -1

    blake2b_increment_counter(S, S.buflen)
    blake2b_set_lastblock(S)
    S.buf[S.buflen:] = bytearray(BLAKE2B_BLOCKBYTES - S.buflen)
    blake2b_compress(S, S.buf)

    for i in range(8):
        store64(buffer, i * 8, S.h[i])

    out[:S.outlen] = buffer[:S.outlen]
    return 0

