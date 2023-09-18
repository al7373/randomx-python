from .Blake2bState import Blake2bState
from .blake2b_update import blake2b_update
from .blake2b_init import blake2b_init
from .blake2b_init_key import blake2b_init_key
from .blake2b_final import blake2b_final
from .const import BLAKE2B_OUTBYTES, BLAKE2B_KEYBYTES

def blake2b(out: bytearray, outlen: int, in_data: bytes, inlen: int,
            key: bytes = None, keylen: int = 0) -> int:
    S = Blake2bState()
    ret = -1

    # Verify parameters
    if in_data is None and inlen > 0:
        return ret

    if out is None or outlen == 0 or outlen > BLAKE2B_OUTBYTES:
        return ret

    if (key is None and keylen > 0) or keylen > BLAKE2B_KEYBYTES:
        return ret

    if keylen > 0:
        if blake2b_init_key(S, outlen, key, keylen) < 0:
            return ret
    else:
        if blake2b_init(S, outlen) < 0:
            return ret

    if blake2b_update(S, in_data, inlen) < 0:
        return ret
    ret = blake2b_final(S, out, outlen)

    return ret

