from ctypes import c_uint64

def randomx_reciprocal(divisor: int) -> int:
    assert divisor != 0, "Divisor must not be 0"

    p2exp63 = 1 << 63

    quotient = c_uint64(p2exp63 // divisor)
    remainder = c_uint64(p2exp63 % divisor)

    bsr = 0
    bit = divisor
    while bit > 0:
        bsr += 1
        bit >>= 1

    for shift in range(bsr):
        if remainder.value >= divisor - remainder.value:
            quotient.value = quotient.value * 2 + 1
            remainder.value = remainder.value * 2 - divisor
        else:
            quotient.value = quotient.value * 2
            remainder.value = remainder.value * 2

    return quotient.value

