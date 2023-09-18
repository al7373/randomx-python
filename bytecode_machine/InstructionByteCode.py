from typing import Union
from randomx.rx_vec_f128 import rx_vec_f128
from randomx.InstructionType import InstructionType

class InstructionByteCode:
    def __init__(self):
        self.idst: Union[int, None] = None
        self.fdst: Union[rx_vec_f128, None] = None
        self.isrc: Union[int, None] = None
        self.fsrc: Union[rx_vec_f128, None] = None
        self.imm: Union[int, None] = None
        self.simm: Union[int, None] = None
        self.type: Union[InstructionType, None] = None
        self.target: Union[int, None] = None
        self.shift: Union[int, None] = None
        self._memMask: Union[int, None] = None

    @property
    def memMask(self):
        return self._memMask

    @memMask.setter
    def memMask(self, value: int):
        self._memMask = (value & 0xFFFFFFFF)
