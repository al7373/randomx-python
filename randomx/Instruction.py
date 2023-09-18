from blake2b.store32 import store32
from blake2b.load32 import load32
import struct

class Instruction:
    size = 8

    def __init__(self):
        self.opcode: int = 0
        self.dst: int = 0
        self.src: int = 0
        self.mod: int = 0
        self.imm32: bytearray = bytearray(4)

    def getImm32(self) -> int:
        return load32(self.imm32)

    def setImm32(self, val: int) -> None:
        store32(self.imm32, 0, val)

    def getModMem(self) -> int:
        return self.mod % 4  # bits 0-1

    def getModShift(self) -> int:
        return (self.mod >> 2) % 4  # bits 2-3

    def getModCond(self) -> int:
        return self.mod >> 4  # bits 4-7

    def setMod(self, val: int) -> None:
        self.mod = val

    @classmethod
    def deserialize(cls, data: bytearray):
        opcode, dst, src, mod, imm32 = struct.unpack('<BBBBI', data)
        instr = cls()
        instr.opcode = opcode
        instr.dst = dst
        instr.src = src
        instr.mod = mod
        instr.setImm32(imm32)
        return instr

