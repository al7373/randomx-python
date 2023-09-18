import unittest
from bytecode_machine.BytecodeMachine import BytecodeMachine, getScratchpadAddress, executeInstruction
from bytecode_machine.InstructionByteCode import InstructionByteCode
from randomx.Instruction import Instruction 
from randomx.InstructionType import InstructionType 
from randomx.ProgramConfiguration import ProgramConfiguration
from superscalar.signExtend2sCompl import signExtend2sCompl
from bytecode_machine.const import * 
from bytecode_machine.NativeRegisterFile import NativeRegisterFile 
from randomx.const import ScratchpadL1Mask, ScratchpadL2Mask, ScratchpadL3Mask, RegisterCountFlt, StoreL3Condition, ConditionOffset, ConditionMask, RegisterNeedsDisplacement
from randomx.randomx_reciprocal import randomx_reciprocal 
import os
from bytecode_machine.Pointer import Pointer 
from randomx.rx_vec_f128 import rx_set_vec_f128, rx_store_vec_f128
from bytecode_machine.RoundingMode import *

class _TestBytecodeMachine(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.reg = NativeRegisterFile()
        cls.decoder = BytecodeMachine()
        cls.decoder.nreg = cls.reg
        cls.ibc = InstructionByteCode()
        cls.config = ProgramConfiguration()
        cls.registerHigh = 192
        cls.registerDst = 0
        cls.registerSrc = 1
        cls.pc = 0
        cls.imm32 = 3234567890
        cls.imm64 = signExtend2sCompl(cls.imm32)

        cls.decoder.beginCompilation(cls.reg)

    def compileInstruction_IADD_RS(self):
        instr = Instruction()
        instr.opcode = ceil_IADD_RS - 1
        instr.dst = type(self).registerHigh | type(self).registerDst
        instr.src = type(self).registerHigh | type(self).registerSrc
        instr.mod = 255
        instr.setImm32(type(self).imm32)
        type(self).decoder.compileInstruction(instr, type(self).pc, type(self).ibc)
        self.assertEqual(type(self).ibc.type, InstructionType.IADD_RS)
        self.assertEqual(type(self).ibc.idst.getAccessor(), type(self).registerDst)
        self.assertEqual(type(self).ibc.isrc.getAccessor(), type(self).registerSrc)
        self.assertEqual(type(self).ibc.idst.getValue(), type(self).reg.r[type(self).registerDst])
        self.assertEqual(type(self).ibc.isrc.getValue(), type(self).reg.r[type(self).registerSrc])
        self.assertEqual(type(self).ibc.shift, 3)
        self.assertEqual(type(self).ibc.imm, 0)

    def executeInstruction_IADD_RS(self):
        # IADD_RS (execute)
        type(self).reg.r[type(self).registerDst] = 0x8000000000000000
        type(self).reg.r[type(self).registerSrc] = 0x1000000000000000
        executeInstruction(type(self).ibc, type(self).pc, None, type(self).config)
        self.assertEqual(type(self).reg.r[type(self).registerDst], 0)

    def compileInstruction_IADD_RS_with_immediate(self):
        instr = Instruction()
        instr.opcode = ceil_IADD_RS - 1
        instr.mod = 8
        instr.dst = type(self).registerHigh | RegisterNeedsDisplacement
        instr.src = type(self).registerHigh | type(self).registerSrc
        instr.setImm32(type(self).imm32)
        type(self).decoder.compileInstruction(instr, type(self).pc, type(self).ibc)
        self.assertEqual(type(self).ibc.type, InstructionType.IADD_RS)
        self.assertEqual(type(self).ibc.idst.getAccessor(), RegisterNeedsDisplacement)
        self.assertEqual(type(self).ibc.isrc.getAccessor(), type(self).registerSrc)
        self.assertEqual(type(self).ibc.idst.getValue(), type(self).reg.r[RegisterNeedsDisplacement])
        self.assertEqual(type(self).ibc.isrc.getValue(), type(self).reg.r[type(self).registerSrc])
        self.assertEqual(type(self).ibc.shift, 2)
        self.assertEqual(type(self).ibc.imm, type(self).imm64)

    def executeInstruction_IADD_RS_with_immediate(self):
        # IADD_RS with immediate (execute)
        type(self).reg.r[RegisterNeedsDisplacement] = 0x8000000000000000
        type(self).reg.r[type(self).registerSrc] = 0x2000000000000000
        executeInstruction(type(self).ibc, type(self).pc, None, type(self).config)
        self.assertEqual(type(self).reg.r[RegisterNeedsDisplacement], type(self).imm64)

    def compileInstruction_IADD_M(self):
        instr = Instruction()
        instr.opcode = ceil_IADD_M - 1
        instr.dst = type(self).registerHigh | type(self).registerDst
        instr.src = type(self).registerHigh | type(self).registerSrc
        instr.mod = 1
        instr.setImm32(type(self).imm32)
        type(self).decoder.compileInstruction(instr, type(self).pc, type(self).ibc)
        self.assertEqual(type(self).ibc.type, InstructionType.IADD_M)
        self.assertEqual(type(self).ibc.idst.getValue(), type(self).reg.r[type(self).registerDst])
        self.assertEqual(type(self).ibc.isrc.getValue(), type(self).reg.r[type(self).registerSrc])
        self.assertEqual(type(self).ibc.imm, type(self).imm64)
        self.assertEqual(type(self).ibc.memMask, ScratchpadL1Mask);

    def compileInstruction_ISUB_R(self):
        instr = Instruction()
        instr.opcode = ceil_ISUB_R - 1
        instr.dst = type(self).registerHigh | type(self).registerDst
        instr.src = type(self).registerHigh | type(self).registerSrc
        instr.setImm32(type(self).imm32)
        type(self).decoder.compileInstruction(instr, type(self).pc, type(self).ibc)
        self.assertEqual(type(self).ibc.type, InstructionType.ISUB_R)
        self.assertEqual(
                type(self).ibc.idst.getValue(), 
                type(self).reg.r[type(self).registerDst]
        )
        self.assertEqual(
                type(self).ibc.isrc.getValue(), 
                type(self).reg.r[type(self).registerSrc]
        )

    def executeInstruction_ISUB_R(self):
        type(self).reg.r[type(self).registerDst] = 1
        type(self).reg.r[type(self).registerSrc] = 0xFFFFFFFF
        executeInstruction(type(self).ibc, type(self).pc, None, type(self).config)
        self.assertEqual(type(self).reg.r[type(self).registerDst], 0xFFFFFFFF00000002)

    def compileInstruction_ISUB_R_with_immediate(self):
        instr = Instruction()
        instr.opcode = ceil_ISUB_R - 1
        instr.dst = type(self).registerHigh | type(self).registerDst
        instr.src = type(self).registerHigh | type(self).registerDst
        instr.setImm32(type(self).imm32)
        type(self).decoder.compileInstruction(instr, type(self).pc, type(self).ibc)
        self.assertEqual(type(self).ibc.type, InstructionType.ISUB_R)
        self.assertEqual(
                type(self).ibc.idst.getValue(), 
                type(self).reg.r[type(self).registerDst]
        )
        self.assertEqual(type(self).ibc.isrc.getValue(), type(self).ibc.imm)

    def executeInstruction_ISUB_R_with_immediate(self):
        type(self).reg.r[type(self).registerDst] = 0
        executeInstruction(type(self).ibc, type(self).pc, None, type(self).config)
        self.assertEqual(type(self).reg.r[type(self).registerDst], (~type(self).imm64 + 1) & 0xFFFFFFFFFFFFFFFF)

    def compileInstruction_ISUB_M(self):
        instr = Instruction()
        instr.opcode = ceil_ISUB_M - 1
        instr.mod = 0
        instr.dst = type(self).registerHigh | type(self).registerDst
        instr.src = type(self).registerHigh | type(self).registerSrc
        instr.setImm32(type(self).imm32)
        type(self).decoder.compileInstruction(instr, type(self).pc, type(self).ibc)
        self.assertEqual(type(self).ibc.type, InstructionType.ISUB_M)
        self.assertEqual(type(self).ibc.idst.getAccessor(), type(self).registerDst)
        self.assertEqual(type(self).ibc.isrc.getAccessor(), type(self).registerSrc)
        self.assertEqual(type(self).ibc.idst.getValue(), type(self).reg.r[type(self).registerDst])
        self.assertEqual(type(self).ibc.isrc.getValue(), type(self).reg.r[type(self).registerSrc])
        self.assertEqual(type(self).ibc.imm, type(self).imm64)
        self.assertEqual(type(self).ibc.memMask, ScratchpadL2Mask)

    def compileInstruction_IMUL_R(self):
        instr = Instruction()
        instr.opcode = ceil_IMUL_R - 1
        instr.mod = 0
        instr.dst = type(self).registerHigh | type(self).registerDst
        instr.src = type(self).registerHigh | type(self).registerSrc
        instr.setImm32(type(self).imm32)
        type(self).decoder.compileInstruction(instr, type(self).pc, type(self).ibc)
        self.assertEqual(type(self).ibc.type, InstructionType.IMUL_R)
        self.assertEqual(type(self).ibc.idst.getValue(), type(self).reg.r[type(self).registerDst])
        self.assertEqual(type(self).ibc.isrc.getValue(), type(self).reg.r[type(self).registerSrc])

    def executeInstruction_IMUL_R(self):
        type(self).reg.r[type(self).registerDst] = 0xBC550E96BA88A72B;
        type(self).reg.r[type(self).registerSrc] = 0xF5391FA9F18D6273;
        executeInstruction(type(self).ibc, type(self).pc, None, type(self).config)
        self.assertEqual(type(self).reg.r[type(self).registerDst], 0x28723424A9108E51)

    def compileInstruction_IMUL_R_with_immediate(self):
        instr = Instruction()
        instr.opcode = ceil_IMUL_R - 1
        instr.dst = type(self).registerHigh | type(self).registerDst
        instr.src = type(self).registerHigh | type(self).registerDst
        instr.setImm32(type(self).imm32);
        type(self).decoder.compileInstruction(instr, type(self).pc, type(self).ibc)
        self.assertEqual(type(self).ibc.type, InstructionType.IMUL_R)
        self.assertEqual(type(self).ibc.idst.getValue(), type(self).reg.r[type(self).registerDst])
        self.assertEqual(type(self).ibc.isrc.getValue(), type(self).ibc.imm)
        self.assertEqual(type(self).ibc.idst.getAccessor(), type(self).registerDst)
        self.assertEqual(type(self).ibc.isrc.getAccessor(), 'imm')

    def executeInstruction_IMUL_R_with_immediate(self):
        type(self).reg.r[type(self).registerDst] = 1
        executeInstruction(type(self).ibc, type(self).pc, None, type(self).config);
        self.assertEqual(type(self).reg.r[type(self).registerDst], type(self).imm64)

    def compileInstruction_IMUL_M(self):
        instr = Instruction()
        instr.opcode = ceil_IMUL_M - 1
        instr.mod = 0
        instr.dst = type(self).registerHigh | type(self).registerDst
        instr.src = type(self).registerHigh | type(self).registerDst
        instr.setImm32(type(self).imm32)
        type(self).decoder.compileInstruction(instr, type(self).pc, type(self).ibc)
        self.assertEqual(type(self).ibc.type, InstructionType.IMUL_M)
        self.assertEqual(
                type(self).ibc.idst.getAccessor(), 
                type(self).registerDst
        )
        self.assertEqual(
                type(self).ibc.isrc.getValue(), 
                0
        )
        self.assertEqual(type(self).ibc.imm, type(self).imm64)
        self.assertEqual(type(self).ibc.memMask, ScratchpadL3Mask)

    def compileInstruction_IMULH_R(self):
        instr = Instruction()
        instr.opcode = ceil_IMULH_R - 1
        instr.mod = 0
        instr.dst = type(self).registerHigh | type(self).registerDst
        instr.src = type(self).registerHigh | type(self).registerSrc
        instr.setImm32(type(self).imm32)
        type(self).decoder.compileInstruction(instr, type(self).pc, type(self).ibc)
        self.assertEqual(type(self).ibc.type, InstructionType.IMULH_R)
        self.assertEqual(type(self).ibc.idst.getValue(), type(self).reg.r[type(self).registerDst])
        self.assertEqual(type(self).ibc.isrc.getValue(), type(self).reg.r[type(self).registerSrc])

    def executeInstruction_IMULH_R(self):
        type(self).reg.r[type(self).registerDst] = 0xBC550E96BA88A72B
        type(self).reg.r[type(self).registerSrc] = 0xF5391FA9F18D6273
        executeInstruction(type(self).ibc, type(self).pc, None, type(self).config)
        self.assertEqual(type(self).reg.r[type(self).registerDst], 0xB4676D31D2B34883)


    def compileInstruction_IMULH_R_squared(self):
        instr = Instruction()
        instr.opcode = ceil_IMULH_R - 1
        instr.dst = type(self).registerHigh | type(self).registerDst
        instr.src = type(self).registerHigh | type(self).registerDst
        instr.setImm32(type(self).imm32)
        type(self).decoder.compileInstruction(instr, type(self).pc, type(self).ibc)
        self.assertEqual(type(self).ibc.type, InstructionType.IMULH_R)
        self.assertEqual(type(self).ibc.idst.getValue(), type(self).reg.r[type(self).registerDst])
        self.assertEqual(type(self).ibc.isrc.getValue(), type(self).reg.r[type(self).registerDst])
        self.assertEqual(type(self).ibc.idst.getAccessor(), type(self).registerDst)
        self.assertEqual(type(self).ibc.isrc.getAccessor(), type(self).registerDst)

    def compileInstruction_IMULH_M(self):
        instr = Instruction()
        instr.opcode = ceil_IMULH_M - 1
        instr.mod = 0
        instr.dst = type(self).registerHigh | type(self).registerDst
        instr.src = type(self).registerHigh | type(self).registerSrc
        instr.setImm32(type(self).imm32)
        type(self).decoder.compileInstruction(instr, type(self).pc, type(self).ibc)
        self.assertEqual(type(self).ibc.type, InstructionType.IMULH_M)
        self.assertEqual(type(self).ibc.idst.getValue(), type(self).reg.r[type(self).registerDst])
        self.assertEqual(type(self).ibc.isrc.getValue(), type(self).reg.r[type(self).registerSrc])
        self.assertEqual(type(self).ibc.imm, type(self).imm64)
        self.assertEqual(type(self).ibc.memMask, ScratchpadL2Mask)

    def compileInstruction_ISMULH_R(self):
        instr = Instruction()
        instr.opcode = ceil_ISMULH_R - 1
        instr.dst = type(self).registerHigh | type(self).registerDst
        instr.src = type(self).registerHigh | type(self).registerSrc
        instr.setImm32(type(self).imm32)
        type(self).decoder.compileInstruction(instr, type(self).pc, type(self).ibc)
        self.assertEqual(type(self).ibc.type, InstructionType.ISMULH_R)
        self.assertEqual(type(self).ibc.idst.getValue(), type(self).reg.r[type(self).registerDst])
        self.assertEqual(type(self).ibc.isrc.getValue(), type(self).reg.r[type(self).registerSrc])

    def executeInstruction_ISMULH_R(self):
        type(self).reg.r[type(self).registerDst] = 0xBC550E96BA88A72B
        type(self).reg.r[type(self).registerSrc] = 0xF5391FA9F18D6273
        executeInstruction(type(self).ibc, type(self).pc, None, type(self).config)
        self.assertEqual(type(self).reg.r[type(self).registerDst], 0x02D93EF1269D3EE5)

    def compileInstruction_ISMULH_R_squared(self):
        instr = Instruction()
        instr.opcode = ceil_ISMULH_R - 1
        instr.dst = type(self).registerHigh | type(self).registerDst
        instr.src = type(self).registerHigh | type(self).registerDst
        instr.setImm32(type(self).imm32)
        type(self).decoder.compileInstruction(instr, type(self).pc, type(self).ibc)
        self.assertEqual(type(self).ibc.type, InstructionType.ISMULH_R)
        self.assertEqual(type(self).ibc.idst.getValue(), type(self).reg.r[type(self).registerDst])
        self.assertEqual(type(self).ibc.isrc.getValue(), type(self).reg.r[type(self).registerDst])

    def compileInstruction_ISMULH_M(self):
        instr = Instruction()
        instr.opcode = ceil_ISMULH_M - 1
        instr.mod = 3
        instr.dst = type(self).registerHigh | type(self).registerDst
        instr.src = type(self).registerHigh | type(self).registerSrc
        instr.setImm32(type(self).imm32)
        type(self).decoder.compileInstruction(instr, type(self).pc, type(self).ibc)
        self.assertEqual(type(self).ibc.type, InstructionType.ISMULH_M)
        self.assertEqual(type(self).ibc.idst.getValue(), type(self).reg.r[type(self).registerDst])
        self.assertEqual(type(self).ibc.isrc.getValue(), type(self).reg.r[type(self).registerSrc])
        self.assertEqual(type(self).ibc.imm, type(self).imm64)
        self.assertEqual(type(self).ibc.memMask, ScratchpadL1Mask)


    def compileInstruction_IMUL_RCP(self):
        instr = Instruction()
        instr.opcode = ceil_IMUL_RCP - 1
        instr.dst = type(self).registerHigh | type(self).registerDst
        instr.setImm32(type(self).imm32)
        type(self).decoder.compileInstruction(instr, type(self).pc, type(self).ibc)
        self.assertEqual(type(self).ibc.type, InstructionType.IMUL_R)
        self.assertEqual(type(self).ibc.idst.getValue(), type(self).reg.r[type(self).registerDst])
        self.assertEqual(type(self).ibc.isrc.getValue(), type(self).ibc.imm)
        self.assertEqual(type(self).ibc.imm, randomx_reciprocal(type(self).imm32))

    def compileInstruction_IMUL_RCP_zero_imm32(self):
        instr = Instruction()
        instr.opcode = ceil_IMUL_RCP - 1
        instr.setImm32(0)
        type(self).decoder.compileInstruction(instr, type(self).pc, type(self).ibc)
        self.assertEqual(type(self).ibc.type, InstructionType.NOP)

    def compileInstruction_INEG_R(self):
        instr = Instruction()
        instr.opcode = ceil_INEG_R - 1
        instr.dst = type(self).registerHigh | type(self).registerDst
        instr.setImm32(type(self).imm32)
        type(self).decoder.compileInstruction(instr, type(self).pc, type(self).ibc)
        self.assertEqual(type(self).ibc.type, InstructionType.INEG_R)
        self.assertEqual(type(self).ibc.idst.getValue(), type(self).reg.r[type(self).registerDst])

    def executeInstruction_INEG_R(self):
        type(self).reg.r[type(self).registerDst] = 0xFFFFFFFFFFFFFFFF
        executeInstruction(type(self).ibc, type(self).pc, None, type(self).config)
        self.assertEqual(type(self).reg.r[type(self).registerDst], 1)

    def compileInstruction_IXOR_R(self):
        instr = Instruction()
        instr.opcode = ceil_IXOR_R - 1
        instr.dst = type(self).registerHigh | type(self).registerDst
        instr.src = type(self).registerHigh | type(self).registerSrc
        instr.setImm32(type(self).imm32)
        type(self).decoder.compileInstruction(instr, type(self).pc, type(self).ibc)
        self.assertEqual(type(self).ibc.type, InstructionType.IXOR_R)
        self.assertEqual(type(self).ibc.idst.getValue(), type(self).reg.r[type(self).registerDst])
        self.assertEqual(type(self).ibc.isrc.getValue(), type(self).reg.r[type(self).registerSrc])

    def executeInstruction_IXOR_R(self):
        type(self).reg.r[type(self).registerDst] = 0x8888888888888888
        type(self).reg.r[type(self).registerSrc] = 0xAAAAAAAAAAAAAAAA
        executeInstruction(type(self).ibc, type(self).pc, None, type(self).config)
        self.assertEqual(type(self).reg.r[type(self).registerDst], 0x2222222222222222)

    def compileInstruction_IXOR_R_with_immediate(self):
        instr = Instruction()
        instr.opcode = ceil_IXOR_R - 1
        instr.dst = type(self).registerHigh | type(self).registerDst
        instr.src = type(self).registerHigh | type(self).registerDst
        instr.setImm32(type(self).imm32)
        type(self).decoder.compileInstruction(instr, type(self).pc, type(self).ibc)
        self.assertEqual(type(self).ibc.type, InstructionType.IXOR_R)
        self.assertEqual(type(self).ibc.idst.getValue(), type(self).reg.r[type(self).registerDst])
        self.assertEqual(type(self).ibc.isrc.getValue(), type(self).ibc.imm)

    def executeInstruction_IXOR_R_with_immediate(self):
        type(self).reg.r[type(self).registerDst] = 0xFFFFFFFFFFFFFFFF
        executeInstruction(type(self).ibc, type(self).pc, None, type(self).config)
        self.assertEqual(type(self).reg.r[type(self).registerDst], (~type(self).imm64) & 0xFFFFFFFFFFFFFFFF)

    def compileInstruction_IXOR_M(self):
        instr = Instruction()
        instr.opcode = ceil_IXOR_M - 1
        instr.dst = type(self).registerHigh | type(self).registerDst
        instr.src = type(self).registerHigh | type(self).registerDst
        instr.setImm32(type(self).imm32)
        type(self).decoder.compileInstruction(instr, type(self).pc, type(self).ibc)
        self.assertEqual(type(self).ibc.type, InstructionType.IXOR_M)
        self.assertEqual(
                type(self).ibc.idst.getValue(), 
                type(self).reg.r[type(self).registerDst]
        )
        self.assertEqual(
                type(self).ibc.isrc.getValue(), 
                0
        )
        self.assertEqual(type(self).ibc.imm, type(self).imm64)
        self.assertEqual(type(self).ibc.memMask, ScratchpadL3Mask)

    def compileInstruction_IROR_R(self):
        instr = Instruction()
        instr.opcode = ceil_IROR_R - 1
        instr.dst = type(self).registerHigh | type(self).registerDst
        instr.src = type(self).registerHigh | type(self).registerSrc
        instr.setImm32(type(self).imm32)
        type(self).decoder.compileInstruction(instr, type(self).pc, type(self).ibc)
        self.assertEqual(type(self).ibc.type, InstructionType.IROR_R)
        self.assertEqual(type(self).ibc.idst.getValue(), type(self).reg.r[type(self).registerDst])
        self.assertEqual(type(self).ibc.isrc.getValue(), type(self).reg.r[type(self).registerSrc])

    def executeInstruction_IROR_R(self):
        type(self).reg.r[type(self).registerDst] = 953360005391419562
        type(self).reg.r[type(self).registerSrc] = 4569451684712230561
        executeInstruction(type(self).ibc, type(self).pc, None, type(self).config)
        self.assertEqual(type(self).reg.r[type(self).registerDst], 0xD835C455069D81EF)

    def compileInstruction_IROL_R(self):
        instr = Instruction()
        instr.opcode = ceil_IROL_R - 1
        instr.dst = type(self).registerHigh | type(self).registerDst
        instr.src = type(self).registerHigh | type(self).registerSrc
        instr.setImm32(type(self).imm32)
        type(self).decoder.compileInstruction(instr, type(self).pc, type(self).ibc)
        self.assertEqual(type(self).ibc.type, InstructionType.IROL_R)
        self.assertEqual(type(self).ibc.idst.getValue(), type(self).reg.r[type(self).registerDst])
        self.assertEqual(type(self).ibc.isrc.getValue(), type(self).reg.r[type(self).registerSrc])

    def executeInstruction_IROL_R(self):
        type(self).reg.r[type(self).registerDst] = 953360005391419562
        type(self).reg.r[type(self).registerSrc] = 4569451684712230561
        executeInstruction(type(self).ibc, type(self).pc, None, type(self).config)
        self.assertEqual(type(self).reg.r[type(self).registerDst], 6978065200552740799)

    def compileInstruction_ISWAP_R(self):
        instr = Instruction()
        instr.opcode = ceil_ISWAP_R - 1
        instr.dst = type(self).registerHigh | type(self).registerDst
        instr.src = type(self).registerHigh | type(self).registerSrc
        type(self).decoder.compileInstruction(instr, type(self).pc, type(self).ibc)
        self.assertEqual(type(self).ibc.type, InstructionType.ISWAP_R)
        self.assertEqual(type(self).ibc.idst.getValue(), type(self).reg.r[type(self).registerDst])
        self.assertEqual(type(self).ibc.isrc.getValue(), type(self).reg.r[type(self).registerSrc])

    def executeInstruction_ISWAP_R(self):
        type(self).reg.r[type(self).registerDst] = 953360005391419562
        type(self).reg.r[type(self).registerSrc] = 4569451684712230561
        executeInstruction(type(self).ibc, type(self).pc, None, type(self).config)
        self.assertEqual(type(self).reg.r[type(self).registerDst], 4569451684712230561)
        self.assertEqual(type(self).reg.r[type(self).registerSrc], 953360005391419562)

    def compileInstruction_FSWAP_R(self):
        instr = Instruction()
        instr.opcode = ceil_FSWAP_R - 1
        instr.dst = type(self).registerHigh | type(self).registerDst
        type(self).decoder.compileInstruction(instr, type(self).pc, type(self).ibc)
        self.assertEqual(type(self).ibc.type, InstructionType.FSWAP_R)
        self.assertEqual(type(self).ibc.fdst.getValue(), type(self).reg.f[type(self).registerDst])

    def executeInstruction_FSWAP_R(self):
        vec = bytearray(16)
        type(self).reg.f[type(self).registerDst] = rx_set_vec_f128(953360005391419562, 4569451684712230561)
        executeInstruction(type(self).ibc, type(self).pc, None, type(self).config)
        rx_store_vec_f128(vec, 0, type(self).reg.f[type(self).registerDst])
        self.assertEqual(vec.hex(), "aa886bb0df033b0da12e95e518f4693f")

    def compileInstruction_FADD_R(self):
        instr = Instruction()
        instr.opcode = ceil_FADD_R - 1
        instr.dst = type(self).registerHigh | type(self).registerDst
        instr.src = type(self).registerHigh | type(self).registerSrc
        instr.setImm32(type(self).imm32)
        type(self).decoder.compileInstruction(instr, type(self).pc, type(self).ibc)
        self.assertEqual(type(self).ibc.type, InstructionType.FADD_R)
        self.assertEqual(type(self).ibc.fdst.getValue(), type(self).reg.f[type(self).registerDst])
        self.assertEqual(type(self).ibc.fsrc.getValue(), type(self).reg.a[type(self).registerSrc])

    def executeInstruction_FADD_R_RoundToNearest(self):
        vec = bytearray(16)
        type(self).reg.f[type(self).registerDst] = rx_set_vec_f128(0x3ffd2c97cc4ef015, 0xc1ce30b3c4223576)
        type(self).reg.a[type(self).registerSrc] = rx_set_vec_f128(0x402a26a86a60c8fb, 0x40b8f684057a59e1)
        rx_set_rounding_mode(RoundToNearest)
        executeInstruction(type(self).ibc, type(self).pc, None, type(self).config)
        rx_store_vec_f128(vec, 0, type(self).reg.f[type(self).registerDst])
        self.assertEqual(vec.hex(), "b932e048a730cec1fea6ea633bcc2d40")

    def executeInstruction_FADD_R_RoundDown(self):
        vec = bytearray(16)
        type(self).reg.f[type(self).registerDst] = rx_set_vec_f128(0x3ffd2c97cc4ef015, 0xc1ce30b3c4223576)
        type(self).reg.a[type(self).registerSrc] = rx_set_vec_f128(0x402a26a86a60c8fb, 0x40b8f684057a59e1)
        rx_set_rounding_mode(RoundDown)
        executeInstruction(type(self).ibc, type(self).pc, None, type(self).config)
        rx_store_vec_f128(vec, 0, type(self).reg.f[type(self).registerDst])
        self.assertEqual(vec.hex(), "b932e048a730cec1fda6ea633bcc2d40")

    def executeInstruction_FADD_R_RoundUp(self):
        vec = bytearray(16)
        type(self).reg.f[type(self).registerDst] = rx_set_vec_f128(0x3ffd2c97cc4ef015, 0xc1ce30b3c4223576)
        type(self).reg.a[type(self).registerSrc] = rx_set_vec_f128(0x402a26a86a60c8fb, 0x40b8f684057a59e1)
        rx_set_rounding_mode(RoundUp)
        executeInstruction(type(self).ibc, type(self).pc, None, type(self).config)
        rx_store_vec_f128(vec, 0, type(self).reg.f[type(self).registerDst])
        self.assertEqual(vec.hex(), "b832e048a730cec1fea6ea633bcc2d40")

    def executeInstruction_FADD_R_RoundToZero(self):
        vec = bytearray(16)
        type(self).reg.f[type(self).registerDst] = rx_set_vec_f128(0x3ffd2c97cc4ef015, 0xc1ce30b3c4223576)
        type(self).reg.a[type(self).registerSrc] = rx_set_vec_f128(0x402a26a86a60c8fb, 0x40b8f684057a59e1)
        rx_set_rounding_mode(RoundToZero)
        executeInstruction(type(self).ibc, type(self).pc, None, type(self).config)
        rx_store_vec_f128(vec, 0, type(self).reg.f[type(self).registerDst])
        self.assertEqual(vec.hex(), "b832e048a730cec1fda6ea633bcc2d40")

    def compileInstruction_FADD_M(self):
        instr = Instruction()
        instr.opcode = ceil_FADD_M - 1
        instr.mod = 1
        instr.dst = type(self).registerHigh | type(self).registerDst
        instr.src = type(self).registerHigh | type(self).registerSrc
        instr.setImm32(type(self).imm32)
        type(self).decoder.compileInstruction(instr, type(self).pc, type(self).ibc)
        self.assertEqual(type(self).ibc.type, InstructionType.FADD_M)
        self.assertEqual(type(self).ibc.fdst.getValue(), type(self).reg.f[type(self).registerDst])
        self.assertEqual(type(self).ibc.isrc.getValue(), type(self).reg.r[type(self).registerSrc])
        self.assertEqual(type(self).ibc.imm, type(self).imm64)
        self.assertEqual(type(self).ibc.memMask, ScratchpadL1Mask)

    def executeInstruction_FADD_M(self):
        mockScratchpad = bytearray([
            0xef,	0xcd,	0xab,	0x90,	0x78,	0x56,	0x34,	0x12
        ])
        vec = bytearray(16)
        type(self).reg.f[type(self).registerDst] = rx_set_vec_f128(0, 0)
        type(self).reg.r[type(self).registerSrc] = 0xFFFFFFFFFFFFE930
        rx_set_rounding_mode(RoundToNearest)
        executeInstruction(
            type(self).ibc, 
            type(self).pc, 
            mockScratchpad, 
            type(self).config
        )
        rx_store_vec_f128(vec, 0, type(self).reg.f[type(self).registerDst])
        self.assertEqual(vec.hex(), "000040840cd5dbc1000000785634b241")

    def compileInstruction_FSUB_R(self):
        instr = Instruction()
        instr.opcode = ceil_FSUB_R - 1
        instr.dst = type(self).registerHigh | type(self).registerDst
        instr.src = type(self).registerHigh | type(self).registerSrc
        instr.setImm32(type(self).imm32)
        type(self).decoder.compileInstruction(instr, type(self).pc, type(self).ibc)
        self.assertEqual(type(self).ibc.type, InstructionType.FSUB_R)
        self.assertEqual(type(self).ibc.fdst.getValue(), type(self).reg.f[type(self).registerDst])
        self.assertEqual(type(self).ibc.fsrc.getValue(), type(self).reg.a[type(self).registerSrc])

    def compileInstruction_FSUB_M(self):
        instr = Instruction()
        instr.opcode = ceil_FSUB_M - 1
        instr.mod = 2
        instr.dst = type(self).registerHigh | type(self).registerDst
        instr.src = type(self).registerHigh | type(self).registerSrc
        instr.setImm32(type(self).imm32)
        type(self).decoder.compileInstruction(instr, type(self).pc, type(self).ibc)
        self.assertEqual(type(self).ibc.type, InstructionType.FSUB_M)
        self.assertEqual(type(self).ibc.fdst.getValue(), type(self).reg.f[type(self).registerDst])
        self.assertEqual(type(self).ibc.isrc.getValue(), type(self).reg.r[type(self).registerSrc])
        self.assertEqual(type(self).ibc.imm, type(self).imm64)
        self.assertEqual(type(self).ibc.memMask, ScratchpadL1Mask)

    def compileInstruction_FSCAL_R(self):
        instr = Instruction()
        instr.opcode = ceil_FSCAL_R - 1
        instr.dst = type(self).registerHigh | type(self).registerDst
        instr.setImm32(type(self).imm32)
        type(self).decoder.compileInstruction(instr, type(self).pc, type(self).ibc)
        self.assertEqual(type(self).ibc.type, InstructionType.FSCAL_R)
        self.assertEqual(type(self).ibc.fdst.getValue(), type(self).reg.f[type(self).registerDst])

    def executeInstruction_FSCAL_R(self):
        vec = bytearray(16)
        type(self).reg.f[type(self).registerDst] = rx_set_vec_f128(0x41dbc35cef248783, 0x40fdfdabb6173d07)
        executeInstruction(type(self).ibc, type(self).pc, None, type(self).config)
        rx_store_vec_f128(vec, 0, type(self).reg.f[type(self).registerDst])
        self.assertEqual(vec.hex(), "073d17b6abfd0dc0838724ef5cc32bc1")

    def compileInstruction_FMUL_R(self):
        instr = Instruction()
        instr.opcode = ceil_FMUL_R - 1
        instr.dst = type(self).registerHigh | type(self).registerDst
        instr.src = type(self).registerHigh | type(self).registerSrc
        instr.setImm32(type(self).imm32)
        type(self).decoder.compileInstruction(instr, type(self).pc, type(self).ibc)
        self.assertEqual(type(self).ibc.type, InstructionType.FMUL_R)
        self.assertEqual(type(self).ibc.fdst.getValue(), type(self).reg.e[type(self).registerDst])
        self.assertEqual(type(self).ibc.fsrc.getValue(), type(self).reg.a[type(self).registerSrc])

    def executeInstruction_FMUL_R_RoundToNearest(self):
        vec = bytearray(16)
        type(self).reg.e[type(self).registerDst] = rx_set_vec_f128(0x41dbc35cef248783, 0x40fdfdabb6173d07)
        type(self).reg.a[type(self).registerSrc] = rx_set_vec_f128(0x40eba861aa31c7c0, 0x41c4561212ae2d50)
        rx_set_rounding_mode(RoundToNearest)
        executeInstruction(type(self).ibc, type(self).pc, None, type(self).config)
        rx_store_vec_f128(vec, 0, type(self).reg.e[type(self).registerDst])
        self.assertEqual(vec.hex(), "69697aff350fd3422f1589cdecfed742")

    def executeInstruction_FMUL_R_RoundDown_RoundToZero(self):
        vec = bytearray(16)
        type(self).reg.e[type(self).registerDst] = rx_set_vec_f128(0x41dbc35cef248783, 0x40fdfdabb6173d07)
        type(self).reg.a[type(self).registerSrc] = rx_set_vec_f128(0x40eba861aa31c7c0, 0x41c4561212ae2d50)
        rx_set_rounding_mode(RoundDown)
        executeInstruction(type(self).ibc, type(self).pc, None, type(self).config)
        rx_store_vec_f128(vec, 0, type(self).reg.e[type(self).registerDst])
        self.assertEqual(vec.hex(), "69697aff350fd3422e1589cdecfed742")

    def executeInstruction_FMUL_R_RoundUp(self):
        vec = bytearray(16)
        type(self).reg.e[type(self).registerDst] = rx_set_vec_f128(0x41dbc35cef248783, 0x40fdfdabb6173d07)
        type(self).reg.a[type(self).registerSrc] = rx_set_vec_f128(0x40eba861aa31c7c0, 0x41c4561212ae2d50)
        rx_set_rounding_mode(RoundUp)
        executeInstruction(type(self).ibc, type(self).pc, None, type(self).config)
        rx_store_vec_f128(vec, 0, type(self).reg.e[type(self).registerDst])
        self.assertEqual(vec.hex(), "6a697aff350fd3422f1589cdecfed742")

    def compileInstruction_FDIV_M(self):
        instr = Instruction()
        instr.opcode = ceil_FDIV_M - 1
        instr.mod = 3
        instr.dst = type(self).registerHigh | type(self).registerDst
        instr.src = type(self).registerHigh | type(self).registerSrc
        instr.setImm32(type(self).imm32)
        type(self).decoder.compileInstruction(instr, type(self).pc, type(self).ibc)
        self.assertEqual(type(self).ibc.type, InstructionType.FDIV_M)
        self.assertEqual(type(self).ibc.fdst.getValue(), type(self).reg.e[type(self).registerDst])
        self.assertEqual(type(self).ibc.isrc.getValue(), type(self).reg.r[type(self).registerSrc])
        self.assertEqual(type(self).ibc.imm, type(self).imm64)
        self.assertEqual(type(self).ibc.memMask, ScratchpadL1Mask)

    def executeInstruction_FDIV_M_RoundToNearest(self):
        cls = type(self)
        vec = bytearray(16)
        mockScratchpad = bytearray([
            0xb6,	0xa1,	0x50,	0xd3,	0xd9,	0x60,	0x24,	0x8b
        ])
        cls.config.eMask[0] = 0x3a0000000005d11a
        cls.config.eMask[1] = 0x39000000001ba31e
        cls.reg.e[cls.registerDst] = rx_set_vec_f128(0x41937f76fede16ee, 0x411b414296ce93b6)
        cls.reg.r[cls.registerSrc] = 0xFFFFFFFFFFFFE930
        rx_set_rounding_mode(RoundToNearest)
        executeInstruction(cls.ibc, cls.pc, mockScratchpad, cls.config)
        rx_store_vec_f128(vec, 0, cls.reg.e[cls.registerDst])
        self.assertEqual(vec.hex(), "e7b269639484434632474a66635ba547")

    def executeInstruction_FDIV_M_RoundDown_RoundToZero(self):
        cls = type(self)
        vec = bytearray(16)
        mockScratchpad = bytearray([
            0xb6,	0xa1,	0x50,	0xd3,	0xd9,	0x60,	0x24,	0x8b
        ])
        cls.config.eMask[0] = 0x3a0000000005d11a
        cls.config.eMask[1] = 0x39000000001ba31e
        cls.reg.e[cls.registerDst] = rx_set_vec_f128(0x41937f76fede16ee, 0x411b414296ce93b6)
        cls.reg.r[cls.registerSrc] = 0xFFFFFFFFFFFFE930
        rx_set_rounding_mode(RoundDown)
        executeInstruction(cls.ibc, cls.pc, mockScratchpad, cls.config)
        rx_store_vec_f128(vec, 0, cls.reg.e[cls.registerDst])
        self.assertEqual(vec.hex(), "e6b269639484434632474a66635ba547")

    def executeInstruction_FDIV_M_RoundUp(self):
        cls = type(self)
        vec = bytearray(16)
        mockScratchpad = bytearray([
            0xb6,	0xa1,	0x50,	0xd3,	0xd9,	0x60,	0x24,	0x8b
        ])
        cls.config.eMask[0] = 0x3a0000000005d11a
        cls.config.eMask[1] = 0x39000000001ba31e
        cls.reg.e[cls.registerDst] = rx_set_vec_f128(0x41937f76fede16ee, 0x411b414296ce93b6)
        cls.reg.r[cls.registerSrc] = 0xFFFFFFFFFFFFE930
        rx_set_rounding_mode(RoundUp)
        executeInstruction(cls.ibc, cls.pc, mockScratchpad, cls.config)
        rx_store_vec_f128(vec, 0, cls.reg.e[cls.registerDst])
        self.assertEqual(vec.hex(), "e7b269639484434633474a66635ba547")

    def compileInstruction_FSQRT_R(self):
        instr = Instruction()
        instr.opcode = ceil_FSQRT_R - 1
        instr.dst = type(self).registerHigh | type(self).registerDst
        type(self).decoder.compileInstruction(instr, type(self).pc, type(self).ibc)
        self.assertEqual(type(self).ibc.type, InstructionType.FSQRT_R)
        self.assertEqual(type(self).ibc.fdst.getValue(), type(self).reg.e[type(self).registerDst])

    def executeInstruction_FSQRT_R_RoundToNearest(self):
        vec = bytearray(16)
        type(self).reg.e[type(self).registerDst] = rx_set_vec_f128(0x41b6b21c11affea7, 0x40526a7e778d9824)
        rx_set_rounding_mode(RoundToNearest)
        executeInstruction(type(self).ibc, type(self).pc, None, type(self).config)
        rx_store_vec_f128(vec, 0, type(self).reg.e[type(self).registerDst])
        self.assertEqual(vec.hex(), "e81f300b612a21408dbaa33f570ed340")

    def executeInstruction_FSQRT_R_RoundDown_RoundToZero(self):
        vec = bytearray(16)
        type(self).reg.e[type(self).registerDst] = rx_set_vec_f128(0x41b6b21c11affea7, 0x40526a7e778d9824)
        rx_set_rounding_mode(RoundDown)
        executeInstruction(type(self).ibc, type(self).pc, None, type(self).config)
        rx_store_vec_f128(vec, 0, type(self).reg.e[type(self).registerDst])
        self.assertEqual(vec.hex(), "e81f300b612a21408cbaa33f570ed340")

    def executeInstruction_FSQRT_R_RoundUp(self):
        vec = bytearray(16)
        type(self).reg.e[type(self).registerDst] = rx_set_vec_f128(0x41b6b21c11affea7, 0x40526a7e778d9824)
        rx_set_rounding_mode(RoundUp);
        executeInstruction(type(self).ibc, type(self).pc, None, type(self).config)
        rx_store_vec_f128(vec, 0, type(self).reg.e[type(self).registerDst])
        self.assertEqual(vec.hex(), "e91f300b612a21408dbaa33f570ed340")

    def compileInstruction_CBRANCH_100(self):
        instr = Instruction()
        instr.opcode = ceil_CBRANCH - 1
        instr.dst = type(self).registerHigh | type(self).registerDst
        instr.setImm32(type(self).imm32)
        instr.mod = 48
        type(self).decoder.compileInstruction(instr, 100, type(self).ibc)
        self.assertEqual(type(self).ibc.type, InstructionType.CBRANCH)
        self.assertEqual(type(self).ibc.idst.getValue(), type(self).reg.r[type(self).registerDst])
        self.assertEqual(type(self).ibc.imm, 0xFFFFFFFFC0CB9AD2)
        self.assertEqual(type(self).ibc.memMask, 0x7F800)
        self.assertEqual(type(self).ibc.target, type(self).pc)

    def compileInstruction_CBRANCH_200(self):
        instr = Instruction()
        instr.opcode = ceil_CBRANCH - 1
        instr.dst = type(self).registerHigh | type(self).registerDst
        instr.setImm32(type(self).imm32)
        instr.mod = 48
        type(self).pc = 200
        type(self).decoder.compileInstruction(instr, type(self).pc, type(self).ibc)
        self.assertEqual(type(self).ibc.type, InstructionType.CBRANCH)
        self.assertEqual(type(self).ibc.idst.getValue(), type(self).reg.r[type(self).registerDst])
        self.assertEqual(type(self).ibc.idst.getAccessor(), type(self).registerDst)
        self.assertEqual(type(self).ibc.imm, 0xFFFFFFFFC0CB9AD2)
        self.assertEqual(type(self).ibc.memMask, 0x7F800)
        self.assertEqual(type(self).ibc.target, 100)

    def executeInstruction_CBRANCH_not_taken(self):
        type(self).reg.r[type(self).registerDst] = 0
        pcPointer = Pointer(type(self), 'pc')
        executeInstruction(type(self).ibc, pcPointer, None, type(self).config)
        self.assertEqual(type(self).pc, 200)

    def executeInstruction_CBRANCH_taken(self):
        type(self).reg.r[type(self).registerDst] = 0xFFFFFFFFFFFC6800
        pcPointer = Pointer(type(self), 'pc')
        executeInstruction(type(self).ibc, pcPointer, None, type(self).config)
        self.assertEqual(type(self).pc, type(self).ibc.target)

    def compileInstruction_CFROUND(self):
        instr = Instruction()
        instr.opcode = ceil_CFROUND - 1
        instr.src = type(self).registerHigh | type(self).registerSrc
        instr.setImm32(type(self).imm32)
        type(self).decoder.compileInstruction(instr, 100, type(self).ibc)
        self.assertEqual(type(self).ibc.type, InstructionType.CFROUND)
        self.assertEqual(type(self).ibc.isrc.getValue(), type(self).reg.r[type(self).registerSrc])
        self.assertEqual(type(self).ibc.imm, 18)

    def compileInstruction_ISTORE(self):
        instr = Instruction()
        instr.opcode = ceil_ISTORE - 1
        instr.src = type(self).registerHigh | type(self).registerSrc
        instr.dst = type(self).registerHigh | type(self).registerDst
        instr.setImm32(type(self).imm32)
        instr.mod = 1
        type(self).decoder.compileInstruction(instr, type(self).pc, type(self).ibc)
        self.assertEqual(type(self).ibc.type, InstructionType.ISTORE)
        self.assertEqual(type(self).ibc.idst.getValue(), type(self).reg.r[type(self).registerDst])
        self.assertEqual(type(self).ibc.isrc.getValue(), type(self).reg.r[type(self).registerSrc])
        self.assertEqual(type(self).ibc.imm, type(self).imm64)
        self.assertEqual(type(self).ibc.memMask, ScratchpadL1Mask)

        instr.mod = 0
        type(self).decoder.compileInstruction(instr, type(self).pc, type(self).ibc)
        self.assertEqual(type(self).ibc.type, InstructionType.ISTORE)
        self.assertEqual(type(self).ibc.idst.getValue(), type(self).reg.r[type(self).registerDst])
        self.assertEqual(type(self).ibc.isrc.getValue(), type(self).reg.r[type(self).registerSrc])
        self.assertEqual(type(self).ibc.imm, type(self).imm64)
        self.assertEqual(type(self).ibc.memMask, ScratchpadL2Mask)

        instr.mod = 224
        type(self).decoder.compileInstruction(instr, type(self).pc, type(self).ibc)
        self.assertEqual(type(self).ibc.type, InstructionType.ISTORE)
        self.assertEqual(type(self).ibc.idst.getValue(), type(self).reg.r[type(self).registerDst])
        self.assertEqual(type(self).ibc.isrc.getValue(), type(self).reg.r[type(self).registerSrc])
        self.assertEqual(type(self).ibc.imm, type(self).imm64)
        self.assertEqual(type(self).ibc.memMask, ScratchpadL3Mask)

class TestBytecodeMachine(unittest.TestCase):


    def test_suite(self):
        cls = _TestBytecodeMachine
        suite = unittest.TestSuite()

        suite.addTest(cls('compileInstruction_IADD_RS'))
        suite.addTest(cls('executeInstruction_IADD_RS'))

        suite.addTest(cls('compileInstruction_IADD_RS_with_immediate'))
        suite.addTest(cls('executeInstruction_IADD_RS_with_immediate'))

        suite.addTest(cls('compileInstruction_IADD_M'))

        suite.addTest(cls('compileInstruction_ISUB_R'))
        suite.addTest(cls('executeInstruction_ISUB_R'))

        suite.addTest(cls('compileInstruction_ISUB_R_with_immediate'))
        suite.addTest(cls('executeInstruction_ISUB_R_with_immediate'))

        suite.addTest(cls('compileInstruction_ISUB_M'))

        suite.addTest(cls('compileInstruction_IMUL_R'))
        suite.addTest(cls('executeInstruction_IMUL_R'))
        suite.addTest(cls('compileInstruction_IMUL_R_with_immediate'))
        suite.addTest(cls('executeInstruction_IMUL_R_with_immediate'))

        suite.addTest(cls('compileInstruction_IMUL_M'))

        suite.addTest(cls('compileInstruction_IMULH_R'))
        suite.addTest(cls('executeInstruction_IMULH_R'))
        suite.addTest(cls('compileInstruction_IMULH_R_squared'))

        suite.addTest(cls('compileInstruction_IMULH_M'))

        suite.addTest(cls('compileInstruction_ISMULH_R'))
        suite.addTest(cls('executeInstruction_ISMULH_R'))
        suite.addTest(cls('compileInstruction_ISMULH_R_squared'))

        suite.addTest(cls('compileInstruction_ISMULH_M'))
        suite.addTest(cls('compileInstruction_IMUL_RCP'))
        suite.addTest(cls('compileInstruction_IMUL_RCP_zero_imm32'))

        suite.addTest(cls('compileInstruction_INEG_R'))
        suite.addTest(cls('executeInstruction_INEG_R'))

        suite.addTest(cls('compileInstruction_IXOR_R'))
        suite.addTest(cls('executeInstruction_IXOR_R'))
        suite.addTest(cls('compileInstruction_IXOR_R_with_immediate'))
        suite.addTest(cls('executeInstruction_IXOR_R_with_immediate'))

        suite.addTest(cls('compileInstruction_IXOR_M'))

        suite.addTest(cls('compileInstruction_IROR_R'))
        suite.addTest(cls('executeInstruction_IROR_R'))

        suite.addTest(cls('compileInstruction_IROL_R'))
        suite.addTest(cls('executeInstruction_IROL_R'))
        
        suite.addTest(cls('compileInstruction_ISWAP_R'))
        suite.addTest(cls('executeInstruction_ISWAP_R'))

        suite.addTest(cls('compileInstruction_FSWAP_R'))
        suite.addTest(cls('executeInstruction_FSWAP_R'))

        suite.addTest(cls('compileInstruction_FADD_R'))
        suite.addTest(cls('executeInstruction_FADD_R_RoundToNearest'))
        suite.addTest(cls('executeInstruction_FADD_R_RoundUp'))
        suite.addTest(cls('executeInstruction_FADD_R_RoundDown'))
        suite.addTest(cls('executeInstruction_FADD_R_RoundToZero'))

        suite.addTest(cls('compileInstruction_FADD_M'))
        suite.addTest(cls('executeInstruction_FADD_M'))

        suite.addTest(cls('compileInstruction_FSUB_R'))
        suite.addTest(cls('compileInstruction_FSUB_M'))

        suite.addTest(cls('compileInstruction_FSCAL_R'))
        suite.addTest(cls('executeInstruction_FSCAL_R'))

        suite.addTest(cls('compileInstruction_FMUL_R'))
        suite.addTest(cls('executeInstruction_FMUL_R_RoundToNearest'))
        suite.addTest(cls('executeInstruction_FMUL_R_RoundDown_RoundToZero'))
        suite.addTest(cls('executeInstruction_FMUL_R_RoundUp'))

        suite.addTest(cls('compileInstruction_FDIV_M'))
        suite.addTest(cls('executeInstruction_FDIV_M_RoundToNearest'))
        suite.addTest(cls('executeInstruction_FDIV_M_RoundDown_RoundToZero'))
        suite.addTest(cls('executeInstruction_FDIV_M_RoundUp'))

        suite.addTest(cls('compileInstruction_FSQRT_R'))
        suite.addTest(cls('executeInstruction_FSQRT_R_RoundToNearest'))
        suite.addTest(cls('executeInstruction_FSQRT_R_RoundDown_RoundToZero'))
        suite.addTest(cls('executeInstruction_FSQRT_R_RoundUp'))

        suite.addTest(cls('compileInstruction_CBRANCH_100'))
        suite.addTest(cls('compileInstruction_CBRANCH_200'))
        suite.addTest(cls('executeInstruction_CBRANCH_not_taken'))
        suite.addTest(cls('executeInstruction_CBRANCH_taken'))

        suite.addTest(cls('compileInstruction_CFROUND'))
        suite.addTest(cls('compileInstruction_ISTORE'))
        runner = unittest.TextTestRunner()
        runner.run(suite)

    def test_getScratchpadAddress_0(self):
        reg = NativeRegisterFile()
        decoder = BytecodeMachine()
        decoder.nreg = reg
        ibc = InstructionByteCode()
        ibc.isrc = Pointer(decoder.nreg.r, 1)
        ibc.isrc.setValue(0)
        ibc.imm = 909495519
        ibc.memMask = 2097144
        self.assertEqual(getScratchpadAddress(ibc), 1428696)

    def test_getScratchpadAddress_10059670208752868472(self):
        reg = NativeRegisterFile()
        decoder = BytecodeMachine()
        decoder.nreg = reg
        ibc = InstructionByteCode()
        ibc.isrc = Pointer(decoder.nreg.r, 0)
        ibc.isrc.setValue(10059670208752868472)
        ibc.imm = 1125683140
        ibc.memMask = 16376
        self.assertEqual(getScratchpadAddress(ibc), 11320)

    def test_getScratchpadAddress_11010621997860170363(self):
        reg = NativeRegisterFile()
        decoder = BytecodeMachine()
        decoder.nreg = reg
        ibc = InstructionByteCode()
        ibc.isrc = Pointer(decoder.nreg.r, 0)
        ibc.isrc.setValue(11010621997860170363)
        ibc.imm = 18446744073563667373
        ibc.memMask = 16376
        self.assertEqual(getScratchpadAddress(ibc), 9768)

    def test_executeInstruction_IADD_M(self):
        reg = NativeRegisterFile()
        decoder = BytecodeMachine()
        decoder.nreg = reg
        pc = [16]
        ibc = InstructionByteCode()
        ibc.type = InstructionType.IADD_M
        ibc.memMask = 2097144
        ibc.imm = 909495519

        ibc.idst = Pointer(decoder.nreg.r, 7)
        ibc.isrc = Pointer(decoder.nreg.r, 0)

        ibc.idst.setValue(6906391120613379856)
        ibc.isrc.setValue(0)

        config = ProgramConfiguration()
        config.eMask = [4035225266128095857, 4467570830353087134]
        config.readReg0 = 0
        config.readReg1 = 3
        config.readReg2 = 4
        config.readReg3 = 7

        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'scratchpad_dump.bin'), 'rb') as f:
            scratchpad = f.read()

        executeInstruction(ibc, Pointer(pc, 0), scratchpad, config)

        self.assertEqual(ibc.idst.getValue(), 10059670208752868472)

    def test_executeInstruction_CFROUND_RoundToNearest(self):
        reg = NativeRegisterFile()
        decoder = BytecodeMachine()
        decoder.nreg = reg

        pc = [160]

        ibc = InstructionByteCode()
        ibc.type = InstructionType.CFROUND
        ibc.memMask = 0
        ibc.imm = 60

        ibc.idst = Pointer(decoder.zero)
        # 0x7fffffffdd10
        ibc.isrc = Pointer(decoder.nreg.r, 0)
        
        ibc.isrc.setValue(9881227932144408393)

        config = ProgramConfiguration()
        config.eMask = [4035225266128095857, 4467570830353087134]
        config.readReg0 = 0
        config.readReg1 = 3
        config.readReg2 = 4
        config.readReg3 = 7

        executeInstruction(ibc, Pointer(pc, 0), None, config)

        self.assertEqual(rx_get_rounding_mode(), RoundToNearest)

    def test_executeInstruction_CFROUND_RoundDown(self):
        reg = NativeRegisterFile()
        decoder = BytecodeMachine()
        decoder.nreg = reg

        pc = [201]

        ibc = InstructionByteCode()
        ibc.type = InstructionType.CFROUND
        ibc.memMask = 0
        ibc.imm = 58

        ibc.idst = Pointer(decoder.zero)
        # 0x7fffffffdd20
        ibc.isrc = Pointer(decoder.nreg.r, 2)
        
        ibc.isrc.setValue(10750622668521953405)

        config = ProgramConfiguration()
        config.eMask = [4035225266128095857, 4467570830353087134]
        config.readReg0 = 0
        config.readReg1 = 3
        config.readReg2 = 4
        config.readReg3 = 7

        executeInstruction(ibc, Pointer(pc, 0), None, config)

        self.assertEqual(rx_get_rounding_mode(), RoundDown)

    def test_executeInstruction_CFROUND_RoundToZero(self):
        reg = NativeRegisterFile()
        decoder = BytecodeMachine()
        decoder.nreg = reg

        pc = [160]

        ibc = InstructionByteCode()
        ibc.type = InstructionType.CFROUND
        ibc.memMask = 0
        ibc.imm = 60

        ibc.idst = Pointer(decoder.zero)
        # 0x7fffffffdd10
        ibc.isrc = Pointer(decoder.nreg.r, 0)
        
        ibc.isrc.setValue(9048559490664862118)

        config = ProgramConfiguration()
        config.eMask = [4035225266128095857, 4467570830353087134]
        config.readReg0 = 0
        config.readReg1 = 3
        config.readReg2 = 4
        config.readReg3 = 7

        executeInstruction(ibc, Pointer(pc, 0), None, config)

        self.assertEqual(rx_get_rounding_mode(), RoundToZero)

    def test_executeInstruction_CFROUND_RoundUp(self):
        reg = NativeRegisterFile()
        decoder = BytecodeMachine()
        decoder.nreg = reg

        pc = [201]

        ibc = InstructionByteCode()
        ibc.type = InstructionType.CFROUND
        ibc.memMask = 0
        ibc.imm = 58

        ibc.idst = Pointer(decoder.zero)
        # 0x7fffffffdd20
        ibc.isrc = Pointer(decoder.nreg.r, 2)
        
        ibc.isrc.setValue(1968078625743192532)

        config = ProgramConfiguration()
        config.eMask = [4035225266128095857, 4467570830353087134]
        config.readReg0 = 0
        config.readReg1 = 3
        config.readReg2 = 4
        config.readReg3 = 7

        executeInstruction(ibc, Pointer(pc, 0), None, config)

        self.assertEqual(rx_get_rounding_mode(), RoundUp)

    def test_executeInstruction_IMUL_M(self):
        reg = NativeRegisterFile()
        decoder = BytecodeMachine()
        decoder.nreg = reg
        pc = [77]
        ibc = InstructionByteCode()
        ibc.type = InstructionType.IMUL_M
        ibc.memMask = 16376
        ibc.imm = 18446744073003581559

        # 0x7fffffffdd10
        ibc.idst = Pointer(decoder.nreg.r, 0)
        # 0x7fffffffdd40
        ibc.isrc = Pointer(decoder.nreg.r, 6)

        ibc.idst.setValue(408683923056601178)
        ibc.isrc.setValue(9374139795281812893)

        config = ProgramConfiguration()
        config.eMask = [3602879701898543400, 3530822107859737062]
        config.readReg0 = 0
        config.readReg1 = 3
        config.readReg2 = 4
        config.readReg3 = 6

        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'scratchpad_dump_1.bin'), 'rb') as f:
            scratchpad = f.read()

        executeInstruction(ibc, Pointer(pc, 0), scratchpad, config)

        self.assertEqual(ibc.idst.getValue(), 12351308275618374690)

    def test_executeInstruction_IMULH_M(self):
        reg = NativeRegisterFile()
        decoder = BytecodeMachine()
        decoder.nreg = reg
        pc = [157]
        ibc = InstructionByteCode()
        ibc.type = InstructionType.IMULH_M
        ibc.memMask = 16376
        ibc.imm = 1958361053

        # 0x7fffffffdd40
        ibc.idst = Pointer(decoder.nreg.r, 6)
        # 0x7fffffffdd20
        ibc.isrc = Pointer(decoder.nreg.r, 2)

        ibc.idst.setValue(6033649618380727543)
        ibc.isrc.setValue(6260831582667587648)

        config = ProgramConfiguration()
        config.eMask = [3602879701898543400, 3530822107859737062]
        config.readReg0 = 0
        config.readReg1 = 3
        config.readReg2 = 4
        config.readReg3 = 6

        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'scratchpad_dump_1.bin'), 'rb') as f:
            scratchpad = f.read()

        executeInstruction(ibc, Pointer(pc, 0), scratchpad, config)

        self.assertEqual(ibc.idst.getValue(), 2000984228566790893)

    def test_executeInstruction_ISMULH_M(self):
        reg = NativeRegisterFile()
        decoder = BytecodeMachine()
        decoder.nreg = reg
        pc = [91]
        ibc = InstructionByteCode()
        ibc.type = InstructionType.ISMULH_M
        ibc.memMask = 16376
        ibc.imm = 285678415

        # 0x7fffffffdd48
        ibc.idst = Pointer(decoder.nreg.r, 7)
        # 0x7fffffffdd38
        ibc.isrc = Pointer(decoder.nreg.r, 5)

        ibc.idst.setValue(43010967849131015)
        ibc.isrc.setValue(14442496944513261383)

        config = ProgramConfiguration()
        config.eMask = [3602879701899126236, 3819052484013955007]
        config.readReg0 = 0
        config.readReg1 = 2
        config.readReg2 = 5
        config.readReg3 = 6

        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'scratchpad_dump_2.bin'), 'rb') as f:
            scratchpad = f.read()

        executeInstruction(ibc, Pointer(pc, 0), scratchpad, config)

        self.assertEqual(ibc.idst.getValue(), 14875899417897291)

    def test_executeInstruction_ISUB_M(self):
        reg = NativeRegisterFile()
        decoder = BytecodeMachine()
        decoder.nreg = reg
        pc = [105]
        ibc = InstructionByteCode()
        ibc.type = InstructionType.ISUB_M
        ibc.memMask = 262136
        ibc.imm = 934831420

        # 0x7fffffffdd10
        ibc.idst = Pointer(decoder.nreg.r, 0)
        # 0x7fffffffdd20
        ibc.isrc = Pointer(decoder.nreg.r, 2)

        ibc.idst.setValue(8077496483976284716)
        ibc.isrc.setValue(17269368130214154657)

        config = ProgramConfiguration()
        config.eMask = [3602879701899126236, 3819052484013955007]
        config.readReg0 = 0
        config.readReg1 = 2
        config.readReg2 = 5
        config.readReg3 = 6

        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'scratchpad_dump_2.bin'), 'rb') as f:
            scratchpad = f.read()

        executeInstruction(ibc, Pointer(pc, 0), scratchpad, config)

        self.assertEqual(ibc.idst.getValue(), 16072817902464534065)

    def test_executeInstruction_IXOR_M(self):
        reg = NativeRegisterFile()
        decoder = BytecodeMachine()
        decoder.nreg = reg
        pc = [117]
        ibc = InstructionByteCode()
        ibc.type = InstructionType.IXOR_M
        ibc.memMask = 16376
        ibc.imm = 655006952

        # 0x7fffffffdd38
        ibc.idst = Pointer(decoder.nreg.r, 5)
        # 0x7fffffffdd10
        ibc.isrc = Pointer(decoder.nreg.r, 0)

        ibc.idst.setValue(14389088374177032781)
        ibc.isrc.setValue(16072817902464534065)

        config = ProgramConfiguration()
        config.eMask = [3602879701899126236, 3819052484013955007]
        config.readReg0 = 0
        config.readReg1 = 2
        config.readReg2 = 5
        config.readReg3 = 6

        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'scratchpad_dump_2.bin'), 'rb') as f:
            scratchpad = f.read()

        executeInstruction(ibc, Pointer(pc, 0), scratchpad, config)

        self.assertEqual(ibc.idst.getValue(), 14224316747007157873)

    def test_executeInstruction_FSUB_M(self):
        reg = NativeRegisterFile()
        decoder = BytecodeMachine()
        decoder.nreg = reg
        pc = [61]
        ibc = InstructionByteCode()
        ibc.type = InstructionType.FSUB_M
        ibc.memMask = 16376
        ibc.imm = 717506265

        registerDst = 0
        registerSrc = 3

        # 0x7fffffffdd50
        ibc.fdst = Pointer(decoder.nreg.f, registerDst)
        # 0x7fffffffdd28
        ibc.isrc = Pointer(decoder.nreg.r, registerSrc)

        # fdst

        # 0xee	0x63	0xc4	0x7c	0x24	0xdf	0xd2	0x41
        # 0x41d2df247cc463ee

        # 0x2f	0x41	0x20	0x31	0x7f	0x14	0xce	0x41
        # 0x41ce147f3120412f							

        fdst = rx_set_vec_f128(0x41ce147f3120412f, 0x41d2df247cc463ee)

        ibc.fdst.setValue(fdst)
        ibc.isrc.setValue(16890553252014488356)

        config = ProgramConfiguration()
        config.eMask = [4035225266128095857, 4467570830353087134]
        config.readReg0 = 0
        config.readReg1 = 3
        config.readReg2 = 4
        config.readReg3 = 7

        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'scratchpad_dump_3.bin'), 'rb') as f:
            scratchpad = f.read()

        executeInstruction(ibc, Pointer(pc, 0), scratchpad, config)

        vec = bytearray(16)
        rx_store_vec_f128(vec, 0, reg.f[registerDst])
        self.assertEqual(vec.hex(), "ee6344a42c9cd7414c1068e33e96e541")

    def test_executeInstruction_ISTORE(self):
        reg = NativeRegisterFile()
        decoder = BytecodeMachine()
        decoder.nreg = reg
        pc = [83]
        ibc = InstructionByteCode()
        ibc.type = InstructionType.ISTORE
        ibc.memMask = 262136
        ibc.imm = 18446744071631865286

        # 0x7fffffffdd18
        registerDst = 1 
        # 0x7fffffffdd10
        registerSrc = 0

        ibc.idst = Pointer(decoder.nreg.r, registerDst)
        ibc.isrc = Pointer(decoder.nreg.r, registerSrc)

        ibc.idst.setValue(8898475812203975723)
        ibc.isrc.setValue(3208647711888319613)

        config = ProgramConfiguration()
        config.eMask = [4035225266128095857, 4467570830353087134]
        config.readReg0 = 0
        config.readReg1 = 3
        config.readReg2 = 4
        config.readReg3 = 7

        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'scratchpad_dump_3.bin'), 'rb') as f:
            scratchpad_0 = bytearray(f.read())

        executeInstruction(ibc, Pointer(pc, 0), scratchpad_0, config)

        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'scratchpad_dump_4.bin'), 'rb') as f:
            scratchpad_1 = f.read()

        self.assertEqual(scratchpad_0.hex(), scratchpad_1.hex())


