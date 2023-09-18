def signExtend2sCompl(x: int) -> int:
    INT32_MAX = 0x7FFFFFFF
    if x > INT32_MAX:
        return x | 0xffffffff00000000
    else:
        return x
