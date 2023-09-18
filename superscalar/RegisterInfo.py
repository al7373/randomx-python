from .SuperscalarInstructionType import SuperscalarInstructionType

class RegisterInfo:
    def __init__(self):
        self.latency = 0
        self.lastOpGroup = SuperscalarInstructionType.INVALID
        self.lastOpPar = -1
        self.value = 0

