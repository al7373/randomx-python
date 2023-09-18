from typing import Any
from .Blake2bState import Blake2bState
from .blake2b_init import blake2b_init
from .blake2b_update import blake2b_update
from .blake2b_final import blake2b_final
from .blake2b import blake2b
from .const import BLAKE2B_OUTBYTES
from .store32 import store32

def blake2b_long(pout: bytearray, outlen: int, in_data: bytes, inlen: int) -> int:
    out = memoryview(pout)
    blake_state = Blake2bState()
    outlen_bytes = bytearray(4)
    ret = -1

    if outlen > (1 << 32) - 1:
        return ret

    store32(outlen_bytes, 0, outlen)

    def TRY(statement: Any) -> Any:
        nonlocal ret
        ret = statement
        if ret < 0:
            raise Exception("TRY failed")
        return None

    try:
        if outlen <= BLAKE2B_OUTBYTES:
            TRY(blake2b_init(blake_state, outlen))
            TRY(blake2b_update(blake_state, outlen_bytes, len(outlen_bytes)))
            TRY(blake2b_update(blake_state, in_data, inlen))
            TRY(blake2b_final(blake_state, out, outlen))
        else:
            toproduce: int
            out_buffer = bytearray(BLAKE2B_OUTBYTES)
            in_buffer = bytearray(BLAKE2B_OUTBYTES)
            TRY(blake2b_init(blake_state, BLAKE2B_OUTBYTES))
            TRY(blake2b_update(blake_state, outlen_bytes, len(outlen_bytes)))
            TRY(blake2b_update(blake_state, in_data, inlen))
            TRY(blake2b_final(blake_state, out_buffer, BLAKE2B_OUTBYTES))
            out[:BLAKE2B_OUTBYTES // 2] = out_buffer[:BLAKE2B_OUTBYTES // 2]
            out = out[BLAKE2B_OUTBYTES // 2:]
            toproduce = outlen - BLAKE2B_OUTBYTES // 2

            while toproduce > BLAKE2B_OUTBYTES:
                in_buffer[:] = out_buffer[:]
                TRY(blake2b(out_buffer, BLAKE2B_OUTBYTES, in_buffer, BLAKE2B_OUTBYTES, None, 0))
                out[:BLAKE2B_OUTBYTES // 2] = out_buffer[:BLAKE2B_OUTBYTES // 2]
                out = out[BLAKE2B_OUTBYTES // 2:]
                toproduce -= BLAKE2B_OUTBYTES // 2

            in_buffer[:] = out_buffer[:]
            TRY(blake2b(out_buffer, toproduce, in_buffer, BLAKE2B_OUTBYTES, None, 0))
            out[:toproduce] = out_buffer[:toproduce]

    except Exception as e:
        return ret

    return 0

