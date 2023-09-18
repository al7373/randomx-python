from typing import List
from randomx.Instruction import Instruction
from randomx.const import SuperscalarMaxSize

class SuperscalarProgram:
    def __init__(self):
        self.programBuffer = [Instruction() for _ in range(SuperscalarMaxSize)]
        self.size = 0
        self.addrReg = 0
        self.ipc = 0.0
        self.codeSize = 0
        self.macroOps = 0
        self.decodeCycles = 0
        self.cpuLatency = 0
        self.asicLatency = 0
        self.mulCount = 0
        self.cpuLatencies = [0] * 8
        self.asicLatencies = [0] * 8

    def __call__(self, pc):
        return self.programBuffer[pc]

    def __str__(self):
        return "".join([str(instr) for instr in self.programBuffer[:self.size]])

    def getSize(self):
        return self.size

    def setSize(self, val):
        self.size = val

    def getAddressRegister(self):
        return self.addrReg

    def setAddressRegister(self, val):
        self.addrReg = val

