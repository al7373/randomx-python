import ctypes
from typing import ByteString
import struct
import bytecode_machine.float_rounder as float_rounder

class rx_vec_d(ctypes.Structure):
    _fields_ = [
        ("lo", ctypes.c_double),
        ("hi", ctypes.c_double)
    ]  # Structure with "hi" and "lo" fields

class rx_vec_i(ctypes.Structure):
    _fields_ = [
        ("u64", ctypes.c_uint64 * 2),  # tableau de deux entiers non signés de 64 bits
    ]

class rx_vec_f128(ctypes.Union):
    _fields_ = [
        ("i", rx_vec_i),
        ("d", rx_vec_d)
    ]

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.lo == other.lo and self.hi == other.hi

    @property
    def lo(self):
        return self.d.lo

    @property
    def hi(self):
        return self.d.hi

def rx_load_vec_f128(pd: ByteString) -> rx_vec_f128:
    x = rx_vec_f128()
    x.d.lo = struct.unpack('<d', pd[0:8])[0]
    x.d.hi = struct.unpack('<d', pd[8:16])[0]
    return x

def rx_set_vec_f128(x1: int, x0: int) -> rx_vec_f128:
    v = rx_vec_f128()
    v.i.u64[0] = x0
    v.i.u64[1] = x1
    return v

def rx_store_vec_f128(dst: bytearray, start_index: int, a: rx_vec_f128) -> None:
    struct.pack_into('<Q', dst, start_index, a.i.u64[0])
    struct.pack_into('<Q', dst, start_index + 8, a.i.u64[1])

def rx_swap_vec_f128(a: rx_vec_f128) -> rx_vec_f128:
    tmp = a.i.u64[0]
    a.i.u64[0] = a.i.u64[1]
    a.i.u64[1] = tmp
    return a

def rx_add_vec_f128(a: rx_vec_f128, b: rx_vec_f128) -> rx_vec_f128:
    x = rx_vec_f128()
    x.d.lo = float_rounder.add(a.d.lo, b.d.lo)
    x.d.hi = float_rounder.add(a.d.hi, b.d.hi)
    return x

def rx_sub_vec_f128(a: rx_vec_f128, b: rx_vec_f128) -> rx_vec_f128:
    x = rx_vec_f128()
    x.d.lo = float_rounder.sub(a.d.lo, b.d.lo)
    x.d.hi = float_rounder.sub(a.d.hi, b.d.hi)
    return x

def rx_set1_vec_f128(x: int) -> rx_vec_f128:
    v = rx_vec_f128()
    v.i.u64[0] = x
    v.i.u64[1] = x
    return v

def rx_xor_vec_f128(a: rx_vec_f128, b: rx_vec_f128) -> rx_vec_f128:
    x = rx_vec_f128()
    x.i.u64[0] = a.i.u64[0] ^ b.i.u64[0]
    x.i.u64[1] = a.i.u64[1] ^ b.i.u64[1]
    return x

def rx_mul_vec_f128(a: rx_vec_f128, b: rx_vec_f128) -> rx_vec_f128:
    x = rx_vec_f128()
    x.d.lo = float_rounder.mul(a.d.lo, b.d.lo)
    x.d.hi = float_rounder.mul(a.d.hi, b.d.hi)
    return x

def rx_sqrt_vec_f128(x: rx_vec_f128) -> rx_vec_f128:
    v = rx_vec_f128()
    v.d.lo = float_rounder.sqrt(x.d.lo)
    v.d.hi = float_rounder.sqrt(x.d.hi)
    return v

def rx_div_vec_f128(a: rx_vec_f128, b: rx_vec_f128) -> rx_vec_f128:
	x = rx_vec_f128()
	x.d.lo = float_rounder.div(a.d.lo, b.d.lo)
	x.d.hi = float_rounder.div(a.d.hi, b.d.hi)
	return x

def rx_cvt_packed_int_vec_f128(mem: bytearray) -> rx_vec_f128:
    v = rx_vec_f128()
    v.d.lo = float(struct.unpack('<i', mem[0:4])[0])
    v.d.hi = float(struct.unpack('<i', mem[4:8])[0])
    return v

def rx_and_vec_f128(a: rx_vec_f128, b: rx_vec_f128) -> rx_vec_f128:
	x = rx_vec_f128()
	x.i.u64[0] = a.i.u64[0] & b.i.u64[0]
	x.i.u64[1] = a.i.u64[1] & b.i.u64[1]
	return x

def rx_or_vec_f128(a: rx_vec_f128, b: rx_vec_f128) -> rx_vec_f128:
	x = rx_vec_f128()
	x.i.u64[0] = a.i.u64[0] | b.i.u64[0]
	x.i.u64[1] = a.i.u64[1] | b.i.u64[1]
	return x

