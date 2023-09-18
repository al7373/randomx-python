from .getStaticExponent import getStaticExponent

def getFloatMask(entropy):
    mask22bit = (1 << 22) - 1
    return (entropy & mask22bit) | getStaticExponent(entropy)

