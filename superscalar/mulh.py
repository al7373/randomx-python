def mulh(a: int, b: int) -> int:
    return ((a * b) >> 64) & 0xFFFFFFFFFFFFFFFF

