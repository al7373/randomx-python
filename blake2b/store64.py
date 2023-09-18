def store64(dst, index, w):
    for i in range(8):
        dst[index + i] = w & 0xFF
        w >>= 8

