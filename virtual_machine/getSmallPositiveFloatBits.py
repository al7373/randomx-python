from randomx.const import mantissaMask, exponentMask, exponentBias, mantissaSize

def getSmallPositiveFloatBits(entropy: int) -> int:
    exponent = entropy >> 59  # 0..31
    mantissa = entropy & mantissaMask
    exponent += exponentBias
    exponent &= exponentMask
    exponent <<= mantissaSize
    return exponent | mantissa

