from typing import List

class Block:

    def __init__(self, v: List[int]):
        self.v = v

    def to_bytes(self):
        byte_array = bytearray()
        for value in self.v:
            byte_array.extend(value.to_bytes(8, 'little'))
        return byte_array

    @classmethod
    def from_bytes(cls, data: bytes):
        int_list = [int.from_bytes(data[i:i+8], 'little') for i in range(0, len(data), 8)]
        return cls(int_list)

