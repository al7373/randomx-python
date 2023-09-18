from .NativeRegisterFile import NativeRegisterFile
from randomx.const import RegistersCount, RegisterCountFlt
from randomx.InstructionType import InstructionType
from .const import *
from randomx.const import RegisterNeedsDisplacement, ScratchpadL1Mask, ScratchpadL2Mask, ScratchpadL3Mask, StoreL3Condition, ConditionOffset, ConditionMask, dynamicMantissaMask 
from superscalar.signExtend2sCompl import signExtend2sCompl
from randomx.isZeroOrPowerOf2 import isZeroOrPowerOf2
from randomx.randomx_reciprocal import randomx_reciprocal 
from .InstructionByteCode import InstructionByteCode
from randomx.ProgramConfiguration import ProgramConfiguration
from .Pointer import Pointer
from randomx.rx_vec_f128 import rx_set_vec_f128, rx_load_vec_f128, rx_and_vec_f128, rx_or_vec_f128, rx_vec_f128
import struct
from typing import List
from randomx.configuration import RANDOMX_PROGRAM_SIZE
from randomx.Program import Program

def maskRegisterExponentMantissa(config: ProgramConfiguration, x: rx_vec_f128) -> rx_vec_f128:
    xmantissaMask = rx_set_vec_f128(dynamicMantissaMask, dynamicMantissaMask)
    xexponentMask = rx_load_vec_f128(bytearray(struct.pack('<QQ', config.eMask[0], config.eMask[1])))
    x = rx_and_vec_f128(x, xmantissaMask)
    x = rx_or_vec_f128(x, xexponentMask)
    return x

def getScratchpadAddress(ibc: InstructionByteCode):
    return (ibc.isrc.getValue() + ibc.imm) & ibc.memMask

def executeInstruction(ibc: InstructionByteCode, pc: Pointer, scratchpad: bytearray, config: ProgramConfiguration):
    if ibc.type == InstructionType.IADD_RS:
        exe_IADD_RS(ibc, pc, scratchpad, config)
    elif ibc.type == InstructionType.IADD_M:
        exe_IADD_M(ibc, pc, scratchpad, config)
    elif ibc.type == InstructionType.ISUB_R:
        exe_ISUB_R(ibc, pc, scratchpad, config)
    elif ibc.type == InstructionType.ISUB_M:
        exe_ISUB_M(ibc, pc, scratchpad, config)
    elif ibc.type == InstructionType.IMUL_R:
        exe_IMUL_R(ibc, pc, scratchpad, config)
    elif ibc.type == InstructionType.IMUL_M:
        exe_IMUL_M(ibc, pc, scratchpad, config)
    elif ibc.type == InstructionType.IMULH_R:
        exe_IMULH_R(ibc, pc, scratchpad, config)
    elif ibc.type == InstructionType.IMULH_M:
        exe_IMULH_M(ibc, pc, scratchpad, config)
    elif ibc.type == InstructionType.ISMULH_R:
        exe_ISMULH_R(ibc, pc, scratchpad, config)
    elif ibc.type == InstructionType.ISMULH_M:
        exe_ISMULH_M(ibc, pc, scratchpad, config)
    elif ibc.type == InstructionType.INEG_R:
        exe_INEG_R(ibc, pc, scratchpad, config)
    elif ibc.type == InstructionType.IXOR_R:
        exe_IXOR_R(ibc, pc, scratchpad, config)
    elif ibc.type == InstructionType.IXOR_M:
        exe_IXOR_M(ibc, pc, scratchpad, config)
    elif ibc.type == InstructionType.IROR_R:
        exe_IROR_R(ibc, pc, scratchpad, config)
    elif ibc.type == InstructionType.IROL_R:
        exe_IROL_R(ibc, pc, scratchpad, config)
    elif ibc.type == InstructionType.ISWAP_R:
        exe_ISWAP_R(ibc, pc, scratchpad, config)
    elif ibc.type == InstructionType.FSWAP_R:
        exe_FSWAP_R(ibc, pc, scratchpad, config)
    elif ibc.type == InstructionType.FADD_R:
        exe_FADD_R(ibc, pc, scratchpad, config)
    elif ibc.type == InstructionType.FADD_M:
        exe_FADD_M(ibc, pc, scratchpad, config)
    elif ibc.type == InstructionType.FSUB_R:
        exe_FSUB_R(ibc, pc, scratchpad, config)
    elif ibc.type == InstructionType.FSUB_M:
        exe_FSUB_M(ibc, pc, scratchpad, config)
    elif ibc.type == InstructionType.FSCAL_R:
        exe_FSCAL_R(ibc, pc, scratchpad, config)
    elif ibc.type == InstructionType.FMUL_R:
        exe_FMUL_R(ibc, pc, scratchpad, config)
    elif ibc.type == InstructionType.FDIV_M:
        exe_FDIV_M(ibc, pc, scratchpad, config)
    elif ibc.type == InstructionType.FSQRT_R:
        exe_FSQRT_R(ibc, pc, scratchpad, config)
    elif ibc.type == InstructionType.CBRANCH:
        exe_CBRANCH(ibc, pc, scratchpad, config)
    elif ibc.type == InstructionType.CFROUND:
        exe_CFROUND(ibc, pc, scratchpad, config)
    elif ibc.type == InstructionType.ISTORE:
        exe_ISTORE(ibc, pc, scratchpad, config)
    elif ibc.type == InstructionType.NOP:
        pass
    elif ibc.type == InstructionType.IMUL_RCP: 
        exe_IMUL_R(ibc, pc, scratchpad, config)
    else:
        raise Exception("Unreachable")

