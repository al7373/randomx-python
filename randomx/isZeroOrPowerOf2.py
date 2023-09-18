def isZeroOrPowerOf2(x: int) -> bool:
    return (x & (x - 1)) == 0
