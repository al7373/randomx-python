from .Blake2bState import Blake2bState 
from .Blake2bParam import Blake2bParam 
from .load64 import load64 
from .blake2b_init0 import blake2b_init0

def blake2b_init_param(S: Blake2bState, P: Blake2bParam) -> int:
    if P is None or S is None:
        return -1

    blake2b_init0(S)
    p = bytearray([P.digest_length, P.key_length, P.fanout, P.depth,
                   *P.leaf_length.to_bytes(4, 'little'),
                   *P.node_offset.to_bytes(8, 'little'),
                   P.node_depth, P.inner_length,
                   *P.reserved,
                   *P.salt,
                   *P.personal])

    for i in range(8):
        S.h[i] ^= load64(p[i * 8:i * 8 + 8])

    S.outlen = P.digest_length
    return 0

