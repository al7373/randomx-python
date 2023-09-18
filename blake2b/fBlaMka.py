def fBlaMka(x: int, y: int) -> int:
    m = 0xFFFFFFFF
    xy = (x & m) * (y & m)
    return (x + y + 2 * xy) & 0xFFFFFFFFFFFFFFFF

