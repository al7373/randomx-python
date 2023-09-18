from randomx.const import RegistersCount, RegisterCountFlt
from randomx.rx_vec_f128 import rx_vec_f128 

class NativeRegisterFile:
    def __init__(self):
        self.r = [0] * RegistersCount
        self.f = [rx_vec_f128() for _ in range(RegisterCountFlt)]
        self.e = [rx_vec_f128() for _ in range(RegisterCountFlt)]
        self.a = [rx_vec_f128() for _ in range(RegisterCountFlt)]

