from .Blake2bState import Blake2bState
from .Blake2bParam import Blake2bParam 
from .const import BLAKE2B_OUTBYTES, BLAKE2B_SALTBYTES, BLAKE2B_PERSONALBYTES
from .blake2b_init_param import blake2b_init_param

def blake2b_init(S: Blake2bState, outlen: int) -> int:
    if S is None:
        return -1

    if outlen == 0 or outlen > BLAKE2B_OUTBYTES:
        blake2b_invalidate_state(S)
        return -1

    # Setup Parameter Block for unkeyed BLAKE2
    P = Blake2bParam(
        digest_length=outlen,
        key_length=0,
        fanout=1,
        depth=1,
        leaf_length=0,
        node_offset=0,
        node_depth=0,
        inner_length=0,
        reserved=bytearray(14),
        salt=bytearray(BLAKE2B_SALTBYTES),
        personal=bytearray(BLAKE2B_PERSONALBYTES)
    )

    return blake2b_init_param(S, P)

