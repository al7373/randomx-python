def load64(src):
    if len(src) < 8:
        src = src.ljust(8, b'\x00')

    p = src
    w = p[0]
    w |= p[1] << 8
    w |= p[2] << 16
    w |= p[3] << 24
    w |= p[4] << 32
    w |= p[5] << 40
    w |= p[6] << 48
    w |= p[7] << 56
    return w

