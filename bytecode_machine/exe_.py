from .InstructionByteCode import InstructionByteCode
from randomx.ProgramConfiguration import ProgramConfiguration
from .BytecodeMachine import maskRegisterExponentMantissa, getScratchpadAddress
import struct
from superscalar.smulh import smulh
from superscalar.rotr import rotr
from randomx.rx_vec_f128 import rx_swap_vec_f128, rx_add_vec_f128, rx_set1_vec_f128, rx_xor_vec_f128, rx_mul_vec_f128, rx_sqrt_vec_f128, rx_cvt_packed_int_vec_f128, rx_div_vec_f128, rx_sub_vec_f128
from .Pointer import Pointer
from .RoundingMode import *

def store64(dst: bytearray, index: int, w: int):
    dst[index:index+8] = w.to_bytes(8, 'little')

def load64(src):
    return struct.unpack('<Q', src)[0]

def rotl(a: int, b: int) -> int:
    return (a << b) | (a >> ((-b) & 63)) & 0xFFFFFFFFFFFFFFFF

def exe_IADD_RS(ibc: InstructionByteCode, pc: Pointer, scratchpad: bytearray, config: ProgramConfiguration):
    ibc.idst.setValue((ibc.idst.getValue() + (ibc.isrc.getValue() << ibc.shift) + ibc.imm) & 0xFFFFFFFFFFFFFFFF)

def exe_IADD_M(ibc: InstructionByteCode, pc: Pointer, scratchpad: bytearray, config: ProgramConfiguration):
    addr = getScratchpadAddress(ibc)
    value = load64(scratchpad[addr:addr+8])
    ibc.idst.setValue((ibc.idst.getValue() + value) & 0xFFFFFFFFFFFFFFFF)

def exe_ISUB_R(ibc: InstructionByteCode, pc: Pointer, scratchpad: bytearray, config: ProgramConfiguration):
    # *ibc.idst -= *ibc.isrc;
    ibc.idst.setValue((ibc.idst.getValue() - ibc.isrc.getValue()) & 0xFFFFFFFFFFFFFFFF)

def exe_ISUB_M(ibc: InstructionByteCode, pc: Pointer, scratchpad: bytearray, config: ProgramConfiguration):
    # *ibc.idst -= load64(getScratchpadAddress(ibc, scratchpad));
    addr = getScratchpadAddress(ibc)
    value = load64(scratchpad[addr:addr+8])
    ibc.idst.setValue((ibc.idst.getValue() - value) & 0xFFFFFFFFFFFFFFFF)

def exe_IMUL_R(ibc: InstructionByteCode, pc: Pointer, scratchpad: bytearray, config: ProgramConfiguration):
    ibc.idst.setValue((ibc.idst.getValue() * ibc.isrc.getValue()) & 0xFFFFFFFFFFFFFFFF)

def exe_IMUL_M(ibc: InstructionByteCode, pc: Pointer, scratchpad: bytearray, config: ProgramConfiguration):
    # *ibc.idst *= load64(getScratchpadAddress(ibc, scratchpad));
    addr = getScratchpadAddress(ibc)
    value = load64(scratchpad[addr:addr+8])
    ibc.idst.setValue((ibc.idst.getValue() * value) & 0xFFFFFFFFFFFFFFFF)

def exe_IMULH_R(ibc: InstructionByteCode, pc: Pointer, scratchpad: bytearray, config: ProgramConfiguration):
    ibc.idst.setValue(((ibc.idst.getValue() * ibc.isrc.getValue()) >> 64) & 0xFFFFFFFFFFFFFFFF)

def exe_IMULH_M(ibc: InstructionByteCode, pc: Pointer, scratchpad: bytearray, config: ProgramConfiguration):
    # *ibc.idst = mulh(*ibc.idst, load64(getScratchpadAddress(ibc, scratchpad)));
    addr = getScratchpadAddress(ibc)
    value = load64(scratchpad[addr:addr+8])
    ibc.idst.setValue(
        ((ibc.idst.getValue() * value) >> 64) & 0xFFFFFFFFFFFFFFFF
    )

def exe_ISMULH_R(ibc: InstructionByteCode, pc: Pointer, scratchpad: bytearray, config: ProgramConfiguration):
    ibc.idst.setValue(smulh(
        ibc.idst.getValue(),
        ibc.isrc.getValue()
    ))

def exe_ISMULH_M(ibc: InstructionByteCode, pc: Pointer, scratchpad: bytearray, config: ProgramConfiguration):
    # *ibc.idst = smulh(unsigned64ToSigned2sCompl(*ibc.idst), unsigned64ToSigned2sCompl(load64(getScratchpadAddress(ibc, scratchpad))));
    addr = getScratchpadAddress(ibc)
    value = load64(scratchpad[addr:addr+8])
    ibc.idst.setValue(smulh(
        ibc.idst.getValue(),
        value
    ))

def exe_INEG_R(ibc: InstructionByteCode, pc: Pointer, scratchpad: bytearray, config: ProgramConfiguration):
    ibc.idst.setValue((~(ibc.idst.getValue()) + 1) & 0xFFFFFFFFFFFFFFFF)

def exe_IXOR_R(ibc: InstructionByteCode, pc: Pointer, scratchpad: bytearray, config: ProgramConfiguration):
    ibc.idst.setValue(ibc.idst.getValue() ^ ibc.isrc.getValue())

