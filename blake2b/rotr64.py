def rotr64(w, c):
    return ((w >> c) | (w << (64 - c))) & 0xFFFFFFFFFFFFFFFF
