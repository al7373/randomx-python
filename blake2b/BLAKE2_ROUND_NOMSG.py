from .fBlaMka import fBlaMka
from .rotr64 import rotr64

def G(a: int, b: int, c: int, d: int) -> tuple[int, int, int, int]:
    a = fBlaMka(a, b)
    d = rotr64(d ^ a, 32)
    c = fBlaMka(c, d)
    b = rotr64(b ^ c, 24)
    a = fBlaMka(a, b)
    d = rotr64(d ^ a, 16)
    c = fBlaMka(c, d)
    b = rotr64(b ^ c, 63)
    return a, b, c, d


def BLAKE2_ROUND_NOMSG(v0: int, v1: int, v2: int, v3: int, v4: int, v5: int, v6: int, v7: int,
                       v8: int, v9: int, v10: int, v11: int, v12: int, v13: int, v14: int, v15: int) -> tuple[int, ...]:
    v0, v4, v8, v12 = G(v0, v4, v8, v12)
    v1, v5, v9, v13 = G(v1, v5, v9, v13)
    v2, v6, v10, v14 = G(v2, v6, v10, v14)
    v3, v7, v11, v15 = G(v3, v7, v11, v15)
    v0, v5, v10, v15 = G(v0, v5, v10, v15)
    v1, v6, v11, v12 = G(v1, v6, v11, v12)
    v2, v7, v8, v13 = G(v2, v7, v8, v13)
    v3, v4, v9, v14 = G(v3, v4, v9, v14)
    return v0, v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11, v12, v13, v14, v15
