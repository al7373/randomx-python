from .load64 import load64
from .const import blake2b_IV, blake2b_sigma
from .rotr64 import rotr64

def blake2b_compress(S, block):

    m = [0] * 16
    v = [0] * 16

    for i in range(16):
        m[i] = load64(block[i * 8:i * 8 + 8])

    for i in range(8):
        v[i] = S.h[i]

    v[8] = blake2b_IV[0]
    v[9] = blake2b_IV[1]
    v[10] = blake2b_IV[2]
    v[11] = blake2b_IV[3]
    v[12] = (blake2b_IV[4] ^ S.t[0])
    v[13] = (blake2b_IV[5] ^ S.t[1])
    v[14] = (blake2b_IV[6] ^ S.f[0])
    v[15] = (blake2b_IV[7] ^ S.f[1])

    def G(r, i, a, b, c, d):
        nonlocal m
        a = (a + b + m[blake2b_sigma[r][2 * i + 0]]) & 0xFFFFFFFFFFFFFFFF
        d = rotr64(d ^ a, 32)
        c = (c + d) & 0xFFFFFFFFFFFFFFFF
        b = rotr64(b ^ c, 24)
        a = (a + b + m[blake2b_sigma[r][2 * i + 1]]) & 0xFFFFFFFFFFFFFFFF
        d = rotr64(d ^ a, 16)
        c = (c + d) & 0xFFFFFFFFFFFFFFFF
        b = rotr64(b ^ c, 63)
        return a, b, c, d

    def ROUND(r):
        nonlocal v
        v[0], v[4], v[8], v[12] = G(r, 0, v[0], v[4], v[8], v[12])
        v[1], v[5], v[9], v[13] = G(r, 1, v[1], v[5], v[9], v[13])
        v[2], v[6], v[10], v[14] = G(r, 2, v[2], v[6], v[10], v[14])
        v[3], v[7], v[11], v[15] = G(r, 3, v[3], v[7], v[11], v[15])
        v[0], v[5], v[10], v[15] = G(r, 4, v[0], v[5], v[10], v[15])
        v[1], v[6], v[11], v[12] = G(r, 5, v[1], v[6], v[11], v[12])
        v[2], v[7], v[8], v[13] = G(r, 6, v[2], v[7], v[8], v[13])
        v[3], v[4], v[9], v[14] = G(r, 7, v[3], v[4], v[9], v[14])


    for r in range(12):
        ROUND(r)
    for i in range(8):
        S.h[i] ^= v[i] ^ v[i + 8]

