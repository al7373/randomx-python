from typing import List
from .SuperscalarInstructionType import SuperscalarInstructionType
from .SuperscalarInstructionInfo import SuperscalarInstructionInfo, slot_3, slot_3L, slot_4, slot_7, slot_8, slot_9, slot_10
from blake2b.Blake2Generator import Blake2Generator 
from randomx.Instruction import Instruction
from randomx.isZeroOrPowerOf2 import isZeroOrPowerOf2
from .RegisterInfo import RegisterInfo
from .selectRegister import selectRegister
from randomx.const import RegisterNeedsDisplacement 

class MetaSuperscalarInstruction(type):
    @property
    def Null(cls):
        return cls(SuperscalarInstructionInfo.NOP)

class SuperscalarInstruction(metaclass=MetaSuperscalarInstruction):

    def __init__(self, info: SuperscalarInstructionInfo = None):
        self.info_ = info
        self.src_ = -1
        self.dst_ = -1
        self.mod_ = None
        self.imm32_ = None
        self.opGroup_ = None
        self.opGroupPar_ = None
        self.canReuse_ = False
        self.groupParIsSource_ = False

    def toInstr(self, instr: Instruction):
        instr.opcode = self.getType().value
        instr.dst = self.dst_
        instr.src = self.src_ if self.src_ >= 0 else self.dst_
        instr.setMod(self.mod_)
        instr.setImm32(self.imm32_)

    def getType(self):
        return self.info_.getType()

    def getSource(self):
        return self.src_

    def getDestination(self):
        return self.dst_

    def getGroup(self):
        return self.opGroup_

    def getGroupPar(self):
        return self.opGroupPar_

    def getInfo(self):
        return self.info_

    def reset(self):
        self.src_ = self.dst_ = -1
        self.canReuse_ = self.groupParIsSource_ = False

    def create(self, info: SuperscalarInstructionInfo, gen: Blake2Generator):
        self.info_ = info
        self.reset()
        instruction_type = info.getType()

        if instruction_type == SuperscalarInstructionType.ISUB_R:
            self.mod_ = 0
            self.imm32_ = 0
            self.opGroup_ = SuperscalarInstructionType.IADD_RS
            self.groupParIsSource_ = True

        elif instruction_type == SuperscalarInstructionType.IXOR_R:
            self.mod_ = 0
            self.imm32_ = 0
            self.opGroup_ = SuperscalarInstructionType.IXOR_R
            self.groupParIsSource_ = True

        elif instruction_type == SuperscalarInstructionType.IADD_RS:
            self.mod_ = gen.get_byte()
            self.imm32_ = 0
            self.opGroup_ = SuperscalarInstructionType.IADD_RS
            self.groupParIsSource_ = True

        elif instruction_type == SuperscalarInstructionType.IMUL_R:
            self.mod_ = 0
            self.imm32_ = 0
            self.opGroup_ = SuperscalarInstructionType.IMUL_R
            self.groupParIsSource_ = True

        elif instruction_type == SuperscalarInstructionType.IROR_C:
            self.mod_ = 0
            while True:
                self.imm32_ = gen.get_byte() & 63
                if self.imm32_ != 0:
                    break
            self.opGroup_ = SuperscalarInstructionType.IROR_C
            self.opGroupPar_ = -1

        elif instruction_type in (SuperscalarInstructionType.IADD_C7, SuperscalarInstructionType.IADD_C8, SuperscalarInstructionType.IADD_C9):
            self.mod_ = 0
            self.imm32_ = gen.get_uint32()
            self.opGroup_ = SuperscalarInstructionType.IADD_C7
            self.opGroupPar_ = -1

        elif instruction_type in (SuperscalarInstructionType.IXOR_C7, SuperscalarInstructionType.IXOR_C8, SuperscalarInstructionType.IXOR_C9):
            self.mod_ = 0
            self.imm32_ = gen.get_uint32()
            self.opGroup_ = SuperscalarInstructionType.IXOR_C7
            self.opGroupPar_ = -1

        elif instruction_type == SuperscalarInstructionType.IMULH_R:
            self.canReuse_ = True
            self.mod_ = 0
            self.imm32_ = 0
            self.opGroup_ = SuperscalarInstructionType.IMULH_R
            self.opGroupPar_ = gen.get_uint32()

        elif instruction_type == SuperscalarInstructionType.ISMULH_R:
            self.canReuse_ = True
            self.mod_ = 0
            self.imm32_ = 0
            self.opGroup_ = SuperscalarInstructionType.ISMULH_R
            self.opGroupPar_ = gen.get_uint32()

        elif instruction_type == SuperscalarInstructionType.IMUL_RCP:
            self.mod_ = 0
            while True:
                self.imm32_ = gen.get_uint32()
                if not isZeroOrPowerOf2(self.imm32_):
                    break
            self.opGroup_ = SuperscalarInstructionType.IMUL_RCP
            self.opGroupPar_ = -1
        else:
            pass

    def createForSlot(self, gen: Blake2Generator, slot_size: int, fetch_type: int, is_last: bool, is_first: bool):
        if slot_size == 3:
            if is_last:
                self.create(slot_3L[gen.get_byte() & 3], gen)
            else:
                self.create(slot_3[gen.get_byte() & 1], gen)
        elif slot_size == 4:
            if fetch_type == 4 and not is_last:
                self.create(SuperscalarInstructionInfo.IMUL_R, gen)
            else:
                self.create(slot_4[gen.get_byte() & 1], gen)
        elif slot_size == 7:
            self.create(slot_7[gen.get_byte() & 1], gen)
        elif slot_size == 8:
            self.create(slot_8[gen.get_byte() & 1], gen)
        elif slot_size == 9:
            self.create(slot_9[gen.get_byte() & 1], gen)
        elif slot_size == 10:
            self.create(slot_10, gen)
        else:
            raise Exception("Unreachable")

    def selectDestination(self, cycle: int, allow_chained_mul: bool, registers: List[RegisterInfo], gen: Blake2Generator) -> bool:
        available_registers = []

        for i in range(8):
            if (registers[i].latency <= cycle and (self.canReuse_ or i != self.src_) and
                (allow_chained_mul or self.opGroup_ != SuperscalarInstructionType.IMUL_R or registers[i].lastOpGroup != SuperscalarInstructionType.IMUL_R) and
                (registers[i].lastOpGroup != self.opGroup_ or registers[i].lastOpPar != self.opGroupPar_) and
                (self.info_.getType() != SuperscalarInstructionType.IADD_RS or i != RegisterNeedsDisplacement)):
                available_registers.append(i)

        selectedRegister = selectRegister(available_registers, gen, registers)
        aRegisterHasBeenSelected = selectedRegister > -1
        if aRegisterHasBeenSelected:
            self.dst_ = selectedRegister 
        return aRegisterHasBeenSelected 


    def selectSource(self, cycle: int, registers: List['RegisterInfo'], gen: 'Blake2Generator') -> bool:
        availableRegisters = [i for i in range(8) if registers[i].latency <= cycle]

        if len(availableRegisters) == 2 and self.info_.getType() == SuperscalarInstructionType.IADD_RS:
            if availableRegisters[0] == RegisterNeedsDisplacement or availableRegisters[1] == RegisterNeedsDisplacement:
                self.opGroupPar_ = self.src_ = RegisterNeedsDisplacement
                return True

        selectedRegister = selectRegister(availableRegisters, gen, registers)
        if selectedRegister > -1:
            self.src_ = selectedRegister 
            if self.groupParIsSource_:
                self.opGroupPar_ = self.src_
            return True

        return False

