from .const import blake2b_IV, BLAKE2B_BLOCKBYTES

class Blake2bState:
    def __init__(self):
        self.h = blake2b_IV.copy()
        self.t = [0, 0]
        self.f = [0, 0]
        self.buflen = 0
        self.buf = bytearray(BLAKE2B_BLOCKBYTES)
        self.outlen = 0
        self.last_node = 0