def executeBytecode(bytecode: List[InstructionByteCode], scratchpad: bytearray, config: ProgramConfiguration) -> None:
    _pc = [0]
    pc = Pointer(_pc, 0)
    while pc.getValue() < RANDOMX_PROGRAM_SIZE:
        ibc = bytecode[pc.getValue()]
        executeInstruction(ibc, pc, scratchpad, config)
        pc.setValue(pc.getValue() + 1)

class BytecodeMachine:

    zero = [0]

    def __init__(self):
        self.nreg = NativeRegisterFile()
        self.registerUsage = [0] * RegistersCount

    def beginCompilation(self, regFile):
        self.registerUsage = [-1 for _ in range(RegistersCount)]
        self.nreg = regFile

    def compileInstruction(self, instr, i, ibc):
        opcode = instr.opcode

        if opcode < ceil_IADD_RS:
            dst = instr.dst % RegistersCount
            src = instr.src % RegistersCount
            ibc.type = InstructionType.IADD_RS
            ibc.idst = Pointer(self.nreg.r, dst)
            if dst != RegisterNeedsDisplacement:
                ibc.isrc = Pointer(self.nreg.r, src)
                ibc.shift = instr.getModShift()
                ibc.imm = 0
            else:
                ibc.isrc = Pointer(self.nreg.r, src)
                ibc.shift = instr.getModShift()
                ibc.imm = signExtend2sCompl(instr.getImm32())
            self.registerUsage[dst] = i
            return

        if opcode < ceil_IADD_M:
            dst = instr.dst % RegistersCount
            src = instr.src % RegistersCount
            ibc.type = InstructionType.IADD_M
            ibc.idst = Pointer(self.nreg.r, dst)
            ibc.imm = signExtend2sCompl(instr.getImm32())
            if src != dst:
                ibc.isrc = Pointer(self.nreg.r, src)
                ibc.memMask = ScratchpadL1Mask if instr.getModMem() else ScratchpadL2Mask
            else:
                ibc.isrc = Pointer(self.zero)
                ibc.memMask = ScratchpadL3Mask
            self.registerUsage[dst] = i
            return

        if opcode < ceil_ISUB_R:
            dst = instr.dst % RegistersCount
            src = instr.src % RegistersCount
            ibc.type = InstructionType.ISUB_R
            ibc.idst = Pointer(self.nreg.r, dst)
            if src != dst:
                ibc.isrc = Pointer(self.nreg.r, src)
            else:
                ibc.imm = signExtend2sCompl(instr.getImm32())
                ibc.isrc = Pointer(ibc, 'imm')
            self.registerUsage[dst] = i
            return

        if opcode < ceil_ISUB_M:
            dst = instr.dst % RegistersCount
            src = instr.src % RegistersCount
            ibc.type = InstructionType.ISUB_M
            ibc.idst = Pointer(self.nreg.r, dst)
            ibc.imm = signExtend2sCompl(instr.getImm32())
            if src != dst:
                ibc.isrc = Pointer(self.nreg.r, src)
                ibc.memMask = ScratchpadL1Mask if instr.getModMem() else ScratchpadL2Mask
            else:
                ibc.isrc = Pointer(self.zero)
                ibc.memMask = ScratchpadL3Mask
            self.registerUsage[dst] = i
            return

        if opcode < ceil_IMUL_R:
            dst = instr.dst % RegistersCount
            src = instr.src % RegistersCount
            ibc.type = InstructionType.IMUL_R
            ibc.idst = Pointer(self.nreg.r, dst)
            if src != dst:
                ibc.isrc = Pointer(self.nreg.r, src)
            else:
                ibc.imm = signExtend2sCompl(instr.getImm32());
                ibc.isrc = Pointer(ibc, 'imm')
            self.registerUsage[dst] = i;
            return

        if opcode < ceil_IMUL_M:
            dst = instr.dst % RegistersCount
            src = instr.src % RegistersCount
            ibc.type = InstructionType.IMUL_M
            ibc.idst = Pointer(self.nreg.r, dst)
            ibc.imm = signExtend2sCompl(instr.getImm32());
            if src != dst:
                ibc.isrc = Pointer(self.nreg.r, src)
                ibc.memMask = ScratchpadL1Mask if instr.getModMem() else ScratchpadL2Mask
            else:
                ibc.isrc = Pointer(self.zero)
                ibc.memMask = ScratchpadL3Mask
            self.registerUsage[dst] = i;
            return

        if opcode < ceil_IMULH_R:
            dst = instr.dst % RegistersCount
            src = instr.src % RegistersCount
            ibc.type = InstructionType.IMULH_R
            ibc.idst = Pointer(self.nreg.r, dst)
            ibc.isrc = Pointer(self.nreg.r, src)
            self.registerUsage[dst] = i
            return

        if opcode < ceil_IMULH_M:
            dst = instr.dst % RegistersCount
            src = instr.src % RegistersCount
            ibc.type = InstructionType.IMULH_M
            ibc.idst = Pointer(self.nreg.r, dst)
            ibc.imm = signExtend2sCompl(instr.getImm32())
            if src != dst:
                ibc.isrc = Pointer(self.nreg.r, src)
                ibc.memMask = ScratchpadL1Mask if instr.getModMem() else ScratchpadL2Mask
            else:
                ibc.isrc = Pointer(self.zero)
                ibc.memMask = ScratchpadL3Mask
            self.registerUsage[dst] = i
            return

        if opcode < ceil_ISMULH_R:
            dst = instr.dst % RegistersCount
            src = instr.src % RegistersCount
            ibc.type = InstructionType.ISMULH_R
            ibc.idst = Pointer(self.nreg.r, dst)
            ibc.isrc = Pointer(self.nreg.r, src)
            self.registerUsage[dst] = i
            return

        if opcode < ceil_ISMULH_M:
            dst = instr.dst % RegistersCount
            src = instr.src % RegistersCount
            ibc.type = InstructionType.ISMULH_M
            ibc.idst = Pointer(self.nreg.r, dst)
            ibc.imm = signExtend2sCompl(instr.getImm32())
            if src != dst:
                ibc.isrc = Pointer(self.nreg.r, src)
                ibc.memMask = ScratchpadL1Mask if instr.getModMem() else ScratchpadL2Mask
            else:
                ibc.isrc = Pointer(self.zero)
                ibc.memMask = ScratchpadL3Mask
            self.registerUsage[dst] = i
            return

        if opcode < ceil_IMUL_RCP:
            divisor = instr.getImm32()
            if not isZeroOrPowerOf2(divisor):
                dst = instr.dst % RegistersCount
                ibc.type = InstructionType.IMUL_R
                ibc.idst = Pointer(self.nreg.r, dst)
                ibc.imm = randomx_reciprocal(divisor)
                ibc.isrc = Pointer(ibc, 'imm')
                self.registerUsage[dst] = i
            else:
                ibc.type = InstructionType.NOP
            return

        if opcode < ceil_INEG_R:
            dst = instr.dst % RegistersCount
            ibc.type = InstructionType.INEG_R
            ibc.idst = Pointer(self.nreg.r, dst)
            self.registerUsage[dst] = i
            return

        if opcode < ceil_IXOR_R:
            dst = instr.dst % RegistersCount
            src = instr.src % RegistersCount
            ibc.type = InstructionType.IXOR_R
            ibc.idst = Pointer(self.nreg.r, dst)
            if src != dst:
                ibc.isrc = Pointer(self.nreg.r, src)
            else:
                ibc.imm = signExtend2sCompl(instr.getImm32())
                ibc.isrc = Pointer(ibc, 'imm')
            self.registerUsage[dst] = i
            return

        if opcode < ceil_IXOR_M:
            src = instr.src % RegistersCount
            dst = instr.dst % RegistersCount
            ibc.type = InstructionType.IXOR_M
            ibc.idst = Pointer(self.nreg.r, dst)
            ibc.imm = signExtend2sCompl(instr.getImm32())
            if src != dst:
                ibc.isrc = Pointer(self.nreg.r, src)
                ibc.memMask = ScratchpadL1Mask if instr.getModMem() else ScratchpadL2Mask
            else:
                ibc.isrc = Pointer(self.zero)
                ibc.memMask = ScratchpadL3Mask
            self.registerUsage[dst] = i
            return

        if opcode < ceil_IROR_R:
            src = instr.src % RegistersCount
            dst = instr.dst % RegistersCount
            ibc.type = InstructionType.IROR_R
            ibc.idst = Pointer(self.nreg.r, dst)
            if src != dst:
                ibc.isrc = Pointer(self.nreg.r, src)
            else:
                ibc.imm = instr.getImm32()
                ibc.isrc = Pointer(ibc, 'imm')
            self.registerUsage[dst] = i
            return

        if opcode < ceil_IROL_R:
            src = instr.src % RegistersCount
            dst = instr.dst % RegistersCount
            ibc.type = InstructionType.IROL_R
            ibc.idst = Pointer(self.nreg.r, dst)
            if src != dst:
                ibc.isrc = Pointer(self.nreg.r, src)
            else:
                ibc.imm = instr.getImm32()
                ibc.isrc = Pointer(ibc, 'imm')
            self.registerUsage[dst] = i
            return

        if opcode < ceil_ISWAP_R:
            src = instr.src % RegistersCount
            dst = instr.dst % RegistersCount
            if src != dst:
                ibc.type = InstructionType.ISWAP_R
                ibc.idst = Pointer(self.nreg.r, dst)
                ibc.isrc = Pointer(self.nreg.r, src)
                self.registerUsage[dst] = i
                self.registerUsage[src] = i
            else:
                ibc.type = InstructionType.NOP
            return

        if opcode < ceil_FSWAP_R:
            dst = instr.dst % RegistersCount
            ibc.type = InstructionType.FSWAP_R;
            if dst < RegisterCountFlt:
                ibc.fdst = Pointer(self.nreg.f, dst)
            else:
                ibc.fdst = Pointer(self.nreg.e, dst - RegisterCountFlt)
            return

        if opcode < ceil_FADD_R:
            dst = instr.dst % RegisterCountFlt
            src = instr.src % RegisterCountFlt
            ibc.type = InstructionType.FADD_R
            ibc.fdst = Pointer(self.nreg.f, dst)
            ibc.fsrc = Pointer(self.nreg.a, src)
            return

        if opcode < ceil_FADD_M:
            dst = instr.dst % RegisterCountFlt
            src = instr.src % RegistersCount
            ibc.type = InstructionType.FADD_M
            ibc.fdst = Pointer(self.nreg.f, dst)
            ibc.isrc = Pointer(self.nreg.r, src)
            ibc.memMask = ScratchpadL1Mask if instr.getModMem() else ScratchpadL2Mask
            ibc.imm = signExtend2sCompl(instr.getImm32())
            return

        if opcode < ceil_FSUB_R:
            dst = instr.dst % RegisterCountFlt
            src = instr.src % RegisterCountFlt
            ibc.type = InstructionType.FSUB_R
            ibc.fdst = Pointer(self.nreg.f, dst)
            ibc.fsrc = Pointer(self.nreg.a, src)
            return

        if opcode < ceil_FSUB_M:
            dst = instr.dst % RegisterCountFlt
            src = instr.src % RegistersCount
            ibc.type = InstructionType.FSUB_M
            ibc.fdst = Pointer(self.nreg.f, dst)
            ibc.isrc = Pointer(self.nreg.r, src)
            ibc.memMask = ScratchpadL1Mask if instr.getModMem() else ScratchpadL2Mask
            ibc.imm = signExtend2sCompl(instr.getImm32())
            return

        if opcode < ceil_FSCAL_R:
            dst = instr.dst % RegisterCountFlt
            ibc.fdst = Pointer(self.nreg.f, dst)
            ibc.type = InstructionType.FSCAL_R
            return

        if opcode < ceil_FMUL_R:
            dst = instr.dst % RegisterCountFlt
            src = instr.src % RegisterCountFlt
            ibc.type = InstructionType.FMUL_R
            ibc.fdst = Pointer(self.nreg.e, dst)
            ibc.fsrc = Pointer(self.nreg.a, src)
            return

        if opcode < ceil_FDIV_M:
            dst = instr.dst % RegisterCountFlt
            src = instr.src % RegistersCount
            ibc.type = InstructionType.FDIV_M
            ibc.fdst = Pointer(self.nreg.e, dst)
            ibc.isrc = Pointer(self.nreg.r, src)
            ibc.memMask = ScratchpadL1Mask if instr.getModMem() else ScratchpadL2Mask
            ibc.imm = signExtend2sCompl(instr.getImm32())
            return

        if opcode < ceil_FSQRT_R:
            dst = instr.dst % RegisterCountFlt
            ibc.type = InstructionType.FSQRT_R
            ibc.fdst = Pointer(self.nreg.e, dst)
            return

        if opcode < ceil_CBRANCH:
            ibc.type = InstructionType.CBRANCH
            #jump condition
            creg = instr.dst % RegistersCount
            ibc.idst = Pointer(self.nreg.r, creg)
            ibc.target = self.registerUsage[creg]
            shift = instr.getModCond() + ConditionOffset
            ibc.imm = signExtend2sCompl(instr.getImm32()) | (1 << shift)
            if ConditionOffset > 0 or shift > 0: #clear the bit below the condition mask - this limits the number of successive jumps to 2
                ibc.imm &= ~(1 << (shift - 1))
            ibc.memMask = ConditionMask << shift
            #mark all registers as used
            for j in range(RegistersCount):
                self.registerUsage[j] = i
            return

        if opcode < ceil_CFROUND:
            src = instr.src % RegistersCount
            ibc.isrc = Pointer(self.nreg.r, src)
            ibc.type = InstructionType.CFROUND
            ibc.imm = instr.getImm32() & 63
            return

        if opcode < ceil_ISTORE:
            dst = instr.dst % RegistersCount
            src = instr.src % RegistersCount
            ibc.type = InstructionType.ISTORE
            ibc.idst = Pointer(self.nreg.r, dst)
            ibc.isrc = Pointer(self.nreg.r, src)
            ibc.imm = signExtend2sCompl(instr.getImm32())
            if instr.getModCond() < StoreL3Condition:
                ibc.memMask = ScratchpadL1Mask if instr.getModMem() else ScratchpadL2Mask
            else:
                ibc.memMask = ScratchpadL3Mask
            return

        if opcode < ceil_NOP:
            ibc.type = InstructionType.NOP
            return

        else:
            raise ValueError(f"Unexpected opcode: {opcode}")

    def compileProgram(self, program: Program, bytecode: List[InstructionByteCode], regFile: NativeRegisterFile) -> None:
        self.beginCompilation(regFile)
        for i in range(RANDOMX_PROGRAM_SIZE): 
            instr = program(i)
            ibc = bytecode[i]
            self.compileInstruction(instr, i, ibc)

from .exe_ import *

