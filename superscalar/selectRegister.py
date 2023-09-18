from typing import List
from .SuperscalarInstructionInfo import SuperscalarInstructionInfo
from .RegisterInfo import RegisterInfo
from blake2b.Blake2Generator import Blake2Generator 

def selectRegister(available_registers: List[int], gen: Blake2Generator, registers: List[RegisterInfo]) -> int:

    if len(available_registers) == 0:
            return -1

    if len(available_registers) > 1:
        index = gen.get_uint32() % len(available_registers)
    else:
        index = 0

    best_register = available_registers[index]

    return best_register

