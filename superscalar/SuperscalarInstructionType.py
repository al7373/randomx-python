from enum import Enum

class SuperscalarInstructionType(Enum):
    ISUB_R = 0
    IXOR_R = 1
    IADD_RS = 2
    IMUL_R = 3
    IROR_C = 4
    IADD_C7 = 5
    IXOR_C7 = 6
    IADD_C8 = 7
    IXOR_C8 = 8
    IADD_C9 = 9
    IXOR_C9 = 10
    IMULH_R = 11
    ISMULH_R = 12
    IMUL_RCP = 13
    COUNT = 14
    INVALID = -1

