def rotr(a: int, b: int) -> int:
    return (a >> b) | (a << ((-b) & 63)) & 0xFFFFFFFFFFFFFFFF

