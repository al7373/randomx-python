
class MemoryRegisters:
    def __init__(self):
        self.mx: int = 0
        self.ma: int = 0
        self.memory: Union[bytearray, None] = None

