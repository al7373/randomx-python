from randomx.fillAes1Rx4 import fillAes1Rx4 
from randomx.fillAes4Rx4 import fillAes4Rx4 
from randomx.hashAes1Rx4 import hashAes1Rx4 
from randomx.const import ScratchpadSize, CacheLineAlignMask, DatasetExtraItems, CacheLineSize
from randomx.Program import Program
from randomx.Instruction import Instruction
from randomx.configuration import RANDOMX_PROGRAM_SIZE 
from randomx.MemoryRegisters import MemoryRegisters
from randomx.ProgramConfiguration import ProgramConfiguration
from randomx.RegisterFile import RegisterFile
from .getSmallPositiveFloatBits import getSmallPositiveFloatBits
from .getFloatMask import getFloatMask 
import struct
from randomx.randomx_dataset import randomx_dataset
from blake2b.blake2b import blake2b

from typing import Union

class randomx_vm:

    def __init__(self):
        self.scratchpad = bytearray(ScratchpadSize)
        self.program = Program()
        self.mem = MemoryRegisters()
        self.config = ProgramConfiguration()
        self.reg = RegisterFile()
        self.datasetOffset: int = 0
        self.datasetPtr: Union[randomx_dataset, None] = None

    def getRegisterFile(self) -> RegisterFile:
        return self.reg

    def initScratchpad(self, seed: bytearray):
        fillAes1Rx4(seed, ScratchpadSize, self.scratchpad)

    def getScratchpad(self):
        return self.scratchpad

    def generateProgram(self, seed: bytearray) -> None:
        entropy_buffer_size = 8 * 16 
        program_data_size = (RANDOMX_PROGRAM_SIZE * Instruction.size) + entropy_buffer_size 
        program_data = bytearray(program_data_size)
        # on doit peut être ici passer seed.copy() à fillAes4Rx4, parce que cette dernière change seed
        fillAes4Rx4(seed, len(program_data), program_data)
        self.program.deserialize(program_data)

    def initialize(self) -> None:
        self.reg.a[0].lo = struct.unpack('<d', struct.pack(
            '<Q', getSmallPositiveFloatBits(self.program.getEntropy(0))
        ))[0]
        self.reg.a[0].hi = struct.unpack('<d', struct.pack(
            '<Q', getSmallPositiveFloatBits(self.program.getEntropy(1))
        ))[0]
        self.reg.a[1].lo = struct.unpack('<d', struct.pack(
            '<Q', getSmallPositiveFloatBits(self.program.getEntropy(2))
        ))[0]
        self.reg.a[1].hi = struct.unpack('<d', struct.pack(
            '<Q', getSmallPositiveFloatBits(self.program.getEntropy(3))
        ))[0]
        self.reg.a[2].lo = struct.unpack('<d', struct.pack(
            '<Q', getSmallPositiveFloatBits(self.program.getEntropy(4))
        ))[0]
        self.reg.a[2].hi = struct.unpack('<d', struct.pack(
            '<Q', getSmallPositiveFloatBits(self.program.getEntropy(5))
        ))[0]
        self.reg.a[3].lo = struct.unpack('<d', struct.pack(
            '<Q', getSmallPositiveFloatBits(self.program.getEntropy(6))
        ))[0]
        self.reg.a[3].hi = struct.unpack('<d', struct.pack(
            '<Q', getSmallPositiveFloatBits(self.program.getEntropy(7))
        ))[0]

        self.mem.ma = self.program.getEntropy(8) & CacheLineAlignMask
        self.mem.mx = self.program.getEntropy(10) & 0xFFFFFFFF

        addressRegisters = self.program.getEntropy(12)

        self.config.readReg0 = 0 + (addressRegisters & 1)
        addressRegisters >>= 1
        self.config.readReg1 = 2 + (addressRegisters & 1)
        addressRegisters >>= 1
        self.config.readReg2 = 4 + (addressRegisters & 1)
        addressRegisters >>= 1
        self.config.readReg3 = 6 + (addressRegisters & 1)

        self.datasetOffset = (self.program.getEntropy(13) % (DatasetExtraItems + 1)) * CacheLineSize

        self.config.eMask[0] = getFloatMask(self.program.getEntropy(14))
        self.config.eMask[1] = getFloatMask(self.program.getEntropy(15))

    def getFinalResult(self, out: bytearray, outSize: int):
        _hash = bytearray(64)
        hashAes1Rx4(self.scratchpad, ScratchpadSize, _hash) 
        self.reg.load_a(_hash)
        _reg = self.reg.to_bytes()
        blake2b(out, outSize, _reg, len(_reg), None, 0)

