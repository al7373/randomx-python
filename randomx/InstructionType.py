from enum import IntEnum

class InstructionType(IntEnum):
    IADD_RS = 0
    IADD_M = 1
    ISUB_R = 2
    ISUB_M = 3
    IMUL_R = 4
    IMUL_M = 5
    IMULH_R = 6
    IMULH_M = 7
    ISMULH_R = 8
    ISMULH_M = 9
    IMUL_RCP = 10
    INEG_R = 11
    IXOR_R = 12
    IXOR_M = 13
    IROR_R = 14
    IROL_R = 15
    ISWAP_R = 16
    FSWAP_R = 17
    FADD_R = 18
    FADD_M = 19
    FSUB_R = 20
    FSUB_M = 21
    FSCAL_R = 22
    FMUL_R = 23
    FDIV_M = 24
    FSQRT_R = 25
    CBRANCH = 26
    CFROUND = 27
    ISTORE = 28
    NOP = 29

