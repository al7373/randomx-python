from virtual_machine.randomx_vm import randomx_vm
from bytecode_machine.BytecodeMachine import BytecodeMachine, maskRegisterExponentMantissa, executeBytecode 
from bytecode_machine.NativeRegisterFile import NativeRegisterFile
from bytecode_machine.InstructionByteCode import InstructionByteCode
from bytecode_machine.exe_ import load64, store64
from randomx.rx_vec_f128 import rx_load_vec_f128, rx_cvt_packed_int_vec_f128, rx_xor_vec_f128, rx_store_vec_f128
from randomx.const import RegisterCountFlt, ScratchpadL3Mask64, RegistersCount, CacheLineAlignMask  
import struct
from randomx.configuration import RANDOMX_PROGRAM_SIZE, RANDOMX_PROGRAM_ITERATIONS 
from typing import List
from randomx.randomx_dataset import randomx_dataset, datasetRead as _datasetRead

class InterpretedVm(randomx_vm, BytecodeMachine):

    def __init__(self):
        randomx_vm.__init__(self)
        BytecodeMachine.__init__(self)
        self.bytecode = [InstructionByteCode() for _ in range(RANDOMX_PROGRAM_SIZE)]

    def datasetRead(self, blockNumber: int, r: List[int]) -> None:
        datasetLine = [0] * RegistersCount
        _datasetRead(self.mem.memory, blockNumber, datasetLine)
        for i in range(RegistersCount):
            r[i] ^= datasetLine[i]

    def datasetPrefetch(self, blockNumber: int) -> None:
		# rx_prefetch_nta(mem.memory + address);
        pass

    def setDataset(self, dataset: randomx_dataset) -> None:
        self.mem.memory = dataset.memory
        self.datasetPtr = dataset
    
    def execute(self):
        nreg = NativeRegisterFile()
        for i in range(RegisterCountFlt):
            nreg.a[i] = rx_load_vec_f128(bytearray(
                struct.pack('<dd', self.reg.a[i].lo, self.reg.a[i].hi)
            ))

        self.compileProgram(self.program, self.bytecode, nreg)

        spAddr0 = self.mem.mx
        spAddr1 = self.mem.ma

        for ic in range(RANDOMX_PROGRAM_ITERATIONS):

            spMix = nreg.r[self.config.readReg0] ^ nreg.r[self.config.readReg1]
            spAddr0 ^= spMix
            spAddr0 &= ScratchpadL3Mask64
            spAddr1 ^= spMix >> 32
            spAddr1 &= ScratchpadL3Mask64

            for i in range(RegistersCount):
                addr = spAddr0 + 8 * i
                nreg.r[i] ^= load64(self.scratchpad[addr:addr+8])

            for i in range(RegisterCountFlt):
                addr = spAddr1 + 8 * i
                nreg.f[i] = rx_cvt_packed_int_vec_f128(self.scratchpad[addr:addr+8])

            for i in range(RegisterCountFlt):
                addr = spAddr1 + 8 * (RegisterCountFlt + i)
                nreg.e[i] = maskRegisterExponentMantissa(
                    self.config, 
                    rx_cvt_packed_int_vec_f128(self.scratchpad[addr:addr+8])
                )

            executeBytecode(self.bytecode, self.scratchpad, self.config)

            self.mem.mx ^= nreg.r[self.config.readReg2] ^ nreg.r[self.config.readReg3]
            self.mem.mx &= CacheLineAlignMask

            self.datasetPrefetch(self.datasetOffset + self.mem.mx)
            self.datasetRead(self.datasetOffset + self.mem.ma, nreg.r)
            self.mem.mx, self.mem.ma = self.mem.ma, self.mem.mx

            for i in range(RegistersCount):
                store64(self.scratchpad, spAddr1 + 8 * i, nreg.r[i])

            for i in range(RegisterCountFlt):
                nreg.f[i] = rx_xor_vec_f128(nreg.f[i], nreg.e[i])

            for i in range(RegisterCountFlt):
                rx_store_vec_f128(self.scratchpad, spAddr0 + 16 * i, nreg.f[i])

            spAddr0 = 0
            spAddr1 = 0

        for i in range(RegistersCount):
            self.reg.r[i] = nreg.r[i]

        for i in range(RegisterCountFlt):
            self.reg.f[i].lo = nreg.f[i].lo
            self.reg.f[i].hi = nreg.f[i].hi

        for i in range(RegisterCountFlt):
            self.reg.e[i].lo = nreg.e[i].lo
            self.reg.e[i].hi = nreg.e[i].hi

    def run(self, seed: bytearray):
        self.generateProgram(seed)
        self.initialize()
        self.execute()