def exe_IXOR_M(ibc: InstructionByteCode, pc: Pointer, scratchpad: bytearray, config: ProgramConfiguration):
    # *ibc.idst ^= load64(getScratchpadAddress(ibc, scratchpad));
    addr = getScratchpadAddress(ibc)
    value = load64(scratchpad[addr:addr+8])
    ibc.idst.setValue(ibc.idst.getValue() ^ value)

def exe_IROR_R(ibc: InstructionByteCode, pc: Pointer, scratchpad: bytearray, config: ProgramConfiguration):
    ibc.idst.setValue(rotr(
        ibc.idst.getValue(),
        ibc.isrc.getValue() & 63
    ) & 0xFFFFFFFFFFFFFFFF)

def exe_IROL_R(ibc: InstructionByteCode, pc: Pointer, scratchpad: bytearray, config: ProgramConfiguration):
    ibc.idst.setValue(rotl(
        ibc.idst.getValue(),
        ibc.isrc.getValue() & 63
    ) & 0xFFFFFFFFFFFFFFFF)

def exe_ISWAP_R(ibc: InstructionByteCode, pc: Pointer, scratchpad: bytearray, config: ProgramConfiguration):
    temp = ibc.isrc.getValue()
    ibc.isrc.setValue(ibc.idst.getValue())
    ibc.idst.setValue(temp)

def exe_FSWAP_R(ibc: InstructionByteCode, pc: Pointer, scratchpad: bytearray, config: ProgramConfiguration):
    ibc.fdst.setValue(rx_swap_vec_f128(ibc.fdst.getValue()))

def exe_FADD_R(ibc: InstructionByteCode, pc: Pointer, scratchpad: bytearray, config: ProgramConfiguration):
    ibc.fdst.setValue(rx_add_vec_f128(
        ibc.fdst.getValue(), 
        ibc.fsrc.getValue()
    ))

def exe_FADD_M(ibc: InstructionByteCode, pc: Pointer, scratchpad: bytearray, config: ProgramConfiguration):
    addr = getScratchpadAddress(ibc)
    fsrc = rx_cvt_packed_int_vec_f128(scratchpad[addr:addr+8])
    ibc.fdst.setValue(rx_add_vec_f128(
        ibc.fdst.getValue(), fsrc
    ))

def exe_FSUB_R(ibc: InstructionByteCode, pc: Pointer, scratchpad: bytearray, config: ProgramConfiguration):
    ibc.fdst.setValue(rx_sub_vec_f128(
        ibc.fdst.getValue(), 
        ibc.fsrc.getValue()
    ))

def exe_FSUB_M(ibc: InstructionByteCode, pc: Pointer, scratchpad: bytearray, config: ProgramConfiguration):
    addr = getScratchpadAddress(ibc)
    fsrc = rx_cvt_packed_int_vec_f128(scratchpad[addr:addr+8])
    ibc.fdst.setValue(rx_sub_vec_f128(
        ibc.fdst.getValue(), fsrc
    ))

def exe_FSCAL_R(ibc: InstructionByteCode, pc: Pointer, scratchpad: bytearray, config: ProgramConfiguration):
    mask = rx_set1_vec_f128(0x80F0000000000000)
    ibc.fdst.setValue(rx_xor_vec_f128(ibc.fdst.getValue(), mask))

def exe_FMUL_R(ibc: InstructionByteCode, pc: Pointer, scratchpad: bytearray, config: ProgramConfiguration):
    ibc.fdst.setValue(rx_mul_vec_f128(
        ibc.fdst.getValue(), 
        ibc.fsrc.getValue()
    ))

def exe_FDIV_M(ibc: InstructionByteCode, pc: Pointer, scratchpad: bytearray, config: ProgramConfiguration):
    addr = getScratchpadAddress(ibc)
    fsrc = maskRegisterExponentMantissa(
        config,
        rx_cvt_packed_int_vec_f128(scratchpad[addr:addr+8])
    )
    ibc.fdst.setValue(rx_div_vec_f128(ibc.fdst.getValue(), fsrc))

def exe_FSQRT_R(ibc: InstructionByteCode, pc: Pointer, scratchpad: bytearray, config: ProgramConfiguration):
    ibc.fdst.setValue(rx_sqrt_vec_f128(ibc.fdst.getValue()))

def exe_CBRANCH(ibc: InstructionByteCode, pc: Pointer, scratchpad: bytearray, config: ProgramConfiguration):
    ibc.idst.setValue((ibc.idst.getValue() + ibc.imm) & 0xFFFFFFFFFFFFFFFF)
    if (ibc.idst.getValue() & ibc.memMask) == 0:
        pc.setValue(ibc.target)

def exe_CFROUND(ibc: InstructionByteCode, pc: Pointer, scratchpad: bytearray, config: ProgramConfiguration):
    rx_set_rounding_mode(rotr(ibc.isrc.getValue(), ibc.imm) % 4)

def exe_ISTORE(ibc: InstructionByteCode, pc: Pointer, scratchpad: bytearray, config: ProgramConfiguration):
    # store64(scratchpad + ((*ibc.idst + ibc.imm) & ibc.memMask), *ibc.isrc);
    store64(
        scratchpad, 
        (ibc.idst.getValue() + ibc.imm) & ibc.memMask,
        ibc.isrc.getValue()
    )

