import struct

class rx_vec_i128:
    #i3 est la partie la plus haute
    #i0 est la partie la plus basse
    def __init__(self, i3=0, i2=0, i1=0, i0=0):
        self.data = struct.pack('<IIII', i3, i2, i1, i0)

    def u32(self):
        return struct.unpack('<IIII', self.data)

    def i64(self):
        i3, i2, i1, i0 = struct.unpack('<IIII', self.data)
        return (
            # La partie haute
            int.from_bytes(struct.pack('<II', i2, i3), byteorder='little', signed=True),
            # La partie basse
            int.from_bytes(struct.pack('<II', i0, i1), byteorder='little', signed=True)
            # Contrairement, dans gdb, la partie basse est affichée en premier
        )

def rx_set_int_vec_i128(i3: int, i2: int, i1: int, i0: int):
    return rx_vec_i128(i3, i2, i1, i0)

def rx_load_vec_i128(p: bytearray):
    i3 = int.from_bytes(p[12:16], byteorder='little', signed=False)
    i2 = int.from_bytes(p[8:12], byteorder='little', signed=False)
    i1 = int.from_bytes(p[4:8], byteorder='little', signed=False)
    i0 = int.from_bytes(p[0:4], byteorder='little', signed=False)
    return rx_vec_i128(i3, i2, i1, i0)

def rx_vec_i128_x(a: rx_vec_i128) -> int:
    return a.u32()[3]

def rx_vec_i128_y(a: rx_vec_i128) -> int:
    return a.u32()[2]

def rx_vec_i128_z(a: rx_vec_i128) -> int:
    return a.u32()[1]

def rx_vec_i128_w(a: rx_vec_i128) -> int:
    return a.u32()[0]

def rx_xor_vec_i128(a: rx_vec_i128, b: rx_vec_i128) -> rx_vec_i128:
    a_int = int.from_bytes(a.data, byteorder='little', signed=True)
    b_int = int.from_bytes(b.data, byteorder='little', signed=True)
    xor_result = a_int ^ b_int
    xor_result = xor_result.to_bytes(16, byteorder='little', signed=True)
    return rx_vec_i128(*struct.unpack('<IIII', xor_result))

def rx_store_vec_i128(dst: bytearray, start: int, vec: rx_vec_i128):
    dst[start + 0:start + 4] = vec.data[12:16]
    dst[start + 4:start + 8] = vec.data[8:12]
    dst[start + 8:start + 12] = vec.data[4:8]
    dst[start + 12:start + 16] = vec.data[0:4]

