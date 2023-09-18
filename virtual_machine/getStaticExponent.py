from randomx.const import constExponentBits, dynamicExponentBits, mantissaSize, staticExponentBits

def getStaticExponent(entropy: int) -> int:
    exponent = constExponentBits
    exponent |= (entropy >> (64 - staticExponentBits)) << dynamicExponentBits
    exponent <<= mantissaSize
    return exponent
