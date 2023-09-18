from .ExecutionPort import ExecutionPort

class MacroOp:

    Add_rr = None
    Sub_rr = None
    Xor_rr = None
    Imul_r = None
    Mul_r = None
    Mov_rr = None

    Lea_sib = None
    Imul_rr = None
    Ror_ri = None

    Add_ri = None
    Xor_ri = None

    Mov_ri64 = None

    Ror_rcl = None
    Xor_self = None
    Cmp_ri = None
    Setcc_r = None
    TestJz_fused = None

    IMULH_R_ops_array = None
    ISMULH_R_ops_array = None
    IMUL_RCP_ops_array = None

    def __init__(self, name, size, latency=0, uop1=ExecutionPort.Null, uop2=ExecutionPort.Null, dependent=False):
        self.name_ = name
        self.size_ = size
        self.latency_ = latency
        self.uop1_ = uop1
        self.uop2_ = uop2
        self.dependent_ = dependent

    def getName(self):
        return self.name_

    def getSize(self):
        return self.size_

    def getLatency(self):
        return self.latency_

    def getUop1(self):
        return self.uop1_

    def getUop2(self):
        return self.uop2_

    def isSimple(self):
        return self.uop2_ == ExecutionPort.Null

    def isEliminated(self):
        return self.uop1_ == ExecutionPort.Null

    def isDependent(self):
        return self.dependent_

MacroOp.Add_rr = MacroOp("add r,r", 3, 1, ExecutionPort.P015)
MacroOp.Sub_rr = MacroOp("sub r,r", 3, 1, ExecutionPort.P015)
MacroOp.Xor_rr = MacroOp("xor r,r", 3, 1, ExecutionPort.P015)
MacroOp.Imul_r = MacroOp("imul r", 3, 4, ExecutionPort.P1, ExecutionPort.P5)
MacroOp.Mul_r = MacroOp("mul r", 3, 4, ExecutionPort.P1, ExecutionPort.P5)
MacroOp.Mov_rr = MacroOp("mov r,r", 3)

MacroOp.Lea_sib = MacroOp("lea r,r+r*s", 4, 1, ExecutionPort.P01)
MacroOp.Imul_rr = MacroOp("imul r,r", 4, 3, ExecutionPort.P1)
MacroOp.Ror_ri = MacroOp("ror r,i", 4, 1, ExecutionPort.P05)

MacroOp.Add_ri = MacroOp("add r,i", 7, 1, ExecutionPort.P015)
MacroOp.Xor_ri = MacroOp("xor r,i", 7, 1, ExecutionPort.P015)

MacroOp.Mov_ri64 = MacroOp("mov rax,i64", 10, 1, ExecutionPort.P015)

MacroOp.Ror_rcl = MacroOp("ror r,cl", 3, 1, ExecutionPort.P0, ExecutionPort.P5)
MacroOp.Xor_self = MacroOp("xor rcx,rcx", 3)
MacroOp.Cmp_ri = MacroOp("cmp r,i", 7, 1, ExecutionPort.P015)
MacroOp.Setcc_r = MacroOp("setcc cl", 3, 1, ExecutionPort.P05)
MacroOp.TestJz_fused = MacroOp("testjz r,i", 13, 0, ExecutionPort.P5)

IMULH_R_ops_array = [MacroOp.Mov_rr, MacroOp.Mul_r, MacroOp.Mov_rr]
ISMULH_R_ops_array = [MacroOp.Mov_rr, MacroOp.Imul_r, MacroOp.Mov_rr]
IMUL_RCP_ops_array = [MacroOp.Mov_ri64, MacroOp("imul r,r", 4, 3, ExecutionPort.P1, dependent=True)]

