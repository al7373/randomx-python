from typing import List
from .const import RegistersCount, RegisterCountFlt 
from .fpu_reg_t import fpu_reg_t 
import struct

class RegisterFile:
    def __init__(self):
        self.r: List[int] = [0] * RegistersCount
        self.f: List[fpu_reg_t] = [fpu_reg_t() for _ in range(RegisterCountFlt)]
        self.e: List[fpu_reg_t] = [fpu_reg_t() for _ in range(RegisterCountFlt)]
        self.a: List[fpu_reg_t] = [fpu_reg_t() for _ in range(RegisterCountFlt)]

    def load_a(self, src: bytearray):
        d = struct.unpack('<8d', src)
        self.a[0].lo = d[0]
        self.a[0].hi = d[1]
        self.a[1].lo = d[2]
        self.a[1].hi = d[3]
        self.a[2].lo = d[4]
        self.a[2].hi = d[5]
        self.a[3].lo = d[6]
        self.a[3].hi = d[7]

    def to_bytes(self):
        r_bytes = struct.pack('<' + 'Q'*len(self.r), *self.r)
        f_bytes = struct.pack('<' + 'd'*2*len(self.f), *[val for sublist in [(f.lo, f.hi) for f in self.f] for val in sublist])
        e_bytes = struct.pack('<' + 'd'*2*len(self.e), *[val for sublist in [(e.lo, e.hi) for e in self.e] for val in sublist])
        a_bytes = struct.pack('<' + 'd'*2*len(self.a), *[val for sublist in [(a.lo, a.hi) for a in self.a] for val in sublist])

        return r_bytes + f_bytes + e_bytes + a_bytes

    def from_bytes(self, byte_string):
        r_len = len(self.r)
        f_len = 2 * len(self.f)
        e_len = 2 * len(self.e)
        a_len = 2 * len(self.a)

        # Calculer les offsets pour chaque attribut dans la chaîne de bytes
        r_offset = 0
        f_offset = r_offset + r_len * 8
        e_offset = f_offset + f_len * 8
        a_offset = e_offset + e_len * 8

        self.r = list(struct.unpack('<' + 'Q' * r_len, byte_string[r_offset:f_offset]))

        self.f = [fpu_reg_t(lo, hi) for lo, hi in zip(*[iter(struct.unpack('<' + 'd' * f_len, byte_string[f_offset:e_offset]))]*2)]
        self.e = [fpu_reg_t(lo, hi) for lo, hi in zip(*[iter(struct.unpack('<' + 'd' * e_len, byte_string[e_offset:a_offset]))]*2)]
        self.a = [fpu_reg_t(lo, hi) for lo, hi in zip(*[iter(struct.unpack('<' + 'd' * a_len, byte_string[a_offset:]))]*2)]

