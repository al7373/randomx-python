def load32(src):
    if len(src) < 4:
        src = src.ljust(4, b'\x00')

    p = src
    w = p[0]
    w |= p[1] << 8
    w |= p[2] << 16
    w |= p[3] << 24
    return w

