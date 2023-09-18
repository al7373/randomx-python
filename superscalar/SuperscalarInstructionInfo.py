from typing import List
from .SuperscalarInstructionType import SuperscalarInstructionType 
from .MacroOp import MacroOp, IMULH_R_ops_array, ISMULH_R_ops_array, IMUL_RCP_ops_array

class SuperscalarInstructionInfo:

    ISUB_R = None
    IXOR_R = None
    IADD_RS = None
    IMUL_R = None
    IROR_C = None

    IADD_C7 = None
    IXOR_C7 = None
    IADD_C8 = None
    IXOR_C8 = None
    IADD_C9 = None
    IXOR_C9 = None

    IMULH_R = None
    ISMULH_R = None
    IMUL_RCP = None

    NOP = None

    def __init__(self, name, type_=SuperscalarInstructionType.INVALID, ops=None, latency=0, resultOp=0, dstOp=0, srcOp=0):
        self.name_ = name
        self.type_ = type_
        self.ops_ = ops if ops is not None else []
        self.latency_ = latency
        self.resultOp_ = resultOp
        self.dstOp_ = dstOp
        self.srcOp_ = srcOp

    def getName(self):
        return self.name_

    def getSize(self):
        return len(self.ops_)

    def isSimple(self):
        return self.getSize() == 1

    def getLatency(self):
        return self.latency_

    def getOp(self, index):
        return self.ops_[index]

    def getType(self):
        return self.type_

    def getResultOp(self):
        return self.resultOp_

    def getDstOp(self):
        return self.dstOp_

    def getSrcOp(self):
        return self.srcOp_

    @classmethod
    def single_op(cls, name, type_, op, srcOp):
        return cls(name, type_, [op], op.getLatency(), srcOp=srcOp)

    @classmethod
    def multi_op(cls, name, type_, arr, resultOp, dstOp, srcOp):
        ops = list(arr)
        latency = sum(op.getLatency() for op in ops)
        return cls(name, type_, ops, latency, resultOp, dstOp, srcOp)

SuperscalarInstructionInfo.ISUB_R = SuperscalarInstructionInfo.single_op("ISUB_R", SuperscalarInstructionType.ISUB_R, MacroOp.Sub_rr, 0)
SuperscalarInstructionInfo.IXOR_R = SuperscalarInstructionInfo.single_op("IXOR_R", SuperscalarInstructionType.IXOR_R, MacroOp.Xor_rr, 0)
SuperscalarInstructionInfo.IADD_RS = SuperscalarInstructionInfo.single_op("IADD_RS", SuperscalarInstructionType.IADD_RS, MacroOp.Lea_sib, 0)
SuperscalarInstructionInfo.IMUL_R = SuperscalarInstructionInfo.single_op("IMUL_R", SuperscalarInstructionType.IMUL_R, MacroOp.Imul_rr, 0)
SuperscalarInstructionInfo.IROR_C = SuperscalarInstructionInfo.single_op("IROR_C", SuperscalarInstructionType.IROR_C, MacroOp.Ror_ri, -1)

SuperscalarInstructionInfo.IADD_C7 = SuperscalarInstructionInfo.single_op("IADD_C7", SuperscalarInstructionType.IADD_C7, MacroOp.Add_ri, -1)
SuperscalarInstructionInfo.IXOR_C7 = SuperscalarInstructionInfo.single_op("IXOR_C7", SuperscalarInstructionType.IXOR_C7, MacroOp.Xor_ri, -1)
SuperscalarInstructionInfo.IADD_C8 = SuperscalarInstructionInfo.single_op("IADD_C8", SuperscalarInstructionType.IADD_C8, MacroOp.Add_ri, -1)
SuperscalarInstructionInfo.IXOR_C8 = SuperscalarInstructionInfo.single_op("IXOR_C8", SuperscalarInstructionType.IXOR_C8, MacroOp.Xor_ri, -1)
SuperscalarInstructionInfo.IADD_C9 = SuperscalarInstructionInfo.single_op("IADD_C9", SuperscalarInstructionType.IADD_C9, MacroOp.Add_ri, -1)
SuperscalarInstructionInfo.IXOR_C9 = SuperscalarInstructionInfo.single_op("IXOR_C9", SuperscalarInstructionType.IXOR_C9, MacroOp.Xor_ri, -1)

SuperscalarInstructionInfo.IMULH_R = SuperscalarInstructionInfo.multi_op("IMULH_R", SuperscalarInstructionType.IMULH_R, IMULH_R_ops_array, 1, 0, 1)
SuperscalarInstructionInfo.ISMULH_R = SuperscalarInstructionInfo.multi_op("ISMULH_R", SuperscalarInstructionType.ISMULH_R, ISMULH_R_ops_array, 1, 0, 1)
SuperscalarInstructionInfo.IMUL_RCP = SuperscalarInstructionInfo.multi_op("IMUL_RCP", SuperscalarInstructionType.IMUL_RCP, IMUL_RCP_ops_array, 1, 1, -1)

SuperscalarInstructionInfo.NOP = SuperscalarInstructionInfo("NOP")

slot_3 = [SuperscalarInstructionInfo.ISUB_R, SuperscalarInstructionInfo.IXOR_R]
slot_3L = [SuperscalarInstructionInfo.ISUB_R, SuperscalarInstructionInfo.IXOR_R, SuperscalarInstructionInfo.IMULH_R, SuperscalarInstructionInfo.ISMULH_R]
slot_4 = [SuperscalarInstructionInfo.IROR_C, SuperscalarInstructionInfo.IADD_RS]
slot_7 = [SuperscalarInstructionInfo.IXOR_C7, SuperscalarInstructionInfo.IADD_C7]
slot_8 = [SuperscalarInstructionInfo.IXOR_C8, SuperscalarInstructionInfo.IADD_C8]
slot_9 = [SuperscalarInstructionInfo.IXOR_C9, SuperscalarInstructionInfo.IADD_C9]
slot_10 = SuperscalarInstructionInfo.IMUL_RCP