class TestFSUB_R(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.reg = NativeRegisterFile()
        cls.decoder = BytecodeMachine()
        cls.decoder.nreg = cls.reg
        cls.ibc = InstructionByteCode()
        cls.config = ProgramConfiguration()
        cls.registerHigh = 192
        cls.registerDst = 0
        cls.registerSrc = 1
        cls.pc = 0
        cls.imm32 = 3234567890
        cls.imm64 = signExtend2sCompl(cls.imm32)

        cls.decoder.beginCompilation(cls.reg)

        instr = Instruction()
        instr.opcode = ceil_FSUB_R - 1
        instr.dst = cls.registerHigh | cls.registerDst
        instr.src = cls.registerHigh | cls.registerSrc
        instr.setImm32(cls.imm32)
        cls.decoder.compileInstruction(instr, cls.pc, cls.ibc)

    def test_executeInstruction_RoundToNearest(self):
        vec = bytearray(16)
        cls = type(self)
        cls.reg.f[cls.registerDst] = rx_set_vec_f128(0x41d04e369d71f45a, 0x41a482f6f17136e9)
        cls.reg.a[cls.registerSrc] = rx_set_vec_f128(0x41d910e2dd5626c0, 0x40b4c4c15c050a5e)
        rx_set_rounding_mode(RoundToNearest)
        executeInstruction(cls.ibc, cls.pc, None, cls.config)
        rx_store_vec_f128(vec, 0, cls.reg.f[cls.registerDst])
        self.assertEqual(vec.hex(), "df7eee67cd82a441cc64c87f5885c1c1")

