from .store32 import store32
from .load32 import load32
from .blake2b import blake2b

class Blake2Generator:
    def __init__(self, seed, seed_size, nonce=0):
        self.data = bytearray(64)
        self.data_index = len(self.data)
        max_seed_size = 60

        self.data[:seed_size] = seed[:max_seed_size] if seed_size > max_seed_size else seed
        store32(self.data, max_seed_size, nonce)

    def get_byte(self):
        self.check_data(1)
        byte = self.data[self.data_index]
        self.data_index += 1
        return byte

    def get_uint32(self):
        self.check_data(4)
        ret = load32(self.data[self.data_index:self.data_index + 4])
        self.data_index += 4
        return ret

    def check_data(self, bytes_needed):
        if self.data_index + bytes_needed > len(self.data):
            blake2b(self.data, len(self.data), self.data, len(self.data), None, 0)
            self.data_index = 0

