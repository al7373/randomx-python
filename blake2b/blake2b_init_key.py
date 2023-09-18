from .Blake2bParam import Blake2bParam
from .Blake2bState import Blake2bState
from .blake2b_invalidate_state import blake2b_invalidate_state
from .blake2b_update import blake2b_update
from .blake2b_init_param import blake2b_init_param
from .const import BLAKE2B_OUTBYTES, BLAKE2B_KEYBYTES, BLAKE2B_BLOCKBYTES

def blake2b_init_key(S: Blake2bState, outlen: int, key: bytes, keylen: int) -> int:
    P = Blake2bParam(
        digest_length=outlen,
        key_length=keylen,
        fanout=1,
        depth=1,
        leaf_length=0,
        node_offset=0,
        node_depth=0,
        inner_length=0
    )

    if S is None:
        return -1

    if outlen == 0 or outlen > BLAKE2B_OUTBYTES:
        blake2b_invalidate_state(S)
        return -1

    if key is None or keylen == 0 or keylen > BLAKE2B_KEYBYTES:
        blake2b_invalidate_state(S)
        return -1

    # Setup Parameter Block for keyed BLAKE2
    if blake2b_init_param(S, P) < 0:
        blake2b_invalidate_state(S)
        return -1

    block = bytearray(BLAKE2B_BLOCKBYTES)
    block[:keylen] = key[:keylen]
    blake2b_update(S, block, BLAKE2B_BLOCKBYTES)

    return 0

