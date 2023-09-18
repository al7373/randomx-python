import ctypes
from .RoundingMode import *

# Chargez la bibliothèque
_float_rounder = ctypes.CDLL('./float_rounder/float_rounder.so')

# Définissez la fonction 'add'
_float_rounder.add.argtypes = [ctypes.c_double, ctypes.c_double, ctypes.c_int]
_float_rounder.add.restype = ctypes.c_double

_float_rounder.sub.argtypes = [ctypes.c_double, ctypes.c_double, ctypes.c_int]
_float_rounder.sub.restype = ctypes.c_double

_float_rounder.mul.argtypes = [ctypes.c_double, ctypes.c_double, ctypes.c_int]
_float_rounder.mul.restype = ctypes.c_double

_float_rounder._div.argtypes = [ctypes.c_double, ctypes.c_double, ctypes.c_int]
_float_rounder._div.restype = ctypes.c_double

_float_rounder._sqrt.argtypes = [ctypes.c_double, ctypes.c_int]
_float_rounder._sqrt.restype = ctypes.c_double

_float_rounder.get_FE_DOWNWARD.restype = ctypes.c_int
FE_DOWNWARD = _float_rounder.get_FE_DOWNWARD()

_float_rounder.get_FE_TOWARDZERO.restype = ctypes.c_int
FE_TOWARDZERO = _float_rounder.get_FE_TOWARDZERO()

_float_rounder.get_FE_UPWARD.restype = ctypes.c_int
FE_UPWARD = _float_rounder.get_FE_UPWARD()

_float_rounder.get_FE_TONEAREST.restype = ctypes.c_int
FE_TONEAREST = _float_rounder.get_FE_TONEAREST()

_rounding_mode = {
    RoundToNearest: FE_TONEAREST,
    RoundDown: FE_DOWNWARD,
    RoundUp: FE_UPWARD,
    RoundToZero: FE_TOWARDZERO
}

def add(a: float, b: float) -> float:
    return _float_rounder.add(a, b, _rounding_mode[rx_get_rounding_mode()])

def sub(a: float, b: float) -> float:
    return _float_rounder.sub(a, b, _rounding_mode[rx_get_rounding_mode()])

def mul(a: float, b: float) -> float:
    return _float_rounder.mul(a, b, _rounding_mode[rx_get_rounding_mode()])

def div(a: float, b: float) -> float:
    return _float_rounder._div(a, b, _rounding_mode[rx_get_rounding_mode()])

def sqrt(x: float) -> float:
    return _float_rounder._sqrt(x, _rounding_mode[rx_get_rounding_mode()])

