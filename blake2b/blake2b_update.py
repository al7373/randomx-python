from .Blake2bState import Blake2bState
from .const import BLAKE2B_BLOCKBYTES
from .blake2b_increment_counter import blake2b_increment_counter 
from .blake2b_compress import blake2b_compress

def blake2b_update(S: Blake2bState, in_data: bytes, inlen: int) -> int:
    if inlen == 0:
        return 0

    # Sanity check
    if S is None or in_data is None:
        return -1

    # Is this a reused state?
    if S.f[0] != 0:
        return -1

    if S.buflen + inlen > BLAKE2B_BLOCKBYTES:
        # Complete current block
        left = S.buflen
        fill = BLAKE2B_BLOCKBYTES - left
        S.buf[left:] = in_data[:fill]
        blake2b_increment_counter(S, BLAKE2B_BLOCKBYTES)
        blake2b_compress(S, S.buf)
        S.buflen = 0
        inlen -= fill
        in_data = in_data[fill:]

        # Avoid buffer copies when possible
        while inlen > BLAKE2B_BLOCKBYTES:
            blake2b_increment_counter(S, BLAKE2B_BLOCKBYTES)
            blake2b_compress(S, in_data[:BLAKE2B_BLOCKBYTES])
            inlen -= BLAKE2B_BLOCKBYTES
            in_data = in_data[BLAKE2B_BLOCKBYTES:]

    S.buf[S.buflen:S.buflen + inlen] = in_data[:inlen]
    S.buflen += inlen

    return 0

