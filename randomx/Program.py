from .Instruction import Instruction
from .configuration import RANDOMX_PROGRAM_SIZE
import struct

class Program:
    def __init__(self):
        self.entropyBuffer = [0] * 16
        self.programBuffer = [Instruction() for _ in range(RANDOMX_PROGRAM_SIZE)]

    def __call__(self, pc):
        return self.programBuffer[pc]

    def getEntropy(self, i: int):
        return self.entropyBuffer[i]

    def deserialize(self, data: bytearray):
        # Lire les données dans entropyBuffer
        for i in range(16):
            self.entropyBuffer[i] = struct.unpack_from('<Q', data, i*8)[0]

        # Lire les données dans programBuffer
        for i in range(RANDOMX_PROGRAM_SIZE):
            offset = 128 + i*Instruction.size
            self.programBuffer[i] = Instruction.deserialize(data[offset:offset + Instruction.size])

